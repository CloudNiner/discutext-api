import dateutil
import logging
import re

logger = logging.getLogger('fd.discussion')


class ForecastDiscussion(object):
    """ ForecastDiscussion, unique on (wfo, valid_at)."""
    TEXT_REGEX = r'  \.(?P<header>[\w\s/]+)\.{3} (?P<text>.+?)  &&'

    def __init__(self, wfo_id, valid_at_str, text):
        self.text = text
        self.wfo_id = wfo_id
        self.valid_at = self._parse_iso_str(valid_at_str)
        self.sections = self._parse_text()

    def serialize(self):
        return {
            'wfo': self.wfo_id,
            'valid_at': self.valid_at,
            'text': self.text,
            'sections': self.sections
        }

    def _parse_iso_str(self, iso_str):
        """Return iso 8601 string as a unix epoch to the nearest second."""
        valid_dt = dateutil.parser.parse(iso_str)
        return int(valid_dt.timestamp())

    def _parse_text(self):
        if self.text is None or len(self.text) == 0:
            return None
        cleaned_text = self.text.replace('\n', ' ')
        return [match.groupdict() for match in re.finditer(self.TEXT_REGEX, cleaned_text)
                    if match is not None]
