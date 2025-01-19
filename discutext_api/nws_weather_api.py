import logging
import sys
from datetime import datetime
from typing import Any, Dict
from urllib.parse import urljoin

import requests
from dateutil.parser import parse as dateutil_parse
from pydantic import BaseModel, validator

from .encoders import datetime_encoder

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


class AFDProduct(BaseModel):
    wfo_id: str
    issuanceTime: datetime
    productText: str

    @validator("issuanceTime")
    def validate_issuanceTime(cls, v: Any) -> datetime:
        if isinstance(v, str):
            valid_at: datetime = dateutil_parse(v)
            if valid_at.tzinfo is None:
                raise ValueError(f"No tzinfo found on {v}")
            return valid_at
        elif isinstance(v, datetime):
            if v.tzinfo is None:
                raise ValueError(f"No tzinfo found on {v}")
            return v
        else:
            raise ValueError("issuanceTime must be datetime or ISO str")

    class Config:
        json_encoders = {datetime: datetime_encoder}


class NWSWeatherAPI:

    session = requests.Session()

    def __init__(self, user_agent: str = "") -> None:
        self.user_agent = user_agent if user_agent else "python NWSWeatherAPI 0.0.1"
        self.session.headers.update({"user-agent": self.user_agent})

    def _get(self, path: str) -> requests.Response:
        HOSTNAME = "https://api.weather.gov"
        url = urljoin(HOSTNAME, path)
        response = self.session.get(url, timeout=5)
        response.raise_for_status()
        return response

    def get_products_types_locations(
        self, type_id: str, location_id: str
    ) -> Dict[str, Any]:
        path = "/products/types/{t}/locations/{l}".format(t=type_id, l=location_id)
        response = self._get(path)
        return response.json()

    def get_afd_latest(self, wfo_id: str) -> AFDProduct:
        response = self.get_products_types_locations("AFD", wfo_id)
        discussion_id = response["@graph"][0]["id"]
        product_response = self._get(f"/products/{discussion_id}")
        logger.info(product_response.json())
        return AFDProduct.parse_obj({"wfo_id": wfo_id, **product_response.json()})
