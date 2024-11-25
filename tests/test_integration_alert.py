import pytest
from modules.alert import ModuleAlert
from schemas.payload import SchemaPayload
from connections.postgreSQLConnection import PostgreSQLConnection

@pytest.fixture
def module_alert():
    return ModuleAlert()

@pytest.fixture
def postgresql_connection():
    return PostgreSQLConnection()

def test_verify_alerts(module_alert, postgresql_connection):
    payload = SchemaPayload(mac="123", data={"temp": 40}, timestamp=1729399539.969931)
    station_parameter_id = 1  # Assumindo que este ID existe no banco de dados
    
    # Limpar alertas históricos antes do teste
    postgresql_connection.cursor.execute("DELETE FROM alertas_historicoalerta WHERE alerta_id IN (SELECT id FROM alertas_alerta WHERE estacao_parametro_id = %s)", (station_parameter_id,))
    postgresql_connection.connection.commit()
    
    module_alert.verify_alerts(station_parameter_id, payload)
    
    # Verificar se os alertas foram processados corretamente
    postgresql_connection.cursor.execute("SELECT * FROM alertas_historicoalerta WHERE alerta_id IN (SELECT id FROM alertas_alerta WHERE estacao_parametro_id = %s)", (station_parameter_id,))
    alert_history = postgresql_connection.cursor.fetchall()
    
    assert len(alert_history) > 0  # Verificar se pelo menos um alerta foi salvo no histórico
    
    # Verificar se os dados do alerta estão corretos
    for alert in alert_history:
        assert alert['timestamp'] == payload.timestamp
        assert alert['alerta_id'] is not None
        assert alert['medicao_id'] is not None
    
    postgresql_connection.close()