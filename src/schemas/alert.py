from .base import Base

class SchemaAlert(Base):
    name: str
    condition: str
    station_parameter_id: int