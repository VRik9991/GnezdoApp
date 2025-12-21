from beanie import Document

class UserModelStats(Document):
    klan: str
    sir_name: str
    generation: int
    health: int
    hunger: int
    strength: int
    stamina: int
    ritualist: bool
    dodge: bool
    true_faith: bool
    feels_infernalist: bool