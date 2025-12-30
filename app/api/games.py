from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.cache_store import cache_get, cache_set
from app.settings import TTL_SCOREBOARD
from app.nba import clients
from app.nba.transform import df_preview
from app.nba.keys import key_scoreboard

router = APIRouter()

@router.get("/scoreboard")
def scoreboard(game_date: str = Query(..., description='MM/DD/YYYY'), db: Session = Depends(get_db)):
    game_date = game_date.strip()
    key = key_scoreboard(game_date)

    cached = cache_get(db, key)
    if cached:
        return {"source": "postgres_cache", **cached}

    games_df, line_df = clients.get_scoreboard_dfs(game_date)
    payload = {
        "query": {"game_date": game_date},
        "games": df_preview(games_df, 50),
        "line_score": df_preview(line_df, 200),
        "games_count": int(games_df.shape[0]),
    }
    saved = cache_set(db, key=key, endpoint="games_scoreboard", payload=payload, ttl_seconds=TTL_SCOREBOARD, game_date=game_date)
    return {"source": "live_fetch", **saved}
