from redisConnection import RedisConnection
from postgreSQLConnection import PostgreSQLConnection
import datetime

class ServiceRedisPostgreSQL:
    def __init__(self):
        self.run = True
    
    def start(self):
        try:
            while self.run:
                redisConnection = RedisConnection()
                postgreSQLConnection = PostgreSQLConnection()
                data = redisConnection.getRedisData()
                while len(data) > 0:
                    d = data.pop()
                    mac_address = d['mac']
                    estacoes = postgreSQLConnection.getMacAddress(mac_address)
                    if len(estacoes) > 0 and len(estacoes) < 2:
                        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação encontrada no PostgreSQL")
                        estacao = estacoes[0]
                        print(estacao)
                    else:
                        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação não encontrada no PostgreSQL")
                    
                    
                    
        except KeyboardInterrupt:
            print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")

    def stop(self):
        self.run = False
        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")