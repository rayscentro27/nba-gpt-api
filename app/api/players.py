from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.cache_store import cache_get, cache_set
from app.settings import TTL_CAREER_SEASONS, TTL_PLAYER_GAMELOG
from app.nba import clients
from app.nba.transform import df_preview
from app.nba.keys import key_player_search, key_player_career_seasons, key_player_gamelog

router = APIRouter()

@router.get("/search")
def player_search(name: str = Query(...), db: Session = Depends(get_db)):
    key = key_player_search(name)
    cached = cache_get(db, key)
    if cached:
        return {"source": "postgres_cache", **cached}

    matches = clients.search_players(name)
    payload = {"query": {"name": name}, "matches": matches}
    saved = cache_set(db, key=key, endpoint="player_search", payload=payload, ttl_seconds=TTL_CAREER_SEASONS)
    return {"source": "live_fetch", **saved}

@router.get("/career_seasons")
def career_seasons(player_id: int = Query(...), db: Session = Depends(get_db)):
    key = key_player_career_seasons(player_id)
    cached = cache_get(db, key)
    if cached:
        return {"source": "postgres_cache", **cached}

    df = clients.get_player_career_seasons_df(player_id)
    payload = {
        "query": {"player_id": player_id},
        "columns": list(df.columns),
        "preview": df_preview(df, 10),
        "row_count": int(df.shape[0]),
    }
    saved = cache_set(
        db, key=key, endpoint="player_career_seasons", payload=payload,
        ttl_seconds=TTL_CAREER_SEASONS, player_id=player_id
    )
    return {"source": "live_fetch", **saved}

@router.get("/gamelog")
def gamelog(
    player_id: int = Query(...),
    season: str = Query(..., description='e.g. "2024-25"'),
    season_type: str = Query("Regular Season"),
    db: Session = Depends(get_db),
):
    season = season.strip()
    season_type = season_type.strip()
    key = key_player_gamelog(player_id, season, season_type)

    cached = cache_get(db, key)
    if cached:
        return {"source": "postgres_cache", **cached}

    df = clients.get_player_gamelog_df(player_id, season, season_type)
    payload = {
        "query": {"player_id": player_id, "season": season, "season_type": season_type},
        "columns": list(df.columns),
        "preview": df_preview(df, 15),
        "row_count": int(df.shape[0]),
    }
    saved = cache_set(
        db, key=key, endpoint="player_gamelog", payload=payload,
        ttl_seconds=TTL_PLAYER_GAMELOG, player_id=player_id, season=season
    )
    return {"source": "live_fetch", **saved}
