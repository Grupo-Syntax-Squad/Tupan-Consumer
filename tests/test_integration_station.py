import pytest
from modules.station import ModuleStation

@pytest.fixture
def module_station():
    return ModuleStation()

def test_get_station_parameters(module_station):
    station_id = 1  # Assumindo que este ID existe no banco de dados
    station_parameters, parameters = module_station.get_station_parameters(station_id)
    
    assert len(station_parameters) > 0
    assert len(parameters) > 0