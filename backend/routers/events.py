from fastapi import APIRouter, Request, HTTPException
import backend.config.config as config

router = APIRouter()

@router.post("/event")
async def create_event(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    data = await request.json()
    title = data["title"]
    description = data["description"]

    print(f"[ETKİNLİK] {title} ➔ {description}")
    return {"status": "event_broadcasted"}

@router.post("/event_cancel")
async def cancel_event(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    data = await request.json()
    title = data["title"]
    reason = data["reason"]

    print(f"[ETKİNLİK İPTAL] {title} ➔ {reason}")
    return {"status": "event_cancelled"}

@router.post("/ban")
async def ban_user(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = await request.json()
    print(f"[BAN] {data['user_id']} - {data['reason']}")
    return {"status": "success"}

@router.post("/kick")
async def kick_user(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = await request.json()
    print(f"[KICK] {data['user_id']} - {data['reason']}")
    return {"status": "success"}

@router.post("/warn")
async def warn_user(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = await request.json()
    print(f"[WARN] {data['user_id']} - {data['reason']}")
    return {"status": "success"}
