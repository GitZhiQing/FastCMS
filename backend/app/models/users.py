from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase
from app.models.mixins import TimestampMixin


class User(ModelBase, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(64), nullable=False)
    avatar: Mapped[str] = mapped_column(String(36), nullable=True)
    power: Mapped[int] = mapped_column(
        SmallInteger, default=1, nullable=False
    )  # 0: BANED 用户 | 1: 普通用户 | 2: 管理员用户 | 3: 超级管理员用户

    posts = relationship("Post", back_populates="author")
