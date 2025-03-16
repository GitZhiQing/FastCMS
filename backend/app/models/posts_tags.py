from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models.base import ModelBase

posts_tags = Table(
    "posts_tags",
    ModelBase.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)
