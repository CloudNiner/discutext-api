from datetime import datetime
from typing import Any, Dict
from urllib.parse import urljoin

import dateutil
import requests
from pydantic import BaseModel, validator


class AFDProduct(BaseModel):
    wfo_id: str
    issuanceTime: datetime
    productText: str

    @validator("issuanceTime")
    def validate_issuanceTime(cls, v):
        if isinstance(v, str):
            valid_at: datetime = dateutil.parser.parse(v)
            if valid_at.tzinfo is None:
                raise ValueError(f"No tzinfo found on {v}")
            return valid_at
        elif isinstance(v, datetime):
            return v
        else:
            raise ValueError("issuanceTime must be datetile or ISO str")


class NWSWeatherAPI:

    session = requests.Session()

    def __init__(self, user_agent: str = None):
        self.user_agent = (
            user_agent if user_agent is not None else "python NWSWeatherAPI 0.0.1"
        )
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
        return AFDProduct.parse_obj({"wfo_id": wfo_id, **product_response.json()})
