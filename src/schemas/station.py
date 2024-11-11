from .base import Base

class SchemaStation(Base):
    name: str
    topic: str
    address_id: int