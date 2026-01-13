from typing import Literal

from beanie import Document
from pydantic import field_validator

from backend.models.UserModelStats import UserModelStats

Role = Literal["admin", "editor", "viewer"]


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
    role: list[Role]

    @field_validator("role", mode="before")
    @classmethod
    def coerce_role(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return value

    class Settings:
        name = "users"
