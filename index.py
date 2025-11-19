import sys
import funcoes_tarefas

def exibir_menu():
    print("""
=====================================
        SISTEMA DE TAREFAS
=====================================
1 - Criar nova tarefa
2 - Pegar próxima tarefa
3 - Atualizar prioridade de tarefa
4 - Concluir tarefa
5 - Arquivar tarefas antigas (+7 dias)
6 - Excluir tarefa (Lógica)
7 - Relatório Geral (Ativas)
8 - Relatório de Arquivadas
9 - Sair
=====================================
    """)

def main():
    # Inicializa dados e arquivos 
    carregar_dados()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        # Validação da opção escolhida
        if opcao not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print("\nErro: Opção inválida! Escolha um número do menu.\n")
            continue

        try:
            if opcao == "1":
                criar_tarefa()
            elif opcao == "2":
                pegar_tarefa()
            elif opcao == "3":
                atualizar_prioridade()
            elif opcao == "4":
                concluir_tarefa()
            elif opcao == "5":
                arquivar_tarefas_antigas()
            elif opcao == "6":
                excluir_tarefa()
            elif opcao == "7":
                relatorio_completo()
            elif opcao == "8":
                relatorio_arquivados()
            elif opcao == "9":
                print("\nSalvando dados... ")
                salvar_dados()
                print("Sistema finalizado!")
                sys.exit()

        except Exception as e:
            print(f"Erro inesperado no menu: {e}")

if __name__ == "__main__":
    _print_debug("main") # Debug no início da execução principal
    main()
