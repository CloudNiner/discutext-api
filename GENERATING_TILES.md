# Generating Vector Tiles

This document describes how to generate the county warning areas vector tiles used by the application.

## Dependencies

- [tippecanoe](https://github.com/mapbox/tippecanoe)
- [mbutil](https://github.com/mapbox/mbutil)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

## The Process

Download the latest [County Warning Areas](https://www.weather.gov/gis/CWABounds) shapefile.

Go to [mapshaper](https://mapshaper.org), upload the zip file, and re-export as GeoJson
after simplifying to about 2.5% and clicking "repair".

Install the tools noted above in the "Dependencies" section

Run the following (tweaking paths as desired):

```
tippecanoe -o county-warning-areas.mbtiles --force -zg -pS county_warning_areas.json
mb-util --image_format=pbf county-warning-areas.mbtiles ./county-warning-areas
aws s3 cp ./county-warning-areas \
  s3://discutext-tiles/county-warning-areas-latest \
  --recursive \
  --acl public-read \
  --content-encoding gzip
```

Be sure to **verify** the CORS configuration on the S3 bucket you push the tiles to.
