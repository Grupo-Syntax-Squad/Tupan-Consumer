import paho.mqtt.subscribe as subscribe
from dotenv import load_dotenv
from os import getenv
from json import loads
import datetime

load_dotenv()

TOPICO=getenv("TOPICO")
HOST=getenv("HOST_MQTT")
PORT=int(getenv("PORT_MQTT"))  

def waitMqttMessage():
    print(f"{datetime.datetime.now()} [MQTTConnection] Aguardando mensagem MQTT")
    response = subscribe.simple(TOPICO, hostname=HOST, port=PORT)
    print(f"{datetime.datetime.now()} [MQTTConnection] Mensagem recebida: ", response.topic, response.payload)
    return response.topic, loads(response.payload)