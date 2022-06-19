import logging
import re

import dateutil

logger = logging.getLogger("fd.discussion")


class ForecastDiscussion(object):
    """ForecastDiscussion, unique on (wfo, valid_at)."""

    HEADER_REGEX = re.compile(r"\.(?P<header>[\w \/]+)\.{3}(?P<text>.*)", re.DOTALL)

    def __init__(self, wfo_id, valid_at_str, text):
        self.text = text
        self.wfo_id = wfo_id
        self.valid_at = self._parse_iso_str(valid_at_str)
        self.sections = self._parse_text()

    def serialize(self):
        return {
            "wfo": self.wfo_id,
            "valid_at": self.valid_at,
            "text": self.text,
            "sections": self.sections,
        }

    def _parse_iso_str(self, iso_str):
        """Return iso 8601 string as a unix epoch to the nearest second."""
        valid_dt = dateutil.parser.parse(iso_str)
        return int(valid_dt.timestamp())

    def _clean_section_text(self, text):
        """Split into paragraphs.

        Steps:
            - Replace newlines separated by only zero or more whitespace with double newlines
            - Split on double newlines
            - For each paragraph:
              - Replace each remaining newline with empty space
              - Reduce each occurence of one or more spaces with one space
              - Strip whitespace from ends of paragraph
        """
        paragraphs = re.sub(r"\n\s*\n", "\n\n", text).split("\n\n")
        return [
            re.sub(r" +", " ", p.replace("\n", " ")).strip() for p in paragraphs if p
        ]

    def _parse_text(self):
        if self.text is None or len(self.text) == 0:
            return None
        sections = self.text.split("&&")
        matches = []
        for section in sections:
            match = self.HEADER_REGEX.search(section)
            if match is not None:
                matches.append(match.groupdict())
            else:
                matches.append({"header": "", "text": section})
        return [
            {
                "header": m.get("header", ""),
                "paragraphs": self._clean_section_text(m.get("text", "")),
            }
            for m in matches
        ]
