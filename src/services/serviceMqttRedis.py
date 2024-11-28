from src.modules.payload import ModulePayload
import datetime

class ServiceMqttRedis:
    def __init__(self):
        self.run = True
        self.modulePayload = ModulePayload()
    
    def start(self):
        try:
            while self.run:
                print(f"{datetime.datetime.now()} [ServiceMqttRedis] Aguardando mensagem MQTT")
                payload = self.modulePayload.receive_payload()
                if payload:
                    self.modulePayload.save_payload(payload)
        except KeyboardInterrupt:
            print(f"{datetime.datetime.now()} [ServiceMqttRedis] Encerrando aplicação")

    def stop(self):
        self.run = False
        print(f"{datetime.datetime.now()} [ServiceMqttRedis] Encerrando aplicação")
