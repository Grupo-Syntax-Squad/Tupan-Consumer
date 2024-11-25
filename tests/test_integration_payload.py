import pytest
from modules.payload import ModulePayload
from schemas.payload import SchemaPayload
from connections.redisConnection import RedisConnection

@pytest.fixture
def module_payload():
    return ModulePayload()

def test_save_payload(module_payload):
    payload = SchemaPayload(mac="123", data={"temp": 40}, timestamp=1729399539.969931)
    module_payload.save_payload(payload)
    
    redis_conn = RedisConnection()
    saved_data = redis_conn.conn.get(payload.mac)
    assert saved_data is not None
    redis_conn.deleteDataLog(payload)
    redis_conn.close()