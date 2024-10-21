from redisConnection import RedisConnection
from postgreSQLConnection import PostgreSQLConnection
import datetime
from time import sleep

class ServiceRedisPostgreSQL:
    def __init__(self):
        self.run = True
    
    def start(self):
        try:
            while self.run:
                sleep(5)
                redisConnection = RedisConnection()
                postgreSQLConnection = PostgreSQLConnection()
                data = redisConnection.getRedisData()
                while len(data) > 0:
                    d = data.pop()
                    mac_address = d['mac']
                    estacoes = postgreSQLConnection.getMacAddress(mac_address)
                    if len(estacoes) <= 0 or len(estacoes) > 2:
                        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação não encontrada no PostgreSQL")
                        redisConnection.deleteDataLog(d)
                    else:
                        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação encontrada no PostgreSQL")
                        estacao = estacoes[0]
                        estacao_parametros, parametros = postgreSQLConnection.getEstacaoParametros(estacao[0])
                        for estacao_parametro in estacao_parametros:
                            try:
                                index = estacao_parametros.index(estacao_parametro)
                                json_name = parametros[index][7]
                                dados = d['dados'][json_name]
                                timestamp = d["timestamp"]
                                timestamp_converido = datetime.datetime.fromtimestamp(timestamp)
                                postgreSQLConnection.setMedicao(timestamp, timestamp_converido, dados, estacao_parametro[0])
                            except Exception as e:
                                print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Erro ao cadastrar a medição do parâmetro: {e}")
                        redisConnection.deleteDataLog(d)
                redisConnection.closeConnection()
                postgreSQLConnection.closeConnection()         
        except KeyboardInterrupt:
            print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")

    def stop(self):
        self.run = False
        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")

if __name__ == "__main__":
    serviceRedisPostgreSQL = ServiceRedisPostgreSQL()
    try:
        serviceRedisPostgreSQL.start()
    except:
        print("Erro")
    finally:
        serviceRedisPostgreSQL.stop()