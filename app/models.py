from datetime import datetime
from sqlalchemy import String, DateTime, Integer, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class ApiCache(Base):
    __tablename__ = "api_cache"

    key: Mapped[str] = mapped_column(String(300), primary_key=True)
    endpoint: Mapped[str] = mapped_column(String(80), index=True)

    player_id: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    season: Mapped[str | None] = mapped_column(String(10), index=True, nullable=True)
    game_date: Mapped[str | None] = mapped_column(String(10), index=True, nullable=True)

    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

Index("ix_api_cache_expires_at", ApiCache.expires_at)
