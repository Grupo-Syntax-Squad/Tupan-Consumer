from .base import Base

class SchemaMeter(Base):
    def __init__(self, id: int, created_at: any, modified_at: any, timestamp: float, converted_timestamp: any, station_parameter_id: int, data: float):
        super().__init__(id, created_at, modified_at)
        self.timestamp: float = timestamp
        self.converted_timestamp: any = converted_timestamp
        self.station_parameter_id: int = station_parameter_id
        self.data: float = data