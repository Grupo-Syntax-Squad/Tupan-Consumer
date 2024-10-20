import redis
from dotenv import load_dotenv
from os import getenv
from json import dumps, loads
import datetime

load_dotenv()

HOST=getenv("HOST_REDIS")
PORT=int(getenv("PORT_REDIS"))
PASSWORD=getenv("PASSWORD_REDIS")

class RedisConnection:
    def __init__(self):
        print(f"{datetime.datetime.now()} [RedisConnection] Abrindo conexão com o Redis")
        self.r = redis.Redis(
            host=HOST,
            port=PORT,
            password=PASSWORD
        )

    def closeConnection(self):
        print(f"{datetime.datetime.now()} [RedisConnection] Fechando conexão com o Redis")
        self.r.close()

    def saveDataLog(self, dataLog):
        print(f"{datetime.datetime.now()} [RedisConnection] Salvando dados no Redis: ", dataLog)
        self.r.set(dataLog['mac'], dumps(dataLog))

    def deleteDataLog(self, dataLog):
        print(f"{datetime.datetime.now()} [RedisConnection] Deletando dados no Redis: ", dataLog)
        self.r.delete(dataLog['mac'])

    def getRedisData(self):
        print(f"{datetime.datetime.now()} [RedisConnection] Buscando dados no Redis")
        keys = self.r.keys('*')

        valores = []
        while len(keys) > 0:
            valores.append(loads(self.r.get(keys.pop())))
        return valores

    def deleteAll(self):
        keys = self.r.keys("*")

        for key in keys:
            self.r.delete(key)
        
        print(f"{datetime.datetime.now()} [RedisConnection] Todos os dados do Redis foram deletados")

