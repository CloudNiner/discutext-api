from typing import Any

from pydantic import BaseModel


class NWSOfficeProperties(BaseModel):
    CWA: str
    WFO: str
    LON: float
    LAT: float
    Region: str
    FullStaId: str
    CityState: str
    City: str
    State: str
    ST: str


class NWSOffice(BaseModel):
    geometry: Any
    properties: NWSOfficeProperties
