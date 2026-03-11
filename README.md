<p align="center">
    <img src="./static/logo.png" alt="Hermes API">
</p>

<p align="center">
    <em>Hermes API, uma API mensageira</em>
</p>

# Sobre

API para uso no Grafana, com conexão com mutiplos bancos de dados. Esta API tem por objetivo ser uma alternativa sem muitas manutenções.

O Grafana gratuito em sua versão 9 não tem conexão direta com o banco de dados Oracle. O Hermes API desempenha o papel de uma ponte, sendo responsável pela conexão.

## Caso de uso

Para uma menor manutenção e simplecidade de uso visando à equipe, pode-se criar endpoints dinâmicos que irão consultar um banco de dados e uma tabela ou view. Por exemplo:

`/grafana/db/oracle/SCHEMA.MINHAVIEW`: O endpoint estará preparado para se conectar em uma engine específica e fazer a consulta na tabela que foi passada `SHEMA.MINHAVIEW`. 

Sua manutenção será mais adaptativa aos critérios de filtros ou padronizar condições para as requisições.

Grafana  -->  API ---> Banco de Dados

## Instalação

Crie um ambiente e instale as dependências

```
python -m venv .venv
```
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```

## Oracle Instantclient

#### Linux Mint 22.x / Ubuntu 24.04

##### 1) Dependências

```
sudo apt update
```
```
sudo apt install -y unzip libaio1t64
```

##### 2) Criar pasta

```
sudo mkdir -p /opt/oracle
```
```
cd /opt/oracle
```

##### 3) Baixar Instant Client (Basic Lite 21.13)

```
sudo wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip
```

##### 4) Descompactar

```
sudo unzip instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip
```

##### 5) Registrar no linker

```
echo "/opt/oracle/instantclient_21_13" | sudo tee /etc/ld.so.conf.d/oracle-instantclient.conf
```
```
sudo ldconfig
```

##### 6) Compatibilidade libaio (Ubuntu 24.04/Mint 22)

```
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1
```
```
sudo ldconfig
```

##### 7) Validar

```
ldconfig -p | rg "libclntsh|libaio.so.1"
```

## Iniciando a API

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Exemplo de serviço

Crie um arquivo em `/etc/systemd/system/hermes-api.service` e insira o exemplo abaixo substituindo os dados em `<MEU_DADO>`

```
[Unit]
Description=Uvicorn instance to serve Hermes API
After=network.target

[Service]
User=<SEU_USUARIO>
Group=www-data
WorkingDirectory=<CAMINHO_DO_PROJETO>/hermes-api
# Carrega arquivo .env
EnvironmentFile=<CAMINHO_DO_PROJETO>/hermes-api/.env
ExecStart=<CAMINHO_DO_PROJETO>/hermes-api/.venv/bin/uvicorn app.main:app --host ${APP_HOST} --port ${APP_PORT}
Restart=always

[Install]
WantedBy=multi-user.target
```
```
sudo systemctl daemon-reload
```
