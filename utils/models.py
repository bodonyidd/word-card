from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class PackageName(BaseModel):
    package_name: str


class Card(BaseModel):
    front: str
    back: str


class CardData(BaseModel):
    """
    {
    "card": {
        "front": "This is the front side",
        "back": "This is the back side"
    },
    "card_info":"asssdd"
    "front": "HU",
    "back": "EN"
    }
    """

    card: Card
    front: str | None = None
    back: str | None = None