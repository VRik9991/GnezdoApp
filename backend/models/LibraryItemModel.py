from enum import Enum
from beanie import Document
from backend.utils.UserUtilsTypes import UserType


class LibraryItemType(Enum):
    LORE = 'Lore'
    GAME_TEXT = 'Game text'
    RULE = 'Rule'



class LibraryItemModel(Document):
    name: str
    item_type: LibraryItemType
    item_text: str
    date: str
    access: UserType
    author: str
    picture: bytes | None