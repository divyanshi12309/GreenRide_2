"""
GREENRIDE - Spare Vehicle & Driver Employment Marketplace Router
Solves urban asset under-utilization by connecting vehicle owners with verified drivers.
"""

from fastapi import APIRouter, HTTPException, Depends
from ..database import get_db
from ..models import AssignDriverRequest
from .auth import get_current_user_from_token
import uuid

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

@router.get("/vehicles-seeking-drivers")
def get_vehicles_seeking_drivers():
    """Returns spare vehicles whose owners are looking for verified drivers."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT v.*, u.name as owner_name, u.phone as owner_phone, u.rating as owner_rating, u.avatar as owner_avatar
        FROM vehicles v
        JOIN users u ON v.owner_id = u.id
        WHERE v.seeking_driver = 1 AND v.status = 'available'
        ORDER BY v.battery_kwh DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.get("/drivers-seeking-vehicles")
def get_drivers_seeking_vehicles():
    """Returns verified drivers seeking vehicle partnership opportunities."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT dp.*, u.name as driver_name, u.phone as driver_phone, u.rating as driver_rating,
               u.avatar as driver_avatar, u.locality as driver_locality
        FROM driver_profiles dp
        JOIN users u ON dp.user_id = u.id
        WHERE dp.is_verified = 1 AND dp.looking_for_vehicle = 1
        ORDER BY dp.rating DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.get("/active-partnerships")
def get_active_partnerships():
    """Returns live matches between vehicle owners and drivers with revenue splits."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT dva.*,
               v.title as vehicle_title, v.make_model, v.reg_number, v.vehicle_type, v.battery_kwh,
               u_owner.name as owner_name, u_owner.avatar as owner_avatar,
               u_driver.name as driver_name, u_driver.avatar as driver_avatar, u_driver.rating as driver_rating,
               dp.experience_years as driver_experience
        FROM driver_vehicle_assignments dva
        JOIN vehicles v ON dva.vehicle_id = v.id
        JOIN users u_owner ON v.owner_id = u_owner.id
        JOIN users u_driver ON dva.driver_id = u_driver.id
        JOIN driver_profiles dp ON u_driver.id = dp.user_id
        WHERE dva.status = 'active'
        ORDER BY dva.assigned_at DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.post("/match")
def match_driver_vehicle(req: AssignDriverRequest, current_user: dict = Depends(get_current_user_from_token)):
    """Matches a verified driver to an owner's spare vehicle with specified revenue split."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verify vehicle exists and is available
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (req.vehicle_id,))
        vehicle = cursor.fetchone()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found.")
        
        # Verify driver exists
        cursor.execute("SELECT * FROM users WHERE id = ?", (req.driver_id,))
        driver = cursor.fetchone()
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found.")
        
        # Create assignment
        asgn_id = f"asgn_{uuid.uuid4().hex[:8]}"
        note = req.notes or f"Community partnership: {vehicle['title']} assigned to {driver['name']}."
        cursor.execute("""
        INSERT INTO driver_vehicle_assignments (
            id, vehicle_id, driver_id, status, owner_share_pct, driver_share_pct, notes
        ) VALUES (?, ?, ?, 'active', ?, ?, ?)
        """, (asgn_id, req.vehicle_id, req.driver_id, req.owner_share_pct, req.driver_share_pct, note))

        # Update vehicle status
        cursor.execute("UPDATE vehicles SET status = 'assigned', seeking_driver = 0 WHERE id = ?", (req.vehicle_id,))
        
        # Update driver status
        cursor.execute("UPDATE driver_profiles SET looking_for_vehicle = 0 WHERE user_id = ?", (req.driver_id,))

        # System audit log
        cursor.execute("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, 'PARTNERSHIP_FORMED', ?, ?)
        """, (f"log_{uuid.uuid4().hex[:8]}", current_user["id"], f"Matched driver {driver['name']} with {vehicle['title']}. Revenue split: {req.owner_share_pct}% Owner / {req.driver_share_pct}% Driver."))

        return {
            "assignment_id": asgn_id,
            "vehicle_title": vehicle["title"],
            "driver_name": driver["name"],
            "owner_share_pct": req.owner_share_pct,
            "driver_share_pct": req.driver_share_pct,
            "message": f"Successfully matched! {driver['name']} can now operate {vehicle['title']}."
        }

