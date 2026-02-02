from typing import Literal

from beanie import Document
from pydantic import field_validator

from backend.Interfaces.ClanModel import ClanModel, ClanNames
from backend.models.UserModelStats import UserModelStats
from backend.utils.UserUtilsTypes import UserType


class UserModel(Document):
    foto: str
    character_name:str
    other_character_name:str
    name:str
    last_name:str
    tg_name:str
    status:str
    stats: UserModelStats
    email:str
    password:str
    role: UserType
    clan: ClanNames

    class Settings:
        name = "users"