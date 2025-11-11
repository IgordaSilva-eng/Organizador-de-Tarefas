# Organizador-de-Tarefas
Um simples, porém funcional, organizador de tarefas feito em Python para a linha de comando. Focado para gerenciar atividades com base em prioridades.

Este projeto foi desenvolvido como uma atividade prática do curso de Ciência da Computação no Centro Universitário Braz Cubas. O objetivo foi aplicar os conceitos de Python em um software funcional e interativo.
Foi realizado por um grupo de 5 alunos do segundo semestre, com a assistência de IAs como ferramenta de aprendizado e produtividade.

O sistema opera através de um menu interativo no terminal, oferecendo as seguintes opções:

1. Criar Tarefa: Permite registrar uma nova tarefa com título, prioridade (Baixa, Média, Alta, Urgente) e origem (E-mail, Telefone, Sistema);
2. Pegar Próxima Tarefa: Seleciona a tarefa de maior prioridade que esteja "Pendente" e a move para o estado "Fazendo". Apenas uma tarefa pode estar "Fazendo" por vez;
3. Atualizar Prioridade: Altera a prioridade de uma tarefa existente usando seu ID único;
4. Concluir Tarefa: Muda o estado da tarefa "Fazendo" para "Concluída";
5. Excluir Tarefas Antigas: Realiza uma limpeza no sistema, removendo tarefas que foram concluídas há mais de 7 dias;
6. Relatório: Exibe uma lista completa de todas as tarefas, independentemente do seu estado ou prioridade;
7. Sair: Encerra a execução do programa.

ELEMENTOS DO PROJETO:

Python 3.13;

datetime.

AUTORES:

Igor da Correa;

Mariana Barbosa;

Maria Gabriela;

Victoria Agatha;

Samara Fernanda.
