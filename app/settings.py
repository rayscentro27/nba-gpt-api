import os
from dotenv import load_dotenv

# Load .env locally (Render uses Environment Variables)
load_dotenv()

# -----------------------------
# DATABASE
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required (set it as an environment variable)")

# Render sometimes provides DATABASE_URL starting with "postgres://"
# SQLAlchemy expects "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

# -----------------------------
# TTL helpers
# -----------------------------
def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw.strip())
    except ValueError:
        return default

# -----------------------------
# CACHE TTLs (seconds)
# -----------------------------
TTL_SCOREBOARD = _int_env("TTL_SCOREBOARD", 30)
TTL_PLAYER_GAMELOG = _int_env("TTL_PLAYER_GAMELOG", 1800)  # 30 min
TTL_LEAGUE_DASH = _int_env("TTL_LEAGUE_DASH", 21600)        # 6 hours
TTL_CAREER_SEASONS = _int_env("TTL_CAREER_SEASONS", 86400)  # 24 hours
