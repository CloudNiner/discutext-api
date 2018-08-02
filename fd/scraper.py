"""Scraper for NWS Forecast Discussions."""
import logging

from bs4 import BeautifulSoup
import requests

from .discussion.models import ForecastDiscussion

logger = logging.getLogger(__name__)

FD_URL = 'http://forecast.weather.gov/product.php'

FD_URL_PARAMS = {
    'site': 'nws',
    'product': 'afd',
    'format': 'txt',
    'version': '1',
    'glossary': 0,
    'highlight': 0,
    'issuedby': None
}


def scrape_discussion(wfo_id):
    """Scrape discussion for provided WFO."""
    params = dict({}, **FD_URL_PARAMS)
    params.update({'issuedby': wfo_id})
    request = requests.get(FD_URL, params)
    soup = BeautifulSoup(request.text, 'html.parser')
    try:
        discussion = soup.find(id='proddiff').get_text()
    except AttributeError as e:
        logger.error("Unable to find #proddiff in discussion for {}".format(wfo_id))
    return ForecastDiscussion(wfo_id, discussion)


def scrape_discussions(wfo_ids):
    """Scrape the list of provided WFOs."""
    try:
        for wfo_id in wfo_ids:
            print(wfo_id)
            yield scrape_discussion(wfo_id)
    except TypeError:
        logger.exception('Must provide iterable to scrape_discussions!')
