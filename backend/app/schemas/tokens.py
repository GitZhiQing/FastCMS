from typing import Literal

from pydantic import BaseModel


class TokenData(BaseModel):
    uid: int
    power: int


class Token(BaseModel):
    token: str
    token_type: Literal["access_token", "refresh_token"]
