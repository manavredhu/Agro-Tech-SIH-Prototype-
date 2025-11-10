# app/config.py
import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "kisanai")
    JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
    JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "10080"))  # 7 days
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

settings = Settings()

# Debug: Print the MONGO_URL to verify it's loaded correctly
if __name__ == "__main__":
    print(f"MONGO_URL: {settings.MONGO_URL}")
    print(f"MONGO_DB: {settings.MONGO_DB}")