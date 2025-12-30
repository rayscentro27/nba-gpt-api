from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.cache_store import cache_get, cache_set
from app.settings import TTL_LEAGUE_DASH
from app.nba import clients

router = APIRouter()

@router.get("/search")
def team_search(name: str = Query(...), db: Session = Depends(get_db)):
    key = f"team_search:{name.strip().lower()}"
    cached = cache_get(db, key)
    if cached:
        return {"source": "postgres_cache", **cached}

    matches = clients.search_teams(name)
    payload = {"query": {"name": name}, "matches": matches}
    saved = cache_set(db, key=key, endpoint="team_search", payload=payload, ttl_seconds=TTL_LEAGUE_DASH)
    return {"source": "live_fetch", **saved}
