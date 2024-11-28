import redis
from dotenv import load_dotenv
from os import getenv
import datetime

load_dotenv()

HOST=getenv("HOST_REDIS")
PORT=int(getenv("PORT_REDIS"))
PASSWORD=getenv("PASSWORD_REDIS")

class RedisConnection:
    def __init__(self):
        print(f"{datetime.datetime.now()} [RedisConnection] Abrindo conexão com o Redis")
        self.conn = redis.Redis(
            host=HOST,
            port=PORT,
            password=PASSWORD
        )

    def close(self):
        print(f"{datetime.datetime.now()} [RedisConnection] Fechando conexão com o Redis")
        self.conn.close()

