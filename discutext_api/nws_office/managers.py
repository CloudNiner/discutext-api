import json
import os


class NWSOfficeManager(object):
    def __init__(self):
        officefile = os.path.join(
            os.path.dirname(__file__), "county-warning-areas.json"
        )
        with open(officefile, "r") as data:
            self._data = json.load(data)

    def get(self, wfo_id: str):
        """Return geojson feature for the requested wfo id."""
        for cwa in self._data["features"]:
            properties = cwa.get("properties", {})
            if properties.get("WFO", None) == wfo_id:
                return cwa
        return None

    def all(self):
        """Return iterator of all CWA features without geometry."""
        features = self._data["features"]
        for feature in features:
            yield feature["properties"]

    def check(self):
        """Test method to print differences between CWA id and WFO id."""
        for cwa in self._data["features"]:
            properties = cwa.get("properties", {})
            wfo_id = properties.get("WFO", None)
            cwa_id = properties.get("CWA", None)
            if wfo_id != cwa_id:
                print("WFO {} != CWA {}", wfo_id, cwa_id)
