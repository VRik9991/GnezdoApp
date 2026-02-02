from pydantic import BaseModel

class UserModelStats(BaseModel):
    sir_name: str
    generation: int
    generation_mod:int
    health: int
    hunger: int
    strength: int
    strength_mod:int
    stamina: int
    stamina_mod:int
    ritualist: bool
    dodge: bool
    true_faith: bool
    feels_infernalist: bool
    torpor_button:bool
    extra_status:str
