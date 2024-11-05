# Tupã Consumer
Serviço de recepção de dados para a aplicação Tupã.

- [Pré requisitos](#pré-requisitos)
- [Setup do ambiente de execução](#setup-do-ambiente-de-execução)
    - [Criando e ativando o ambiente virtual (Opcional)](#criando-e-ativando-o-ambiente-virtual-opcional)
    - [Instalando dependências](#instalando-dependências)
    - [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Rodando o serviço](#rodando-o-serviço)
- [Formato do json recebido pelo MQTT](#formato-do-json-recebido-pelo-mqtt)
- [Script de teste de envio de dados ao serviço](#script-de-teste-de-envio-de-dados-ao-serviço)

## Pré requisitos
- Python
- Redis
- PostgreSQL

## Setup do ambiente de execução

### Criando e ativando o ambiente virtual (Opcional)
```bash
python -m venv .venv & ./.venv/Scripts/activate
```

> [!WARNING]
> É possível que a política de execução de scripts do Windows impossibilite a criação do ambiente virtual, caso aconteça segue o artigo sobre políticas de execução: [https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4)

### Instalando dependências
```bash
pip install -r ./requirements.txt
```

### Variáveis de ambiente
Copie o arquivo .env_sample e adapte os valores das variáveis de ambiente para seu ambiente de execução.
```bash
cp ./.env_sample ./.env
```

## Rodando o serviço
```bash
python ./src/main.py
```

## Formato do json recebido pelo MQTT
```json
{
    "mac": "123",
    "dados": {
        "temp": 40,
        "umid": 3
    },
    "timestamp": 1729399539.969931
}
```
> [!NOTE]
> Vale ressaltar que as chaves dos dados variam de estação para estação, ou seja, nem sempre a temperatura vai ter uma chave chamada "temp", e haverá casos em que nem existirá temperatura.

## Script de teste de envio de dados ao serviço
Caso surgir a necessidade de um envio de dados manual de teste esse script fará o envio utilizando todo o setup do serviço.
```py
import paho.mqtt.publish as publish
from dotenv import load_dotenv
from os import getenv
from json import dumps
from datetime import datetime

load_dotenv()

TOPICO=getenv("TOPICO")
HOST=getenv("HOST_MQTT")
PORT=int(getenv("PORT_MQTT"))

mensagem = {
    "mac": "123",
    "dados": {
        "temp": 40,
        "umid": 3
    },
    "timestamp": datetime.now().timestamp()
}

publish.single(
    topic=TOPICO,
    payload=dumps(mensagem),
    hostname=HOST,
    port=PORT
)

print(f"Mensagem publicada no tópico {TOPICO}: {mensagem}")
```
