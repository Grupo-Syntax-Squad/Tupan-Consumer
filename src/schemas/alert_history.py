from schemas.base import Base

class SchemaAlertHistory(Base):
    timestamp: float
    converted_timestamp: any
    alert_id: int
    meter_id: int