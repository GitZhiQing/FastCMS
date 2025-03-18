from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int | None = None
    tag_ids: list[int] = []


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None


class PostResp(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    category_id: int | None = None
    tag_ids: list[int] | None = None
    created_at: int
    updated_at: int
    model_config = ConfigDict(from_attributes=True)
