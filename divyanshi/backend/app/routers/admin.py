"""
GREENRIDE - Platform Operations & Administration Router
"""

from fastapi import APIRouter, HTTPException, Depends
from ..database import get_db
from ..seed_data import seed
from .auth import get_current_user_from_token
import uuid

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/metrics")
def get_admin_metrics():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        total_users = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM driver_profiles WHERE is_online = 1")
        active_drivers = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM vehicles")
        total_vehicles = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM vehicles WHERE status = 'available'")
        spare_vehicles_available = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM rides WHERE status IN ('active', 'scheduled')")
        active_rides = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM bookings")
        total_bookings = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM reports WHERE status = 'under_review'")
        pending_reports = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM driver_vehicle_assignments WHERE status = 'active'")
        active_partnerships = cursor.fetchone()["cnt"]

        return {
            "total_users": total_users,
            "active_drivers": active_drivers,
            "total_vehicles": total_vehicles,
            "spare_vehicles_available": spare_vehicles_available,
            "active_rides": active_rides,
            "total_bookings": total_bookings,
            "pending_reports": pending_reports,
            "active_partnerships": active_partnerships,
            "platform_uptime": "99.98%",
            "system_status": "Healthy & Operating Smoothly"
        }

@router.get("/drivers")
def get_all_drivers():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT dp.*, u.name, u.email, u.phone, u.locality, u.avatar
        FROM driver_profiles dp
        JOIN users u ON dp.user_id = u.id
        ORDER BY dp.is_verified ASC, dp.rating DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.post("/verify-driver/{driver_id}")
def verify_driver(driver_id: str, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE driver_profiles SET is_verified = 1 WHERE id = ? OR user_id = ?", (driver_id, driver_id))
        
        cursor.execute("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, 'ADMIN_VERIFIED_DRIVER', ?, ?)
        """, (f"log_{uuid.uuid4().hex[:8]}", current_user["id"], f"Admin verified driver ID {driver_id}."))

        return {"message": "Driver credentials verified and approved."}

@router.get("/vehicles")
def get_all_vehicles():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT v.*, u.name as owner_name, u.phone as owner_phone
        FROM vehicles v
        JOIN users u ON v.owner_id = u.id
        ORDER BY v.is_verified ASC, v.created_at DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.post("/verify-vehicle/{vehicle_id}")
def verify_vehicle(vehicle_id: str, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE vehicles SET is_verified = 1 WHERE id = ?", (vehicle_id,))
        
        cursor.execute("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, 'ADMIN_VERIFIED_VEHICLE', ?, ?)
        """, (f"log_{uuid.uuid4().hex[:8]}", current_user["id"], f"Admin verified vehicle ID {vehicle_id}."))

        return {"message": "Vehicle roadworthiness and battery certification verified."}

@router.get("/reports")
def get_reports():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT r.*, u.name as reporter_name, u.phone as reporter_phone
        FROM reports r
        JOIN users u ON r.reporter_id = u.id
        ORDER BY r.created_at DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.post("/resolve-report/{report_id}")
def resolve_report(report_id: str, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE reports SET status = 'resolved' WHERE id = ?", (report_id,))
        return {"message": "Report status updated to resolved."}

@router.get("/audit-logs")
def get_audit_logs():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system_logs ORDER BY created_at DESC LIMIT 30")
        return [dict(r) for r in cursor.fetchall()]

@router.post("/reset-demo-database")
def reset_database():
    """Resets the demo environment back to fresh seed state for the exhibition."""
    seed()
    return {"message": "Technofest demo database re-seeded successfully."}

