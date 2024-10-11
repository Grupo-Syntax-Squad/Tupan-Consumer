import redis
from dotenv import load_dotenv
from os import getenv
from json import dumps

load_dotenv()

HOST=getenv("HOST_REDIS")
PORT=int(getenv("PORT_REDIS"))
PASSWORD=getenv("PASSWORD_REDIS")


r = redis.Redis(
    host=HOST,
    port=PORT,
    password=PASSWORD
)

def setData(response):
    r.set(response[1]['mac'], dumps(response[1]))
    print("Dados enviados para o redis:", response)

def getRedisData(response):
    return r.get(response[1]['mac'])
