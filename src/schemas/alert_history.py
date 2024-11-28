from typing import Any
from .base import Base

class SchemaAlertHistory(Base):
    timestamp: float
    converted_timestamp: Any
    alert_id: int
    meter_id: int