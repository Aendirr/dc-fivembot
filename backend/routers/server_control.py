from fastapi import APIRouter, Request, HTTPException
import backend.config.config as config

router = APIRouter()

@router.post("/restart")
async def restart_server(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    print("[RESTART] Sunucu yeniden başlatılıyor...")
    return {"status": "restart_requested"}
