
from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter(prefix="/faostat", tags=["faostat"])

BASE = "https://fenixservices.fao.org/faostat/api/v1/en/data"

CROP_CODES = {
    "wheat": "15",
    "rice": "27",
    "maize": "56",
}

COUNTRY_CODES = {
    "india": "100",
    "china": "351",
    "united states": "231", "usa": "231", "us": "231",
}

@router.get("/production")
async def production(country: str = Query(...), crop: str = Query(...), year: int = Query(...)):
    item = CROP_CODES.get(crop.lower())
    area = COUNTRY_CODES.get(country.lower())
    if not item or not area:
        raise HTTPException(status_code=400, detail="Unsupported crop or country (demo mapping).")
    url = f"{BASE}/QCL"
    params = {"item_code": item, "area_code": area, "year": str(year)}
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="FAOSTAT error")
        data = r.json().get("data", [])
        if not data:
            return {"message": "No data", "country": country, "crop": crop, "year": year}
        row = data[0]
        return {
            "country": country,
            "crop": crop,
            "year": year,
            "value": row.get("value"),
            "unit": row.get("unit"),
            "item_code": item,
            "area_code": area
        }
