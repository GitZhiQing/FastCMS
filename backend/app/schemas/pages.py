from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: dict

    model_config = ConfigDict(
        json_schema_extra={"example": {"data": [], "meta": {"total": 100, "page": 1, "per_page": 20, "total_pages": 5}}}
    )
