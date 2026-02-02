from pydantic import BaseModel

from backend.models.LibraryItemModel import LibraryItemType
from backend.utils.UserUtilsTypes import UserType


class CreateLibraryItemInterface(BaseModel):
    name: str
    item_type: LibraryItemType
    item_text: str
    date: str
    access: UserType
    author: str
    picture: bytes