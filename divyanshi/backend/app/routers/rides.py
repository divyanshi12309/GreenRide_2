"""
GREENRIDE - Rides and Route Matching Router
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from ..database import get_db
from ..models import RideSearchRequest, RideCreateRequest
from ..matching import resolve_coords, calculate_route_overlap, haversine_distance, calculate_co2_savings
from .auth import get_current_user_from_token
from typing import Optional
import uuid

router = APIRouter(prefix="/api/rides", tags=["rides"])

@router.get("/list")
def list_rides(status: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
        SELECT r.*, 
               u.name as driver_name, u.rating as driver_rating, u.avatar as driver_avatar,
               v.title as vehicle_title, v.vehicle_type, v.make_model, v.reg_number, v.battery_kwh, v.ev_range_km,
               v.fuel_type, v.photo_url as vehicle_photo
        FROM rides r
        JOIN users u ON r.driver_id = u.id
        JOIN vehicles v ON r.vehicle_id = v.id
        """
        params = []
        if status:
            query += " WHERE r.status = ?"
            params.append(status)
        else:
            query += " WHERE r.status IN ('active', 'scheduled')"
            
        query += " ORDER BY r.departure_time ASC"
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        return rows

@router.post("/search")
def search_rides(req: RideSearchRequest):
    u_orig_lat, u_orig_lng = resolve_coords(req.origin, fallback_lat=25.2800, fallback_lng=82.9995)
    u_dest_lat, u_dest_lng = resolve_coords(req.destination, fallback_lat=25.3280, fallback_lng=82.9860)

    user_trip_dist = haversine_distance(u_orig_lat, u_orig_lng, u_dest_lat, u_dest_lng)

    with get_db() as conn:
        cursor = conn.cursor()
        query = """
        SELECT r.*, 
               u.name as driver_name, u.rating as driver_rating, u.avatar as driver_avatar,
               dp.is_verified as driver_verified, dp.experience_years as driver_experience,
               v.title as vehicle_title, v.vehicle_type, v.make_model, v.reg_number, v.battery_kwh, v.ev_range_km,
               v.fuel_type, v.photo_url as vehicle_photo
        FROM rides r
        JOIN users u ON r.driver_id = u.id
        LEFT JOIN driver_profiles dp ON u.id = dp.user_id
        JOIN vehicles v ON r.vehicle_id = v.id
        WHERE r.status IN ('scheduled', 'active')
          AND r.available_seats >= ?
        """
        params = [req.seats]
        if req.vehicle_type and req.vehicle_type != "all":
            query += " AND v.vehicle_type = ?"
            params.append(req.vehicle_type)

        cursor.execute(query, params)
        all_rides = [dict(row) for row in cursor.fetchall()]

    results = []
    for ride in all_rides:
        overlap_score = calculate_route_overlap(
            u_orig_lat, u_orig_lng,
            u_dest_lat, u_dest_lng,
            ride["origin_lat"], ride["origin_lng"],
            ride["dest_lat"], ride["dest_lng"]
        )

        co2_saved = calculate_co2_savings(max(user_trip_dist, 3.2), ride["vehicle_type"], req.seats)
        
        # Vehicle badge labeling for Technofest clarity
        badge_info = {
            "ev_car": {"label": "⚡ EV CARPOOL", "color": "emerald", "desc": "Low-Impact Shared Journey"},
            "e_auto": {"label": "⚡ E-AUTO POOL", "color": "amber", "desc": "Clean Last-Mile Mobility"},
            "e_scooter": {"label": "⚡ E-SCOOTER RIDE", "color": "cyan", "desc": "Solo Micro-Mobility"},
            "ev_van": {"label": "⚡ EV SHUTTLE", "color": "blue", "desc": "High-Capacity Shared Transit"}
        }.get(ride["vehicle_type"], {"label": "🌱 SHARED RIDE", "color": "emerald", "desc": "Sustainable Commute"})

        # Solo cab price comparison for visual savings
        estimated_solo_cab_price = round(max(user_trip_dist * 22.0 + 50.0, 120.0))
        shared_price = round(ride["price_per_seat"] * req.seats)
        money_saved = max(estimated_solo_cab_price - shared_price, 30)

        results.append({
            **ride,
            "route_match_score": overlap_score,
            "match_reason": f"Your route overlaps with this ride by {overlap_score}%.",
            "co2_saved_kg": co2_saved,
            "distance_km": round(user_trip_dist, 1),
            "estimated_solo_cab_price": estimated_solo_cab_price,
            "money_saved_inr": money_saved,
            "badge": badge_info,
            "user_coords": {
                "origin": [u_orig_lat, u_orig_lng],
                "destination": [u_dest_lat, u_dest_lng]
            }
        })

    # Sort primarily by route match score descending
    results.sort(key=lambda x: x["route_match_score"], reverse=True)
    return {
        "searched_origin": req.origin,
        "searched_destination": req.destination,
        "distance_km": round(user_trip_dist, 1),
        "results_count": len(results),
        "rides": results
    }

@router.get("/{ride_id}")
def get_ride_details(ride_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT r.*, 
               u.name as driver_name, u.rating as driver_rating, u.avatar as driver_avatar, u.phone as driver_phone,
               dp.is_verified as driver_verified, dp.experience_years as driver_experience,
               v.title as vehicle_title, v.vehicle_type, v.make_model, v.reg_number, v.battery_kwh, v.ev_range_km,
               v.fuel_type, v.photo_url as vehicle_photo
        FROM rides r
        JOIN users u ON r.driver_id = u.id
        LEFT JOIN driver_profiles dp ON u.id = dp.user_id
        JOIN vehicles v ON r.vehicle_id = v.id
        WHERE r.id = ?
        """, (ride_id,))
        ride = cursor.fetchone()
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        ride_dict = dict(ride)
        # Fetch current passengers booked on this ride
        cursor.execute("""
        SELECT b.id, b.passenger_id, b.seats_booked, b.pickup_name, b.dropoff_name, b.status,
               u.name as passenger_name, u.avatar as passenger_avatar
        FROM bookings b
        JOIN users u ON b.passenger_id = u.id
        WHERE b.ride_id = ? AND b.status IN ('confirmed', 'active')
        """, (ride_id,))
        ride_dict["passengers"] = [dict(p) for p in cursor.fetchall()]
        return ride_dict

@router.post("/create")
def create_ride(req: RideCreateRequest, current_user: dict = Depends(get_current_user_from_token)):
    ride_id = f"ride_{uuid.uuid4().hex[:8]}"
    dist = haversine_distance(req.origin_lat, req.origin_lng, req.dest_lat, req.dest_lng)
    co2 = calculate_co2_savings(dist, req.ride_type, req.total_seats)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO rides (
            id, driver_id, vehicle_id, origin_name, origin_lat, origin_lng,
            dest_name, dest_lat, dest_lng, departure_time, total_seats,
            available_seats, price_per_seat, ride_type, status, co2_savings_kg,
            current_lat, current_lng
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'scheduled', ?, ?, ?)
        """, (
            ride_id, current_user["id"], req.vehicle_id, req.origin_name, req.origin_lat, req.origin_lng,
            req.dest_name, req.dest_lat, req.dest_lng, req.departure_time, req.total_seats,
            req.total_seats, req.price_per_seat, req.ride_type, co2,
            req.origin_lat, req.origin_lng
        ))
        return {"id": ride_id, "message": "Shared ride published successfully!"}

@router.post("/{ride_id}/simulate-step")
def simulate_step(ride_id: str):
    """Advances vehicle position towards destination for live tracking simulation."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rides WHERE id = ?", (ride_id,))
        ride = cursor.fetchone()
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        c_lat = ride["current_lat"] or ride["origin_lat"]
        c_lng = ride["current_lng"] or ride["origin_lng"]
        d_lat = ride["dest_lat"]
        d_lng = ride["dest_lng"]

        # Step 20% closer to destination
        new_lat = c_lat + (d_lat - c_lat) * 0.20
        new_lng = c_lng + (d_lng - c_lng) * 0.20

        # If very close, snap to destination
        remaining_dist = haversine_distance(new_lat, new_lng, d_lat, d_lng)
        status = ride["status"]
        if remaining_dist < 0.2:
            new_lat = d_lat
            new_lng = d_lng
            status = "completed"
        else:
            status = "active"

        cursor.execute("""
        UPDATE rides 
        SET current_lat = ?, current_lng = ?, status = ?
        WHERE id = ?
        """, (new_lat, new_lng, status, ride_id))

        return {
            "ride_id": ride_id,
            "current_lat": new_lat,
            "current_lng": new_lng,
            "remaining_dist_km": round(remaining_dist, 2),
            "status": status
        }

