# 🌿 GREENRIDE — Sustainable Community Mobility Platform
> **Technofest / School Technology Exhibition Edition**  
> *"Move together. Earn together. Grow sustainably."*

---

## 🌟 Executive Summary: What Problem Does GreenRide Solve?

In growing urban centers like Varanasi, cities face a dual mobility crisis:
1. **Severe Traffic Congestion & Emissions:** Thousands of commuters make duplicate journeys in personal petrol/diesel vehicles along the same corridors (e.g., Lanka ➔ BHU, Assi ➔ Godowlia, Sigra ➔ Cantt Station).
2. **Underutilized Assets & Unemployment:** At the same time, millions of vehicles sit parked in driveways **95% of the day** depreciating. Meanwhile, skilled drivers seek honest employment but cannot afford ₹12–15 Lakh to purchase an electric car.

### The GreenRide Breakthrough: Community Mobility
GREENRIDE is **NOT** just another cab-booking app (like Uber or Ola) and **NOT** simply an EV taxi company.

It is a **three-way community mobility ecosystem** that connects:
* 👤 **Passengers:** Finding affordable, zero-emission shared carpools along their existing daily routes.
* 🚗 **Verified Drivers:** Accessing employment opportunities and income without taking on vehicle loan debt.
* 🔑 **Spare Vehicle Owners:** Putting unused personal EVs and electric auto-rickshaws to work with a transparent revenue split (e.g., 70% Owner / 30% Driver).

```
   TRADITIONAL CAB MODEL                        GREENRIDE COMMUNITY MODEL
   =====================                        =========================
   4 Commuters ➔ 4 Separate Cars                4 Commuters ➔ 1 Shared Electric Vehicle
   Emissions: ~768g CO₂/km combined             Direct Emissions: ZERO Tailpipe Emissions
   Congestion: 4x road footprint                Congestion: 75% Traffic Reduction
   Cost: ₹160 - ₹220 per solo cab               Cost: ₹35 - ₹55 per shared seat
   Asset Utilization: Zero (depreciating)       Asset Utilization: Passive owner income + driver job
```

---

## 🏆 Technofest Demonstration Guide (5-Minute Tour for Judges)

When presenting to exhibition judges, follow this structured walkthrough:

### Step 1: Open the Application
* URL: **`http://localhost:8000`**
* Notice the **Top Technofest Exhibition Bar** with the **1-Click Role Switcher** and **✨ Guided Tour for Judges** button.

### Step 2: The Core Problem & Visual Storytelling (Minute 1)
* Scroll down to the **"Why Duplicate Journeys When We Can Share?"** comparison widget.
* Point out how 4 individual cars create 4x congestion and high tailpipe emissions, whereas GreenRide combines them into 1 shared EV journey with 75% traffic reduction.

### Step 3: Passenger Carpool & Route Overlap Matching (Minute 2)
* Click **👤 Ananya (Passenger)** on the top bar or navigate to **Find a Ride**.
* Search from **Lanka** to **Varanasi Cantt Station**.
* Show the judge the **Route Match Score** (e.g. *"94% Route Match: Your route overlaps with Rahul's Nexon EV corridor by 94%"*).
* Click **Reserve Seat** and confirm the booking.

### Step 4: Live Telemetry & Safety Tracking (Minute 3)
* The system transitions to the **Live Ride Tracking** screen.
* Show the interactive Leaflet map with the green EV pin.
* Click **"Advance Vehicle 20% Along Route"** to show real-time GPS telemetry simulation.
* Click **🚨 SOS** to demonstrate the safety beacon and operations room protocol.
* Complete the trip and submit a 5-star rating with CO₂ savings feedback.

### Step 5: The Driver + Vehicle Marketplace (Minute 4)
* Click **🔑 Vikram (Vehicle Owner)** or navigate to **Marketplace**.
* Explain how Vikram owns an idle Piaggio Ape E-City / Tata Nexon EV.
* Show the judge the **"Match Driver + Vehicle"** action:
  * Select spare vehicle + select verified driver (e.g. Sunita or Rahul).
  * Adjust the **Configurable Revenue Split Slider** (70% Owner / 30% Driver).
  * Click **Form Community Partnership** — instantly assigning the vehicle and updating the database!

### Step 6: 3D Sustainability Dashboard & Accessibility (Minute 5)
* Navigate to **Sustainability Impact**:
  * **🌱 PLANET:** CO₂ avoided in kg, duplicate vehicle-km eliminated, trees equivalent.
  * **👥 PEOPLE:** Commuters connected, student carpools, verified driver livelihoods created.
  * **💰 PROSPERITY:** Commuter travel expenditure saved, owner & driver earnings generated.
  * Switch between filters: **Today | Week | Month | All Time**.
* Test **Accessibility**:
  * Click **👓 Simple Mode** in the header to demonstrate large typography, bold high-contrast buttons, and simplified plain language designed for elderly citizens.
  * Click **[A+]** to show font scaling and **[◐]** for high contrast.

---

## 👥 Demo Personas & Pre-Loaded Accounts

| Role | Name | Email | Persona & Context |
| :--- | :--- | :--- | :--- |
| **Passenger** | Ananya Sharma | `passenger@greenride.org` | Daily commuter & BHU student seeking safe, affordable travel. |
| **Driver** | Rahul Kumar | `driver@greenride.org` | Verified professional EV driver operating Vikram's Nexon EV. |
| **Vehicle Owner** | Vikram Singh | `owner@greenride.org` | Spare EV host earning passive revenue on idle assets. |
| **Platform Admin** | Pooja Verma | `admin@greenride.org` | GreenRide City Operations & Safety Oversight Lead. |

*Password for all demo accounts:* `demo123` (or use the instant 1-click switcher).

---

## 🛠️ Architecture & Technical Stack

```
   ┌────────────────────────────────────────────────────────┐
   │             MODERN FRONTEND (SPA)                      │
   │  • HTML5 Semantic & WCAG 2.1 AAA Accessibility        │
   │  • Custom Design System (Slate Charcoal & Emerald)    │
   │  • Leaflet.js Interactive Map (Varanasi Corridors)    │
   │  • Chart.js Sustainability Visualizations             │
   │  • Simple Mode & High-Contrast Support                │
   └──────────────────────────┬─────────────────────────────┘
                              │ REST API Requests
   ┌──────────────────────────▼─────────────────────────────┐
   │             FASTAPI BACKEND (Python 3.14)              │
   │  • Uvicorn High-Performance Async ASGI Server         │
   │  • Carpool Corridor Matching Algorithm                │
   │  • Haversine Overlap & Bearing Vector Calculations     │
   │  • PyJWT Authentication & Role-Based Permissions      │
   │  • Pydantic v2 Request & Response Validation          │
   └──────────────────────────┬─────────────────────────────┘
                              │ SQLite PRAGMA Foreign Keys
   ┌──────────────────────────▼─────────────────────────────┐
   │             RELATIONAL DATABASE (greenride.db)         │
   │  • users & driver_profiles                            │
   │  • vehicles & driver_vehicle_assignments              │
   │  • rides & bookings                                   │
   │  • ratings, reports, system_logs, communities         │
   └────────────────────────────────────────────────────────┘
```

---

## 🚀 Running the Project

### Method 1: Windows 1-Click Launch (Recommended)
Double-click the **`start.bat`** file in the project root. It will:
1. Verify the Python environment.
2. Launch the backend server at `http://localhost:8000`.
3. Open your default web browser automatically!

### Method 2: Command Line
```powershell
# 1. Start the server
py backend/run.py

# 2. Access the platform
# Web Application: http://localhost:8000
# Interactive API Docs: http://localhost:8000/docs
```

### Method 3: Running Automated Tests
```powershell
py -m pytest tests/test_api.py -v
```
*Validates all 10 core integration tests across auth, carpool matching, bookings, marketplace assignment, impact metrics, and safety simulations.*

---

## 📐 REST API Endpoints Overview

* **Authentication & Roles:**
  * `POST /api/auth/login` — Session authentication
  * `GET  /api/auth/demo-switch/{role}` — 1-click Technofest role switcher
  * `GET  /api/auth/me` — Current authenticated user profile
* **Carpooling & Rides:**
  * `POST /api/rides/search` — Corridor matching algorithm returning overlap % & CO₂ saved
  * `GET  /api/rides/list` — Active and scheduled shared rides
  * `POST /api/rides/{ride_id}/simulate-step` — Telemetry advance simulation
* **Reservations & Bookings:**
  * `POST /api/bookings/create` — Reserves seats & decrements capacity
  * `GET  /api/bookings/my-bookings` — Commuter trip history & active tickets
  * `POST /api/bookings/rate` — Driver feedback and community scoring
* **Spare Vehicle Marketplace:**
  * `GET  /api/marketplace/vehicles-seeking-drivers` — Spare vehicles listed by owners
  * `GET  /api/marketplace/drivers-seeking-vehicles` — Verified drivers looking for vehicles
  * `POST /api/marketplace/match` — Forms community partnership with configurable revenue split
* **Sustainability & Safety:**
  * `GET  /api/impact/summary?period=all` — 3D metrics across Planet, People, Prosperity
  * `POST /api/safety/sos-alert` — Emergency telemetry beacon simulation
  * `POST /api/admin/reset-demo-database` — 1-click restore to fresh state for next judge

---

## 🌿 Final Word: Why This is More Than a Cab App

GreenRide proves that urban technology does not have to add more vehicles to our streets. By **connecting idle assets with eager drivers and daily commuters**, it simultaneously tackles traffic congestion, vehicle emissions, and unemployment — creating a cleaner, fairer, and more connected community.

