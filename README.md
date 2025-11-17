# Organizador-de-Tarefas
Um simples, porém funcional, organizador de tarefas feito em Python para a linha de comando. Focado para gerenciar atividades com base em prioridades.

Este projeto foi desenvolvido como uma atividade prática do curso de Ciência da Computação no Centro Universitário Braz Cubas. O objetivo foi aplicar os conceitos de Python em um software funcional e interativo.
Foi realizado por um grupo de 5 alunos do segundo semestre, com a assistência de IAs como ferramenta de aprendizado e produtividade.

As tarefas ativas são carregadas de um arquivo tarefas.json ao iniciar e salvas de volta ao sair. Um arquivo tarefas_arquivadas.json é usado para manter um histórico de todas as tarefas concluídas ou excluídas, garantindo que nenhum dado seja perdido.

O sistema opera através de um menu interativo no terminal, oferecendo as seguintes opções:

1. ​Criar Tarefa: Permite registrar uma nova tarefa com título, descrição, prioridade (Urgente, Alta, Média, Baixa) e origem (Email, Telefone, Chamado do Sistema). O sistema automaticamente adiciona um ID único e a data de criação.

2. ​Pegar Próxima Tarefa: Seleciona a tarefa "Pendente" de maior prioridade disponível e a move para o estado "Fazendo". Apenas uma tarefa pode estar "Fazendo" por vez.

3. ​Atualizar Prioridade: Altera a prioridade de uma tarefa existente usando seu ID único.

​4. Concluir Tarefa: Muda o estado da tarefa "Fazendo" para "Concluída" e registra a data/hora da conclusão.

5. ​Arquivar Tarefas Antigas: Realiza uma limpeza no sistema, movendo tarefas "Concluídas" há mais de 7 dias para o estado "Arquivado". Essas tarefas são movidas para o arquivo de histórico (tarefas_arquivadas.json).

6. ​Excluir Tarefa (Exclusão Lógica): Marca uma tarefa existente como "Excluída". A tarefa não é removida da lista principal, mas fica oculta dos relatórios ativos e é movida para o arquivo de histórico.

​7. Relatório Geral (Ativas): Exibe uma lista detalhada de todas as tarefas que não estão 'Arquivadas' ou 'Excluídas'. Para tarefas concluídas, calcula e exibe o tempo total de execução.

8. ​Relatório de Tarefas Arquivadas: Exibe uma lista de todas as tarefas que estão com o status "Arquivado" (não inclui tarefas "Excluídas").

9. ​Salvar e Sair: Salva o estado atual de todas as tarefas no arquivo tarefas.json e encerra a execução do programa..

ELEMENTOS DO PROJETO:

Python 3.13 (ou compatível);

​datetime, para manipulação de datas (criação, conclusão, e verificação de 7 dias);

​json, para persistência de dados (salvar e carregar a lista de tarefas);

​os, para verificar se os arquivos .json existem antes de tentar lê-los;

​sys, para finalizar o programa de forma controlada (sys.exit()).

AUTORES:

Igor Correa;

Mariana Moreira Barbosa;

Maria Nascimento;

Victoria Fagundes;

Samara Fernandes.
