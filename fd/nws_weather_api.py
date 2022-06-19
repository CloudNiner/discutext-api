from urllib.parse import urljoin

import requests


class NWSWeatherAPI:

    session = requests.Session()

    def __init__(self, user_agent=None):
        self.user_agent = (
            user_agent if user_agent is not None else "python NWSWeatherAPI 0.0.1"
        )
        self.session.headers.update({"user-agent": self.user_agent})

    def _get(self, path):
        HOSTNAME = "https://api.weather.gov"
        url = urljoin(HOSTNAME, path)
        response = self.session.get(url, timeout=5)
        response.raise_for_status()
        return response

    def get_products_types_locations(self, type_id, location_id):
        path = "/products/types/{t}/locations/{l}".format(t=type_id, l=location_id)
        response = self._get(path)
        return response.json()

    def get_product(self, product_id):
        path = "/products/{p}".format(p=product_id)
        response = self._get(path)
        return response.json()
