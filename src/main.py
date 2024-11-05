from serviceMqttRedis import ServiceMqttRedis
from serviceRedisPostgreSQL import ServiceRedisPostgreSQL
import threading
import datetime
import signal
import sys

serviceMqttRedis = ServiceMqttRedis()
serviceRedisPostgreSQL = ServiceRedisPostgreSQL()

def signal_handler(sig, frame):
    print(f"{datetime.datetime.now()} [Main] Recebendo sinal de encerramento")
    serviceMqttRedis.stop()
    serviceRedisPostgreSQL.stop()
    thread1.join()
    thread2.join()
    print(f"{datetime.datetime.now()} [Main] Encerrando aplicação")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

thread1 = threading.Thread(target=serviceMqttRedis.start)
thread2 = threading.Thread(target=serviceRedisPostgreSQL.start)

thread1.start()
thread2.start()

# Manter o programa em execução até receber um sinal
try:
    while True:
        pass
except KeyboardInterrupt:
    signal_handler(None, None)  # Captura Ctrl+C também