"""
GREENRIDE - Vehicle Owner & Fleet Management Router
"""

from fastapi import APIRouter, HTTPException, Depends
from ..database import get_db
from ..models import VehicleCreateRequest
from .auth import get_current_user_from_token
import uuid

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])

@router.get("/my-vehicles")
def get_my_vehicles(current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT v.*,
               dva.driver_id, dva.status as assignment_status, dva.owner_share_pct, dva.driver_share_pct,
               u.name as assigned_driver_name, u.phone as assigned_driver_phone, u.rating as assigned_driver_rating,
               u.avatar as assigned_driver_avatar
        FROM vehicles v
        LEFT JOIN driver_vehicle_assignments dva ON v.id = dva.vehicle_id AND dva.status = 'active'
        LEFT JOIN users u ON dva.driver_id = u.id
        WHERE v.owner_id = ?
        ORDER BY v.status ASC
        """, (current_user["id"],))
        rows = [dict(r) for r in cursor.fetchall()]
        return rows

@router.post("/register")
def register_vehicle(req: VehicleCreateRequest, current_user: dict = Depends(get_current_user_from_token)):
    veh_id = f"veh_{uuid.uuid4().hex[:8]}"
    with get_db() as conn:
        cursor = conn.cursor()
        # Verify user has owner role
        if "owner" not in current_user.get("roles", ""):
            # Grant owner role automatically
            new_roles = current_user["roles"] + ",owner"
            cursor.execute("UPDATE users SET roles = ? WHERE id = ?", (new_roles, current_user["id"]))

        default_photos = {
            "ev_car": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=500",
            "e_auto": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=500",
            "e_scooter": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=500",
            "ev_van": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=500"
        }
        photo = default_photos.get(req.vehicle_type, default_photos["ev_car"])

        cursor.execute("""
        INSERT INTO vehicles (
            id, owner_id, title, vehicle_type, make_model, reg_number,
            seats, battery_kwh, ev_range_km, fuel_type, is_spare,
            seeking_driver, is_verified, status, revenue_share_owner,
            revenue_share_driver, locality, photo_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Electric (EV)', 1, ?, 1, 'available', ?, ?, ?, ?)
        """, (
            veh_id, current_user["id"], req.title, req.vehicle_type, req.make_model, req.reg_number,
            req.seats, req.battery_kwh, req.ev_range_km, 1 if req.seeking_driver else 0,
            req.revenue_share_owner, req.revenue_share_driver, req.locality, photo
        ))

        # Log system event
        cursor.execute("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, 'VEHICLE_LISTED', ?, ?)
        """, (f"log_{uuid.uuid4().hex[:8]}", current_user["id"], f"Listed spare vehicle {req.title} ({req.reg_number})."))

        return {
            "id": veh_id,
            "message": "Spare vehicle listed on GreenRide! Verified drivers can now discover it.",
            "title": req.title
        }

@router.post("/{vehicle_id}/toggle-seeking-driver")
def toggle_seeking_driver(vehicle_id: str, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id = ? AND owner_id = ?", (vehicle_id, current_user["id"]))
        v = cursor.fetchone()
        if not v:
            raise HTTPException(status_code=404, detail="Vehicle not found.")
        
        new_state = 0 if v["seeking_driver"] else 1
        cursor.execute("UPDATE vehicles SET seeking_driver = ? WHERE id = ?", (new_state, vehicle_id))
        return {
            "vehicle_id": vehicle_id,
            "seeking_driver": bool(new_state),
            "message": "Marketplace listing status updated."
        }

@router.get("/list")
def list_all_vehicles():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT v.*, u.name as owner_name, u.rating as owner_rating, u.avatar as owner_avatar
        FROM vehicles v
        JOIN users u ON v.owner_id = u.id
        WHERE v.status = 'available'
        """)
        return [dict(r) for r in cursor.fetchall()]

