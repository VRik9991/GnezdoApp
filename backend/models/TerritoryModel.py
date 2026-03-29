from __future__ import annotations
from pydantic import BaseModel, Field, conint
from enum import Enum
from beanie import Document, Link
from backend.models import UserModel


class RegionStatus(Enum):
    ABUNDANT = 'Abundant'
    CALM = 'Calm'
    TENSE = 'Tense',
    EXCITED = 'Excited',
    CONFLICT = 'Conflict',
    WAR = 'War'

class RegionConditions(Enum):
    HUNTERS = 'Охотники'
    WEREWOLVES = 'Оборотни'
    SPIRITS = 'Духи'
    FEY = 'Феи'
    WIZARDS = 'Маги'
    DEMONS = 'Демоны'

class RegionModel(Document):
    name: str
    owner: Link[UserModel] | None
    status: RegionStatus
    resource: int
    conditions: list[RegionConditions]


    class Settings:
        name = "regions"