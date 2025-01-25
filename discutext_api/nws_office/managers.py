import json
import os
from typing import Generator

from .models import NWSOffice, NWSOfficeProperties


class NWSOfficeManager(object):
    def __init__(self) -> None:
        officefile = os.path.join(
            os.path.dirname(__file__), "county-warning-areas.json"
        )
        with open(officefile, "r") as data:
            self._data = json.load(data)

    def get(self, wfo_id: str) -> NWSOffice | None:
        """Return geojson feature for the requested wfo id."""
        for cwa in self._data["features"]:
            properties = cwa.get("properties", {})
            if properties.get("WFO", None) == wfo_id:
                return NWSOffice.model_validate(cwa)
        return None

    def all(self) -> Generator[NWSOfficeProperties, None, None]:
        """Return iterator of all CWA features without geometry."""
        features = self._data["features"]
        for feature in features:
            yield NWSOfficeProperties.model_validate(feature["properties"])

    def check(self) -> None:
        """Test method to print differences between CWA id and WFO id."""
        for cwa in self._data["features"]:
            properties = cwa.get("properties", {})
            wfo_id = properties.get("WFO", None)
            cwa_id = properties.get("CWA", None)
            if wfo_id != cwa_id:
                print("WFO {} != CWA {}", wfo_id, cwa_id)
