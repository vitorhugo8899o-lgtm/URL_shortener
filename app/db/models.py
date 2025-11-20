from __future__ import annotations

from datetime import datetime
from sqlalchemy import Integer, String, func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )

    urls: Mapped[list[URL]] = relationship(
        back_populates="user",
        default_factory=list
    )


@table_registry.mapped_as_dataclass
class URL:
    __tablename__ = 'urls'

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)

    
    original_url: Mapped[str] = mapped_column(String, nullable=False)
    short_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="urls")

    clicks: Mapped[int] = mapped_column(Integer, default=0)

    