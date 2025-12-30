from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.players import router as players_router
from app.api.teams import router as teams_router
from app.api.league import router as league_router
from app.api.games import router as games_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(players_router, prefix="/player", tags=["players"])
router.include_router(teams_router, prefix="/team", tags=["teams"])
router.include_router(league_router, prefix="/league", tags=["league"])
router.include_router(games_router, prefix="/games", tags=["games"])

