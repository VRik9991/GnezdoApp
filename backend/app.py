from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from backend.models.ActionModel import ActionModel, ActionType
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


class ActionCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_email: str
    region_name: str

    action_type: ActionType

    resources_used: int = Field(default=0, ge=0)
    notes: str = ""

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


@app.post("/action")
async def create_action(payload: ActionCreate):
    if not payload.user_email.strip():
        raise HTTPException(status_code=400, detail="user_email is required")
    user = await UserModel.find_one(UserModel.email == payload.user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    action = ActionModel(
        user_email=payload.user_email,
        region_name=payload.region_name,
        action_type=payload.action_type,
        resources_used=payload.resources_used,
        notes=payload.notes,
    )
    await action.save()
    return action


@app.get("/action")
async def read_actions(user_email: Optional[str] = None):
    query = ActionModel.find_all()
    if user_email:
        query = ActionModel.find(ActionModel.user_email == user_email)
    actions = await query.sort(-ActionModel.created_at).to_list()
    return actions


@app.put("/action/{action_id}")
async def update_action(action_id: str, payload: ActionCreate):
    action = await ActionModel.get(action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    action.user_email = payload.user_email
    action.territory_name = payload.territory_name
    action.territory_status = payload.territory_status
    action.action_type = payload.action_type
    action.attackers = payload.attackers
    action.defenders = payload.defenders
    action.resources_used = payload.resources_used
    action.notes = payload.notes
    action.updated_at = datetime.now(timezone.utc)
    await action.save()
    return action


