from .base import Base
from datetime import datetime

class SchemaStation(Base):
    def __init__(self, id: int, created_at: datetime, modified_at: datetime, active: bool, name: str, topic: str, address_id: int):
        self.id: int = id
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at
        self.active: bool = active
        self.name: str
        self.topic: str
        self.address_id: int