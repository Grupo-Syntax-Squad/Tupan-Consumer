from modules.base import Base
from schemas.payload import SchemaPayload
import datetime
from json import dumps, loads

class ModulePayload(Base):
    def save_payload(self, payload: SchemaPayload) -> None:
        print(f"{datetime.datetime.now()} [RedisConnection] Salvando dados no Redis: ", payload.__dict__)
        self.redisConnection.conn.set(payload.mac, dumps(payload.__dict__))

    def delete_payload(self, payload: SchemaPayload) -> None:
        print(f"{datetime.datetime.now()} [RedisConnection] Deletando dados no Redis: ", payload.__dict__)
        self.redisConnection.conn.delete(payload.mac)

    def get_payloads_from_redis(self) -> list[SchemaPayload]:
        print(f"{datetime.datetime.now()} [RedisConnection] Buscando dados no Redis")
        keys = self.redisConnection.conn.keys('*')

        payloads: list[SchemaPayload] = []
        while len(keys) > 0:
            data = loads(self.redisConnection.conn.get(keys.pop()))
            payload = SchemaPayload(
                mac=data['mac'],
                data=data['data'],
                timestamp=data['timestamp'],
            )
            payloads.append(payload)
        return payloads
    
    def receive_payload(self) -> SchemaPayload:
        topic, payload = self.wait_mqtt_message()
        payload = SchemaPayload(
            mac=payload['mac'],
            data=payload['data'],
            timestamp=payload['timestamp']
        )
        return payload

    def delete_all_payloads_from_redis(self) -> None:
        keys = self.redisConnection.conn.keys("*")

        for key in keys:
            self.redisConnection.conn.delete(key)
        
        print(f"{datetime.datetime.now()} [RedisConnection] Todos os dados do Redis foram deletados")