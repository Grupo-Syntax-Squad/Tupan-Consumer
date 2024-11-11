from .base import Base

class SchemaStation(Base):
    def __init__(self):
        self.name: str
        self.topic: str
        self.address_id: int