import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def encode(data):
    try:
        return jwt.encode(data, os.getenv("JWT_SECRET"), algorithm="HS256")
    except Exception as e:
        print(e)

def decode(token):
    try:
        return jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except Exception as e:
        print(e)