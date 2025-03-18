from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    power: int
