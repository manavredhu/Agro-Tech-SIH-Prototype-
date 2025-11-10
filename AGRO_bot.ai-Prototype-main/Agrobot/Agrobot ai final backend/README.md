
# KisanAI Mongo Backend (Clean + Straightforward)

## What you get
- FastAPI + MongoDB (Motor)
- Simple JWT auth (register, login, /me)
- Weather (OpenWeather), Soil (SoilGrids), FAOSTAT production
- Simple irrigation recommendation endpoint
- Docker Compose for one-command startup

## Quick start
1. Copy `.env.example` → `.env` and set values.
2. Start: `docker compose up --build -d`
3. Docs: http://localhost:8000/docs
4. (Optional) Seed sample user: `make seed`

## Sample curl
Register:
```
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"name":"Vikram","email":"vikram@example.com","password":"changeme123"}'
```
Login:
```
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=vikram@example.com&password=changeme123"
```
Use token:
```
curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000/me
```
Soil:
```
curl "http://localhost:8000/soil?lat=28.6&lon=77.2"
```
Weather:
```
curl "http://localhost:8000/weather?lat=28.6&lon=77.2"
```
FAOSTAT:
```
curl "http://localhost:8000/faostat/production?country=India&crop=Wheat&year=2020"
```
Irrigation recommendation:
```
curl "http://localhost:8000/irrigation/recommendation?lat=28.6&lon=77.2&crop=wheat"
```
