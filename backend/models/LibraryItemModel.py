from beanie import Document

class UserModel(Document):
    name: str
    item_type: str
    item_text: str
    date: str