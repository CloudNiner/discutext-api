"""Scraper for NWS Forecast Discussions."""
import logging
from typing import Generator, List

from .discussion.models import ForecastDiscussion
from .nws_weather_api import AFDProduct, NWSWeatherAPI

logger = logging.getLogger(__name__)


def scrape_discussion(nws_api: NWSWeatherAPI, wfo_id: str) -> ForecastDiscussion:
    afd_product = nws_api.get_afd_latest(wfo_id)
    return ForecastDiscussion.from_afd_product(afd_product)


def scrape_discussions(
    nws_api: NWSWeatherAPI, wfo_ids: List[str]
) -> Generator[ForecastDiscussion, None, None]:
    """Scrape the list of provided WFOs."""
    try:
        for wfo_id in wfo_ids:
            print(wfo_id)
            yield scrape_discussion(nws_api, wfo_id)
    except TypeError:
        logger.exception("Must provide iterable to scrape_discussions!")
