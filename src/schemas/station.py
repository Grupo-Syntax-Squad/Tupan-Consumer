import datetime
from .base import Base
from datetime import datetime

class SchemaStation(Base):
    def __init__(self, id: int, created_at: datetime, modified_at: datetime, active: bool, name: str, topic: str, address_id: str) -> None:
        super().__init__(id, created_at, modified_at, active)
        self.name: str
        self.topic: str
        self.address_id: int
