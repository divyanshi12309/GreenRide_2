"""
=============================================================================
GREENRIDE - Sustainable Community Mobility Platform
Fully Streamlit-Powered Full-Stack Web Application (Technofest Edition)
"Move together. Earn together. Grow sustainably."
=============================================================================
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
import sys
import math
from datetime import datetime

# Add root directory to sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app.database import get_db, init_db
from backend.app.seed_data import seed
from backend.app.matching import resolve_coords, calculate_route_overlap, haversine_distance, calculate_co2_savings

# Ensure database is initialized and seeded
init_db()
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM users")
    if cursor.fetchone()["cnt"] == 0:
        seed()

# -----------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GREENRIDE | Sustainable Community Mobility",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for GreenRide modern design system
CUSTOM_CSS = """
<style>
    /* GreenRide Color Palette */
    :root {
        --primary-emerald: #059669;
        --primary-light: #ECFDF5;
        --slate-dark: #0F172A;
        --slate-card: #1E293B;
    }
    
    /* Header styles */
    .stApp header {
        background-color: transparent;
    }
    
    /* Top Brand Banner */
    .brand-hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    
    .brand-hero-title span {
        color: #059669;
    }
    
    .brand-pill {
        display: inline-block;
        background-color: #ECFDF5;
        border: 1px solid #10B981;
        color: #065F46;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 8px;
    }

    /* Comparison Card Box */
    .comparison-box-traditional {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }
    
    .comparison-box-greenride {
        background-color: #ECFDF5;
        border: 2px solid #10B981;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
    }
    
    /* Ride Match Card */
    .ride-match-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #059669;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    
    /* Simple Mode text scaling */
    .simple-mode-text {
        font-size: 1.25rem !important;
        line-height: 1.7 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "active_role" not in st.session_state:
    st.session_state.active_role = "passenger"
if "simple_mode" not in st.session_state:
    st.session_state.simple_mode = False
if "active_ride_id" not in st.session_state:
    st.session_state.active_ride_id = "ride_1"
if "last_booking" not in st.session_state:
    st.session_state.last_booking = None
if "search_origin" not in st.session_state:
    st.session_state.search_origin = "Lanka, Varanasi"
if "search_dest" not in st.session_state:
    st.session_state.search_dest = "Varanasi Cantt Railway Station"

# -----------------------------------------------------------------------------
# SIDEBAR: 1-CLICK ROLE SWITCHER & TECHNOFEST CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌿 GREENRIDE")
    st.markdown("**Community Mobility Platform**  \n*Varanasi Smart Corridor*")
    st.markdown("---")

    # 1-Click Role Switcher for Technofest Judges
    st.markdown("### 🎓 1-Click Demo Persona")
    role_options = {
        "passenger": "👤 Ananya (Passenger)",
        "driver": "🚗 Rahul (EV Driver)",
        "owner": "🔑 Vikram (Vehicle Owner)",
        "admin": "🛡️ Pooja (Admin Lead)"
    }
    selected_role_key = st.selectbox(
        "Switch Persona for Demonstration:",
        options=list(role_options.keys()),
        format_func=lambda k: role_options[k],
        index=list(role_options.keys()).index(st.session_state.active_role)
    )
    if selected_role_key != st.session_state.active_role:
        st.session_state.active_role = selected_role_key
        st.rerun()

    # User Profile Pill
    with get_db() as conn:
        cursor = conn.cursor()
        email_map = {
            "passenger": "passenger@greenride.org",
            "driver": "driver@greenride.org",
            "owner": "owner@greenride.org",
            "admin": "admin@greenride.org"
        }
        cursor.execute("SELECT * FROM users WHERE email = ?", (email_map[st.session_state.active_role],))
        current_user = dict(cursor.fetchone() or {})

    st.success(f"**Logged In:** {current_user.get('name', 'User')}\n\n📍 {current_user.get('locality', 'Varanasi')}")

    st.markdown("---")

    # Navigation Menu
    nav_options = [
        "🏠 Home & Visual Story",
        "🔍 Find a Shared Ride (Passenger)",
        "📡 Live Ride Tracking & SOS",
        "🤝 Driver + Vehicle Marketplace",
        "🚗 Driver Operations & Earnings",
        "🔑 Vehicle Owner Hub",
        "🌱 Sustainability Impact Dashboard",
        "🛡️ Platform Administration"
    ]
    
    # Auto-focus navigation based on chosen role if just switched
    default_nav_idx = 0
    if st.session_state.active_role == "passenger":
        default_nav_idx = 1
    elif st.session_state.active_role == "driver":
        default_nav_idx = 4
    elif st.session_state.active_role == "owner":
        default_nav_idx = 5
    elif st.session_state.active_role == "admin":
        default_nav_idx = 7

    selected_nav = st.radio(
        "Explore GreenRide Modules:",
        nav_options,
        index=default_nav_idx
    )

    st.markdown("---")

    # Accessibility & Simple Mode Toggle
    st.markdown("### 👓 Accessibility")
    simple_toggle = st.checkbox("Enable Simple Mode (for Elderly & Non-Tech Users)", value=st.session_state.simple_mode)
    if simple_toggle != st.session_state.simple_mode:
        st.session_state.simple_mode = simple_toggle
        st.rerun()

    if st.session_state.simple_mode:
        st.info("👓 **Simple Mode Active:** High contrast & plain language enabled.")

    # Technofest 5-Min Walkthrough Script
    with st.expander("✨ 5-Min Judge Presentation Script"):
        st.markdown("""
        **1. Problem (Min 1):** Point out duplicate petrol car trips causing 4x congestion in Lanka/BHU, while vehicles sit idle 95% of the day.
        
        **2. GreenRide (Min 2):** Show the *'4 Cars vs 1 Shared EV'* comparison on the Home tab.
        
        **3. Matching (Min 3):** Go to *Find a Shared Ride*. Search Lanka ➔ Cantt. Show the **94% Route Match** and ₹115 fare savings!
        
        **4. Marketplace (Min 4):** Go to *Marketplace*. Match Vikram's spare EV with Rahul using the 70/30 revenue split slider.
        
        **5. Impact (Min 5):** Go to *Sustainability Dashboard*. Point to Planet, People, and Prosperity real-time metrics!
        """)

    # 1-Click Reset Database Button
    if st.button("🔄 Reset Demo Database"):
        seed()
        st.session_state.last_booking = None
        st.success("Technofest demo data refreshed!")
        st.rerun()

# -----------------------------------------------------------------------------
# VIEW 1: HOME & VISUAL STORYTELLING
# -----------------------------------------------------------------------------
if selected_nav == "🏠 Home & Visual Story":
    st.markdown('<span class="brand-pill">🌱 COMMUNITY MOBILITY PLATFORM • VARANASI</span>', unsafe_allow_html=True)
    st.markdown("""
        <h1 class="brand-hero-title">
            Move together. Earn together.<br>
            <span>Grow sustainably.</span>
        </h1>
        <p style="font-size: 1.15rem; color: #475569; max-width: 800px; margin-bottom: 24px;">
            A community-powered mobility network connecting passengers, EV drivers, and spare vehicle owners 
            for cleaner, smarter, and more affordable shared journeys.
        </p>
    """, unsafe_allow_html=True)

    # Core Philosophical Distinction: 4 Cars vs 1 Shared EV
    st.markdown("---")
    st.markdown("### 🎯 The Core Innovation: Why Duplicate Journeys When We Can Share?")
    st.caption("Instead of 4 separate petrol vehicles making duplicate trips along the same road, GreenRide brings 4 commuters together into 1 shared zero-emission journey.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="comparison-box-traditional">
                <h4 style="color: #991B1B; margin-bottom: 8px;">❌ Traditional Solo Commuting</h4>
                <div style="font-size: 1.5rem; margin-bottom: 8px;">🚗 🚗 🚗 🚗</div>
                <strong style="color: #7F1D1D;">4 People • 4 Cars • 4x Congestion</strong>
                <ul style="color: #991B1B; font-size: 0.9rem; line-height: 1.7; margin-top: 8px;">
                    <li>4 separate vehicles burning fuel on the same Varanasi corridor.</li>
                    <li>High tailpipe emissions: ~768g CO₂/km combined.</li>
                    <li>Heavy bottleneck jams at Lanka Chauraha and Sigra.</li>
                    <li>Spare vehicles sit idle parked at home 95% of the day.</li>
                    <li>High expense: ₹160 - ₹220 for solo private cabs.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="comparison-box-greenride">
                <h4 style="color: #065F46; margin-bottom: 8px;">✅ GREENRIDE Community Mobility</h4>
                <div style="font-size: 1.5rem; margin-bottom: 8px;">⚡🚗 👥👥👥👥</div>
                <strong style="color: #047857;">4 People • 1 Shared EV • 75% Less Traffic</strong>
                <ul style="color: #065F46; font-size: 0.9rem; line-height: 1.7; margin-top: 8px;">
                    <li>Corridor matching combines trips along overlapping routes.</li>
                    <li>Zero direct tailpipe emissions & cleaner local air quality.</li>
                    <li>3 vehicles completely eliminated from the road corridor.</li>
                    <li>Spare vehicle owner earns passive income (70/30 split).</li>
                    <li>Affordable shared fare: only ₹35 - ₹55 per passenger.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Three-party ecosystem explanation
    st.markdown("---")
    st.markdown("### 🤝 One Platform. Three Beneficiaries.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            **1. Passengers (Commuters)**  
            Find verified shared EV rides along your regular route. Split the fare, pay 60% less than a private taxi, and cut urban emissions.
        """)
    with c2:
        st.markdown("""
            **2. Verified Drivers (Jobs)**  
            Access dignified driving livelihoods without needing to buy a ₹15 Lakh car. Partner with spare vehicle owners and start earning immediately.
        """)
    with c3:
        st.markdown("""
            **3. Spare Vehicle Owners (Income)**  
            Turn idle cars and electric auto-rickshaws into earning assets. Host them on GreenRide with verified background-checked drivers.
        """)

    # Diverse vehicle categories
    st.markdown("---")
    st.markdown("### ⚡ Multimodal Fleet Categories")
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.metric(label="⚡ EV Carpool", value="Tata Nexon EV", delta="👥 3-4 Seats")
        st.caption("Intercity and university corridor carpools.")
    with mc2:
        st.metric(label="⚡ E-Auto Pool", value="Mahindra Treo", delta="👥 3 Seats")
        st.caption("Clean last-mile transit through busy ghats.")
    with mc3:
        st.metric(label="⚡ E-Scooter Shift", value="Ather 450X", delta="👤 1 Rider")
        st.caption("Quick single-commuter campus links.")
    with mc4:
        st.metric(label="🚐 Community Shuttle", value="EV Minibus", delta="👥 8-12 Seats")
        st.caption("Scheduled campus and hospital routes.")

# -----------------------------------------------------------------------------
# VIEW 2: PASSENGER - FIND A SHARED RIDE & CARPOOL MATCHING
# -----------------------------------------------------------------------------
elif selected_nav == "🔍 Find a Shared Ride (Passenger)":
    st.markdown("## 🔍 Find a Shared Ride (Carpool Corridor Matcher)")
    st.caption("Search overlapping routes in Varanasi. Powered by intelligent vector alignment and emissions calculation.")

    # Search Form
    with st.form("ride_search_form"):
        col_orig, col_dest = st.columns(2)
        with col_orig:
            origin_input = st.text_input("From (Pickup Locality):", value=st.session_state.search_origin)
        with col_dest:
            dest_input = st.text_input("To (Destination):", value=st.session_state.search_dest)

        # Quick preset buttons row
        st.markdown("**Quick Destinations in Varanasi:**")
        q_cols = st.columns(5)
        if q_cols[0].form_submit_button("📍 BHU Gate"):
            dest_input = "BHU Gate / Vishwanath Temple"
        if q_cols[1].form_submit_button("📍 Assi Ghat"):
            dest_input = "Assi Ghat, Varanasi"
        if q_cols[2].form_submit_button("📍 Godowlia"):
            dest_input = "Godowlia Crossing"
        if q_cols[3].form_submit_button("📍 Cantt Station"):
            dest_input = "Varanasi Cantt Railway Station"
        if q_cols[4].form_submit_button("📍 Sarnath"):
            dest_input = "Sarnath Heritage Complex"

        c_pass, c_mode, c_btn = st.columns([1, 1, 2])
        with c_pass:
            passengers_cnt = st.selectbox("Passengers:", [1, 2, 3], index=0)
        with c_mode:
            veh_mode = st.selectbox("Vehicle Type:", ["All Modes", "ev_car", "e_auto", "e_scooter"])
        with c_btn:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            search_submitted = st.form_submit_button("⚡ SEARCH SHARED CORRIDORS", use_container_width=True)

    # Compute matches
    u_lat, u_lng = resolve_coords(origin_input, 25.2800, 82.9995)
    d_lat, d_lng = resolve_coords(dest_input, 25.3280, 82.9860)
    trip_distance = round(haversine_distance(u_lat, u_lng, d_lat, d_lng), 1)

    # Query matching rides from SQLite
    with get_db() as conn:
        cursor = conn.cursor()
        q = """
            SELECT r.*, u.name as driver_name, u.rating as driver_rating, u.avatar as driver_avatar,
                   v.title as vehicle_title, v.vehicle_type, v.reg_number, v.battery_kwh, v.fuel_type
            FROM rides r
            JOIN users u ON r.driver_id = u.id
            JOIN vehicles v ON r.vehicle_id = v.id
            WHERE r.status IN ('scheduled', 'active')
              AND r.available_seats >= ?
        """
        params = [passengers_cnt]
        if veh_mode != "All Modes":
            q += " AND v.vehicle_type = ?"
            params.append(veh_mode)
        cursor.execute(q, params)
        rides = [dict(r) for r in cursor.fetchall()]

    # Calculate match overlap score for each ride
    matched_rides = []
    for r in rides:
        overlap = calculate_route_overlap(
            u_lat, u_lng, d_lat, d_lng,
            r["origin_lat"], r["origin_lng"], r["dest_lat"], r["dest_lng"]
        )
        co2_saved = calculate_co2_savings(max(trip_distance, 3.0), r["vehicle_type"], passengers_cnt)
        solo_price = round(max(trip_distance * 22.0 + 50.0, 140.0))
        shared_price = round(r["price_per_seat"] * passengers_cnt)
        money_saved = max(solo_price - shared_price, 30)

        matched_rides.append({
            **r,
            "route_match_score": overlap,
            "co2_saved_kg": co2_saved,
            "solo_price": solo_price,
            "shared_price": shared_price,
            "money_saved": money_saved
        })

    # Sort descending by match score
    matched_rides.sort(key=lambda x: x["route_match_score"], reverse=True)

    # Results Layout: Cards on Left, Interactive Map on Right
    st.markdown(f"#### Verified Carpool Options ({len(matched_rides)} found along this corridor)")
    
    col_cards, col_map = st.columns([1.1, 0.9])
    with col_cards:
        for r in matched_rides:
            with st.container():
                st.markdown(f"""
                    <div class="ride-match-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="brand-pill">⚡ {r['route_match_score']}% ROUTE MATCH</span>
                            <span style="font-size: 1.3rem; font-weight: 800; color: #0F172A;">
                                ₹{r['price_per_seat']} <span style="font-size: 0.8rem; font-weight: 500; color: #64748B;">/ seat</span>
                            </span>
                        </div>
                        <h4 style="margin: 6px 0 2px; color: #0F172A;">{r['vehicle_title']}</h4>
                        <div style="font-size: 0.85rem; color: #475569; margin-bottom: 8px;">
                            <strong>Route:</strong> {r['origin_name'].split(',')[0]} ➔ {r['dest_name'].split(',')[0]}
                        </div>
                        <div style="font-size: 0.82rem; color: #059669; font-weight: 700; margin-bottom: 6px;">
                            🌱 Saves {r['co2_saved_kg']} kg CO₂ • Save ₹{r['money_saved']} vs solo cab!
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748B;">
                            <span>Driver: <strong>{r['driver_name']}</strong> (⭐ {r['driver_rating']})</span>
                            <span>Seats Left: <strong>{r['available_seats']} of {r['total_seats']}</strong></span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                c_book, c_track = st.columns([2, 1])
                with c_book:
                    if st.button(f"Reserve {passengers_cnt} Seat(s) (₹{r['shared_price']})", key=f"book_{r['id']}", use_container_width=True):
                        with get_db() as conn:
                            cur = conn.cursor()
                            booking_id = f"bk_{os.urandom(4).hex()}"
                            cur.execute("""
                                INSERT INTO bookings (id, ride_id, passenger_id, seats_booked, total_price, pickup_name, dropoff_name, status, route_match_score, co2_saved_kg)
                                VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                            """, (booking_id, r["id"], current_user["id"], passengers_cnt, r["shared_price"], origin_input, dest_input, r["route_match_score"], r["co2_saved_kg"]))
                            cur.execute("UPDATE rides SET available_seats = available_seats - ? WHERE id = ?", (passengers_cnt, r["id"]))
                        
                        st.session_state.active_ride_id = r["id"]
                        st.session_state.last_booking = {
                            "booking_id": booking_id,
                            "vehicle": r["vehicle_title"],
                            "driver": r["driver_name"],
                            "price": r["shared_price"],
                            "co2": r["co2_saved_kg"]
                        }
                        st.success("🎉 Seat confirmed! Your carpool reservation is active.")
                        st.balloons()
                with c_track:
                    if st.button("📡 Track Live", key=f"track_{r['id']}", use_container_width=True):
                        st.session_state.active_ride_id = r["id"]
                        st.session_state.active_nav = "📡 Live Ride Tracking & SOS"
                        st.info("Switched to Live Tracking view in sidebar!")

    with col_map:
        st.markdown("**📍 Varanasi Route Corridor Map**")
        # Build DataFrame for Streamlit map
        map_points = [
            {"lat": u_lat, "lon": u_lng, "name": "Pickup Point"},
            {"lat": d_lat, "lon": d_lng, "name": "Destination"}
        ]
        for r in matched_rides:
            map_points.append({
                "lat": r["current_lat"] or r["origin_lat"],
                "lon": r["current_lng"] or r["origin_lng"],
                "name": r["vehicle_title"]
            })
        map_df = pd.DataFrame(map_points)
        st.map(map_df, latitude="lat", longitude="lon", size=30, zoom=12)
        st.caption("🟢 Green circles represent active electric vehicle pins along Lanka, BHU, Assi, and Cantt corridors.")

# -----------------------------------------------------------------------------
# VIEW 3: LIVE RIDE TRACKING & SOS SIMULATION
# -----------------------------------------------------------------------------
elif selected_nav == "📡 Live Ride Tracking & SOS":
    st.markdown("## 📡 Live Ride Tracking & Telemetry")
    st.caption("Monitor your shared EV in real time along the Varanasi corridor.")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, u.name as driver_name, u.phone as driver_phone, u.rating as driver_rating,
                   v.title as vehicle_title, v.reg_number, v.battery_kwh, v.fuel_type
            FROM rides r
            JOIN users u ON r.driver_id = u.id
            JOIN vehicles v ON r.vehicle_id = v.id
            WHERE r.id = ?
        """, (st.session_state.active_ride_id,))
        ride = cursor.fetchone()

    if not ride:
        st.warning("No active ride selected. Reserve a ride in the search tab first.")
    else:
        ride = dict(ride)
        col_telemetry, col_map_live = st.columns([1, 1])

        with col_telemetry:
            st.markdown(f"""
                ### ⚡ {ride['vehicle_title']}
                **Registration:** `{ride['reg_number']}` • **Status:** `{ride['status'].upper()}`
            """)
            st.info(f"""
                **Driver:** {ride['driver_name']} 🛡️ (Police Verified)  
                **Rating:** ⭐ {ride['driver_rating']} | **Contact:** {ride['driver_phone']}
            """)

            st.success(f"""
                **Origin:** {ride['origin_name']}  
                **Destination:** {ride['dest_name']}  
                🌱 **CO₂ Reduction on this ride:** {ride['co2_savings_kg']} kg
            """)

            # Technofest Telemetry Simulation Controls
            st.markdown("#### 🕹️ Technofest Telemetry Simulation")
            st.caption("Click to demonstrate real-time vehicle movement on the map to judges:")
            
            sim_col1, sim_col2 = st.columns(2)
            with sim_col1:
                if st.button("⏩ Advance Vehicle 20%", use_container_width=True):
                    # Step 20% closer to destination
                    c_lat = ride["current_lat"] or ride["origin_lat"]
                    c_lng = ride["current_lng"] or ride["origin_lng"]
                    new_lat = c_lat + (ride["dest_lat"] - c_lat) * 0.25
                    new_lng = c_lng + (ride["dest_lng"] - c_lng) * 0.25
                    with get_db() as conn:
                        conn.cursor().execute("UPDATE rides SET current_lat = ?, current_lng = ? WHERE id = ?", (new_lat, new_lng, ride["id"]))
                    st.toast("Vehicle moved 20% closer to destination!")
                    st.rerun()

            with sim_col2:
                if st.button("✅ Complete Trip & Rate", use_container_width=True):
                    st.success("🎉 Trip successfully completed!")
                    st.balloons()

            st.markdown("---")
            st.markdown("#### 🚨 Safety & Emergency Protocol")
            if st.button("🚨 TRIGGER EMERGENCY SOS BEACON", type="primary", use_container_width=True):
                st.error("""
                    **🚨 SIMULATED EMERGENCY SOS BROADCAST:**
                    - Live GPS beacon dispatched to GreenRide 24/7 Operations Desk.
                    - Simulated SMS alert with live link sent to passenger's trusted contact.
                    - Nearest Varanasi community patrol notified along Lanka-Assi corridor.
                    *(Exhibition demonstration note: In a real emergency in India, dial 112 directly).*
                """)

        with col_map_live:
            st.markdown("**📍 Live GPS Telemetry View**")
            cur_lat = ride["current_lat"] or ride["origin_lat"]
            cur_lng = ride["current_lng"] or ride["origin_lng"]
            telemetry_df = pd.DataFrame([
                {"lat": cur_lat, "lon": cur_lng, "name": "Current Vehicle Location"},
                {"lat": ride["dest_lat"], "lon": ride["dest_lng"], "name": "Destination"}
            ])
            st.map(telemetry_df, latitude="lat", longitude="lon", zoom=13)
            st.caption(f"Current Telemetry: Lat {cur_lat:.4f}° N, Lon {cur_lng:.4f}° E")

# -----------------------------------------------------------------------------
# VIEW 4: DRIVER + SPARE VEHICLE MARKETPLACE
# -----------------------------------------------------------------------------
elif selected_nav == "🤝 Driver + Vehicle Marketplace":
    st.markdown("## 🤝 Driver + Spare Vehicle Marketplace")
    st.markdown("**Connecting spare vehicle owners with verified drivers to create employment without loan debt.**")
    st.caption("Example revenue model: 70% Owner / 30% Driver (configurable demo arrangement).")

    # Interactive Matchmaker Form
    st.markdown("### ⚡ Form a New Community Mobility Partnership")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT v.*, u.name as owner_name FROM vehicles v JOIN users u ON v.owner_id = u.id WHERE v.seeking_driver = 1")
        spare_vehs = [dict(v) for v in cursor.fetchall()]
        
        cursor.execute("SELECT dp.*, u.name as driver_name FROM driver_profiles dp JOIN users u ON dp.user_id = u.id WHERE dp.looking_for_vehicle = 1")
        seeking_drvs = [dict(d) for d in cursor.fetchall()]

    if not spare_vehs or not seeking_drvs:
        st.info("All demo spare vehicles and drivers are currently paired in active partnerships! Check the partnerships table below or reset the database in the sidebar.")
    else:
        with st.form("marketplace_match_form"):
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                chosen_veh = st.selectbox(
                    "Select Spare Vehicle Listed by Owner:",
                    options=spare_vehs,
                    format_func=lambda v: f"{v['title']} ({v['reg_number']}) - Owner: {v['owner_name']}"
                )
            with m_col2:
                chosen_drv = st.selectbox(
                    "Select Verified Driver Seeking Vehicle:",
                    options=seeking_drvs,
                    format_func=lambda d: f"{d['driver_name']} (⭐ {d['rating']} • {d['experience_years']} yrs exp)"
                )

            split_owner = st.slider("Revenue Split: Vehicle Owner Share (%)", min_value=40, max_value=80, value=70, step=5)
            split_driver = 100 - split_owner
            st.info(f"**Selected Revenue Split:** {split_owner}% Vehicle Owner / {split_driver}% Driver")

            if st.form_submit_button("🤝 FORM PARTNERSHIP & ASSIGN VEHICLE", use_container_width=True):
                with get_db() as conn:
                    cur = conn.cursor()
                    asgn_id = f"asgn_{os.urandom(4).hex()}"
                    cur.execute("""
                        INSERT INTO driver_vehicle_assignments (id, vehicle_id, driver_id, status, owner_share_pct, driver_share_pct, notes)
                        VALUES (?, ?, ?, 'active', ?, ?, 'Technofest Streamlit Match')
                    """, (asgn_id, chosen_veh["id"], chosen_drv["user_id"], split_owner, split_driver))
                    cur.execute("UPDATE vehicles SET status = 'assigned', seeking_driver = 0 WHERE id = ?", (chosen_veh["id"],))
                    cur.execute("UPDATE driver_profiles SET looking_for_vehicle = 0 WHERE user_id = ?", (chosen_drv["user_id"],))
                
                st.success(f"✨ Successfully paired! {chosen_drv['driver_name']} will now operate {chosen_veh['title']} at a {split_owner}/{split_driver} revenue split.")
                st.rerun()

    # Active Partnerships Table
    st.markdown("---")
    st.markdown("### 📋 Live Active Community Partnerships")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dva.id, v.title as vehicle, v.reg_number, u_owner.name as owner, u_drv.name as driver,
                   dva.owner_share_pct || '% / ' || dva.driver_share_pct || '%' as revenue_split,
                   dva.assigned_at
            FROM driver_vehicle_assignments dva
            JOIN vehicles v ON dva.vehicle_id = v.id
            JOIN users u_owner ON v.owner_id = u_owner.id
            JOIN users u_drv ON dva.driver_id = u_drv.id
            WHERE dva.status = 'active'
        """)
        asgns = [dict(r) for r in cursor.fetchall()]

    if asgns:
        st.dataframe(pd.DataFrame(asgns), use_container_width=True)

# -----------------------------------------------------------------------------
# VIEW 5: DRIVER OPERATIONS & EARNINGS
# -----------------------------------------------------------------------------
elif selected_nav == "🚗 Driver Operations & Earnings":
    st.markdown("## 🚗 Driver Operations & Livelihood Hub")
    st.caption("Active Driver Persona: Rahul Kumar (Verified EV Community Partner)")

    # Metrics
    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    c_m1.metric("Today's Payout", "₹1,240", "+₹210 vs yesterday")
    c_m2.metric("Total Net Earnings", "₹24,150", "Direct UPI / Bank")
    c_m3.metric("Green Mobility Bonus", "₹850", "Zero-emission rewards")
    c_m4.metric("Completed Trips", "184", "⭐ 4.92 Rating")

    st.markdown("---")
    col_drv1, col_drv2 = st.columns(2)

    with col_drv1:
        st.markdown("### 🔑 Assigned Vehicle Details")
        st.info("""
            **Vehicle:** Tata Nexon EV Max (`UP-65-EV-4401`)  
            **Owner:** Vikram Singh (Spare Vehicle Host)  
            **Revenue Arrangement:** 70% Owner / 30% Driver  
            💡 *No vehicle loan payments or down-payment debt required!*
        """)

        # Go Online / Offline control
        is_online = st.toggle("Driver Availability (Online / Accepting Carpools)", value=True)
        if is_online:
            st.success("🟢 Online & visible to Lanka-BHU commuters.")
        else:
            st.warning("⚪ Offline (Rest mode).")

    with col_drv2:
        st.markdown("### 🚀 Publish a New Shared Corridor Ride")
        with st.form("offer_ride_form"):
            o_orig = st.text_input("Origin:", value="Lanka Chauraha")
            o_dest = st.text_input("Destination:", value="BHU Gate")
            o_time = st.text_input("Departure Time:", value="09:15 AM Today")
            o_price = st.number_input("Fare per Seat (₹):", min_value=20, max_value=100, value=35)
            o_seats = st.number_input("Available Seats:", min_value=1, max_value=4, value=3)

            if st.form_submit_button("Publish Ride for Commuters", use_container_width=True):
                with get_db() as conn:
                    cur = conn.cursor()
                    r_id = f"ride_{os.urandom(4).hex()}"
                    cur.execute("""
                        INSERT INTO rides (id, driver_id, vehicle_id, origin_name, origin_lat, origin_lng, dest_name, dest_lat, dest_lng, departure_time, total_seats, available_seats, price_per_seat, ride_type, status, co2_savings_kg)
                        VALUES (?, 'usr_driver_1', 'veh_1', ?, 25.2800, 82.9995, ?, 25.2720, 82.9975, ?, ?, ?, ?, 'shared_ev', 'scheduled', 2.8)
                    """, (r_id, o_orig, o_dest, o_time, o_seats, o_seats, o_price))
                st.success("Shared ride published to commuters!")
                st.rerun()

# -----------------------------------------------------------------------------
# VIEW 6: VEHICLE OWNER HUB (MONETIZING SPARE VEHICLES)
# -----------------------------------------------------------------------------
elif selected_nav == "🔑 Vehicle Owner Hub":
    st.markdown("## 🔑 Spare Vehicle Owner Hub")
    st.caption("Active Owner Persona: Vikram Singh (Spare EV Host, Lanka Varanasi)")

    # Owner Asset Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Monthly Passive Income", "₹18,450", "+ ₹2,100 vs last month")
    m2.metric("Idle Hours Monetized", "196 hrs", "Saved from driveway depreciation")
    m3.metric("CO₂ Emissions Avoided", "284 kg", "Clean EV miles shared")

    st.markdown("---")
    st.markdown("### 🚘 Your Registered Vehicles")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE owner_id = 'usr_owner_1'")
        owner_vehs = [dict(v) for v in cursor.fetchall()]

    for v in owner_vehs:
        with st.container():
            st.markdown(f"""
                <div class="ride-match-card">
                    <h4>{v['title']} ({v['reg_number']})</h4>
                    <p style="color: #64748B; font-size: 0.85rem;">
                        <strong>Range:</strong> {v['ev_range_km']} km • <strong>Battery:</strong> {v['battery_kwh']} kWh • <strong>Status:</strong> {v['status'].upper()}
                    </p>
                    <p style="color: #059669; font-size: 0.85rem; font-weight: 700;">
                        Revenue Split: {v['revenue_share_owner']}% Owner / {v['revenue_share_driver']}% Driver
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # Form to add spare vehicle
    with st.expander("➕ List Another Spare / Unused Vehicle"):
        with st.form("add_spare_veh_form"):
            v_name = st.text_input("Vehicle Model:", value="Tata Tiago EV Long Range")
            v_cat = st.selectbox("Category:", ["ev_car", "e_auto", "e_scooter", "ev_van"])
            v_reg = st.text_input("Registration Number:", value="UP-65-EV-9821")
            v_rng = st.number_input("EV Range (km):", min_value=50, max_value=500, value=315)
            v_sts = st.number_input("Seats:", min_value=1, max_value=8, value=4)

            if st.form_submit_button("List Spare Vehicle in Marketplace"):
                with get_db() as conn:
                    cur = conn.cursor()
                    v_id = f"veh_{os.urandom(4).hex()}"
                    cur.execute("""
                        INSERT INTO vehicles (id, owner_id, title, vehicle_type, make_model, reg_number, seats, battery_kwh, ev_range_km, fuel_type, is_spare, seeking_driver, is_verified, status, revenue_share_owner, revenue_share_driver, locality)
                        VALUES (?, 'usr_owner_1', ?, ?, ?, ?, ?, 24.0, ?, 'Electric (EV)', 1, 1, 1, 'available', 70.0, 30.0, 'Lanka, Varanasi')
                    """, (v_id, v_name, v_cat, v_name, v_reg, v_sts, v_rng))
                st.success(f"✨ {v_name} listed! Verified drivers can now discover it in the Marketplace.")
                st.rerun()

# -----------------------------------------------------------------------------
# VIEW 7: SUSTAINABILITY IMPACT DASHBOARD (PLANET, PEOPLE, PROSPERITY)
# -----------------------------------------------------------------------------
elif selected_nav == "🌱 Sustainability Impact Dashboard":
    st.markdown("## 🌱 Three-Dimensional Sustainability Dashboard")
    st.caption("Quantifying verified environmental, social, and economic change in Varanasi.")

    period = st.radio("Time Horizon:", ["Today", "This Week", "This Month", "All Time"], horizontal=True)
    mult = {"Today": 0.05, "This Week": 0.25, "This Month": 0.65, "All Time": 1.0}[period]

    co2_kg = int(1960 * mult)
    trips = int(1420 * mult)
    km_saved = int(11928 * mult)
    trees = int(co2_kg / 21)
    savings_inr = int(96560 * mult)
    driver_inr = int(177500 * mult)

    # 3 Pillars
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("### 🌱 PLANET (Environment)")
        st.metric("CO₂ Avoided", f"{co2_kg:,} kg", f"≈ {trees} Mature Trees")
        st.metric("Vehicle-km Eliminated", f"{km_saved:,} km", "Zero direct emissions")

    with col_p2:
        st.markdown("### 👥 PEOPLE (Social Mobility)")
        st.metric("Commuters Connected", f"{int(3890 * mult):,}", "Safe, verified carpools")
        st.metric("Driver Livelihoods", "28 Jobs", "Dignified employment")

    with col_p3:
        st.markdown("### 💰 PROSPERITY (Economic)")
        st.metric("Commuter Fare Savings", f"₹{savings_inr:,}", "Kept in local economy")
        st.metric("Driver Earnings Generated", f"₹{driver_inr:,}", "Fair direct income")

    st.markdown("---")
    st.markdown("### 📈 Monthly Growth in Avoided Emissions (kg CO₂)")
    trend_df = pd.DataFrame({
        "Month": ["May", "Jun", "Jul", "Aug", "Sep", "Oct (Current)"],
        "Avoided CO2 (kg)": [240, 420, 680, 950, 1380, co2_kg],
        "Shared Commutes": [110, 190, 320, 460, 680, trips]
    })
    st.line_chart(trend_df, x="Month", y=["Avoided CO2 (kg)", "Shared Commutes"])

# -----------------------------------------------------------------------------
# VIEW 8: ADMIN OPERATIONS & SAFETY OVERSIGHT
# -----------------------------------------------------------------------------
elif selected_nav == "🛡️ Platform Administration":
    st.markdown("## 🛡️ Platform Administration & Verification Oversight")
    st.caption("Administrator: Pooja Verma (GreenRide Operations & Safety Lead, Varanasi)")

    # Metrics
    am1, am2, am3, am4 = st.columns(4)
    am1.metric("Registered Commuters", "842", "+34 this week")
    am2.metric("Active EV Drivers", "28", "100% Police Verified")
    am3.metric("Fleet Vehicles", "32", "Battery Certified")
    am4.metric("Active SOS Alerts", "0 Critical", "99.98% System Uptime")

    st.markdown("---")
    st.markdown("### 📋 Driver Document Verification Queue")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dp.id, u.name, dp.license_number, dp.experience_years, dp.is_verified
            FROM driver_profiles dp
            JOIN users u ON dp.user_id = u.id
        """)
        drv_list = [dict(d) for d in cursor.fetchall()]

    for d in drv_list:
        c_info, c_action = st.columns([3, 1])
        c_info.write(f"**{d['name']}** — DL: `{d['license_number']}` ({d['experience_years']} yrs exp)")
        if d['is_verified']:
            c_action.success("Verified ✓")
        else:
            if c_action.button("Approve", key=f"appr_{d['id']}"):
                with get_db() as conn:
                    conn.cursor().execute("UPDATE driver_profiles SET is_verified = 1 WHERE id = ?", (d['id'],))
                st.rerun()

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("🌿 **GREENRIDE Community Mobility** • Developed for School Technology Exhibition / Technofest Demonstration.")

