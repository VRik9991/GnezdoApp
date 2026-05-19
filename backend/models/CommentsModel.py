from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import logging

from pydantic import BaseModel, Field


def serbia_now() -> datetime:
    return datetime.now(ZoneInfo("Europe/Belgrade"))

class CommentModel(BaseModel):
    text: str
    owner: str

    date: datetime = Field(
        default_factory=serbia_now
    )

    owner_pic: str = ""
