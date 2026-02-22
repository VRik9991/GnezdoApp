from __future__ import annotations

from pydantic import BaseModel, Field, conint


class UserDisciplinePower(BaseModel):
    discipline_en: str
    power_en: str
    level: conint(ge=1, le=5)


class UserModelStats(BaseModel):
    clan: str
    sir_name: str
    generation: int
    generation_mod: int
    health: int
    hunger: int
    strength: int
    strength_mod: int
    stamina: int
    stamina_mod: int
    ritualist: bool
    dodge: bool
    true_faith: bool
    feels_infernalist: bool
    torpor_button: bool
    extra_status: str
    disciplines: list[UserDisciplinePower] = Field(default_factory=list)
