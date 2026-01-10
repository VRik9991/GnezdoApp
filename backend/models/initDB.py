from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from backend.models.UserModel import UserModel
from backend.models.LibraryItemModel import LibraryItemModel


MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_LOGIN = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_URI = f"mongodb://localhost:27017"

async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(
        database=client["Gnezdo"],
        document_models=[
            UserModel,
            LibraryItemModel
        ]
    )