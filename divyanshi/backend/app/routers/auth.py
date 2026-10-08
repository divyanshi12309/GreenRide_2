"""
GREENRIDE - Authentication & Role Switching Router
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from ..database import get_db
from ..models import UserLogin, UserRegister, RoleSwitchRequest
import hashlib
import uuid
import jwt
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])
SECRET_KEY = "greenride-technofest-secret-key-varanasi-2026"

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def create_token(user_id: str, email: str, role: str) -> str:
    payload = {"sub": user_id, "email": email, "role": role}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_current_user_from_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        # Default fallback to Demo Passenger for seamless Technofest exploration
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = 'passenger@greenride.org'")
            user = cursor.fetchone()
            if user:
                return dict(user)
        return None
    try:
        token = authorization.replace("Bearer ", "")
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (data["sub"],))
            user = cursor.fetchone()
            if user:
                return dict(user)
    except Exception:
        pass
    
    # Fallback to demo passenger if token invalid
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = 'passenger@greenride.org'")
        user = cursor.fetchone()
        return dict(user) if user else None

@router.post("/login")
def login(payload: UserLogin):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (payload.email,))
        user = cursor.fetchone()
        if not user or user["password_hash"] != hash_pw(payload.password):
            raise HTTPException(status_code=401, detail="Invalid credentials. Use demo accounts or sign up.")
        
        user_dict = dict(user)
        del user_dict["password_hash"]
        token = create_token(user_dict["id"], user_dict["email"], user_dict["active_role"])
        return {"token": token, "user": user_dict}

@router.post("/signup")
def signup(payload: UserRegister):
    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (payload.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="User with this email already exists.")
        
        cursor.execute("""
        INSERT INTO users (id, name, email, phone, password_hash, roles, active_role, rating, locality)
        VALUES (?, ?, ?, ?, ?, ?, ?, 5.0, ?)
        """, (user_id, payload.name, payload.email, payload.phone, hash_pw(payload.password), payload.role, payload.role, payload.locality))
        
        if payload.role == "driver":
            prof_id = f"drv_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
            INSERT INTO driver_profiles (id, user_id, license_number, experience_years, preferred_area, languages, vehicle_category, is_verified, is_online, rating, trips_completed, looking_for_vehicle)
            VALUES (?, ?, ?, 2, ?, 'Hindi, English', 'EV Car', 1, 1, 5.0, 0, 1)
            """, (prof_id, user_id, f"UP-65-{uuid.uuid4().hex[:6].upper()}", payload.locality))

        token = create_token(user_id, payload.email, payload.role)
        return {
            "token": token,
            "user": {
                "id": user_id,
                "name": payload.name,
                "email": payload.email,
                "phone": payload.phone,
                "roles": payload.role,
                "active_role": payload.role,
                "rating": 5.0,
                "locality": payload.locality
            }
        }

@router.get("/demo-switch/{role}")
def demo_switch(role: str):
    """Instant Technofest 1-click role switcher between demo users."""
    role_email_map = {
        "passenger": "passenger@greenride.org",
        "driver": "driver@greenride.org",
        "owner": "owner@greenride.org",
        "admin": "admin@greenride.org"
    }
    email = role_email_map.get(role.lower(), "passenger@greenride.org")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Demo account not found.")
        user_dict = dict(user)
        del user_dict["password_hash"]
        token = create_token(user_dict["id"], user_dict["email"], user_dict["active_role"])
        return {
            "token": token,
            "user": user_dict,
            "role_title": {
                "passenger": "Ananya Sharma (Passenger - Daily Commuter)",
                "driver": "Rahul Kumar (EV Driver & Community Partner)",
                "owner": "Vikram Singh (Spare Vehicle Owner & Host)",
                "admin": "Pooja Verma (GreenRide Operations Admin)"
            }.get(role.lower(), role)
        }

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user_from_token)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    u = dict(current_user)
    if "password_hash" in u:
        del u["password_hash"]
    return u

@router.post("/switch-active-role")
def switch_active_role(payload: RoleSwitchRequest, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET active_role = ? WHERE id = ?", (payload.role, current_user["id"]))
        cursor.execute("SELECT * FROM users WHERE id = ?", (current_user["id"],))
        user = dict(cursor.fetchone())
        del user["password_hash"]
        token = create_token(user["id"], user["email"], user["active_role"])
        return {"token": token, "user": user}

