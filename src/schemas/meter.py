from .base import Base

class SchemaMeter(Base):
    timestamp: float
    converted_timestamp: any
    station_parameter_id: int
    data: float