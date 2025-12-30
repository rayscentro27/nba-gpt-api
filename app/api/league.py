from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.cache_store import cache_get, cache_set
from app.settings import TTL_LEAGUE_DASH
from app.nba import clients
from app.nba.transform import df_preview
from app.nba.keys import key_league_player_stats, key_league_team_stats

router = APIRouter()

@router.get("/player_stats")
def player_stats(
    season: str = Query(..., description='e.g. "2024-25"'),
    season_type: str = Query("Regular Season"),
    per_mode: str = Query("PerGame"),
    db: Session = Depends(get_db),
):
    key = key_league_player_stats(season, season_type, per_mode)
    cached = cache_get(db, key)
    if cached:
        return {"source": "postgres_cache", **cached}

    df = clients.get_league_player_stats_df(season, season_type, per_mode)
    payload = {
        "query": {"season": season, "season_type": season_type, "per_mode": per_mode},
        "columns": list(df.columns),
        "preview": df_preview(df, 25),
        "row_count": int(df.shape[0]),
    }
    saved = cache_set(db, key=key, endpoint="league_player_stats", payload=payload, ttl_seconds=TTL_LEAGUE_DASH, season=season)
    return {"source": "live_fetch", **saved}

@router.get("/team_stats")
def team_stats(
    season: str = Query(..., description='e.g. "2024-25"'),
    season_type: str = Query("Regular Season"),
    per_mode: str = Query("PerGame"),
    db: Session = Depends(get_db),
):
    key = key_league_team_stats(season, season_type, per_mode)
    cached = cache_get(db, key)
    if cached:
        return {"source": "postgres_cache", **cached}

    df = clients.get_league_team_stats_df(season, season_type, per_mode)
    payload = {
        "query": {"season": season, "season_type": season_type, "per_mode": per_mode},
        "columns": list(df.columns),
        "preview": df_preview(df, 25),
        "row_count": int(df.shape[0]),
    }
    saved = cache_set(db, key=key, endpoint="league_team_stats", payload=payload, ttl_seconds=TTL_LEAGUE_DASH, season=season)
    return {"source": "live_fetch", **saved}
