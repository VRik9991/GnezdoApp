from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from backend.models.UserModel import UserModel
from backend.models.LibraryItemModel import LibraryItemModel


MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_LOGIN = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_URI = "mongodb://localhost:27017"

_client: Optional[AsyncIOMotorClient] = None
_initialized = False

async def init_db() -> None:
    global _client, _initialized
    if _initialized:
        return
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(
        database=_client["Gnezdo"],
        document_models=[
            UserModel,
            LibraryItemModel
        ]
    )
    _initialized = True
