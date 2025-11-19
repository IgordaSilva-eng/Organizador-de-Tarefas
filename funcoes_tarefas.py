import datetime
import json
import os
import sys

# ===========================
# CONSTANTES DO SISTEMA
# ===========================
ARQUIVO_TAREFAS = "tarefas.json"
ARQUIVO_ARQUIVADAS = "tarefas_arquivadas.json"

# Status definidos no PDF 
STATUS_PENDENTE = "Pendente"
STATUS_FAZENDO = "Fazendo"
STATUS_CONCLUIDA = "Concluída"
STATUS_ARQUIVADA = "Arquivado"
STATUS_EXCLUIDA = "Excluída"

# Dados obrigatórios do PDF 
PRIORIDADES_VALIDAS = ["Urgente", "Alta", "Média", "Baixa"]
ORIGENS_VALIDAS = ["E-mail", "Telefone", "Chamado do Sistema"]

# Mapeamento para ordenação (Urgente é mais importante)
MAPA_PRIORIDADE = {"Urgente": 1, "Alta": 2, "Média": 3, "Baixa": 4}

tarefas = []
tarefas_arquivadas = []
id_contador = 1


# =====================================
# FUNÇÕES AUXILIARES (DEBUG & VALIDAÇÃO)
# =====================================

def _print_debug(nome_funcao):
    """
    Prints de Execução para Testes.
    Imprime no console que a função iniciou.
    
    Parâmetros: nome_funcao (str)
    Retorno: nenhum
    """
    print(f"Executando a função {nome_funcao}")


def _validar_input_opcoes(mensagem, opcoes):
    """
    Validação Lógica (1ª Defesa).
    Informar opções válidas durante o preenchimento.
    
    Parâmetros: mensagem (str), opcoes (list)
    Retorno: str (opção válida escolhida)
    """
    _print_debug("_validar_input_opcoes")
    
    # Informa as opções antes de pedir 
    print(f"Opções disponíveis: {', '.join(opcoes)}")
    
    while True:
        valor = input(mensagem).strip().capitalize()
        # Tratamento especial para "E-mail" que pode ter hifen
        if valor == "Email": valor = "E-mail"
        
        # Verifica se o valor está na lista de opções
        for op in opcoes:
            if valor.lower() == op.lower():
                return op 
        
        print(f"Inválido. Tente uma das opções: {', '.join(opcoes)}")


def _buscar_tarefa_por_id(id_busca):
    """
    Busca tarefa pelo ID na lista de ativas.
    
    Parâmetros: id_busca (int)
    Retorno: dict ou None
    """
    _print_debug("_buscar_tarefa_por_id")
    for t in tarefas:
        if t["id"] == id_busca:
            return t
    return None


def _registrar_no_historico(tarefa):
    """
    Registrar tarefa no arquivo de histórico.
    Chamado ao Arquivar ou Excluir.
    
    Parâmetros: tarefa (dict)
    Retorno: nenhum
    """
    _print_debug("_registrar_no_historico")
    
    # Verifica se já não está lá para evitar duplicidade
    for t in tarefas_arquivadas:
        if t["id"] == tarefa["id"]:
            tarefas_arquivadas.remove(t)
            break
    
    tarefas_arquivadas.append(tarefa)


# =============================
# PERSISTÊNCIA (JSON)
# =============================

def verificar_arquivos_iniciais():
    """
    Criação Automática de Arquivos Necessários.
    Verifica se existem; se não, cria com lista vazia [].
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("verificar_arquivos_iniciais")
    
    arquivos = [ARQUIVO_TAREFAS, ARQUIVO_ARQUIVADAS]
    
    for arq in arquivos:
        # Se não existir, cria automaticamente
        if not os.path.exists(arq):
            print(f"Arquivo '{arq}' não encontrado. Criando automaticamente...")
            try:
                with open(arq, "w", encoding="utf-8") as f:
                    json.dump([], f)
            except IOError as e:
                print(f"Erro crítico ao criar arquivo: {e}")


def carregar_dados():
    """
    Persistência (Carregamento no início).
    Lê o arquivo tarefas.json e carrega na memória.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("carregar_dados")
    global tarefas, tarefas_arquivadas, id_contador

    # Garante que arquivos existem antes de ler 
    verificar_arquivos_iniciais()

    # Carrega tarefas ativas
    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, dict):
                tarefas = dados.get("tarefas", [])
                id_contador = dados.get("id_contador", 1)
            else:
                tarefas = dados
                if tarefas:
                    max_id = max(t["id"] for t in tarefas)
                    id_contador = max_id + 1
                else:
                    id_contador = 1
    except Exception as e:
        print(f"Erro ao carregar tarefas: {e}")
        tarefas = []
        id_contador = 1

    # Carrega histórico (necessário para acumular)
    try:
        with open(ARQUIVO_ARQUIVADAS, "r", encoding="utf-8") as f:
            tarefas_arquivadas = json.load(f)
    except:
        tarefas_arquivadas = []


def salvar_dados():
    """
    Persistência (Salvamento ao sair).
    Salva as listas atualizadas nos arquivos JSON.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("salvar_dados")
    
    dados_ativas = {
        "tarefas": tarefas,
        "id_contador": id_contador
    }
    
    try:
        with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
            json.dump(dados_ativas, f, indent=4, ensure_ascii=False)
            
        # Arquivo deve acumular histórico
        with open(ARQUIVO_ARQUIVADAS, "w", encoding="utf-8") as f:
            json.dump(tarefas_arquivadas, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


# =====================================
# CICLO DE VIDA 
# =====================================

def criar_tarefa():
    """
    Criação.
    Solicita dados, valida opções e armazena na lista.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("criar_tarefa")
    global id_contador

    print("\n=== Criar nova tarefa ===")
    titulo = input("Título (Obrigatório): ").strip()
    while not titulo:
        print("Título é obrigatório.")
        titulo = input("Título: ").strip()

    descricao = input("Descrição: ").strip()
    
    # Informar opções durante preenchimento
    prioridade = _validar_input_opcoes("Prioridade: ", PRIORIDADES_VALIDAS)
    origem = _validar_input_opcoes("Origem: ", ORIGENS_VALIDAS)

    tarefa = {
        "id": id_contador,
        "titulo": titulo,
        "descricao": descricao,
        "data_criacao": datetime.datetime.now().isoformat(),
        "data_conclusao": None,
        "origem": origem,
        "prioridade": prioridade,
        "status": STATUS_PENDENTE
    }

    tarefas.append(tarefa)
    id_contador += 1
    print(f"\nSucesso! Tarefa criada com ID {tarefa['id']}.\n")


def pegar_tarefa():
    """
    Verificação de Urgência.
    Pega a tarefa 'Pendente' de maior prioridade.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("pegar_tarefa")

    for t in tarefas:
        if t["status"] == STATUS_FAZENDO:
            print("\nErro: Já existe uma tarefa 'Fazendo'. Conclua-a primeiro.\n")
            return

    pendentes = [t for t in tarefas if t["status"] == STATUS_PENDENTE]
    
    if not pendentes:
        print("\nNenhuma tarefa pendente encontrada.\n")
        return

    # Ordena por prioridade (Urgente=1)
    pendentes.sort(key=lambda x: (MAPA_PRIORIDADE.get(x["prioridade"], 99), x["data_criacao"]))
    
    tarefa = pendentes[0]
    tarefa["status"] = STATUS_FAZENDO

    print(f"\nTarefa selecionada: '{tarefa['titulo']}' (Prioridade: {tarefa['prioridade']})")
    print("Status atualizado para 'Fazendo'.\n")


def atualizar_prioridade():
    """
    Atualização de Prioridade.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("atualizar_prioridade")
    
    try:
        id_busca = int(input("Digite o ID da tarefa: "))
    except ValueError:
        print("Erro: O ID deve ser um número.")
        return

    tarefa = _buscar_tarefa_por_id(id_busca)
    
    if not tarefa or tarefa["status"] == STATUS_EXCLUIDA:
        print("Tarefa não encontrada ou excluída.")
        return

    print(f"Prioridade atual: {tarefa['prioridade']}")
    nova_prio = _validar_input_opcoes("Nova Prioridade: ", PRIORIDADES_VALIDAS)
    
    tarefa["prioridade"] = nova_prio
    print("Prioridade atualizada com sucesso!\n")


def concluir_tarefa():
    """
    Conclusão.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("concluir_tarefa")
    
    try:
        id_busca = int(input("Digite o ID da tarefa para concluir: "))
    except ValueError:
        print("Erro: O ID deve ser um número.")
        return

    tarefa = _buscar_tarefa_por_id(id_busca)
    if not tarefa: 
        print("Tarefa não encontrada.")
        return

    if tarefa["status"] != STATUS_FAZENDO:
        print(f"Aviso: A tarefa está '{tarefa['status']}'. Deveria estar 'Fazendo'.")

    tarefa["status"] = STATUS_CONCLUIDA
    tarefa["data_conclusao"] = datetime.datetime.now().isoformat()
    print("Tarefa concluída com sucesso!\n")


def arquivar_tarefas_antigas():
    """
    Arquivamento (+7 dias).
    Registrar no histórico separado.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("arquivar_tarefas_antigas")
    
    agora = datetime.datetime.now()
    contador = 0
    
    for t in tarefas[:]:
        if t["status"] == STATUS_CONCLUIDA and t["data_conclusao"]:
            dt_conclusao = datetime.datetime.fromisoformat(t["data_conclusao"])
            
            if (agora - dt_conclusao).days > 7:
                t["status"] = STATUS_ARQUIVADA
                _registrar_no_historico(t)
                tarefas.remove(t)
                contador += 1
    
    print(f"Limpeza concluída. {contador} tarefas foram arquivadas.\n")


def excluir_tarefa():
    """
    Exclusão Lógica.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("excluir_tarefa")
    
    try:
        id_busca = int(input("Digite o ID da tarefa a excluir: "))
    except ValueError:
        print("Erro: O ID deve ser numérico.")
        return

    tarefa = _buscar_tarefa_por_id(id_busca)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    tarefa["status"] = STATUS_EXCLUIDA
    _registrar_no_historico(tarefa)
    print("Tarefa marcada como 'Excluída' e registrada no histórico.\n")


def relatorio_completo():
    """
    Relatório Geral.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("relatorio_completo")
    
    print("\n=== RELATÓRIO DE TAREFAS ATIVAS ===")
    encontrou = False
    
    for t in tarefas:
        if t["status"] == STATUS_EXCLUIDA:
            continue

        print(f"\nID: {t['id']} | Título: {t['titulo']}")
        print(f"Desc: {t['descricao']}")
        print(f"Prioridade: {t['prioridade']} | Origem: {t['origem']}")
        print(f"Status: {t['status']}")
        print(f"Criada em: {t['data_criacao']}")
        
        if t["status"] == STATUS_CONCLUIDA and t["data_conclusao"]:
            print(f"Concluída em: {t['data_conclusao']}")
            inicio = datetime.datetime.fromisoformat(t["data_criacao"])
            fim = datetime.datetime.fromisoformat(t["data_conclusao"])
            print(f"Tempo de Execução: {fim - inicio}")
            
        encontrou = True

    if not encontrou:
        print("Nenhuma tarefa ativa no momento.")
    print("-" * 30)


def relatorio_arquivados():
    """
    Relatório Arquivados.
    
    Parâmetros: nenhum
    Retorno: nenhum
    """
    _print_debug("relatorio_arquivados")
    
    print("\n=== RELATÓRIO DE HISTÓRICO (ARQUIVADAS) ===")
    
    if not tarefas_arquivadas:
        print("O histórico está vazio.")
        return

    for t in tarefas_arquivadas:
        if t["status"] == STATUS_EXCLUIDA:
            continue
            
        print(f"ID: {t['id']} | Título: {t['titulo']} | Status: {t['status']}")
        print(f"Conclusão: {t.get('data_conclusao', 'N/A')}")
    print("-" * 30)
