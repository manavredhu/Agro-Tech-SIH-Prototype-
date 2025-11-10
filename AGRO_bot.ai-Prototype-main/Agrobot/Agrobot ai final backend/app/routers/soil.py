
from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter(prefix="/soil", tags=["soil"])

# Try SoilGrids v2 first; fallback to legacy endpoint for robustness
async def fetch_soil(lat: float, lon: float):
    v2 = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lat={lat}&lon={lon}&property=phh2o&property=soc&depth=0-5cm&value=mean"
    legacy = f"https://rest.soilgrids.org/query?lat={lat}&lon={lon}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(v2)
        if r.status_code == 200:
            return {"source": "SoilGrids v2", "raw": r.json()}
        r2 = await client.get(legacy)
        if r2.status_code == 200:
            return {"source": "SoilGrids legacy", "raw": r2.json()}
    raise HTTPException(status_code=502, detail="SoilGrids unavailable")

@router.get("")
async def get_soil(lat: float = Query(...), lon: float = Query(...)):
    data = await fetch_soil(lat, lon)
    return data
