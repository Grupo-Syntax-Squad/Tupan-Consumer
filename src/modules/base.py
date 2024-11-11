from connections.postgreSQLConnection import PostgreSQLConnection
from connections.redisConnection import RedisConnection
from connections.mqttConnection import wait_mqtt_message

class Base:
    def __init__(self):
        self.postgreSQLConnection = PostgreSQLConnection()
        self.redisConnection = RedisConnection()
        self.wait_mqtt_message = wait_mqtt_message
