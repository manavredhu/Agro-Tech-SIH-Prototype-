# app/db.py
import motor.motor_asyncio
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create a MongoDB client using the connection string from .env
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)

# Pick the database name (from .env)
database = client[settings.MONGO_DB]

# Function to return the database instance
def get_database():
    return database

# Connect function that other parts of your app are trying to import
async def connect():
    """Connect to MongoDB and test the connection"""
    try:
        # Test the connection
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e

# Optional: disconnect function
async def disconnect():
    """Close the database connection"""
    client.close()
    logger.info("MongoDB connection closed")