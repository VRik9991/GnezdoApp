from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


_CLANS_JSON_PATH = Path(__file__).with_name("clans.json")
_KEY_SANITIZER = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True, slots=True)
class Clan:
    key: str
    name: str
    name_ru: str
    disciplines: tuple[str, ...]
    disciplines_ru: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "key": self.key,
            "name": self.name,
            "name_ru": self.name_ru,
            "disciplines": list(self.disciplines),
            "disciplines_ru": list(self.disciplines_ru),
        }


def _make_key(name: str) -> str:
    return _KEY_SANITIZER.sub("_", name.lower()).strip("_")


def _load_clans() -> tuple[Clan, ...]:
    payload = json.loads(_CLANS_JSON_PATH.read_text(encoding="utf-8"))
    items = payload.get("clans", [])
    loaded: list[Clan] = []

    for item in items:
        name_en = str(item.get("en", "")).strip()
        name_ru = str(item.get("ru", "")).strip()
        dis_items = item.get("dis", []) or []

        disciplines_en = tuple(
            str(discipline.get("en", "")).strip()
            for discipline in dis_items
            if str(discipline.get("en", "")).strip()
        )
        disciplines_ru = tuple(
            str(discipline.get("ru", "")).strip()
            for discipline in dis_items
            if str(discipline.get("ru", "")).strip()
        )

        if not name_en:
            continue

        loaded.append(
            Clan(
                key=_make_key(name_en),
                name=name_en,
                name_ru=name_ru,
                disciplines=disciplines_en,
                disciplines_ru=disciplines_ru,
            )
        )

    return tuple(loaded)


clans: tuple[Clan, ...] = _load_clans()
ALL_CLANS: tuple[Clan, ...] = clans
CLANS_BY_KEY: dict[str, Clan] = {clan.key: clan for clan in clans}

