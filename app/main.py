from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
import os
import jwt   

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

@app.get("/")
def read_root():
    return { "msg": "Namaste!", "v": "0.1" }

@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": item_id, "q": q}

@app.get("/secret")
def read_secret(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid")
    return {"secret": "Let's wish for the peace"}

MESSAGES = [
    { "id": 1, "user_id": 1, "text": "Welcome to the platform!" },
    { "id": 2, "user_id": 2, "text": "Your report is ready for download." },
    { "id": 3, "user_id": 1, "text": "You have a new notification." },
    { "id": 4, "user_id": 3, "text": "Password will expire in 5 days." },
    { "id": 5, "user_id": 2, "text": "New login detected from a new device." },
    { "id": 6, "user_id": 3, "text": "Your subscription has been updated." }
]

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/messages")
def get_messages(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ")[1]
    payload = verify_jwt(token)

    user_id = payload.get("sub")
    role = payload.get("role")

    if role == "admin":
        return MESSAGES

    return [m for m in MESSAGES if m["user_id"] == user_id]
