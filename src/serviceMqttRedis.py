from redisConnection import RedisConnection
from mqttConnection import waitMqttMessage
import datetime

class ServiceMqttRedis:
    def __init__(self):
        self.run = True
    
    def start(self):
        try:
            while self.run:
                response = waitMqttMessage()
                redisConnection = RedisConnection()
                redisConnection.saveDataLog(response[1])
                redisConnection.closeConnection()
        except KeyboardInterrupt:
            print(f"{datetime.datetime.now()} [ServiceMqttRedis] Encerrando aplicação")

    def stop(self):
        self.run = False
        print(f"{datetime.datetime.now()} [ServiceMqttRedis] Encerrando aplicação")
    