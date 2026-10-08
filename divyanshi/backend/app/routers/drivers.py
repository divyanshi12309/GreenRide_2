"""
GREENRIDE - Driver Operations & Employment Dashboard Router
"""

from fastapi import APIRouter, HTTPException, Depends
from ..database import get_db
from ..models import DriverStatusUpdate
from .auth import get_current_user_from_token
import uuid

router = APIRouter(prefix="/api/drivers", tags=["drivers"])

@router.get("/profile")
def get_driver_profile(current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT dp.*, u.name, u.email, u.phone, u.avatar, u.locality, u.rating as user_rating
        FROM driver_profiles dp
        JOIN users u ON dp.user_id = u.id
        WHERE dp.user_id = ?
        """, (current_user["id"],))
        profile = cursor.fetchone()
        
        # If no profile exists, create a default driver profile for demo convenience
        if not profile:
            prof_id = f"drv_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
            INSERT INTO driver_profiles (id, user_id, license_number, experience_years, preferred_area, languages, vehicle_category, is_verified, is_online, rating, trips_completed, looking_for_vehicle)
            VALUES (?, ?, 'UP-65-2024-DEMO', 3, 'Varanasi Central / Lanka / BHU', 'Hindi, English', 'EV Car, E-Auto', 1, 1, 4.9, 45, 1)
            """, (prof_id, current_user["id"]))
            cursor.execute("""
            SELECT dp.*, u.name, u.email, u.phone, u.avatar, u.locality, u.rating as user_rating
            FROM driver_profiles dp
            JOIN users u ON dp.user_id = u.id
            WHERE dp.user_id = ?
            """, (current_user["id"],))
            profile = cursor.fetchone()

        prof_dict = dict(profile)

        # Check assigned vehicle
        cursor.execute("""
        SELECT v.*, dva.owner_share_pct, dva.driver_share_pct, u.name as owner_name, u.phone as owner_phone
        FROM driver_vehicle_assignments dva
        JOIN vehicles v ON dva.vehicle_id = v.id
        JOIN users u ON v.owner_id = u.id
        WHERE dva.driver_id = ? AND dva.status = 'active'
        """, (current_user["id"],))
        assigned_veh = cursor.fetchone()
        prof_dict["assigned_vehicle"] = dict(assigned_veh) if assigned_veh else None

        return prof_dict

@router.post("/toggle-status")
def toggle_status(payload: DriverStatusUpdate, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE driver_profiles SET is_online = ? WHERE user_id = ?", (1 if payload.is_online else 0, current_user["id"]))
        return {"is_online": payload.is_online, "message": "Driver status updated."}

@router.get("/earnings")
def get_driver_earnings(current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        # Find trips completed
        cursor.execute("""
        SELECT r.id, r.origin_name, r.dest_name, r.price_per_seat, r.status, r.departure_time,
               COUNT(b.id) as passenger_count, SUM(b.total_price) as gross_fare
        FROM rides r
        LEFT JOIN bookings b ON r.id = b.ride_id AND b.status IN ('confirmed', 'active', 'completed')
        WHERE r.driver_id = ?
        GROUP BY r.id
        ORDER BY r.created_at DESC
        """, (current_user["id"],))
        rides = [dict(r) for r in cursor.fetchall()]

        # Compute calculated mock earnings for demo presentation
        total_trips = len(rides) + 140
        gross_earnings = 34500.0 # INR
        driver_payout = 24150.0  # 70% direct income after partner split
        today_earnings = 1240.0
        green_rewards = 850.0 # Technofest sustainability incentive points

        return {
            "driver_name": current_user["name"],
            "total_trips": total_trips,
            "gross_earnings_inr": gross_earnings,
            "net_driver_earnings_inr": driver_payout,
            "today_earnings_inr": today_earnings,
            "green_mobility_bonus_inr": green_rewards,
            "recent_trips": rides[:5]
        }

@router.get("/assigned-rides")
def get_driver_rides(current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT r.*, v.title as vehicle_title, v.make_model, v.reg_number
        FROM rides r
        JOIN vehicles v ON r.vehicle_id = v.id
        WHERE r.driver_id = ?
        ORDER BY r.departure_time ASC
        """, (current_user["id"],))
        return [dict(r) for r in cursor.fetchall()]

