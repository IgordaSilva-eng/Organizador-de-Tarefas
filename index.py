from funcoes_tarefas import (
    carregar_dados,
    salvar_dados,
    criar_tarefa,
    pegar_tarefa,
    atualizar_prioridade,
    concluir_tarefa,
    excluir_tarefa,
    arquivar_tarefas_antigas,
    relatorio_completo,
    relatorio_arquivadas
)

def exibir_menu():
    print("""
=====================================
        SISTEMA DE TAREFAS
=====================================

1 - Criar nova tarefa
2 - Pegar próxima tarefa
3 - Atualizar prioridade de tarefa
4 - Concluir tarefa
5 - Excluir tarefa
6 - Relatório completo
7 - Relatório de tarefas arquivadas
8 - Arquivar tarefas antigas (+7 dias)
9 - Sair

=====================================
    """)

def main():
    carregar_dados()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_tarefa()

        elif opcao == "2":
            pegar_tarefa()

        elif opcao == "3":
            atualizar_prioridade()

        elif opcao == "4":
            concluir_tarefa()

        elif opcao == "5":
            excluir_tarefa()

        elif opcao == "6":
            relatorio_completo()

        elif opcao == "7":
            relatorio_arquivadas()

        elif opcao == "8":
            arquivar_tarefas_antigas()

        elif opcao == "9":
            print("\nSalvando dados... ")
            salvar_dados()
            print("Sistema finalizado! Até mais \n")
            break

        else:
            print("\n Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    main()

