from flask import Flask, abort, jsonify

from fd.nws_office import NWSOfficeManager
from fd.scraper import scrape_discussion


app = Flask(__name__)


@app.route('/')
def hello():
    return jsonify({'message': 'Welcome to the discutext API'})


@app.route('/search/<lat>/<lon>')
def search_lat_lon(lat, lon):
    # TODO: Remove? Client might have to implement this with something like turf.js
    #       since supporting geospatial operations is a mess in Lambda
    # TODO: Write and use better FloatConverter
    #       http://werkzeug.pocoo.org/docs/0.14/routing/#werkzeug.routing.FloatConverter
    try:
        lat = float(lat)
    except ValueError:
        abort(400)
    try:
        lon = float(lon)
    except ValueError:
        abort(400)

    return 'Search: ({}, {})\n'.format(lat, lon)


@app.route('/discussion/<office_id>/latest')
def latest_discussion(office_id):
    discussion = scrape_discussion(office_id)
    return jsonify(discussion.serialize())


@app.route('/nws-office')
def nws_office_list():
    manager = NWSOfficeManager()
    return jsonify(list(manager.all()))


@app.route('/nws-office/<office_id>')
def nws_office_detail(office_id):
    manager = NWSOfficeManager()
    office = manager.get(office_id)
    if office:
        return jsonify(office)
    else:
        abort(404)


@app.route('/nws-office/<office_id>/geojson')
def nws_office_detail_geojson(office_id):
    manager = NWSOfficeManager()
    office = manager.geojson(office_id)
    if office:
        return jsonify(office)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
