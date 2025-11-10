# main.py
from fastapi import FastAPI, Depends
from app.db import connect, disconnect
from app.auth import get_current_user  # Import directly from app.auth
from app.routers import auth, soil, weather, faostat, irrigation

app = FastAPI(title="KisanAI Mongo Backend (Clean)")

app.include_router(auth.router)
app.include_router(soil.router)
app.include_router(weather.router)
app.include_router(faostat.router)
app.include_router(irrigation.router)

@app.on_event("startup")
async def on_startup():
    await connect()

@app.on_event("shutdown")
async def on_shutdown():
    await disconnect()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/me")
async def me(user=Depends(get_current_user)):
    return user