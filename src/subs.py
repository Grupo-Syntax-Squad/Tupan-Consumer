import paho.mqtt.subscribe as subscribe
from dotenv import load_dotenv
from os import getenv
from json import loads

load_dotenv()

TOPICO=getenv("TOPICO")
HOST=getenv("HOST_MQTT")
PORT=int(getenv("PORT_MQTT"))


def getData():
    response = subscribe.simple(TOPICO, hostname=HOST, port=PORT)
    return response.topic, loads(response.payload)