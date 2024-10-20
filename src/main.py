from serviceMqttRedis import ServiceMqttRedis
from serviceRedisPostgreSQL import ServiceRedisPostgreSQL
import threading
import datetime

serviceMqttRedis = ServiceMqttRedis()
serviceRedisPostgreSQL = ServiceRedisPostgreSQL()
thread1 = threading.Thread(target=serviceMqttRedis.start)
thread2 = threading.Thread(target=serviceRedisPostgreSQL.start)

thread1.start()
thread2.start()

input(f"{datetime.datetime.now()} [Main] Pressione ENTER para encerrar a aplicação\n")

serviceMqttRedis.stop()
serviceRedisPostgreSQL.stop()

thread1.join()
thread2.join()

print(f"{datetime.datetime.now()} [Main] Encerrando aplicação")