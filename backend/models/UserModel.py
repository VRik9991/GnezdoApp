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
    @classmethod
    def from_dict( user: dict):
        return UserModel(
            foto=user["foto"],
            character_name=user["character_name"],
            other_character_name=user["other_character_name"],
            name=user["name"],
            last_name=user["last_name"],
            tg_name=user["tg_name"],
            status=user["status"],
            stats=user["stats"],
            email=user["email"],
            password=user["password"],
            role=user["role"],
        )

    class Settings:
        name = "users"
