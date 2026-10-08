"""
GREENRIDE - Pydantic Request & Response Data Models
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str = "passenger" # passenger, driver, owner, admin
    locality: str = "Lanka, Varanasi"

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    roles: str
    active_role: str
    rating: float
    locality: str
    avatar: str

class RoleSwitchRequest(BaseModel):
    role: str

class RideSearchRequest(BaseModel):
    origin: str
    destination: str
    date: Optional[str] = "Today"
    time: Optional[str] = "Now"
    seats: int = 1
    vehicle_type: Optional[str] = "all"

class RideCreateRequest(BaseModel):
    origin_name: str
    origin_lat: float
    origin_lng: float
    dest_name: str
    dest_lat: float
    dest_lng: float
    departure_time: str
    total_seats: int
    price_per_seat: float
    vehicle_id: str
    ride_type: str = "shared_ev"

class BookingCreateRequest(BaseModel):
    ride_id: str
    seats_booked: int = 1
    pickup_name: str
    dropoff_name: str

class RateRideRequest(BaseModel):
    ride_id: str
    score: float = Field(..., ge=1.0, le=5.0)
    comment: str = ""

class ReportCreateRequest(BaseModel):
    target_type: str # driver, vehicle, ride, general
    target_id: str
    category: str
    description: str

class VehicleCreateRequest(BaseModel):
    title: str
    vehicle_type: str # ev_car, e_auto, e_scooter, ev_van
    make_model: str
    reg_number: str
    seats: int = 4
    battery_kwh: float = 30.0
    ev_range_km: int = 250
    seeking_driver: bool = True
    revenue_share_owner: float = 70.0
    revenue_share_driver: float = 30.0
    locality: str = "Lanka, Varanasi"

class AssignDriverRequest(BaseModel):
    vehicle_id: str
    driver_id: str
    owner_share_pct: float = 70.0
    driver_share_pct: float = 30.0
    notes: Optional[str] = ""

class DriverStatusUpdate(BaseModel):
    is_online: bool

