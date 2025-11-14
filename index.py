#importação da lógica do código
import funcoes_tarefas

# --- Bloco da execução principal ---

if __name__ == "__main__":
    """
    Este é o ponto de entrada do programa.
    Ele chama as funções de inicialização e o menu
    do módulo 'funcoes_tarefas'.
    """

    #verifica a existência dos arquivos json e os criar(se necessário)
    funcoes_tarefas.verificar_e_criar_arquivos()
    
    #carrega os arquivos para a memória
    funcoes_tarefas.carregar_tarefas_json()

    #inicia nosso loop
    funcoes_tarefas.menu()
