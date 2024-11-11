from datetime import datetime

class Base:
    def __init__(self):
        self.id: int
        self.created_at: datetime
        self.modified_at: datetime
        self.active: bool