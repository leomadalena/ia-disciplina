# ia-disciplina
Protótipo de Sistema Inteligente para Escolha de Disciplinas

Este é um protótipo de sistema inteligente para escolha de disciplinas. Ele utiliza o banco de dados MongoDB para armazenar informações sobre as disciplinas e os alunos.
Requisitos

Para executar o sistema, é necessário ter o Python3 instalado e as seguintes bibliotecas:

    pymongo
    tkinter
    pprint

Utilização

Para executar o sistema, basta rodar o arquivo "prototipoIA.py". O sistema abrirá uma janela com as opções para o usuário.
Escolha de Disciplinas

A primeira opção do sistema é a escolha de disciplinas que o aluno já cursou. Para selecionar as disciplinas, o aluno deve marcar as caixas de seleção correspondentes às disciplinas.
Escolha de Área de Conhecimento

A segunda opção do sistema é a escolha de áreas de conhecimento. O aluno deve marcar as caixas de seleção correspondentes às áreas que tem interesse.
Resultado

Ao concluir a escolha das disciplinas e áreas de conhecimento, o sistema exibirá uma lista de disciplinas recomendadas para o aluno, com base nas seguintes regras:

    Se o aluno tiver interesse em uma determinada área de conhecimento, é recomendável selecionar disciplinas nessa área para ele.
    Se a relevância de uma disciplina for alta para o curso que o aluno está fazendo, é recomendável que o aluno selecione essa disciplina.
    Se a disciplina for obrigatória para o curso do aluno, então ele deve selecioná-la.
    Se a área de conhecimento de uma disciplina for muito diferente da área de conhecimento principal do curso do aluno, é melhor evitar essa disciplina ou avaliar cuidadosamente sua relevância.

As disciplinas são exibidas em ordem de relevância, e o sistema também verifica se a soma dos créditos das disciplinas recomendadas não ultrapassa um limite definido (30 créditos, por padrão).
Funcionamento

O código utiliza a biblioteca pymongo para se conectar ao banco de dados MongoDB e fazer consultas e atualizações nos documentos da coleção "disciplinas". O código também utiliza a biblioteca tkinter para criar a interface gráfica do sistema.

As disciplinas são armazenadas no banco de dados como documentos JSON, com os seguintes campos:

    nome
    area_conhecimento
    creditos
    nucleo
    relevancia
    cursado

O campo "cursado" é atualizado pelo sistema de acordo com as escolhas do usuário.
Autores

Este protótipo foi desenvolvido por [nome do autor] e [nome do autor], como parte do projeto [nome do projeto].
