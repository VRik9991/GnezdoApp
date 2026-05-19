from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import Field
from backend.models.CommentsModel import CommentModel, serbia_now




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
 


    class Settings:
        name = "news"
