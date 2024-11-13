class SchemaStationParameter:
    def __init__(self, id: int, station_id: int, parameter_id: int):
        self.id: int = id
        self.station_id: int = station_id
        self.parameter_id: int = parameter_id