
# seed.py
import asyncio
from app.db import connect, get_database, disconnect
from app.auth import get_password_hash  # Import directly from app.auth

async def run():
    await connect()
    db = get_database()
    
    if await db.users.find_one({"email": "demo@kisan.ai"}):
        print("Demo user already exists.")
    else:
        await db.users.insert_one({
            "name": "Demo Farmer",
            "username": "demo",
            "email": "demo@kisan.ai",
            "hashed_password": get_password_hash("changeme123")
        })
        print("Created demo user: demo / changeme123")
    await disconnect()

if __name__ == "__main__":
    asyncio.run(run())