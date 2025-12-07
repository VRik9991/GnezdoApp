from fastapi import FastAPI
from backend.models.UserModel import UserModel
from backend.services.initDB import init_db

async def lifespan(app : FastAPI):
    await init_db()
    yield


app = FastAPI(title="GnezdoApp", version="1.0",lifespan=lifespan)

@app.post("/users")
async def create_user(foto: str,character_name:str,other_character_name:str,name:str,tg_name:str,status:str):
    user = UserModel(
        foto=foto,
        character_name=character_name,
        other_character_name=other_character_name,
        name=name,
        tg_name=tg_name,
        status=status
    )
    await user.save()
