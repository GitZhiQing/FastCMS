from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


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


class CategoryResp(BaseModel):
    id: int
    name: str
    posts: list[PostResp] = []
    model_config = ConfigDict(from_attributes=True)
