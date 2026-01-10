from os import access
from typing import Optional
import logging

from fastapi import FastAPI, HTTPException

from backend.Interfaces.CreateLibraryItemInterface import CreateLibraryItemInterface
from backend.models.UserModel import UserModel
from backend.models.LibraryItemModel import LibraryItemModel, LibraryItemType
from backend.models.UserModelStats import UserModelStats
from backend.models.initDB import init_db

async def lifespan(app : FastAPI):
    await init_db()
    yield
logger = logging.getLogger()

app = FastAPI(title="GnezdoApp", version="1.0",lifespan=lifespan)

@app.post("/user")
async def create_user(foto: str,character_name:str,other_character_name:str,name:str,tg_name:str,status:str,stats:UserModelStats):
    user = UserModel(
        foto=foto,
        character_name=character_name,
        other_character_name=other_character_name,
        name=name,
        tg_name=tg_name,
        status=status,
        stats=stats
    )
    await user.save()
    return user


@app.get("/user")
async def read_user(name: str):
    user = await UserModel.find_one(UserModel.name == name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user")
async def update_user(
    name: str,
    new_foto: Optional[str] = None,
    new_character_name: Optional[str] = None,
    new_other_character_name: Optional[str] = None,
    new_name: Optional[str] = None,
    new_status: Optional[str] = None,
    new_tg_name: Optional[str] = None,
):
    user = await read_user(name)
    if new_foto is not None:
        user.foto = new_foto
    if new_character_name is not None:
        user.character_name = new_character_name
    if new_other_character_name is not None:
        user.other_character_name = new_other_character_name
    if new_name is not None:
        user.name = new_name
    if new_status is not None:
        user.status = new_status
    if new_tg_name is not None:
        user.tg_name = new_tg_name
    await user.save()
    return user

@app.delete("/user")
async def delete_user(name:str):
    user = await read_user(name)
    await user.delete()
    return {"detail": "User deleted"}

@app.post("/library")
async def create_library_item(data: CreateLibraryItemInterface):
    try:
        item = LibraryItemModel(
        name=data.name,
        item_type=data.item_type,
        item_text=data.item_text,
        date=data.date,
        access=data.access,
        author=data.author,
        picture=data.picture
        )
    except Exception as e:
        return str(e)
    await item.save()

@app.get("/library")
async def get_library():
    library = await LibraryItemModel.find_all().to_list()
    logger.error(str(library))
    return library