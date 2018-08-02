import datetime
import logging
import re

import pytz

logger = logging.getLogger('fd.discussion')

TZ_MAP = {
    'AKST': 'US/Alaska',
    'AKDT': 'US/Alaska',
    'AST': 'America/Halifax',
    'ADT': 'America/Halifax',
    'EST': 'US/Eastern',
    'EDT': 'US/Eastern',
    'CST': 'US/Central',
    'CDT': 'US/Central',
    'MST': 'US/Mountain',
    'MDT': 'US/Mountain',
    'PST': 'US/Pacific',
    'PDT': 'US/Pacific',
    'SST': 'US/Samoa',
    'SDT': 'US/Samoa',
    'CHST': 'Pacific/Guam'
}


class ForecastDiscussion(object):
    """ ForecastDiscussion, unique on (wfo, valid_at)."""
    re_valid_at = re.compile(r'(?P<time>[0-9]{3,4})\s+(?P<meridian>AM|PM)\s+(?P<tz>[A-Za-z]{3,4})\s+(?P<wkday>[A-Za-z]{3})\s+(?P<mon>[A-Za-z]{3})\s+(?P<day>[0-9]{1,2})\s+(?P<year>20[0-9]{2})')
    TEXT_REGEX = r'  \.(?P<header>[\w\s/]+)\.{3} (?P<text>.+?)  &&'

    def __init__(self, wfo_id, text):
        self.text = text
        self.wfo_id = wfo_id
        self.valid_at = self._set_valid_at()
        self.sections = self._parse_text()

    def serialize(self):
        return {
            'wfo': self.wfo_id,
            'valid_at': self.valid_at,
            'text': self.text,
            'sections': self.sections
        }

    def _set_valid_at(self):
        """ Return a unix epoch for the valid_at of this FD

        Parsed from the text via regex

        """
        match = self.re_valid_at.search(self.text)

        if match:
            try:
                valid_at_groups = match.groupdict()
                if len(valid_at_groups['time']) > 3:
                    hour = int(valid_at_groups['time'][:2])
                    minute = int(valid_at_groups['time'][2:])
                else:
                    hour = int(valid_at_groups['time'][:1])
                    minute = int(valid_at_groups['time'][1:])
                if valid_at_groups['meridian'].lower() == 'pm' and hour < 12:
                    hour += 12
                month = datetime.datetime.strptime(valid_at_groups['mon'], '%b').month
                valid_at_local = datetime.datetime(int(valid_at_groups['year']),
                                                   month,
                                                   int(valid_at_groups['day']),
                                                   hour,
                                                   minute)
                try:
                    timezone = pytz.timezone(valid_at_groups['tz'].upper())
                except pytz.UnknownTimeZoneError:
                    timezone = pytz.timezone(TZ_MAP[valid_at_groups['tz'].upper()])

                valid_at_local = timezone.localize(valid_at_local)
                return valid_at_local.astimezone(pytz.utc).timestamp()
            except KeyError as e:
                logger.error(e)
                return None
        else:
            logger.warning("{}: Found no regex match for valid_at time".format(self.wfo_id))
            return None

    def _parse_text(self):
        if self.text is None or len(self.text) == 0:
            return None
        cleaned_text = self.text.replace('\n', ' ')
        return [match.groupdict() for match in re.finditer(self.TEXT_REGEX, cleaned_text)
                    if match is not None]
