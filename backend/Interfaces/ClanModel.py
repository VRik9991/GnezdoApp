from enum import Enum

from pydantic import BaseModel

class ClanNames(Enum):
    VENTRUE = 'вентру'
    TOREODOR = 'тореодор'

class ClanModel(BaseModel):
    name: ClanNames
    description: str