# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.db import get_database
from app import auth  # Import the main auth module

router = APIRouter(prefix="/auth", tags=["auth"])

# Request models (without EmailStr)
class RegisterRequest(BaseModel):
    name: str
    email: str  # Regular string instead of EmailStr
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Simple email validation function
def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[1]

@router.post("/register")
async def register(data: RegisterRequest, db=Depends(get_database)):
    # Basic email validation
    if not is_valid_email(data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check if user exists
    existing = await db["users"].find_one({"username": data.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    existing_email = await db["users"].find_one({"email": data.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = auth.get_password_hash(data.password)

    # Create user document
    user_doc = {
        "name": data.name,
        "email": data.email,
        "username": data.username,
        "hashed_password": hashed_pw,
    }
    result = await db["users"].insert_one(user_doc)

    return {"msg": "User registered successfully", "user_id": str(result.inserted_id)}

@router.post("/login")
async def login(data: LoginRequest, db=Depends(get_database)):
    user = await db["users"].find_one({"username": data.username})
    if not user or not auth.verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = auth.create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(current_user=Depends(auth.get_current_user)):
    return {"msg": f"Hello {current_user['username']}, you accessed a protected route!"}