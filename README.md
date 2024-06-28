## Integração com API GoTo e Banco de Dados

Este script Python integra-se com a API GoTo para obter relatórios de atividade de usuários e armazenar os dados em um banco de dados SQL Server.

## Pré-requisitos

Antes de executar o script, certifique-se de ter os seguintes requisitos instalados e configurados:

- Python 3.x
- Pacotes Python: `requests`, `pyodbc`, `dotenv`
- Um banco de dados SQL Server configurado com acesso adequado

Além disso, configure um arquivo `.env` com as seguintes variáveis:

refresh_token_previous='seu_refresh_token_aqui'


## Instalação

1. Clone o repositório para o seu ambiente local:

   ```bash
   git clone https://github.com/welingtonwpv/goto-user-activity-db-script

Instale as dependências Python usando o pip:


pip install -r requirements.txt
Configuração
Configure as variáveis de ambiente no arquivo .env conforme mencionado acima.

Verifique se o acesso ao banco de dados está configurado corretamente no script (dados_conexao).

## Uso

Execute o script main.py para iniciar a integração:

## python main.py

O script realiza as seguintes operações:

Obtém um novo access token da API GoTo usando um refresh token.
Coleta dados de atividade de usuários para a última semana.
Calcula métricas diárias específicas (volume e duração de chamadas).
Insere os dados na tabela SUATABELAAQUI no banco de dados especificado.
Certifique-se de que o script tenha permissões adequadas para acessar a API GoTo e o banco de dados SQL Server.

## Contribuição

Contribuições adicionais são bem-vindas via pull requests. Para mudanças importantes, abra um problema primeiro para discutir o que você gostaria de mudar.
