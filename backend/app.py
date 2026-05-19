from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from backend.models.CommentsModel import CommentModel, serbia_now
from backend.models.NewsModel import NewsModel
from backend.models.UserModel import UserModel
from backend.models.UserModelStats import UserModelStats
from backend.models.initDB import init_db


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    email: str
    foto: Optional[str] = None
    character_name: Optional[str] = None
    other_character_name: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    tg_name: Optional[str] = None
    status: Optional[str] = None
    stats: Optional[UserModelStats] = None
    password: Optional[str] = None
    role: Optional[list[str]] = None


class NewsUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    active: Optional[bool] = None
    pic: Optional[str] = None
    fancy_comment: Optional[str] = None
    text: Optional[str] = None
    owner: Optional[str] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    publish_date: Optional[datetime] = None
    comments: Optional[list[CommentModel]] = None

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


async def get_owner_pic(owner: str) -> str:
    user = await UserModel.find_one(
        (UserModel.email == owner)

    )
    if user is None:
        return ""
    return user.foto


async def fill_comment_owner_pic(comment: CommentModel) -> CommentModel:
    if comment.owner_pic:
        return comment
    comment.owner_pic = await get_owner_pic(comment.owner)
    return comment


async def news_with_owner_pics(news: NewsModel) -> dict:
    news.owner_pic = await get_owner_pic(news.owner)
    news.comments = [
        await fill_comment_owner_pic(comment)
        for comment in news.comments
    ]
    return news.model_dump(mode="json")


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
    role: list[str]
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
        role=role
    )
    await user.save()
    return user


@app.get("/user")
async def read_user(email: str):
    user = await UserModel.find_one(UserModel.email == email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user")
async def update_user(payload: UserUpdate):
    user = await UserModel.find_one(UserModel.email == payload.email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updates = payload.model_dump(exclude_unset=True)
    updates.pop("email", None)
    for key, value in updates.items():
        setattr(user, key, value)
    await user.save()
    return user

@app.delete("/user")
async def delete_user(email: str):
    user = await read_user(email)
    await user.delete()
    return {"detail": "User deleted"}


@app.post("/news")
async def create_news(payload: NewsModel):
    payload.comments = [
        await fill_comment_owner_pic(comment)
        for comment in payload.comments
    ]
    payload.owner_pic = await get_owner_pic(payload.owner)
    await payload.save()
    return await news_with_owner_pics(payload)


@app.post("/comment")
async def post_comment(news_name: str, payload: CommentModel):
    news = await NewsModel.find_one(NewsModel.name == news_name)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    payload.date = serbia_now()
    payload.owner_pic = await get_owner_pic(payload.owner)
    news.comments.append(payload)
    await news.save()
    return payload.model_dump(mode="json")


@app.delete("/comment")
async def delete_comment(news_name: str, payload: CommentModel):
    news = await NewsModel.find_one(NewsModel.name == news_name)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    comment_index = None
    for index, comment in enumerate(news.comments):
        if (
            comment.text == payload.text
            and comment.owner == payload.owner
            and comment.date == payload.date
        ):
            comment_index = index
            break
    if comment_index is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    news.comments.pop(comment_index)
    await news.save()
    return {"detail": "Comment deleted"}


@app.get("/news")
async def get_news(name: str):
    news = await NewsModel.find_one(NewsModel.name == name)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return await news_with_owner_pics(news)


@app.put("/news")
async def change_news(payload: NewsUpdate):
    news = await NewsModel.find_one(NewsModel.name == payload.name)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")

    updates = payload.model_dump(exclude_unset=True)
    updates.pop("name", None)
    comments = updates.pop("comments", None)
    for key, value in updates.items():
        setattr(news, key, value)
    if comments is not None:
        news.comments = [
            await fill_comment_owner_pic(CommentModel.model_validate(comment))
            for comment in comments
        ]
    news.owner_pic = await get_owner_pic(news.owner)
    news.update_date = serbia_now()
    await news.save()
    return await news_with_owner_pics(news)


@app.delete("/news")
async def delete_news(name: str):
    news = await NewsModel.find_one(NewsModel.name == name)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    await news.delete()
    return {"detail": "News deleted"}
