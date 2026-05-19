from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import Field, field_validator
from backend.models.CommentsModel import CommentModel, parse_datetime_or_none, serbia_now




class NewsModel(Document):
    active: bool = True
    pic: str = ""
    fancy_comment: str = ""
    name: str
    owner_pic:str = ""
    text:str
    owner:str
    likes:int = 0
    dislikes:int = 0
    publish_date:datetime = Field(default_factory=serbia_now)
    update_date:Optional[datetime] = None
    comments: List[CommentModel] = Field(default_factory=list)
 
    @field_validator("publish_date", mode="before")
    @classmethod
    def validate_publish_date(cls, value):
        parsed = parse_datetime_or_none(value)
        if parsed is None:
            return serbia_now()
        return parsed

    @field_validator("update_date", mode="before")
    @classmethod
    def validate_update_date(cls, value):
        return parse_datetime_or_none(value)


    class Settings:
        name = "news"
