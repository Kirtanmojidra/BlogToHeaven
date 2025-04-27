import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def encode(data):
    try:
        secret = os.getenv("JWT_SECRET")
        if not secret:
            raise ValueError("JWT_SECRET not found in environment variables")
        return jwt.encode(data, secret.encode('utf-8'), algorithm="HS256")
    except Exception as e:
        print(f"JWT Encoding Error: {e}")
        return None

def decode(token):
    try:
        if not token:
            return None
        secret = os.getenv("JWT_SECRET")
        if not secret:
            raise ValueError("JWT_SECRET not found in environment variables")
        return jwt.decode(token, secret.encode('utf-8'), algorithms=["HS256"])
    except Exception as e:
        print(f"JWT Decoding Error: {e}")
        return None