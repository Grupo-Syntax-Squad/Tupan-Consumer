import datetime
from schemas.base import Base

from .base import Base

class SchemaAlert(Base):
    def __init__(self, id: int, created_at: datetime, modified_at: datetime, name: str, condition: str, station_parameter_id: int):
        super().__init__(id, created_at, modified_at)
        self.name: str = name
        self.condition: str = condition
        self.station_parameter_id: int = station_parameter_id