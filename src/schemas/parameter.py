from .base import Base

class SchemaParameter(Base):
    name: str
    fator: float
    offset: float
    json_name: str
    description: str
    category_id: int
