import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import ClientError
from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from fd.nws_office import NWSOfficeManager
from fd.nws_weather_api import NWSWeatherAPI
from fd.scraper import scrape_discussion

DISCUSSION_FETCH_TIMEOUT = timedelta(hours=1)

DISCUTEXT_VERSION = "0.1.0"

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

app = Flask(__name__)
CORS(app)

s3 = boto3.resource("s3")

user_agent = "discutext {v}: operations@discutext.com".format(v=DISCUTEXT_VERSION)
nws_api = NWSWeatherAPI(user_agent=user_agent)


def copy_s3_object(s3_resource, src_bucket, src_key, dest_bucket, dest_key):
    copy_src = {
        "Bucket": src_bucket,
        "Key": src_key,
    }
    bucket = s3_resource.Bucket(dest_bucket)
    bucket.copy(copy_src, dest_key)


@app.route("/")
def hello():
    return jsonify({"message": "Welcome to the discutext API"})


@app.route("/search/<lat>/<lon>")
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

    return "Search: ({}, {})\n".format(lat, lon)


@app.route("/discussion/<office_id>/latest")
def latest_discussion(office_id):
    bucket = os.environ.get("AWS_S3_STORAGE_BUCKET", None)
    logger.debug("Bucket: {}".format(bucket))
    if bucket:
        discussion_path = "discussions/{}/{}-latest.json".format(office_id, office_id)
        # Attempt to load from S3 cache
        try:
            obj = s3.Object(bucket_name=bucket, key=discussion_path)
            if obj.last_modified + DISCUSSION_FETCH_TIMEOUT < datetime.now(
                timezone.utc
            ):
                raise ValueError()
            logger.info("Returning S3 cached discussion for {}".format(office_id))
            discussion_dict = json.load(obj.get()["Body"])
            return jsonify(discussion_dict)
        # If there are any failures, parse new discussion and save to S3
        # TODO: Better cache busting
        except (ClientError, ValueError):
            logger.info("Retrieving new discussion for {}".format(office_id))
            discussion = scrape_discussion(nws_api, office_id)
            discussion_dict = discussion.serialize()
            discussion_datetime = datetime.fromtimestamp(
                discussion_dict["valid_at"], timezone.utc
            )
            permanent_path = "discussions/{0}/{1}/{2:02d}/{3:02d}/{0}-{1}{2:02d}{3:02d}T{4:02d}.json".format(
                office_id,
                discussion_datetime.year,
                discussion_datetime.month,
                discussion_datetime.day,
                discussion_datetime.hour,
            )
            logger.info(
                "Saving discussion to S3: s3://{}/{}".format(bucket, permanent_path)
            )
            obj.put(Body=json.dumps(discussion_dict))
            copy_s3_object(s3, bucket, discussion_path, bucket, permanent_path)
            return jsonify(discussion_dict)
    else:
        logger.warning("S3 bucket not configured, caching disabled")
        logger.info("Retrieving new discussion for {}".format(office_id))
        discussion = scrape_discussion(nws_api, office_id)
        return jsonify(discussion.serialize())


@app.route("/nws-office")
def nws_office_list():
    manager = NWSOfficeManager()
    offices = manager.all()

    name = request.args.get("name", None)
    if name:
        offices = filter(lambda o: name.lower() in o["CityState"].lower(), offices)

    return jsonify(list(offices))


@app.route("/nws-office/<office_id>")
def nws_office_detail(office_id):
    manager = NWSOfficeManager()
    office = manager.get(office_id)
    if office:
        return jsonify(office)
    else:
        abort(404)


@app.route("/nws-office/<office_id>/geojson")
def nws_office_detail_geojson(office_id):
    manager = NWSOfficeManager()
    office = manager.geojson(office_id)
    if office:
        return jsonify(office)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
