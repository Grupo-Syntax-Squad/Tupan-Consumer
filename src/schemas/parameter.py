import datetime

class SchemaParameter:
    def __init__(self, id: int, created_at: datetime, updated_at: datetime, name: str, fator: float, offset: float, json_name: str, description: str, category_id: int):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name: str = name
        self.fator: float = fator
        self.offset: float = offset
        self.json_name: str = json_name
        self.description: str = description
        self.category_id: int = category_id
