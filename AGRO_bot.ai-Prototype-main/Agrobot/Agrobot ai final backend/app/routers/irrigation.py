
from fastapi import APIRouter, Query
import httpx
from app.config import settings

router = APIRouter(prefix="/irrigation", tags=["irrigation"])

KC = {"wheat": 0.8, "rice": 1.05, "maize": 1.0}

def simple_et0_from_temp(tmin, tmax):
    # Hargreaves-ish very simplified
    d = max(0.0, tmax - tmin)
    return max(0.5, 0.0023 * ((tmin + tmax)/2 + 17.8) * (d ** 0.5))

@router.get("/recommendation")
async def recommend(lat: float = Query(...), lon: float = Query(...), crop: str = Query("wheat")):
    key = settings.OPENWEATHER_API_KEY
    rain_forecast_mm = 0.0
    tmin = 20.0
    tmax = 30.0
    if key:
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,alerts&units=metric&appid={key}"
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
            if r.status_code == 200:
                j = r.json()
                daily = j.get("daily", [])
                if daily:
                    today = daily[0]
                    rain_forecast_mm = today.get("rain", 0.0) or 0.0
                    tmin = today.get("temp", {}).get("min", tmin)
                    tmax = today.get("temp", {}).get("max", tmax)

    et0 = simple_et0_from_temp(tmin, tmax)
    kc = KC.get(crop.lower(), 0.9)
    crop_need_mm = et0 * kc

    # If rain forecast is substantial, suggest skipping irrigation
    if rain_forecast_mm >= crop_need_mm * 0.7:
        return {
            "recommendation": "skip",
            "reason": f"Forecast rain ~{rain_forecast_mm:.1f} mm likely covers most water need (~{crop_need_mm:.1f} mm).",
            "et0_mm": round(et0, 2),
            "kc": kc,
            "crop_need_mm": round(crop_need_mm, 2)
        }

    # Otherwise suggest irrigation amount (mm)
    suggested_mm = max(0.0, crop_need_mm - rain_forecast_mm)
    return {
        "recommendation": "irrigate",
        "suggested_water_mm": round(suggested_mm, 1),
        "et0_mm": round(et0, 2),
        "kc": kc,
        "rain_forecast_mm": round(rain_forecast_mm, 1)
    }
