import base64
from os import access
from typing import Optional, Literal
import logging

from fastapi import Depends, FastAPI, HTTPException
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.Interfaces.ClanModel import ClanNames, ClanModel
from backend.Interfaces.CreateLibraryItemInterface import CreateLibraryItemInterface
from backend.models.LibraryItemModel import LibraryItemModel, LibraryItemType
from backend.models.UserModel import UserModel
from backend.models.UserModelStats import UserModelStats
from backend.models.UserModelStats import UserModelStats
from backend.models.initDB import init_db
from backend.utils.UserUtilsTypes import UserType


async def lifespan(app : FastAPI):
    await init_db()
    yield

async def ensure_db() -> None:
    await init_db()

app = FastAPI(
    title="GnezdoApp",
    version="1.0",
    lifespan=lifespan,
    dependencies=[Depends(ensure_db)],
)

@app.post("/clan")
async  def create_clan(
        name: ClanNames,
    description: str):
    clan = ClanModel(
        name=name,
        description=description
    )
    await clan.save()
    return clan
@app.get("/user_credentials")
async def user_credentials():
    users_credentials = dict()
    for user in await UserModel.find_all().to_list():
        users_credentials[user.email]={
            "email": user.email,
            "failed_login_attempts": 0,
            "first_name": user.name,
            "last_name": user.last_name,
            "logged_in": False,
            "password": user.password,
            "roles": user.role,}



    return{"usernames": users_credentials}



@app.post("/user")
async def create_user(
    foto: str,
    character_name: str,
    other_character_name: str,
    name: str,
    last_name: str,
    tg_name: str,
    status: str,
    stats: UserModelStats,
    email: str,
    password: str,
    role: UserType,
    clan: ClanNames
):
    user = UserModel(
        foto=foto,
        character_name=character_name,
        other_character_name=other_character_name,
        name=name,
        last_name=last_name,
        tg_name=tg_name,
        status=status,
        stats=stats,
        email=email,
        password=password,
        role=role,
        clan=clan
    )
    await user.save()
    return user


@app.get("/user")
async def read_user(email: str):
    user = await UserModel.find_one(UserModel.email == email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users_characters_preview")
async def get_all_characters_preview():
    characters_preview = dict()
    for user in await UserModel.find_all().to_list():
        characters_preview[user.email] = {
            "_id": str(user.id),
            "foto": user.foto,
            "character_name": user.character_name,
            "username": user.name,
            "clan": user.clan,
            "email": user.email}

    return {"characters_preview": characters_preview}

@app.put("/user")
async def update_user(
    name: str,
    new_foto: Optional[str] = None,
    new_character_name: Optional[str] = None,
    new_other_character_name: Optional[str] = None,
    new_name: Optional[str] = None,
    new_last_name: Optional[str] = None,
    new_status: Optional[str] = None,
    new_tg_name: Optional[str] = None,
    new_stats: Optional[UserModelStats] = None,
    new_email: Optional[str] = None,
    new_password: Optional[str] = None,
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
    if new_last_name is not None:
        user.last_name = new_last_name
    if new_status is not None:
        user.status = new_status
    if new_tg_name is not None:
        user.tg_name = new_tg_name
    if new_stats is not None:
        user.stats = new_stats
    if new_email is not None:
        user.email = new_email
    if new_password is not None:
        user.password = new_password
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

@app.get("/library/all")
async def get_library():
    items = await LibraryItemModel.find_all().to_list()
    return items

@app.get("/library/one")
async def get_library_item(item_id):
    item = await LibraryItemModel.get(ObjectId(item_id))

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

class PutItemModel(BaseModel):
    id: str
    name: str
    item_text: str
    item_type: LibraryItemType
    access: UserType
    picture: bytes | None

@app.put("/library")
async def put_library_item(data: PutItemModel):
    item = await get_library_item(data.id)
    if data.access is not None:
        item.access = data.access
    if data.item_text is not None:
        item.item_text = data.item_text
    if data.name is not None:
        item.name = data.name
    if data.item_type is not None:
        item.item_type = data.item_type
    if data.picture is not None:
        item.picture = data.picture
    await item.save()
    return item