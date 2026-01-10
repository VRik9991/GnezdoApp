from pydantic import BaseModel

from backend.models.LibraryItemModel import LibraryItemType, LibraryAccessType


class CreateLibraryItemInterface(BaseModel):
    name: str
    item_type: LibraryItemType
    item_text: str
    date: str
    access: LibraryAccessType
    author: str
    picture: bytes