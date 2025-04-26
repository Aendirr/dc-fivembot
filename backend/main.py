from fastapi import FastAPI
from backend.routers import inventory, events, player_data, server_control
import backend.config.config as config


app = FastAPI(
    title="FiveM Yönetim Backend API",
    description="Discord botu ve sunucu kontrol sistemine API sağlar.",
    version="1.0.0"
)

# Router bağlantıları
app.include_router(inventory.router)
app.include_router(events.router)
app.include_router(player_data.router)
app.include_router(server_control.router)

# Sağlık kontrolü / root test endpoint
@app.get("/")
async def root():
    return {"message": "✅ FiveM Backend API aktif durumda."}
