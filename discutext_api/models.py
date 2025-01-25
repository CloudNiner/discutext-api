import json
import logging
import re
from datetime import datetime
from typing import Any, List, Self

from pydantic import BaseModel, ConfigDict

from .encoders import datetime_encoder
from .nws_weather_api import AFDProduct, NWSWeatherAPI

logger = logging.getLogger(__name__)


HEADER_REGEX = re.compile(r"\.(?P<header>[\w \/]+)\.{3}(?P<text>.*)", re.DOTALL)


class ForecastDiscussionSection(BaseModel):
    header: str
    paragraphs: List[str]


class ForecastDiscussion(BaseModel):
    """ForecastDiscussion, unique on (wfo, valid_at)."""

    text: str
    wfo_id: str
    valid_at: datetime
    sections: List[ForecastDiscussionSection]

    @classmethod
    def from_afd_product(cls, afd_product: AFDProduct) -> Self:
        return cls(
            wfo_id=afd_product.wfo_id,
            valid_at=afd_product.issuanceTime,
            text=afd_product.productText,
            sections=cls._parse_text(afd_product.productText),
        )

    @classmethod
    def from_nws_api(cls, nws_api: NWSWeatherAPI, wfo_id: str) -> Self:
        afd_product = nws_api.get_afd_latest(wfo_id)
        return cls.from_afd_product(afd_product)

    @classmethod
    def _clean_section_text(cls, text: str) -> List[str]:
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

    @classmethod
    def _parse_text(cls, afd_text: str) -> List[ForecastDiscussionSection]:
        if not afd_text:
            raise ValueError("afd_text cannot be empty")
        sections: list[str] = afd_text.split("&&")
        matches: list[dict[str, str]] = []
        for section in sections:
            match = HEADER_REGEX.search(section)
            if match is not None:
                matches.append(match.groupdict())
            else:
                matches.append({"header": "", "text": section})
        return [
            ForecastDiscussionSection(
                header=m.get("header", ""),
                paragraphs=cls._clean_section_text(m.get("text", "")),
            )
            for m in matches
        ]

    def json_dict(self) -> Any:
        return json.loads(self.model_dump_json())

    model_config = ConfigDict(json_encoders={datetime: datetime_encoder})
