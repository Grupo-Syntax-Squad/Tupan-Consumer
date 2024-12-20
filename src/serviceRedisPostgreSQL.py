from redisConnection import RedisConnection
from modules.station import ModuleStation
import datetime
from time import sleep

class ServiceRedisPostgreSQL:
    def __init__(self):
        self.run = True
        self.module = ModuleStation()
    
    def start(self):
        try:
            while self.run:
                sleep(5)
                redisConnection = self.create_redis_connection()
                data = redisConnection.getRedisData()
                while len(data) > 0:
                    payload = data.pop()
                    mac_address = payload['mac']
                    stations = self.module.get_station_by_mac_address(mac_address)
                    if self.has_station(stations):
                        self.send_meters(redisConnection, payload, stations)
                    else:
                        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação não encontrada no PostgreSQL")
                        redisConnection.deleteDataLog(payload)
                redisConnection.closeConnection()       
        except KeyboardInterrupt:
            print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")

    def stop(self):
        self.run = False
        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")

    def create_redis_connection(self) -> RedisConnection:
        return RedisConnection()

    def has_station(self, stations: list) -> bool:
        return len(stations) <= 0 or len(stations) > 2

    def send_meters(self, redisConnection: RedisConnection, payload: dict, stations: list) -> None:
        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação encontrada no PostgreSQL")
        estacao = stations[0]
        station_parameters, parameters = self.module.get_station_parameters(estacao[0])
        for station_parameter in station_parameters:
            try:
                index = station_parameters.index(station_parameter)
                json_name = parameters[index].json_name
                data = payload["data"][json_name]
                timestamp = payload["timestamp"]
                converted_timestamp = datetime.datetime.fromtimestamp(timestamp)
                self.module.set_meter(timestamp, converted_timestamp, data, station_parameter.id)
            except Exception as e:
                print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Erro ao cadastrar a medição do parâmetro: {e}")
        redisConnection.deleteDataLog(payload)
        return

if __name__ == "__main__":
    serviceRedisPostgreSQL = ServiceRedisPostgreSQL()
    try:
        serviceRedisPostgreSQL.start()
    except:
        print("Erro")
    finally:
        serviceRedisPostgreSQL.stop()