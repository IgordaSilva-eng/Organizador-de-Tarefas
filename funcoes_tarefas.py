import datetime
import json
import os
import sys

print()
print("- - - - - - - - - - - - - - - - - - - - -")
print("- - -   Bloco de Codigo: Tarefas    - - -")
print("- - - - - - - - - - - - - - - - - - - - -")


# Declaração das globais

tarefas = []
id_contador = 1  

# Constantes de validação, atualizada
PRIORIDADES_VALIDAS = ["urgente", "alta", "média", "baixa"]
ORIGENS_VALIDAS = ["email", "telefone", "chamado do sistema"]
STATUS_VALIDOS = ["pendente", "fazendo", "concluída", "arquivado", "excluída"]

# Nomes dos arquivos json, recente
ARQUIVO_TAREFAS = "tarefas.json"
ARQUIVO_ARQUIVADAS = "tarefas_arquivadas.json"

def _json_date_converter(obj):
    """
    Converte objetos datetime para string no formato ISO
    para que possam ser salvos em JSON.
    
    Parâmetros: obj (object) - O objeto a ser verificado.
    Retorno: str (obj.isoformat()) ou o objeto inalterado.
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


def verificar_e_criar_arquivos():
    """
    Verifica se os arquivos JSON obrigatórios existem.
    Se não existirem, cria-os com uma lista vazia.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("verificar_e_criar_arquivos")
    
    for arquivo in [ARQUIVO_TAREFAS, ARQUIVO_ARQUIVADAS]:
        if not os.path.exists(arquivo):
            print(f"Aviso: Arquivo '{arquivo}' não encontrado. Criando...")
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump([], f) 
            except IOError as e:
                print(f"ERRO CRÍTICO: Não foi possível criar o arquivo '{arquivo}'. {e}")
                sys.exit(1) 


def carregar_tarefas_json():
    """
    Carrega as tarefas do 'tarefas.json'
    para a variável global 'tarefas' no início do programa.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("carregar_tarefas_json")
    
    global tarefas
    global id_contador
    
    try:
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as f:
            tarefas = json.load(f)
        
        max_id = 0
        for tarefa in tarefas:
            if 'data_criacao' in tarefa:
                tarefa['data_criacao'] = datetime.datetime.fromisoformat(tarefa['data_criacao'])
            if 'data_conclusao' in tarefa and tarefa['data_conclusao']:
                tarefa['data_conclusao'] = datetime.datetime.fromisoformat(tarefa['data_conclusao'])
            
            if tarefa['id'] > max_id:
                max_id = tarefa['id']
                
        id_contador = max_id + 1
        print(f"Sucesso: {len(tarefas)} tarefas carregadas de '{ARQUIVO_TAREFAS}'.")

    except json.JSONDecodeError:
        print(f"Aviso: O arquivo '{ARQUIVO_TAREFAS}' está vazio ou corrompido. Iniciando com lista vazia.")
        tarefas = []
    except IOError as e:
        print(f"ERRO CRÍTICO: Não foi possível ler o arquivo '{ARQUIVO_TAREFAS}'. {e}")
        sys.exit(1)


def salvar_tarefas_json():
    """
    (Req 13) Salva a lista global 'tarefas' no
    arquivo 'tarefas.json' ao sair.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("salvar_tarefas_json")
    
    try:
        with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as f:
            json.dump(tarefas, f, indent=4, default=_json_date_converter)
        print(f"Sucesso: Tarefas salvas em '{ARQUIVO_TAREFAS}'.")
    except IOError as e:
        print(f"ERRO: Não foi possível salvar as tarefas. {e}")


def arquivar_tarefa_no_historico(tarefa):
    """
    Adiciona uma tarefa ao arquivo de histórico
    'tarefas_arquivadas.json' (acumulativo).
    
    Parâmetros: tarefa (dict) - A tarefa a ser arquivada.
    Retorno: nenhum
    """
    _print_debug("arquivar_tarefa_no_historico")
    
    historico = []
    try:
        with open(ARQUIVO_ARQUIVADAS, 'r', encoding='utf-8') as f:
            historico = json.load(f)
    except (IOError, json.JSONDecodeError):
        print(f"Aviso: Arquivo '{ARQUIVO_ARQUIVADAS}' não encontrado ou corrompido. Criando novo histórico.")
        historico = []

    historico.append(tarefa)
    
    try:
        with open(ARQUIVO_ARQUIVADAS, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=4, default=_json_date_converter)
        print(f"Tarefa ID {tarefa['id']} registrada no histórico '{ARQUIVO_ARQUIVADAS}'.")
    except IOError as e:
        print(f"ERRO: Não foi possível arquivar a tarefa no histórico. {e}")

def _print_debug(nome_funcao):
    """
    Imprime uma mensagem de depuração (debug).
    
    Parâmetros: nome_funcao (str) - O nome da função a ser impressa.
    Retorno: nenhum
    """
    print(f"\n--- [Debug] Executando a função: {nome_funcao} ---")


def _validar_input_opcoes(mensagem_prompt, opcoes_validas):
    """
    Pede um input ao usuário e o valida contra uma
    lista de opções permitidas.
    
    Parâmetros:
        mensagem_prompt (str): A mensagem a ser exibida.
        opcoes_validas (list): A lista de strings válidas.
        
    Retorno: str - A opção validada, em minúsculas.
    """
    _print_debug("_validar_input_opcoes")
    
    print(f"Opções disponíveis: {', '.join(opcoes_validas)}")
    
    while True:
        entrada = input(f"{mensagem_prompt}: ").lower()
        if entrada in opcoes_validas:
            return entrada
        else:
            print(f"Opção inválida. Por favor, digite uma das opções: {', '.join(opcoes_validas)}")


def _buscar_tarefa_por_id():
    """
    Permite encontrar uma tarefa pelo ID.
    Implementa Tratamento de Exceções (2ª Defesa).
    
    Parâmetros: nenhum
    Retorno: dict (a tarefa encontrada) ou None (se não encontrar).
    """
    _print_debug("_buscar_tarefa_por_id")
    try:
        id_busca = int(input("Digite o ID da tarefa: "))
        
        for tarefa in tarefas:
            if tarefa['id'] == id_busca:
                if tarefa['status'] == 'excluída':
                    print(f"Erro: Tarefa com ID {id_busca} foi excluída.")
                    return None
                print(f"Tarefa encontrada: {tarefa['titulo']} (ID: {tarefa['id']})")
                return tarefa 
 
        print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
        return None
        
    except ValueError:
        print("Erro técnico: O ID deve ser um número inteiro. Tente novamente.")
        return None


# Ciclo de vida das tarefas

def criar_tarefa():
    """
    Cria uma nova tarefa com 'Descrição' e 'Data de Criação'.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("criar_tarefa")
    
    global tarefas
    global id_contador
    
    titulo = input("Digite o título da tarefa (obrigatório): ")
    if not titulo:
        print("Erro: O título é obrigatório.")
        return
        
    descricao = input("Digite a descrição da tarefa (opcional): ")
    prioridade = _validar_input_opcoes("Digite a prioridade", PRIORIDADES_VALIDAS)
    origem = _validar_input_opcoes("Digite a origem", ORIGENS_VALIDAS)
    
    tarefa = {
        'id': id_contador, 
        'titulo': titulo,
        'descricao': descricao,
        'prioridade': prioridade,
        'status': 'pendente',
        'origem': origem,
        'data_criacao': datetime.datetime.now(),
        'data_conclusao': None
    }
    tarefas.append(tarefa)
    id_contador += 1
    
    print(f"Tarefa criada com sucesso! (ID: {tarefa['id']})")


def pegar_tarefa():
    """
    Pega a tarefa 'Pendente' de maior prioridade.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("pegar_tarefa")
    global tarefas
 
    fazendo = [t for t in tarefas if t['status'] == 'fazendo']
    if fazendo:
        print("Já há uma tarefa em execução. Conclua-a antes de pegar outra.")
        return
 
    for prio in PRIORIDADES_VALIDAS:
        pendentes = [t for t in tarefas if t['status'] == 'pendente' and t['prioridade'] == prio]
        if pendentes:
            tarefa = pendentes[0]
            tarefa['status'] = 'fazendo'
            print(f"Tarefa selecionada: {tarefa['titulo']} (ID: {tarefa['id']}, Prioridade: {tarefa['prioridade']})")
            return
            
    print("Nenhuma tarefa pendente encontrada.")


def atualizar_prioridade():
    """
    Atualiza a prioridade de uma tarefa.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("atualizar_prioridade")
    global tarefas
    
    tarefa = _buscar_tarefa_por_id()
    
    if tarefa:  
        print(f"Prioridade atual: {tarefa['prioridade']}")
        nova_prioridade = _validar_input_opcoes("Digite a nova prioridade", PRIORIDADES_VALIDAS)
        
        tarefa['prioridade'] = nova_prioridade
        print("Prioridade atualizada com sucesso!")


def concluir_tarefa():
    """
    Conclui uma tarefa que está 'Fazendo'.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("concluir_tarefa")
    global tarefas
    
    tarefa = _buscar_tarefa_por_id()
    
    if tarefa: 
        if tarefa['status'] == 'fazendo':
            tarefa['status'] = 'concluída' 
            tarefa['data_conclusao'] = datetime.datetime.now()
            print("Tarefa concluída com sucesso!")
        elif tarefa['status'] == 'concluída':
            print("Erro: Esta tarefa já foi concluída.")
        else:
            print(f"Erro: A tarefa '{tarefa['titulo']}' está pendente. É preciso pegá-la primeiro.")


def arquivar_tarefas_antigas():
    """
    Altera o status de tarefas 'Concluídas' (+7 dias)
    para 'Arquivado'.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("arquivar_tarefas_antigas")
    
    global tarefas
    agora = datetime.datetime.now()
    arquivadas_count = 0
    
    for tarefa in tarefas:
        if (tarefa['status'] == 'concluída' and 
            tarefa['data_conclusao'] and 
            (agora - tarefa['data_conclusao']).days > 7):
            
            arquivar_tarefa_no_historico(tarefa)
            tarefa['status'] = 'arquivado'
            arquivadas_count += 1
            
    if arquivadas_count > 0:
        print(f"{arquivadas_count} tarefa(s) antiga(s) foi(ram) arquivada(s).")
    else:
        print("Nenhuma tarefa antiga para arquivar.")


def excluir_tarefa_logica():
    """
    Exclusão Lógica: Altera o status para 'Excluída'.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("excluir_tarefa_logica")
    
    global tarefas
    
    tarefa = _buscar_tarefa_por_id()
    
    if tarefa:
        arquivar_tarefa_no_historico(tarefa)
        tarefa['status'] = 'excluída'
        print(f"Tarefa ID {tarefa['id']} marcada como 'Excluída' e arquivada.")


def relatorio_geral():
    """
    Relatório de tarefas ativas e calcula
    o tempo de execução.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("relatorio_geral")
    
    tarefas_ativas = [t for t in tarefas if t['status'] not in ['arquivado', 'excluída']]
    
    if not tarefas_ativas:
        print("Nenhuma tarefa ativa para exibir.")
        return
        
    print("\n--- Relatório de Tarefas Ativas ---")
    for tarefa in tarefas_ativas:
        print(f"\nID: {tarefa['id']}")
        print(f"  Título: {tarefa['titulo']}")
        print(f"  Descrição: {tarefa['descricao']}")
        print(f"  Status: {tarefa['status'].capitalize()}")
        print(f"  Prioridade: {tarefa['prioridade'].capitalize()}")
        print(f"  Origem: {tarefa['origem'].capitalize()}")
        
        if tarefa.get('data_criacao'):
            data_formatada = tarefa['data_criacao'].strftime("%d/%m/%Y %H:%M:%S")
            print(f"  Data de Criação: {data_formatada}")
        
        if tarefa.get('data_conclusao'):
            data_formatada = tarefa['data_conclusao'].strftime("%d/%m/%Y %H:%M:%S")
            print(f"  Data de Conclusão: {data_formatada}")
            
            if tarefa.get('data_criacao'):
                tempo_execucao = tarefa['data_conclusao'] - tarefa['data_criacao']
                print(f"  Tempo de Execução: {tempo_execucao}")


def relatorio_arquivados():
    """
    Relatório que exibe APENAS as tarefas 'Arquivadas'.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("relatorio_arquivados")
    
    tarefas_arquivadas = [t for t in tarefas if t['status'] == 'arquivado']
    
    if not tarefas_arquivadas:
        print("Nenhuma tarefa arquivada para exibir.")
        return
        
    print("\n--- Relatório de Tarefas Arquivadas ---")
    for tarefa in tarefas_arquivadas:
        print(f"\nID: {tarefa['id']} (Título: {tarefa['titulo']})")
        print(f"  Status: {tarefa['status'].capitalize()}")
        if tarefa.get('data_conclusao'):
            data_formatada = tarefa['data_conclusao'].strftime("%d/%m/%Y %H:%M:%S")
            print(f"  Data de Conclusão: {data_formatada}")


# Nosso menu

def menu():
    """
    Menu Principal (Abstração de Controle).
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("menu")
    
    while True:
        print("\n--- Menu Principal ---")
        print("1. Criar Tarefa")
        print("2. Pegar Próxima Tarefa")
        print("3. Atualizar Prioridade")
        print("4. Concluir Tarefa")
        print("5. Arquivar Tarefas Antigas (+7d)")
        print("6. Excluir Tarefa (Exclusão Lógica)")
        print("7. Relatório Geral (Ativas)")
        print("8. Relatório de Tarefas Arquivadas")
        print("0. Salvar e Sair")
        
        try:
            opcao = input("Escolha uma opção: ")
            opcao_num = int(opcao)
            
            if opcao_num not in range(0, 9):
                 print("Opção inválida. Escolha um número entre 0 e 8.")
                 continue

            if opcao_num == 1:
                criar_tarefa()
            elif opcao_num == 2:
                pegar_tarefa()
            elif opcao_num == 3:
                atualizar_prioridade()
            elif opcao_num == 4:
                concluir_tarefa()
            elif opcao_num == 5:
                arquivar_tarefas_antigas()
            elif opcao_num == 6:
                excluir_tarefa_logica()
            elif opcao_num == 7:
                relatorio_geral()
            elif opcao_num == 8:
                relatorio_arquivados()
            elif opcao_num == 0:
                print("Salvando tarefas...")
                salvar_tarefas_json() 
                print("Saindo do sistema.")
                sys.exit() 
                
        except ValueError:
            print("Erro técnico: Por favor, digite apenas números.")
