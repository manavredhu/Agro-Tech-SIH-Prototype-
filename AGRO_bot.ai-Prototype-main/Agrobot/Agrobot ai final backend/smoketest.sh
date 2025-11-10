
#!/bin/bash
set -e

API="http://localhost:8000"

echo "🔑 Registering user..."
curl -s -X POST "$API/auth/register" -H "Content-Type: application/json" -d '{
  "name": "Vikram",
  "email": "vikram@example.com",
  "password": "changeme123"
}' | jq . || true

echo "🔐 Logging in..."
TOKEN=$(curl -s -X POST "$API/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=vikram@example.com&password=changeme123" | jq -r .access_token)
echo "Token: ${TOKEN:0:20}..."

echo "👤 Calling /me..."
curl -s -H "Authorization: Bearer $TOKEN" "$API/me" | jq .

echo "🌦 Weather (requires OPENWEATHER_API_KEY)"
curl -s "$API/weather?lat=28.6&lon=77.2" | jq '.daily[0] | {temp, rain}' || true

echo "🌍 SoilGrids"
curl -s "$API/soil?lat=28.6&lon=77.2" | jq '.source' || true

echo "📊 FAOSTAT production (wheat, India, 2020)"
curl -s "$API/faostat/production?country=India&crop=Wheat&year=2020" | jq . || true

echo "💧 Irrigation recommendation (wheat)"
curl -s "$API/irrigation/recommendation?lat=28.6&lon=77.2&crop=wheat" | jq .
