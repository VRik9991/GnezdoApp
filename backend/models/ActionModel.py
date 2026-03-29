from datetime import datetime, timezone
from typing import Literal

from beanie import Document
from pydantic import Field, field_validator

ActionType = Literal["Атака", "Защита", "Шпионаж", "Пропаганда", "Подстрекательство", "Другая"]


class ActionModel(Document):
    user_id: str
    region_name: str
    action_type: ActionType
    resources_used: int = Field(default=0, ge=0)
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("notes", mode="before")
    @classmethod
    def normalize_notes(cls, value: object) -> str:
        return str(value or "").strip()

    class Settings:
        name = "actions"
