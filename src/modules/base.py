from src.connections.postgreSQLConnection import PostgreSQLConnection
from src.connections.redisConnection import RedisConnection
from src.connections.mqttConnection import wait_mqtt_message
from pydantic import BaseModel

class Base(BaseModel):
    postgreSQLConnection: PostgreSQLConnection = PostgreSQLConnection()
    redisConnection: RedisConnection = RedisConnection()
    wait_mqtt_message: function = wait_mqtt_message
