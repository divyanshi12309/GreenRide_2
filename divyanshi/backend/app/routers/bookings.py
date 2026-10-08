"""
GREENRIDE - Bookings & Ride Reservations Router
"""

from fastapi import APIRouter, HTTPException, Depends
from ..database import get_db
from ..models import BookingCreateRequest, RateRideRequest
from .auth import get_current_user_from_token
import uuid

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.post("/create")
def create_booking(req: BookingCreateRequest, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rides WHERE id = ?", (req.ride_id,))
        ride = cursor.fetchone()
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found.")
        
        if ride["available_seats"] < req.seats_booked:
            raise HTTPException(status_code=400, detail="Not enough seats available on this ride.")
        
        booking_id = f"bk_{uuid.uuid4().hex[:8]}"
        total_price = ride["price_per_seat"] * req.seats_booked
        co2_saved = round((ride["co2_savings_kg"] or 2.5) * (req.seats_booked / max(ride["total_seats"], 1)), 2)

        # Insert booking
        cursor.execute("""
        INSERT INTO bookings (
            id, ride_id, passenger_id, seats_booked, total_price,
            pickup_name, dropoff_name, status, route_match_score, co2_saved_kg
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', 94, ?)
        """, (
            booking_id, req.ride_id, current_user["id"], req.seats_booked,
            total_price, req.pickup_name, req.dropoff_name, co2_saved
        ))

        # Decrement available seats in ride
        new_available = ride["available_seats"] - req.seats_booked
        cursor.execute("""
        UPDATE rides SET available_seats = ?, status = CASE WHEN status = 'scheduled' THEN 'active' ELSE status END
        WHERE id = ?
        """, (new_available, req.ride_id))

        # Log system event
        cursor.execute("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, 'SEAT_RESERVED', ?, ?)
        """, (f"log_{uuid.uuid4().hex[:8]}", current_user["id"], f"Reserved {req.seats_booked} seat(s) on ride {req.ride_id}."))

        return {
            "booking_id": booking_id,
            "status": "confirmed",
            "seats_booked": req.seats_booked,
            "total_price": total_price,
            "co2_saved_kg": co2_saved,
            "message": "Seat successfully reserved! Your ride is confirmed."
        }

@router.get("/my-bookings")
def get_my_bookings(current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT b.*, 
               r.origin_name, r.dest_name, r.departure_time, r.price_per_seat, r.status as ride_status,
               r.current_lat, r.current_lng, r.origin_lat, r.origin_lng, r.dest_lat, r.dest_lng,
               u.name as driver_name, u.phone as driver_phone, u.rating as driver_rating, u.avatar as driver_avatar,
               v.title as vehicle_title, v.vehicle_type, v.make_model, v.reg_number
        FROM bookings b
        JOIN rides r ON b.ride_id = r.id
        JOIN users u ON r.driver_id = u.id
        JOIN vehicles v ON r.vehicle_id = v.id
        WHERE b.passenger_id = ?
        ORDER BY b.booking_time DESC
        """, (current_user["id"],))
        rows = [dict(r) for r in cursor.fetchall()]
        return rows

@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: str, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE id = ? AND passenger_id = ?", (booking_id, current_user["id"]))
        booking = cursor.fetchone()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found.")
        
        cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE id = ?", (booking_id,))
        # Restore seats
        cursor.execute("UPDATE rides SET available_seats = available_seats + ? WHERE id = ?", (booking["seats_booked"], booking["ride_id"]))
        return {"message": "Booking cancelled successfully. Seats restored."}

@router.post("/rate")
def rate_ride(req: RateRideRequest, current_user: dict = Depends(get_current_user_from_token)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rides WHERE id = ?", (req.ride_id,))
        ride = cursor.fetchone()
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found.")
        
        rate_id = f"rat_{uuid.uuid4().hex[:8]}"
        cursor.execute("""
        INSERT INTO ratings (id, ride_id, from_user_id, to_user_id, score, comment)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (rate_id, req.ride_id, current_user["id"], ride["driver_id"], req.score, req.comment))

        # Recalculate average rating for driver
        cursor.execute("SELECT AVG(score) as avg_score FROM ratings WHERE to_user_id = ?", (ride["driver_id"],))
        avg_score = cursor.fetchone()["avg_score"] or 5.0
        cursor.execute("UPDATE users SET rating = ? WHERE id = ?", (round(avg_score, 2), ride["driver_id"]))

        return {"message": "Rating submitted! Thank you for supporting community mobility."}

