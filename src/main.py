from serviceMqttRedis import ServiceMqttRedis
import threading
import datetime

serviceMqttRedis = ServiceMqttRedis()
thread = threading.Thread(target=serviceMqttRedis.start)

input(f"{datetime.datetime.now()} [Main] Pressione ENTER para encerrar a aplicação\n")
serviceMqttRedis.stop()

print(f"{datetime.datetime.now()} [Main] Encerrando aplicação")