from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import logging

from dateutil import parser
from pydantic import BaseModel, Field, field_validator


def serbia_now() -> datetime:
    return datetime.now(ZoneInfo("Europe/Belgrade"))


def parse_datetime_or_none(value):
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return parser.parse(value)
        except (TypeError, ValueError):
            return None
    return value

class CommentModel(BaseModel):
    text: str
    owner: str

    date: datetime = Field(
        default_factory=serbia_now
    )

    owner_pic: str = ""

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        parsed = parse_datetime_or_none(value)
        if parsed is None:
            return serbia_now()
        return parsed
