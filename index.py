import datetime
 
 
print()
print("- - - - - - - - - - - - - - - - - - - - -")
print("- - -   Bloco de Codigo: Tarefas    - - -")
print("- - - - - - - - - - - - - - - - - - - - -")
 
 
tarefas = []
id_contador = 1  
 
 
PRIORIDADES_VALIDAS = ["urgente", "alta", "média", "baixa"]
ORIGENS_VALIDAS = ["email", "telefone", "chamado do sistema"]
 
 
def _print_debug(nome_funcao):
    """
    Requisito 10: Imprime prints de execução para testes (Debugging).
    """
    print(f"\n--- [Debug] Executando a função: {nome_funcao} ---")
 
 
 
def _validar_input_opcoes(mensagem_prompt, opcoes_validas):
    """
    Requisito 8: Função de Validação (1ª Defesa).
    Evita repetição de código e garante dados lógicos.
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
    Requisito 9 e 11: Permite encontrar uma tarefa pelo ID[cite: 70].
    Implementa Tratamento de Exceções (2ª Defesa).
    """
    _print_debug("_buscar_tarefa_por_id")
    try:
 
 
        id_busca = int(input("Digite o ID da tarefa: "))
 
 
        for tarefa in tarefas:
            if tarefa['id'] == id_busca:
                print(f"Tarefa encontrada: {tarefa['titulo']} (ID: {tarefa['id']})")
                return tarefa 
 
 
        print(f"Erro: Tarefa com ID {id_busca} não encontrada.")
        return None
        
    except ValueError:
 
 
        print("Erro técnico: O ID deve ser um número inteiro. Tente novamente.")
        return None
 
 
def criar_tarefa():
    """
    Ciclo de Vida 1: Criação de uma nova tarefa[cite: 20].
    """
    _print_debug("criar_tarefa")
 
 
    global tarefas
    global id_contador
    
    titulo = input("Digite o título da tarefa: ")
 
    prioridade = _validar_input_opcoes("Digite a prioridade", PRIORIDADES_VALIDAS)
    origem = _validar_input_opcoes("Digite a origem", ORIGENS_VALIDAS)
    
    tarefa = {
        'id': id_contador, 
        'titulo': titulo,
        'prioridade': prioridade,
        'status': 'Pendente',
        'origem': origem
    }
    tarefas.append(tarefa)
    id_contador += 1
    
    print(f"Tarefa criada com sucesso! (ID: {tarefa['id']})")
 
 
 
def pegar_tarefa():
    """
    Ciclo de Vida 2: Verificação de Urgência[cite: 22].
    """
    _print_debug("pegar_tarefa")
    global tarefas
 
 
    fazendo = [t for t in tarefas if t['status'] == 'Fazendo']
    if fazendo:
        print("Já há uma tarefa em execução. Conclua-a antes de pegar outra.")
        return
 
 
    for prio in PRIORIDADES_VALIDAS:
        pendentes = [t for t in tarefas if t['status'] == 'Pendente' and t['prioridade'] == prio]
        if pendentes:
            tarefa = pendentes[0]
            tarefa['status'] = 'Fazendo'
            print(f"Tarefa selecionada: {tarefa['titulo']} (ID: {tarefa['id']}, Prioridade: {tarefa['prioridade']})")
            return
            
    print("Nenhuma tarefa pendente encontrada.")
 
 
 
def atualizar_prioridade():
    """
    Ciclo de Vida 3: Atualização de Prioridade[cite: 26].
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
    Ciclo de Vida 4: Conclusão das tarefas[cite: 27].
    """
    _print_debug("concluir_tarefa")
    global tarefas
 
 
    tarefa = _buscar_tarefa_por_id()
    
    if tarefa: 
        if tarefa['status'] == 'Fazendo':
            tarefa['status'] = 'Concluída' 
            tarefa['data_conclusao'] = datetime.datetime.now()
            print("Tarefa concluída com sucesso!")
        elif tarefa['status'] == 'Concluída':
            print("Erro: Esta tarefa já foi concluída.")
        else:
            print(f"Erro: A tarefa '{tarefa['titulo']}' está pendente. É preciso pegá-la primeiro.")
    
 
 
 
def excluir_antigas():
    """
    Ciclo de Vida 5: Exclusão de Concluídas Antigas[cite: 29].
    """
    _print_debug("excluir_antigas")
    global tarefas
    agora = datetime.datetime.now()
    tarefas_mantidas = [t for t in tarefas if not (
        t.get('status') == 'Concluída' and 
        t.get('data_conclusao') and 
        (agora - t['data_conclusao']).days > 7
    )]
    
    excluidas_count = len(tarefas) - len(tarefas_mantidas)
    tarefas = tarefas_mantidas
    
    if excluidas_count > 0:
        print(f"{excluidas_count} tarefa(s) antiga(s) foi(ram) excluída(s).")
    else:
        print("Nenhuma tarefa antiga para excluir.")
 
 
 
def relatorio():
    """
    Ciclo de Vida 6: Relatório de tarefas[cite: 30].
    """
    _print_debug("relatorio")
    
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
        
    print("\n--- Relatório Completo de Tarefas ---")
    for tarefa in tarefas:
        print(f"\nID: {tarefa['id']}")
        print(f"  Título: {tarefa['titulo']}")
        print(f"  Status: {tarefa['status']}")
        print(f"  Prioridade: {tarefa['prioridade']}")
        print(f"  Origem: {tarefa['origem']}")
        
        if tarefa.get('data_conclusao'):
            data_formatada = tarefa['data_conclusao'].strftime("%d/%m/%Y %H:%M:%S")
            print(f"  Data de Conclusão: {data_formatada}")
 
 
def menu():
    """
    Requisito 1: Menu Principal (Abstração de Controle)[cite: 36].
    """
    _print_debug("menu")
    while True:
        print("\nMenu Principal:")
        print("1. Criar Tarefa")
        print("2. Pegar Próxima Tarefa (Verificar Urgência)")
        print("3. Atualizar Prioridade")
        print("4. Concluir Tarefa")
        print("5. Excluir Tarefas Antigas")
        print("6. Relatório")
        print("7. Sair")
        try:
            opcao = input("Escolha uma opção: ")
            opcao_num = int(opcao)
            if opcao_num == 1:
                criar_tarefa()
            elif opcao_num == 2:
                pegar_tarefa()
            elif opcao_num == 3:
                atualizar_prioridade()
            elif opcao_num == 4:
                concluir_tarefa()
            elif opcao_num == 5:
                excluir_antigas()
            elif opcao_num == 6:
                relatorio()
            elif opcao_num == 7:
                print("Saindo...")
                break
            else:
                print("Opção inválida. Escolha um número entre 1 e 7.")
                
        except ValueError:
            print("Erro técnico: Por favor, digite apenas números.")
 
 
if __name__ == "__main__":
    menu()