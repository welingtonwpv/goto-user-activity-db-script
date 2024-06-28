import requests
import base64
import json
import http.client
import pyodbc
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


# Definir as credenciais do cliente
client_id = "SEU_CLIENT_ID_AQUI"
client_secret = "SEU_CLIENT_SECRET_AQUI"
creds = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


# Acessa a variável de ambiente "refresh_token_previous"
refresh_token_previous = os.getenv("refresh_token_previous")


# Verifica se o token foi encontrado e o imprime
if refresh_token_previous:
    print("Refresh Token presente!")
else:
    print("A variável refresh_token_previous não está definida no arquivo .env.")


# Pegando refresh_token na variável de ambiente
refresh_token = refresh_token_previous


# Função para obter um novo access_token
def obter_novo_access_token(refresh_token, creds):
    token_url = "https://authentication.logmeininc.com/oauth/token"
    data = {"redirect_uri": "http://www.google.com", "grant_type": "refresh_token", "refresh_token": refresh_token}
    headers = {"Authorization": "Basic " + creds, "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    response = requests.post(token_url, headers=headers, data=data)
    return response.json()


# Função para fazer a solicitação à API com datas dinâmicas
def get_users_activity(access_token, start_time, end_time):
    conn = http.client.HTTPSConnection("api.goto.com")
    headers = {'Authorization': 'Bearer ' + access_token}
    endpoint = f"/call-reports/v1/reports/user-activity?startTime={start_time}&endTime={end_time}"
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data)


# Função para converter milisegundos em hh:mm:ss
def milliseconds_to_timestamp(milliseconds):
    seconds = milliseconds / 1000.0
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


# Verificar se há um novo refresh_token disponível
response = obter_novo_access_token(refresh_token, creds)
if "refresh_token" in response:
    print("Refresh Token Atualizado!")
    # Aqui você deve atualizar seu arquivo .env com o novo refresh token:
    # with open('.env', 'w') as env_file:
    #     env_file.write(f"refresh_token_previous='{response['refresh_token']}'")
    # Lembre-se de garantir que o arquivo .env esteja corretamente configurado no ambiente de execução.


# Definir datas de início e término dinâmicas
start_date = datetime.now() - timedelta(days=7)  # Data de 7 dias atrás
end_date = datetime.now()  # Data atual


# Converter datas para strings no formato ISO 8601
start_time = start_date.strftime("%Y-%m-%dT%H:%M:%S")
end_time = end_date.strftime("%Y-%m-%dT%H:%M:%S")

# Fazer a solicitação à API com as datas dinâmicas
# Instrua os usuários a inserirem suas próprias credenciais e configurações antes de executar este código.


# Fazer a solicitação à API para o último dia
last_day_start = datetime.now() - timedelta(days=1)  # Data do último dia
last_day_end = datetime.now() # Data atual

last_day_start_time = last_day_start.strftime("%Y-%m-%dT%H:%M:%S")
last_day_end_time = last_day_end.strftime("%Y-%m-%dT%H:%M:%S")

# Instrua os usuários a inserirem suas próprias credenciais e configurações antes de executar este código.


# Conectar ao Banco de Dados
dados_conexao = (
    "Driver={SQL Server};"
    "Server=SEU_ENDERECO_DO_SERVIDOR_SQL_AQUI;"  # Substitua pelo endereço do seu servidor
    "Database=SEU_BANCO_DE_DADOS_AQUI;"  # Substitua pelo nome do seu banco de dados
    "UID=SEU_USUARIO_AQUI;"  # Substitua pelo nome de usuário
    "PWD=SUA_SENHA_AQUI;"  # Substitua pela senha
)

try:
    # Tentar estabelecer a conexão
    conexao = pyodbc.connect(dados_conexao)
    print("Conexão com o banco de dados bem sucedida!")

    cursor = conexao.cursor()

    # Iterar sobre cada item na lista de itens
    for item in users_activity_data['items']:
        # Obter o nome do usuário e o volume de chamadas
        userId = item['userId']
        user_name = item['userName']
        outbound_calls_duration = item['dataValues']['outboundDuration']
        volume = item['dataValues']['volume']
        averageDuration = item['dataValues']['averageDuration']

        # Instrua os usuários a inserirem suas próprias credenciais e configurações antes de executar este código.

        # Inserir os dados no banco de dados
        if outbound_calls_duration != 0:
            comando = f"""INSERT INTO NomeDaSuaTabela(UserId, UserName, WeeklyCallVolume, WeeklyCallsDuration, DailyCallVolume, DailyCallsDuration, averageDuration, AddDate)
            VALUES
                ('{userId}', '{user_name}', {volume}, {outbound_calls_duration}, {total_volume_day}, {total_calls_last_day}, {averageDuration}, '{end_date}')"""
            
            cursor.execute(comando)
            conexao.commit()

    print("Dados inseridos no banco de dados com sucesso!")

    # Fechando a conexão
    conexao.close()

except pyodbc.Error as ex:
    print("Falha na conexão com o banco de dados:", ex)
