"""
GREENRIDE - SQLite Database Manager & Schema Definition
Provides relational data store with robust tables and seed helpers.
"""

import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "greenride.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initializes the database schema if tables do not exist."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            roles TEXT NOT NULL DEFAULT 'passenger', -- comma-separated e.g. passenger,driver
            active_role TEXT NOT NULL DEFAULT 'passenger',
            rating REAL DEFAULT 5.0,
            locality TEXT DEFAULT 'Lanka, Varanasi',
            avatar TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Driver Profiles
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS driver_profiles (
            id TEXT PRIMARY KEY,
            user_id TEXT UNIQUE NOT NULL,
            license_number TEXT NOT NULL,
            experience_years INTEGER DEFAULT 3,
            preferred_area TEXT DEFAULT 'Varanasi Central / Lanka / BHU',
            languages TEXT DEFAULT 'Hindi, English, Bhojpuri',
            vehicle_category TEXT DEFAULT 'EV Car, E-Auto',
            is_verified INTEGER DEFAULT 1,
            is_online INTEGER DEFAULT 1,
            rating REAL DEFAULT 4.9,
            trips_completed INTEGER DEFAULT 142,
            looking_for_vehicle INTEGER DEFAULT 0, -- 1 if driver needs vehicle
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 3. Vehicles
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id TEXT PRIMARY KEY,
            owner_id TEXT NOT NULL,
            title TEXT NOT NULL,
            vehicle_type TEXT NOT NULL, -- ev_car, e_auto, e_scooter, ev_van
            make_model TEXT NOT NULL,
            reg_number TEXT NOT NULL,
            seats INTEGER NOT NULL DEFAULT 4,
            battery_kwh REAL DEFAULT 30.2,
            ev_range_km INTEGER DEFAULT 250,
            fuel_type TEXT DEFAULT 'Electric (EV)',
            is_spare INTEGER DEFAULT 1,
            seeking_driver INTEGER DEFAULT 1,
            is_verified INTEGER DEFAULT 1,
            status TEXT DEFAULT 'available', -- available, assigned, in_service
            revenue_share_owner REAL DEFAULT 70.0,
            revenue_share_driver REAL DEFAULT 30.0,
            locality TEXT DEFAULT 'Lanka, Varanasi',
            photo_url TEXT DEFAULT '',
            FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 4. Driver-Vehicle Assignments (Marketplace matches)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS driver_vehicle_assignments (
            id TEXT PRIMARY KEY,
            vehicle_id TEXT NOT NULL,
            driver_id TEXT NOT NULL,
            status TEXT DEFAULT 'active', -- requested, active, terminated
            owner_share_pct REAL DEFAULT 70.0,
            driver_share_pct REAL DEFAULT 30.0,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT DEFAULT '',
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
            FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 5. Rides (Available & active carpool / shared rides)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rides (
            id TEXT PRIMARY KEY,
            driver_id TEXT NOT NULL,
            vehicle_id TEXT NOT NULL,
            origin_name TEXT NOT NULL,
            origin_lat REAL NOT NULL,
            origin_lng REAL NOT NULL,
            dest_name TEXT NOT NULL,
            dest_lat REAL NOT NULL,
            dest_lng REAL NOT NULL,
            departure_time TEXT NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL,
            price_per_seat REAL NOT NULL,
            ride_type TEXT DEFAULT 'shared_ev', -- shared_ev, carpool, e_auto_pool, e_scooter
            status TEXT DEFAULT 'scheduled', -- scheduled, active, completed, cancelled
            co2_savings_kg REAL DEFAULT 2.8,
            current_lat REAL,
            current_lng REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (driver_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        );
        """)

        # 6. Bookings (Passenger ride reservations)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id TEXT PRIMARY KEY,
            ride_id TEXT NOT NULL,
            passenger_id TEXT NOT NULL,
            seats_booked INTEGER NOT NULL DEFAULT 1,
            total_price REAL NOT NULL,
            pickup_name TEXT NOT NULL,
            dropoff_name TEXT NOT NULL,
            status TEXT DEFAULT 'confirmed', -- confirmed, active, completed, cancelled
            route_match_score INTEGER DEFAULT 92,
            co2_saved_kg REAL DEFAULT 2.4,
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ride_id) REFERENCES rides(id) ON DELETE CASCADE,
            FOREIGN KEY (passenger_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 7. Ratings & Reviews
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id TEXT PRIMARY KEY,
            ride_id TEXT NOT NULL,
            from_user_id TEXT NOT NULL,
            to_user_id TEXT NOT NULL,
            score REAL NOT NULL,
            comment TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 8. Issues & Safety Reports
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            reporter_id TEXT NOT NULL,
            target_type TEXT NOT NULL, -- driver, vehicle, ride, general
            target_id TEXT NOT NULL,
            category TEXT NOT NULL, -- safety, delay, cleanliness, pricing
            description TEXT NOT NULL,
            status TEXT DEFAULT 'under_review', -- under_review, resolved, dismissed
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 9. Communities (Colleges, Workplaces, Societies)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS communities (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL, -- college, corporate, residential
            locality TEXT NOT NULL,
            description TEXT NOT NULL,
            members_count INTEGER DEFAULT 1
        );
        """)

        # 10. Platform System Logs / Admin Audit
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            actor_id TEXT NOT NULL,
            details TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)

