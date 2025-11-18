import datetime
import json
import os

# ===========================
# CONSTANTES DO SISTEMA
# ===========================
ARQUIVO_TAREFAS = "tarefas.json"
ARQUIVO_ARQUIVADAS = "tarefas_arquivadas.json"
STATUS_PENDENTE = "pendente"
STATUS_FAZENDO = "fazendo"
STATUS_CONCLUIDA = "concluída"
STATUS_ARQUIVADA = "arquivada"
STATUS_EXCLUIDA = "excluída"

tarefas = []
tarefas_arquivadas = []
id_contador = 1


# =============================
# CARREGAMENTO E SALVAMENTO
# =============================
def carregar_dados():
    global tarefas, tarefas_arquivadas, id_contador

    if os.path.exists(ARQUIVO_TAREFAS):
        try:
            with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                tarefas = dados.get("tarefas", [])
                id_contador = dados.get("id_contador", 1)
        except:
            tarefas = []
            id_contador = 1
    else:
        tarefas = []
        id_contador = 1

    if os.path.exists(ARQUIVO_ARQUIVADAS):
        try:
            with open(ARQUIVO_ARQUIVADAS, "r", encoding="utf-8") as f:
                tarefas_arquivadas = json.load(f)
        except:
            tarefas_arquivadas = []
    else:
        tarefas_arquivadas = []


def salvar_dados():
    dados = {
        "tarefas": tarefas,
        "id_contador": id_contador
    }
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    with open(ARQUIVO_ARQUIVADAS, "w", encoding="utf-8") as f:
        json.dump(tarefas_arquivadas, f, indent=4, ensure_ascii=False)


# =====================================
# FUNÇÕES DE REGRAS E VALIDAÇÃO
# =====================================
def validar_prioridade(valor):
    try:
        valor = int(valor)
        return 1 <= valor <= 5
    except:
        return False


def validar_data(data):
    try:
        datetime.datetime.fromisoformat(data)
        return True
    except:
        return False


def buscar_tarefa_por_id(id_busca):
    for t in tarefas:
        if t["id"] == id_busca:
            return t
    return None


# =====================================
# CRIAR UMA NOVA TAREFA
# =====================================
def criar_tarefa():
    global id_contador

    print("\n=== Criar nova tarefa ===")
    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    data_prevista = input("Data prevista (YYYY-MM-DD): ").strip()
    
    origem = input("Origem (manual/sistema): ").strip().lower()
    while origem not in ["manual", "sistema"]:
        origem = input("Origem inválida. Digite 'manual' ou 'sistema': ")

    prioridade = input("Prioridade (1 a 5): ").strip()
    while not validar_prioridade(prioridade):
        prioridade = input("Inválida. Digite prioridade de 1 a 5: ")

    tarefa = {
        "id": id_contador,
        "titulo": titulo,
        "descricao": descricao,
        "data_criacao": datetime.datetime.now().isoformat(),
        "data_prevista": data_prevista,
        "data_conclusao": None,
        "origem": origem,
        "prioridade": int(prioridade),
        "status": STATUS_PENDENTE
    }

    tarefas.append(tarefa)
    id_contador += 1

    print(f"\n Tarefa criada com ID {tarefa['id']}!\n")


# ======================================
# PEGAR TAREFA POR PRIORIDADE
# ======================================
def pegar_tarefa():
    print("\n=== Pegar próxima tarefa ===")

    # verificar se já tem tarefa em FAZENDO
    for t in tarefas:
        if t["status"] == STATUS_FAZENDO:
            print("\n⚠ Já existe uma tarefa em andamento. Conclua antes de pegar outra.\n")
            return

    # ordenar por prioridade (menor primeiro)
    pendentes = [t for t in tarefas if t["status"] == STATUS_PENDENTE]
    if not pendentes:
        print("\n⚠ Não há tarefas pendentes.\n")
        return

    pendentes.sort(key=lambda x: (x["prioridade"], x["data_criacao"]))
    tarefa = pendentes[0]
    tarefa["status"] = STATUS_FAZENDO

    print(f"\n Tarefa {tarefa['id']} movida para 'fazendo'.\n")


# ======================================
# ATUALIZAR PRIORIDADE
# ======================================
def atualizar_prioridade():
    print("\n=== Atualizar prioridade ===")
    try:
        id_busca = int(input("ID da tarefa: "))
    except:
        print(" ID inválido.")
        return

    tarefa = buscar_tarefa_por_id(id_busca)
    if not tarefa or tarefa["status"] == STATUS_EXCLUIDA:
        print(" Tarefa não encontrada ou excluída.")
        return

    nova = input("Nova prioridade (1 a 5): ")
    while not validar_prioridade(nova):
        nova = input("Inválida. Digite de 1 a 5: ")

    tarefa["prioridade"] = int(nova)
    print("\n Prioridade atualizada!\n")


# ======================================
# CONCLUIR TAREFA
# ======================================
def concluir_tarefa():
    print("\n=== Concluir tarefa ===")
    try:
        id_busca = int(input("ID da tarefa: "))
    except:
        print(" ID inválido.")
        return

    tarefa = buscar_tarefa_por_id(id_busca)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    if tarefa["status"] != STATUS_FAZENDO:
        print(" Só é possível concluir tarefas que estão em 'fazendo'.")
        return

    tarefa["status"] = STATUS_CONCLUIDA
    tarefa["data_conclusao"] = datetime.datetime.now().isoformat()

    print("\n Tarefa concluída!\n")


# ======================================
# EXCLUIR TAREFA
# ======================================
def excluir_tarefa():
    print("\n=== Excluir tarefa ===")
    try:
        id_busca = int(input("ID da tarefa: "))
    except:
        print(" ID inválido.")
        return

    tarefa = buscar_tarefa_por_id(id_busca)
    if not tarefa:
        print(" Tarefa não encontrada.")
        return

    tarefa["status"] = STATUS_EXCLUIDA
    print("\n Tarefa excluída (não aparecerá mais nos relatórios).\n")


# ======================================
# ARQUIVAR TAREFAS ANTIGAS
# ======================================
def arquivar_tarefas_antigas():
    print("\n=== Arquivar tarefas concluídas há +7 dias ===")

    agora = datetime.datetime.now()
    count = 0

    for t in tarefas[:]:
        if t["status"] == STATUS_CONCLUIDA and validar_data(t["data_conclusao"]):
            dt = datetime.datetime.fromisoformat(t["data_conclusao"])
            if (agora - dt).days >= 7:
                t["status"] = STATUS_ARQUIVADA
                tarefas_arquivadas.append(t)
                tarefas.remove(t)
                count += 1

    print(f"\n {count} tarefa(s) arquivada(s).\n")


# ======================================
# RELATÓRIO COMPLETO
# ======================================
def relatorio_completo():
    print("\n=== RELATÓRIO GERAL ===\n")

    for t in tarefas:
        if t["status"] == STATUS_EXCLUIDA:
            continue  # excluídas não aparecem

        print(f"ID: {t['id']}")
        print(f"Título: {t['titulo']}")
        print(f"Descrição: {t['descricao']}")
        print(f"Status: {t['status']}")
        print(f"Origem: {t['origem']}")
        print(f"Prioridade: {t['prioridade']}")
        print(f"Data criação: {t['data_criacao']}")
        print(f"Data prevista: {t['data_prevista']}")
        print(f"Data conclusão: {t['data_conclusao']}")

        if t["status"] == STATUS_CONCLUIDA:
            dtc = datetime.datetime.fromisoformat(t["data_conclusao"])
            dtc0 = datetime.datetime.fromisoformat(t["data_criacao"])
            duracao = dtc - dtc0
            print(f"Tempo total: {duracao}")

        print("-" * 30)


# ======================================
# RELATÓRIO DE ARQUIVADAS
# ======================================
def relatorio_arquivadas():
    print("\n=== RELATÓRIO DE TAREFAS ARQUIVADAS ===\n")

    if not tarefas_arquivadas:
        print("Nenhuma tarefa arquivada.")
        return

    for t in tarefas_arquivadas:
        print(f"ID: {t['id']}")
        print(f"Título: {t['titulo']}")
        print(f"Origem: {t['origem']}")
        print(f"Prioridade: {t['prioridade']}")
        print(f"Data criação: {t['data_criacao']}")
        print(f"Data conclusão: {t['data_conclusao']}")
        print("-" * 30)    
            
