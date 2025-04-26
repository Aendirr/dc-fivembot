from fastapi import APIRouter, Request, HTTPException
import backend.config.config as config

router = APIRouter()

@router.get("/playerinfo/{discord_id}")
async def player_info(discord_id: str, request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    dummy_data = {
        "total_playtime": "5 saat 32 dakika"
    }
    return dummy_data
