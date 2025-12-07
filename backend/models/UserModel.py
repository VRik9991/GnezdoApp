
from beanie import Document

class UserModel(Document):
    foto: str
    character_name:str
    other_character_name:str
    name:str
    tg_name:str
    status:str
    class Settings:
        name = "users"
