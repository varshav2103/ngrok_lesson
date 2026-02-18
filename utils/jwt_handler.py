import os
import time
from typing import Dict
import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def token_response(token: str, refresh_token: str):
    return {
        "access_token": token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

def sign_jwt(user_id: int, email: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "email": email,
        "expires": time.time() + 600
    }
    
    refresh_payload = {
        "user_id": user_id,
        "email": email,
        "expires": time.time() + 30000000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token, refresh_token)

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def create_tokens(user_id: int, email: str): # Alias for sign_jwt to match user_routes usage
    return sign_jwt(user_id, email)

def verify_token(token: str): # Alias for decode_jwt
    return decode_jwt(token)
