from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    category_id: int | None = None
    tag_ids: list[int] | None = None
    created_at: int
    updated_at: int
    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    id: int
    name: str
    posts: list[PostResponse] = []
    model_config = ConfigDict(from_attributes=True)
