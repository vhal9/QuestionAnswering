# QuestionAnswering

## Resumo:
  Este é um repositório contém o desenvolvimento de um projeto de IC, que consiste em uma ferramenta de perguntas e respostas com enfâse em linguagem informal, utilizando a base de conhecimento estruturados da Wikidata e não estruturados da Wikipedia.

## Projeto Desenvolvido no Python 3.6.

## Bibliotecas:
### Processamento de textos
- unicode
- nltk
- spacy

### Rotinas de requisições
- requests
- wikipedia
### Manipulação de dados
- sqlite3
- os
- pandas
### bibliotecas para desenvolvimento(opcionais)
- virtualenv
- jupyter

## Estado Atual
- Arquivo jupyter do processamento das perguntas, processando as perguntas e buscando a resposta utilizando a classe RotinaBD
- Classe RotinaBD que busca a resposta a pergunta no banco de dados.
- Classe QuestionProcessing: primeira versão com retorno de dicionario: {entidade, propriedade, indicadorPergunta, sinonimoPropriedade}, utilizando apenas o WordNet para desambiguar

## Como executar o projeto (versão atual):

> Criar a virtual env ```vitualenv [nomeDaVM]```

> Prepare o ambiente virtual ``` source [nomeDaVM]/bin/activate```

> Clone o repositório ```git clone [Repositório]```

> Vá para a pasta do repositório ```cd [Repositório]```

> Instalar pacotes necessários ```pip3 install -r requirements.txt```

> Suba o servidor de notebooks ```jupyter notebook```

## Diagrama da Arquitetura ao Final do Projeto 
![Screenshot](ArquiteturaDoProjeto.jpg)

## Diagrama do Banco de dados
![Screenshot](notebook/database/databaseIC.jpeg)

