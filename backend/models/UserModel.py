from beanie import Document

from backend.models.UserModelStats import UserModelStats

class UserModel(Document):
    foto: str
    character_name:str
    other_character_name:str
    name:str
    tg_name:str
    status:str
    stats: UserModelStats
    class Settings:
        name = "users"