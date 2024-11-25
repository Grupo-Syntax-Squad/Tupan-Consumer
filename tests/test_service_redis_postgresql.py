import pytest
from unittest.mock import patch, MagicMock
from serviceRedisPostgreSQL import ServiceRedisPostgreSQL
from redisConnection import RedisConnection

@pytest.fixture
def service():
    return ServiceRedisPostgreSQL()

def test_create_redis_connection(service):
    with patch('serviceRedisPostgreSQL.RedisConnection') as MockRedisConnection:
        mock_redis_connection = MockRedisConnection.return_value
        redis_connection = service.create_redis_connection()
        assert redis_connection == mock_redis_connection
        MockRedisConnection.assert_called_once()

def test_has_station(service):
    stations = [1]
    assert service.has_station(stations) == True

    stations = []
    assert service.has_station(stations) == False

    stations = [1, 2, 3]
    assert service.has_station(stations) == False

def test_send_meters(service):
    payload = {
        "mac": "123",
        "data": {
            "temp": 40
        },
        "timestamp": 1729399539.969931
    }
    stations = [MagicMock()]
    with patch.object(service.module_station, 'get_station_parameters', return_value=([], [])) as mock_get_station_parameters, \
         patch.object(service.module_station, 'set_meter') as mock_set_meter, \
         patch.object(service.module_alert, 'verify_alerts') as mock_verify_alerts, \
         patch.object(service.module_payload, 'delete_payload') as mock_delete_payload:
        
        service.send_meters(payload, stations)
        
        mock_get_station_parameters.assert_called_once_with(stations[0][0])
        mock_set_meter.assert_not_called()
        mock_verify_alerts.assert_not_called()
        mock_delete_payload.assert_called_once_with(payload)