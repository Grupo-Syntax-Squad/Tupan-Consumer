from datetime import datetime
from .base import Base

class SchemaParameter(Base):
    def __init__(self, id: int, created_at: datetime, modified_at: datetime, active: bool, name: str, fator: float, offset: float, json_name: str, description: str, category_id: int) -> None:
        super().__init__(id, created_at, modified_at, active)
        self.name: str = name
        self.fator: float = fator
        self.offset: float = offset
        self.json_name: str = json_name
        self.description: str = description
        self.category_id: int = category_id
