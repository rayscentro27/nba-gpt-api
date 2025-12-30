import os
from dotenv import load_dotenv

# Load .env locally (Render ignores .env and uses real env vars)
load_dotenv()

# ------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required (set it as an environment variable)")

# Render sometimes provides DATABASE_URL starting with "postgres://"
# SQLAlchemy requires "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg2://",
        1
    )

# ------------------------------------------------------------------
# TTL HELPERS
# ------------------------------------------------------------------

def _int_env(name: str, default: int) -> int:
    """
    Read an int from env vars safely.
    Falls back to default if missing or invalid.
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default

# ------------------------------------------------------------------
# CACHE TTLs (seconds)
# ------------------------------------------------------------------

# Live games change fast
TTL_SCOREBOARD = _int_env("TTL_SCOREBOARD", 30)

# Player game logs update slowly after games
TTL_PLAYER_GAMELOG = _int_env("TTL_PLAYER_GAMELOG", 1

