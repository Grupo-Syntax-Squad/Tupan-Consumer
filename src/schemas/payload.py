from typing import Any
from pydantic import BaseModel

class SchemaPayload(BaseModel):
    mac: str
    data: dict[str, Any]
    timestamp: float
