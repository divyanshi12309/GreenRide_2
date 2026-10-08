"""
GREENRIDE - Realistic Technofest Seed Data
Populates the platform with realistic Varanasi demo data:
Lanka, Assi Ghat, BHU, Godowlia, Cantt Railway Station, Sarnath.
"""

from .database import get_db, init_db
import hashlib

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def seed():
    init_db()
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if already seeded
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        if cursor.fetchone()["cnt"] > 0:
            print("Database already contains data, updating/refreshing...")

        # Clear existing tables for a clean Technofest demo state
        cursor.execute("DELETE FROM bookings")
        cursor.execute("DELETE FROM rides")
        cursor.execute("DELETE FROM driver_vehicle_assignments")
        cursor.execute("DELETE FROM vehicles")
        cursor.execute("DELETE FROM driver_profiles")
        cursor.execute("DELETE FROM ratings")
        cursor.execute("DELETE FROM reports")
        cursor.execute("DELETE FROM communities")
        cursor.execute("DELETE FROM system_logs")
        cursor.execute("DELETE FROM users")

        # 1. Insert Demo Users
        users = [
            (
                "usr_passenger_1",
                "Ananya Sharma",
                "passenger@greenride.org",
                "+91 98765 43210",
                hash_pw("demo123"),
                "passenger",
                "passenger",
                4.95,
                "Lanka, Varanasi",
                "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
            ),
            (
                "usr_driver_1",
                "Rahul Kumar",
                "driver@greenride.org",
                "+91 98111 22334",
                hash_pw("demo123"),
                "driver",
                "driver",
                4.92,
                "Assi Ghat, Varanasi",
                "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"
            ),
            (
                "usr_driver_2",
                "Suresh Yadav",
                "suresh.driver@greenride.org",
                "+91 98333 44556",
                hash_pw("demo123"),
                "driver",
                "driver",
                4.85,
                "Godowlia, Varanasi",
                "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"
            ),
            (
                "usr_driver_3",
                "Sunita Maurya",
                "sunita.driver@greenride.org",
                "+91 98555 66778",
                hash_pw("demo123"),
                "driver",
                "driver",
                4.97,
                "BHU Campus, Varanasi",
                "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150"
            ),
            (
                "usr_owner_1",
                "Vikram Singh",
                "owner@greenride.org",
                "+91 98222 33445",
                hash_pw("demo123"),
                "owner",
                "owner",
                4.98,
                "Lanka / BHU Road, Varanasi",
                "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"
            ),
            (
                "usr_owner_2",
                "Meera Patel",
                "meera.owner@greenride.org",
                "+91 98444 55667",
                hash_pw("demo123"),
                "owner",
                "owner",
                4.91,
                "Ravindrapuri, Varanasi",
                "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150"
            ),
            (
                "usr_admin_1",
                "Pooja Verma",
                "admin@greenride.org",
                "+91 98999 00112",
                hash_pw("demo123"),
                "admin",
                "admin",
                5.0,
                "GreenRide City HQ, Varanasi",
                "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150"
            )
        ]

        cursor.executemany("""
        INSERT INTO users (id, name, email, phone, password_hash, roles, active_role, rating, locality, avatar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, users)

        # 2. Insert Driver Profiles
        driver_profiles = [
            (
                "drv_prof_1",
                "usr_driver_1",
                "UP-65-2019-008129",
                4,
                "Lanka, BHU, Assi, Cantt Station",
                "Hindi, English, Bhojpuri",
                "EV Car, E-Auto",
                1, # is_verified
                1, # is_online
                4.92,
                184,
                0  # looking_for_vehicle (already matched with Vikram's EV)
            ),
            (
                "drv_prof_2",
                "usr_driver_2",
                "UP-65-2021-004312",
                3,
                "Godowlia, Chowk, Cantt, Sarnath",
                "Hindi, Bhojpuri",
                "E-Auto, E-Scooter",
                1,
                1,
                4.85,
                92,
                0 # operates Meera's Mahindra Treo E-Auto
            ),
            (
                "drv_prof_3",
                "usr_driver_3",
                "UP-65-2020-009943",
                5,
                "BHU Campus, Lanka, DLW, Kashi",
                "Hindi, English",
                "EV Car, Electric Shuttle",
                1,
                1,
                4.97,
                210,
                1 # Looking for spare vehicle partnership in marketplace!
            )
        ]

        cursor.executemany("""
        INSERT INTO driver_profiles (id, user_id, license_number, experience_years, preferred_area, languages, vehicle_category, is_verified, is_online, rating, trips_completed, looking_for_vehicle)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, driver_profiles)

        # 3. Insert Vehicles (Owner spare vehicles + active shared vehicles)
        vehicles = [
            (
                "veh_1",
                "usr_owner_1",
                "Tata Nexon EV Max",
                "ev_car",
                "Tata Nexon EV (Empowered Dark)",
                "UP-65-EV-4401",
                4,
                40.5,
                380,
                "Pure Electric (EV)",
                1, # spare vehicle
                0, # already assigned to Rahul
                1, # verified
                "assigned",
                70.0,
                30.0,
                "Lanka, Varanasi",
                "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=500"
            ),
            (
                "veh_2",
                "usr_owner_1",
                "Piaggio Ape E-City FX",
                "e_auto",
                "Piaggio Ape E-City Electric 3-Wheeler",
                "UP-65-EA-8820",
                3,
                7.5,
                110,
                "Battery Electric",
                1, # spare vehicle
                1, # seeking driver in marketplace!
                1, # verified
                "available",
                70.0,
                30.0,
                "BHU Gate, Varanasi",
                "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=500"
            ),
            (
                "veh_3",
                "usr_owner_2",
                "Mahindra Treo Electric Auto",
                "e_auto",
                "Mahindra Treo Li-Ion Shared Auto",
                "UP-65-EA-1923",
                3,
                8.0,
                130,
                "Li-ion Electric",
                1,
                0,
                1,
                "assigned",
                70.0,
                30.0,
                "Godowlia, Varanasi",
                "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=500"
            ),
            (
                "veh_4",
                "usr_owner_2",
                "MG ZS EV Excite",
                "ev_car",
                "MG ZS EV Long Range",
                "UP-65-EV-9011",
                4,
                50.3,
                420,
                "Pure Electric (EV)",
                1,
                1, # seeking driver!
                1,
                "available",
                65.0,
                35.0,
                "Ravindrapuri, Varanasi",
                "https://images.unsplash.com/photo-1563720223185-11003d516935?w=500"
            ),
            (
                "veh_5",
                "usr_owner_1",
                "Ather 450X Gen 3",
                "e_scooter",
                "Ather 450X High-Speed E-Scooter",
                "UP-65-ES-3312",
                1,
                3.7,
                105,
                "Electric 2-Wheeler",
                1,
                0,
                1,
                "available",
                80.0,
                20.0,
                "Assi Ghat, Varanasi",
                "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=500"
            )
        ]

        cursor.executemany("""
        INSERT INTO vehicles (id, owner_id, title, vehicle_type, make_model, reg_number, seats, battery_kwh, ev_range_km, fuel_type, is_spare, seeking_driver, is_verified, status, revenue_share_owner, revenue_share_driver, locality, photo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, vehicles)

        # 4. Insert Driver-Vehicle Assignments
        assignments = [
            (
                "asgn_1",
                "veh_1",
                "usr_driver_1",
                "active",
                70.0,
                30.0,
                "Active partnership: Vikram's spare Tata Nexon EV is driven by Rahul Kumar."
            ),
            (
                "asgn_2",
                "veh_3",
                "usr_driver_2",
                "active",
                70.0,
                30.0,
                "Active partnership: Meera's Mahindra Treo is driven by Suresh Yadav."
            )
        ]

        cursor.executemany("""
        INSERT INTO driver_vehicle_assignments (id, vehicle_id, driver_id, status, owner_share_pct, driver_share_pct, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, assignments)

        # 5. Insert Active & Scheduled Shared Rides (Carpooling routes in Varanasi)
        # Coordinates:
        # Lanka: 25.2800, 82.9995
        # BHU: 25.2720, 82.9975
        # Assi Ghat: 25.2925, 83.0065
        # Godowlia: 25.3110, 83.0070
        # Cantt Station: 25.3280, 82.9860
        # Sarnath: 25.3811, 83.0214
        rides = [
            (
                "ride_1",
                "usr_driver_1", # Rahul
                "veh_1",        # Tata Nexon EV Max
                "Lanka Market, Varanasi",
                25.2800,
                82.9995,
                "Varanasi Cantt Railway Station",
                25.3280,
                82.9860,
                "08:45 AM Today",
                3, # total passenger seats
                2, # available seats left
                45.0, # price per seat in INR
                "shared_ev",
                "active",
                3.8, # CO2 saved in kg
                25.2910, # current lat (en route near Assi)
                83.0030
            ),
            (
                "ride_2",
                "usr_driver_1",
                "veh_1",
                "Assi Ghat, Varanasi",
                25.2925,
                83.0065,
                "BHU Gate / Vishwanath Temple",
                25.2720,
                82.9975,
                "10:15 AM Today",
                3,
                3,
                30.0,
                "carpool",
                "scheduled",
                2.4,
                25.2925,
                83.0065
            ),
            (
                "ride_3",
                "usr_driver_2", # Suresh
                "veh_3",        # Mahindra Treo E-Auto
                "Godowlia Crossing",
                25.3110,
                83.0070,
                "Lanka Chauraha via BHU",
                25.2800,
                82.9995,
                "09:10 AM Today",
                3,
                1, # only 1 seat left!
                25.0,
                "e_auto_pool",
                "active",
                2.9,
                25.2980,
                83.0040
            ),
            (
                "ride_4",
                "usr_driver_3", # Sunita
                "veh_5",        # Ather E-Scooter
                "BHU Campus",
                25.2720,
                82.9975,
                "Assi Ghat",
                25.2925,
                83.0065,
                "11:00 AM Today",
                1,
                1,
                20.0,
                "e_scooter",
                "scheduled",
                1.5,
                25.2720,
                82.9975
            ),
            (
                "ride_5",
                "usr_driver_2",
                "veh_3",
                "Varanasi Cantt Station",
                25.3280,
                82.9860,
                "Sarnath Heritage Complex",
                25.3811,
                83.0214,
                "02:30 PM Today",
                3,
                3,
                55.0,
                "e_auto_pool",
                "scheduled",
                4.6,
                25.3280,
                82.9860
            )
        ]

        cursor.executemany("""
        INSERT INTO rides (id, driver_id, vehicle_id, origin_name, origin_lat, origin_lng, dest_name, dest_lat, dest_lng, departure_time, total_seats, available_seats, price_per_seat, ride_type, status, co2_savings_kg, current_lat, current_lng)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rides)

        # 6. Insert Bookings (Passenger ride history and active confirmed ride)
        bookings = [
            (
                "bk_1",
                "ride_1", # Ananya is currently booked on Rahul's ride from Lanka to Cantt!
                "usr_passenger_1",
                1,
                45.0,
                "Lanka Chauraha (Near MMV)",
                "Cantt Platform 1 Drop",
                "active",
                96, # 96% route match!
                3.1
            ),
            (
                "bk_2",
                "ride_3",
                "usr_passenger_1",
                1,
                25.0,
                "Assi Crossing",
                "Godowlia Ghat",
                "completed",
                89,
                2.2
            )
        ]

        cursor.executemany("""
        INSERT INTO bookings (id, ride_id, passenger_id, seats_booked, total_price, pickup_name, dropoff_name, status, route_match_score, co2_saved_kg)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, bookings)

        # 7. Insert Ratings
        ratings = [
            (
                "rat_1",
                "ride_3",
                "usr_passenger_1",
                "usr_driver_2",
                5.0,
                "Smooth electric auto ride, reached on time and avoided taking my own scooter. Great initiative!"
            ),
            (
                "rat_2",
                "ride_1",
                "usr_passenger_1",
                "usr_driver_1",
                5.0,
                "Rahul is a very courteous and safe driver. The Nexon EV was super quiet and clean."
            )
        ]

        cursor.executemany("""
        INSERT INTO ratings (id, ride_id, from_user_id, to_user_id, score, comment)
        VALUES (?, ?, ?, ?, ?, ?)
        """, ratings)

        # 8. Insert Safety Reports / Inquiries
        reports = [
            (
                "rep_1",
                "usr_passenger_1",
                "driver",
                "usr_driver_2",
                "pricing",
                "Driver suggested a UPI discount outside the app. Resolved peacefully.",
                "resolved"
            )
        ]

        cursor.executemany("""
        INSERT INTO reports (id, reporter_id, target_type, target_id, category, description, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, reports)

        # 9. Insert Communities
        communities = [
            (
                "com_1",
                "BHU Student & Faculty Mobility Circle",
                "college",
                "Banaras Hindu University, Varanasi",
                "Official shared carpool and e-rickshaw network for BHU scholars, professors, and resident staff.",
                842
            ),
            (
                "com_2",
                "Kashi Tech Park & Freelance Commute",
                "corporate",
                "Sigra / Cantt, Varanasi",
                "Shared EV rides for IT professionals and startups reducing peak morning congestion on Sigra Road.",
                326
            ),
            (
                "com_3",
                "Lanka-Assi Green Neighborhood Society",
                "residential",
                "Lanka & Ravindrapuri, Varanasi",
                "Community members pooling spare EVs and morning market errands together.",
                510
            )
        ]

        cursor.executemany("""
        INSERT INTO communities (id, name, category, locality, description, members_count)
        VALUES (?, ?, ?, ?, ?, ?)
        """, communities)

        # 10. System Logs
        logs = [
            ("log_1", "DRIVER_VERIFIED", "usr_admin_1", "Verified Rahul Kumar DL and Police Clearance Certificate."),
            ("log_2", "VEHICLE_ASSIGNED", "usr_owner_1", "Assigned Tata Nexon EV (UP-65-EV-4401) to verified driver Rahul Kumar at 70/30 split."),
            ("log_3", "RIDE_BOOKED", "usr_passenger_1", "Booked 1 seat on Shared EV route Lanka -> Cantt Railway Station.")
        ]

        cursor.executemany("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, ?, ?, ?)
        """, logs)

        print("Technofest demo seed data injected successfully!")

if __name__ == "__main__":
    seed()

