from entities.User import User
from beanie import Document

class UserModel(Document,User):
    foto: str
    character_name:str
    other_character_name:str
    name:str
    tgname:str
    status:str
    class Settings:
        name = "users"
