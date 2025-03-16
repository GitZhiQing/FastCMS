from time import time

from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    # 秒级时间戳
    created_at: Mapped[int] = mapped_column(default=lambda: int(time()))
    updated_at: Mapped[int] = mapped_column(default=lambda: int(time()), onupdate=lambda: int(time()))
