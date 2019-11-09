"""Scraper for NWS Forecast Discussions."""
import logging

from .discussion.models import ForecastDiscussion

logger = logging.getLogger(__name__)


def scrape_discussion(nws_api, wfo_id):
    """Scrape discussion for provided WFO."""
    response = nws_api.get_products_types_locations("AFD", wfo_id)
    discussion_id = response['@graph'][0]['id']
    response = nws_api.get_product(discussion_id)

    return ForecastDiscussion(wfo_id, response['issuanceTime'], response['productText'])


def scrape_discussions(nws_api, wfo_ids):
    """Scrape the list of provided WFOs."""
    try:
        for wfo_id in wfo_ids:
            print(wfo_id)
            yield scrape_discussion(nws_api, wfo_id)
    except TypeError:
        logger.exception('Must provide iterable to scrape_discussions!')
