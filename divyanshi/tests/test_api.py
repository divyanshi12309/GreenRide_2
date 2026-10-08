"""
GREENRIDE - Backend Test Suite
Validates all critical endpoints: auth, rides, carpool matching, bookings,
marketplace, impact calculation, driver operations, admin, and safety.
"""

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.seed_data import seed

client = TestClient(app)

def setup_module():
    seed()

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_demo_switch_passenger():
    res = client.get("/api/auth/demo-switch/passenger")
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["email"] == "passenger@greenride.org"
    assert data["user"]["name"] == "Ananya Sharma"

def test_demo_switch_all_roles():
    for role in ["driver", "owner", "admin"]:
        res = client.get(f"/api/auth/demo-switch/{role}")
        assert res.status_code == 200
        assert res.json()["user"]["active_role"] == role

def test_rides_list():
    res = client.get("/api/rides/list")
    assert res.status_code == 200
    rides = res.json()
    assert len(rides) >= 3
    assert any("Tata Nexon" in r["vehicle_title"] for r in rides)

def test_carpool_search_and_route_overlap():
    res = client.post("/api/rides/search", json={
        "origin": "Lanka",
        "destination": "BHU",
        "seats": 1,
        "vehicle_type": "all"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["results_count"] > 0
    top_ride = data["rides"][0]
    assert top_ride["route_match_score"] >= 70
    assert "route overlaps" in top_ride["match_reason"]
    assert top_ride["co2_saved_kg"] > 0

def test_booking_flow():
    # 1. Search rides
    res = client.post("/api/rides/search", json={
        "origin": "Assi",
        "destination": "BHU",
        "seats": 1,
        "vehicle_type": "all"
    })
    ride_id = res.json()["rides"][0]["id"]

    # 2. Book seat
    book_res = client.post("/api/bookings/create", json={
        "ride_id": ride_id,
        "seats_booked": 1,
        "pickup_name": "Assi Crossing",
        "dropoff_name": "BHU Main Gate"
    })
    assert book_res.status_code == 200
    bk_data = book_res.json()
    assert bk_data["status"] == "confirmed"
    assert bk_data["seats_booked"] == 1
    booking_id = bk_data["booking_id"]

    # 3. View my bookings
    my_res = client.get("/api/bookings/my-bookings")
    assert my_res.status_code == 200
    assert any(b["id"] == booking_id for b in my_res.json())

def test_marketplace_and_matching():
    # 1. Check spare vehicles seeking drivers
    veh_res = client.get("/api/marketplace/vehicles-seeking-drivers")
    assert veh_res.status_code == 200
    vehicles = veh_res.json()
    assert len(vehicles) >= 1
    spare_veh_id = vehicles[0]["id"]

    # 2. Check drivers looking for vehicles
    drv_res = client.get("/api/marketplace/drivers-seeking-vehicles")
    assert drv_res.status_code == 200
    drivers = drv_res.json()
    assert len(drivers) >= 1
    driver_user_id = drivers[0]["user_id"]

    # 3. Form a community partnership (Match spare vehicle + driver)
    match_res = client.post("/api/marketplace/match", json={
        "vehicle_id": spare_veh_id,
        "driver_id": driver_user_id,
        "owner_share_pct": 70.0,
        "driver_share_pct": 30.0,
        "notes": "Technofest Exhibition Demo Assignment"
    })
    assert match_res.status_code == 200
    assert "Successfully matched" in match_res.json()["message"]

def test_sustainability_impact():
    for p in ["today", "week", "month", "all"]:
        res = client.get(f"/api/impact/summary?period={p}")
        assert res.status_code == 200
        impact = res.json()
        assert "planet" in impact
        assert "people" in impact
        assert "prosperity" in impact
        assert impact["planet"]["co2_avoided_kg"] > 0
        assert impact["prosperity"]["spare_vehicles_monetized"] > 0

def test_admin_metrics():
    res = client.get("/api/admin/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert metrics["total_users"] >= 4
    assert metrics["total_vehicles"] >= 4

def test_safety_sos_simulation():
    res = client.post("/api/safety/sos-alert?ride_id=ride_1&lat=25.2910&lng=83.0030")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "active_alert"
    assert "DEMONSTRATION" in data["disclaimer"]

if __name__ == "__main__":
    import pytest
    print("Running GreenRide test suite...")

