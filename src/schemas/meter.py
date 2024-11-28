from typing import Any
from .base import Base

class SchemaMeter(Base):
    timestamp: float
    converted_timestamp: Any
    station_parameter_id: int
    data: float