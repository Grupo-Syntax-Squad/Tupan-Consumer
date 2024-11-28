from pydantic import BaseModel


class SchemaStationParameter(BaseModel):
    id: int
    station_id: int
    parameter_id: int