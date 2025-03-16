from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserEmailLogin(BaseModel):
    email: EmailStr
    password: str


class UserNameLogin(BaseModel):
    username: str
    password: str


class UserResp(BaseModel):
    id: int
    email: EmailStr
    username: str
    avatar: str | None = None
    power: int
    created_at: int
    updated_at: int
    model_config = ConfigDict(from_attributes=True)
