# Projeto LGPD com Python e SQLAlchemy

## Descrição

Este projeto tem como objetivo aplicar conceitos da Lei Geral de Proteção de Dados (LGPD) em um sistema de manipulação de dados utilizando Python e banco de dados PostgreSQL.

A aplicação realiza a leitura de dados de usuários e executa processos de anonimização, geração de arquivos e medição de desempenho.

## Funcionalidades

### 1. Anonimização de Dados (LGPD)
Os dados sensíveis dos usuários são tratados conforme regras de anonimização:

- Nome: mantém apenas a primeira letra do primeiro nome
- CPF: oculta parcialmente os números
- Email: mantém apenas o primeiro caractere antes do domínio
- Telefone: exibe apenas os últimos 4 dígitos

### 2. Geração de Arquivos por Ano
Cria arquivos CSV separados por ano de nascimento dos usuários.

Exemplo:
- 1990.csv
- 1991.csv

Todos os dados nesses arquivos estão anonimizados.

### 3. Geração de Arquivo Geral
Cria um arquivo único contendo:
- Nome
- CPF

Neste caso, os dados não são anonimizados.

Arquivo gerado:
- todos.csv

### 4. Medição de Tempo de Execução
Utiliza um decorator para medir o tempo de execução das funções principais:

- atividade2
- atividade3

Os resultados são registrados em um arquivo de log:

- log.txt

## Tecnologias Utilizadas

- Python
- SQLAlchemy
- PostgreSQL
- psycopg2
- python-dotenv

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/nataliathomazelliferreira/Mini_ProjetoII.git
cd Mini_ProjetoII
````

### 2. Criar ambiente virtual

No terminal, execute:

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DATABASE_URL=postgresql+psycopg2://usuario:senha@host:porta/banco
```

### 6. Executar o projeto

```bash
python main.py
```

## Estrutura do Projeto

```
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── log.txt
├── *.csv
```

## Observações

* Os arquivos `.csv` e `log.txt` são gerados automaticamente e não devem ser versionados.
* O arquivo `.env` contém informações sensíveis e também não deve ser enviado ao repositório.
* O projeto segue práticas básicas de segurança e organização de código.

Projeto desenvolvido para fins acadêmicos.
