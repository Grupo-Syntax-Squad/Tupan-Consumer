from datetime import datetime

class Base:
    id: int
    created_at: datetime
    modified_at: datetime
    active: bool