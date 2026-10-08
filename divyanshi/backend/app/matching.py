"""
GREENRIDE - Carpool Matching Engine
Calculates route overlap, bearing alignment, distance, and CO2 emissions saved.
"""

import math
from typing import Dict, Any, Tuple

# Pre-defined known coordinates in Varanasi for instant high-accuracy matching
KNOWN_LOCALITIES: Dict[str, Tuple[float, float]] = {
    "lanka": (25.2800, 82.9995),
    "bhu": (25.2720, 82.9975),
    "bhu gate": (25.2750, 82.9985),
    "assi": (25.2925, 83.0065),
    "assi ghat": (25.2925, 83.0065),
    "godowlia": (25.3110, 83.0070),
    "dashashwamedh": (25.3075, 83.0100),
    "kashi": (25.3109, 83.0107),
    "cantt": (25.3280, 82.9860),
    "varanasi cantt": (25.3280, 82.9860),
    "cantt railway station": (25.3280, 82.9860),
    "sarnath": (25.3811, 83.0214),
    "ravindrapuri": (25.2890, 83.0020),
    "sigra": (25.3160, 82.9890),
    "dlw": (25.2880, 82.9680),
    "durgakund": (25.2860, 83.0005)
}

def resolve_coords(location_name: str, fallback_lat: float = 25.2800, fallback_lng: float = 82.9995) -> Tuple[float, float]:
    """Resolves coordinates for a known locality or returns provided fallbacks."""
    key = location_name.lower().strip()
    for name, coords in KNOWN_LOCALITIES.items():
        if name in key or key in name:
            return coords
    return fallback_lat, fallback_lng

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two points in kilometers."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_route_overlap(
    user_orig_lat: float, user_orig_lng: float,
    user_dest_lat: float, user_dest_lng: float,
    ride_orig_lat: float, ride_orig_lng: float,
    ride_dest_lat: float, ride_dest_lng: float
) -> int:
    """
    Computes a percentage match (e.g. 75% - 98%) based on origin proximity,
    destination proximity, and corridor vector alignment.
    """
    # Distance between user origin and ride origin
    orig_dist = haversine_distance(user_orig_lat, user_orig_lng, ride_orig_lat, ride_orig_lng)
    # Distance between user destination and ride destination
    dest_dist = haversine_distance(user_dest_lat, user_dest_lng, ride_dest_lat, ride_dest_lng)
    
    # Total ride span
    ride_total_dist = max(haversine_distance(ride_orig_lat, ride_orig_lng, ride_dest_lat, ride_dest_lng), 1.0)
    user_total_dist = max(haversine_distance(user_orig_lat, user_orig_lng, user_dest_lat, user_dest_lng), 1.0)

    # Detour penalty
    penalty = (orig_dist + dest_dist) / (ride_total_dist + user_total_dist)
    
    # Vector directional alignment (cosine similarity of movement vectors)
    u_dx = user_dest_lat - user_orig_lat
    u_dy = user_dest_lng - user_orig_lng
    r_dx = ride_dest_lat - ride_orig_lat
    r_dy = ride_dest_lng - ride_orig_lng
    
    dot = (u_dx * r_dx) + (u_dy * r_dy)
    mag_u = math.sqrt(u_dx**2 + u_dy**2) or 0.001
    mag_r = math.sqrt(r_dx**2 + r_dy**2) or 0.001
    cos_sim = max(0.0, dot / (mag_u * mag_r)) # 1.0 if same direction, 0.0 if opposite

    # Compute raw match score
    base_score = 60.0 + (cos_sim * 30.0) - (min(penalty, 1.5) * 15.0)
    score = int(max(65, min(98, round(base_score))))
    return score

def calculate_co2_savings(distance_km: float, vehicle_type: str = "ev_car", seats_shared: int = 1) -> float:
    """
    Computes kilograms of CO2 avoided.
    Conventional internal combustion engine (ICE) car emits ~192g CO2/km (0.192 kg).
    By carpooling in an EV, each shared passenger avoids an entire separate ICE vehicle trip.
    """
    ice_emission_factor = 0.192 # kg CO2 per km
    # EV operational emissions from renewable/grid avg is ~0.04kg/km vs 0.192kg ICE
    net_savings_per_km = 0.165
    total_saved = distance_km * net_savings_per_km * seats_shared
    return round(max(0.5, total_saved), 2)
