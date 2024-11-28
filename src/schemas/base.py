from datetime import datetime
from pydantic import BaseModel

class Base(BaseModel):
    id: int
    created_at: datetime
    modified_at: datetime
    active: bool