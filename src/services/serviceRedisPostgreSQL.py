from modules.payload import ModulePayload
from modules.station import ModuleStation
from modules.alert import ModuleAlert
import datetime
from time import sleep

class ServiceRedisPostgreSQL:
    def __init__(self):
        self.run = True
        self.module_station = ModuleStation()
        self.module_payload = ModulePayload()
        self.module_alert = ModuleAlert()
    
    def start(self):
        try:
            while self.run:
                sleep(5)
                data = self.module_payload.get_payloads_from_redis()
                while len(data) > 0:
                    payload = data.pop()
                    mac_address = payload.mac
                    stations = self.module_station.get_station_by_mac_address(mac_address)
                    if self.has_station(stations):
                        self.send_meters(payload, stations)
                    else:
                        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação não encontrada no PostgreSQL")
                        self.module_payload.delete_payload(payload)   
        except KeyboardInterrupt:
            print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")

    def stop(self):
        self.run = False
        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Encerrando aplicação")

    def has_station(self, stations: list) -> bool:
        return len(stations) == 1

    def send_meters(self, payload: dict, stations: list) -> None:
        print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Estação encontrada no PostgreSQL")
        estacao = stations[0]
        station_parameters, parameters = self.module_station.get_station_parameters(estacao[0])
        for station_parameter in station_parameters:
            try:
                index = station_parameters.index(station_parameter)
                json_name = parameters[index].json_name
                data = payload["data"][json_name]
                timestamp = payload["timestamp"]
                converted_timestamp = datetime.datetime.fromtimestamp(timestamp)
                self.module_station.set_meter(timestamp, converted_timestamp, data, station_parameter.id)
                self.module_alert.verify_alerts(station_parameter.id, payload)
            except Exception as e:
                print(f"{datetime.datetime.now()} [ServiceRedisPostgreSQL] Erro ao cadastrar a medição do parâmetro: {e}")
        self.module_payload.delete_payload(payload)
        return

if __name__ == "__main__":
    serviceRedisPostgreSQL = ServiceRedisPostgreSQL()
    try:
        serviceRedisPostgreSQL.start()
    except:  # noqa: E722
        print("Erro")
    finally:
        serviceRedisPostgreSQL.stop()