from datetime import datetime

class Base:
    def __init__(self, id: int, created_at: datetime, modified_at: datetime, active: bool = True) -> None:
        self.id: int = id
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at
        self.active: bool = active