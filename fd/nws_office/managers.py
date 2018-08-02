import json
import os


class NWSOffice(object):

    def __init__(self, id=None, wfo=None, lat=None, lon=None, geom=None):
        self.id = id
        self.wfo = wfo
        self.lat = lat
        self.lon = lon
        self.geom = geom

    def serialize(self):
        return {
            'id': self.id,
            'wfo': self.wfo,
            'lat': self.lat,
            'lon': self.lon,
            'geometry': self.geom,
        }


class NWSOfficeManager(object):

    def __init__(self):
        officefile = os.path.join(os.path.dirname(__file__), 'county-warning-areas.json')
        with open(officefile, 'r') as data:
            self._data = json.load(data)

    def get(self, wfo_id):
        office_geojson = self.geojson(wfo_id)
        if office_geojson:
            return NWSOffice(id=office_geojson['properties']['CWA'],
                             wfo=office_geojson['properties']['WFO'],
                             lat=office_geojson['properties']['LAT'],
                             lon=office_geojson['properties']['LON'],
                             geom=office_geojson['geometry'])
        else:
            None

    def geojson(self, wfo_id):
        """Return NWSOffice for the requested wfo id."""
        for cwa in self._data['features']:
            properties = cwa.get('properties', {})
            if properties.get('WFO', None) == wfo_id:
                return cwa
        return None

    def all(self):
        """Return iterator of all CWA features without geometry."""
        features = self._data['features']
        for feature in features:
            yield NWSOffice(id=feature['properties']['CWA'],
                            wfo=feature['properties']['WFO'],
                            lat=feature['properties']['LAT'],
                            lon=feature['properties']['LON'])

    def check(self):
        """Test method to print differences between CWA id and WFO id."""
        for cwa in self._data['features']:
            properties = cwa.get('properties', {})
            wfo_id = properties.get('WFO', None)
            cwa_id = properties.get('CWA', None)
            if wfo_id != cwa_id:
                print('WFO {} != CWA {}', wfo_id, cwa_id)
