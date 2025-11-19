import sys
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
    relatorio_arquivados,
    _print_debug
)

def exibir_menu():
    """
    Exibe as opções do menu principal.
    """
    print("""
=====================================
        SISTEMA DE TAREFAS
=====================================
1 - Criar nova tarefa
2 - Pegar próxima tarefa (Verificar Urgência)
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
    """
    Função principal de execução.
    """
    # Debug inicial
    _print_debug("main")

    # Carregar dados e criar arquivos se necessário
    carregar_dados()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print("\nErro: Opção inválida! Escolha um número de 1 a 9.\n")
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
    main()
