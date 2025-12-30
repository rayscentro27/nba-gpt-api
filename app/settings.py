import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required in .env or env vars")

def _int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        return int(raw)
    except ValueError:
        return default

TTL_SCOREBOARD = _int("TTL_SCOREBOARD", 30)
TTL_PLAYER_GAMELOG = _int("TTL_PLAYER_GAMELOG", 1800)
TTL_LEAGUE_DASH = _int("TTL_LEAGUE_DASH", 21600)
TTL_CAREER_SEASONS = _int("TTL_CAREER_SEASONS", 86400)
