from __future__ import annotations
from pydantic import BaseModel, Field, conint

class TerritoryModel(Document):
    status:str
    owner:str
    post_effects:dict[str:int]