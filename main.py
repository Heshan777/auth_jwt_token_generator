import os
import datetime
import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_HOURS = int(os.getenv("TOKEN_EXPIRE_HOURS", 24))

app = FastAPI(title="SLT JWT Auth Service")

# Request Model
class TokenRequest(BaseModel):
    user_id: str
    role: str = "agent" # Optional: add roles like 'admin' or 'supervisor'

# Response Model
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_hours: int

@app.post("/generate-token", response_model=TokenResponse)
async def generate_token(request: TokenRequest):
    try:
        # Define the token payload
        payload = {
            "sub": request.user_id,
            "role": request.role,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=EXPIRE_HOURS)
        }

        # Sign the token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in_hours": EXPIRE_HOURS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token generation failed: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "Auth service is running successfully."}