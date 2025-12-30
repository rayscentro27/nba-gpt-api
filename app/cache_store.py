from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import ApiCache

def cache_get(db: Session, key: str) -> dict | None:
    row = db.get(ApiCache, key)
    if not row:
        return None
    if row.expires_at <= datetime.utcnow():
        db.delete(row)
        db.commit()
        return None
    return row.payload

def cache_set(
    db: Session,
    *,
    key: str,
    endpoint: str,
    payload: dict,
    ttl_seconds: int,
    player_id: int | None = None,
    season: str | None = None,
    game_date: str | None = None,
) -> dict:
    now = datetime.utcnow()
    expires_at = now + timedelta(seconds=ttl_seconds)

    existing = db.get(ApiCache, key)
    if existing:
        db.delete(existing)
        db.flush()

    row = ApiCache(
        key=key,
        endpoint=endpoint,
        payload=payload,
        player_id=player_id,
        season=season,
        game_date=game_date,
        created_at=now,
        expires_at=expires_at,
    )

    db.add(row)
    db.commit()
    return payload
