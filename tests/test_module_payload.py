import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.modules.payload import ModulePayload
from src.schemas.payload import SchemaPayload

@pytest.fixture
def module_payload() -> ModulePayload:
    return ModulePayload()

def test_get_payloads_from_redis(module_payload):
    payloads = module_payload.get_payloads_from_redis()

    assert isinstance(payloads) == list[SchemaPayload]

def test_save_payload(module_payload):
    sended_payload = {
        "mac": "123",
        "data": {
            "temp": 40,
            "umid": 3
        },
        "timestamp": 1729399539.969931
    }
    module_payload.save_payload(sended_payload)
    payloads = module_payload.get_payloads_from_redis()
    for payload in payloads:
        if payload.mac == sended_payload.mac:
            assert sended_payload['mac'] == payload.mac
            assert sended_payload['data'] == payload.data
            assert sended_payload['timestamp'] == payload.timestamp
            break

def test_delete_payload(module_payload):
    sended_payload = {
        "mac": "123",
        "data": {
            "temp": 40,
            "umid": 3
        },
        "timestamp": 1729399539.969931
    }

    module_payload.save_payload(sended_payload)

    sended_payload = {
        "mac": "124",
        "data": {
            "temp": 40,
            "umid": 3
        },
        "timestamp": 1729399539.969931
    }
    
    module_payload.save_payload(sended_payload)
    module_payload.delete_payload(sended_payload)

    payloads = module_payload.get_payloads_from_redis()

    assert isinstance(payloads) == list[SchemaPayload]
    assert len(payloads) > 0
