
from fastapi import APIRouter, HTTPException, Query
import httpx, os
from app.config import settings

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("")
async def get_weather(lat: float = Query(...), lon: float = Query(...)):
    key = settings.OPENWEATHER_API_KEY
    if not key:
        raise HTTPException(status_code=400, detail="OPENWEATHER_API_KEY not set")
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,alerts&units=metric&appid={key}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="OpenWeather error")
        return r.json()
