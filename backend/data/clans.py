from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar


class Clan(ABC):
    name: ClassVar[str]
    disciplines: ClassVar[tuple[str, ...]]

    @classmethod
    @abstractmethod
    def key(cls) -> str:
        """Stable key for storage/search."""

    @classmethod
    def to_dict(cls) -> dict[str, object]:
        return {
            "key": cls.key(),
            "name": cls.name,
            "disciplines": list(cls.disciplines),
        }


class BanuHaqimClan(Clan):
    name = "Banu Haqim"
    disciplines = ("Blood Sorcery", "Celerity", "Obfuscate")

    @classmethod
    def key(cls) -> str:
        return "banu_haqim"


class BrujahClan(Clan):
    name = "Brujah"
    disciplines = ("Celerity", "Potence", "Presence")

    @classmethod
    def key(cls) -> str:
        return "brujah"


class CaitiffClan(Clan):
    name = "Caitiff"
    disciplines = ("Any 3 disciplines (player choice)",)

    @classmethod
    def key(cls) -> str:
        return "caitiff"


class GangrelClan(Clan):
    name = "Gangrel"
    disciplines = ("Animalism", "Fortitude", "Protean")

    @classmethod
    def key(cls) -> str:
        return "gangrel"


class HecataClan(Clan):
    name = "Hecata"
    disciplines = ("Auspex", "Fortitude", "Oblivion")

    @classmethod
    def key(cls) -> str:
        return "hecata"


class LasombraClan(Clan):
    name = "Lasombra"
    disciplines = ("Dominate", "Oblivion", "Potence")

    @classmethod
    def key(cls) -> str:
        return "lasombra"


class MalkavianClan(Clan):
    name = "Malkavian"
    disciplines = ("Auspex", "Dominate", "Obfuscate")

    @classmethod
    def key(cls) -> str:
        return "malkavian"


class MinistryClan(Clan):
    name = "Ministry"
    disciplines = ("Obfuscate", "Presence", "Protean")

    @classmethod
    def key(cls) -> str:
        return "ministry"


class NosferatuClan(Clan):
    name = "Nosferatu"
    disciplines = ("Animalism", "Obfuscate", "Potence")

    @classmethod
    def key(cls) -> str:
        return "nosferatu"


class RavnosClan(Clan):
    name = "Ravnos"
    disciplines = ("Animalism", "Obfuscate", "Presence")

    @classmethod
    def key(cls) -> str:
        return "ravnos"


class SalubriClan(Clan):
    name = "Salubri"
    disciplines = ("Auspex", "Dominate", "Fortitude")

    @classmethod
    def key(cls) -> str:
        return "salubri"


class ThinBloodClan(Clan):
    name = "Thin-Blood"
    disciplines = ("Thin-blood Alchemy",)

    @classmethod
    def key(cls) -> str:
        return "thin_blood"


class ToreadorClan(Clan):
    name = "Toreador"
    disciplines = ("Auspex", "Celerity", "Presence")

    @classmethod
    def key(cls) -> str:
        return "toreador"


class TremereClan(Clan):
    name = "Tremere"
    disciplines = ("Auspex", "Blood Sorcery", "Dominate")

    @classmethod
    def key(cls) -> str:
        return "tremere"


class TzimisceClan(Clan):
    name = "Tzimisce"
    disciplines = ("Animalism", "Dominate", "Protean")

    @classmethod
    def key(cls) -> str:
        return "tzimisce"


class VentrueClan(Clan):
    name = "Ventrue"
    disciplines = ("Dominate", "Fortitude", "Presence")

    @classmethod
    def key(cls) -> str:
        return "ventrue"


clans: tuple[type[Clan], ...] = (
    BanuHaqimClan,
    BrujahClan,
    CaitiffClan,
    GangrelClan,
    HecataClan,
    LasombraClan,
    MalkavianClan,
    MinistryClan,
    NosferatuClan,
    RavnosClan,
    SalubriClan,
    ThinBloodClan,
    ToreadorClan,
    TremereClan,
    TzimisceClan,
    VentrueClan,
)

CLANS_BY_KEY: dict[str, type[Clan]] = {clan.key(): clan for clan in ALL_CLANS}

