import time
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True, "ts": int(time.time())}
