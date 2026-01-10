from enum import Enum

from beanie import Document

class LibraryItemType(Enum):
    LORE = 'Lore'
    GAME_TEXT = 'Game text'
    RULE = 'Rule'

class LibraryAccessType(Enum):
    PLAYER = 'Player'
    GAME_TECH = 'Game technician'
    MACRO = 'Macronosphere'
    MASTER = 'Master'

class LibraryItemModel(Document):
    name: str
    item_type: LibraryItemType
    item_text: str
    date: str
    access: LibraryAccessType
    author: str
    picture: bytes