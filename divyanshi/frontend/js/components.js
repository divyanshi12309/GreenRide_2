/**
 * GREENRIDE - Dynamic View Components
 * Renders Home, Ride Finder, Live Tracking, Driver Dashboard,
 * Vehicle Owner Dashboard, Marketplace, Impact Dashboard, and Admin.
 */

window.components = {
    // 1. HOME & HERO VIEW
    renderHome: () => `
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="container hero-grid">
                <div>
                    <span class="brand-badge" style="margin-bottom: 12px; display: inline-block;">
                        🌱 Community Mobility Platform • Varanasi
                    </span>
                    <h1 class="hero-title">
                        Move together.<br>
                        Earn together.<br>
                        <span>Grow sustainably.</span>
                    </h1>
                    <p class="hero-subtitle">
                        A community-powered mobility platform connecting passengers, EV drivers, and spare vehicle owners for cleaner, smarter shared journeys.
                    </p>
                    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                        <button onclick="window.app.navigate('find-ride')" class="btn btn-primary btn-lg">
                            🔍 Find a Shared Ride
                        </button>
                        <button onclick="window.app.navigate('marketplace')" class="btn btn-secondary btn-lg">
                            🤝 Driver & Vehicle Marketplace
                        </button>
                    </div>
                </div>

                <!-- Hero Search Widget -->
                <div class="search-ride-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <h2 style="font-size: 1.15rem; font-weight: 700; color: #0F172A;">
                            Find a Shared Ride
                        </h2>
                        <span class="match-badge">⚡ 100% Electric First</span>
                    </div>

                    <form id="hero-search-form" onsubmit="window.app.handleHeroSearch(event)">
                        <div style="margin-bottom: 14px;">
                            <label class="form-label" for="search-origin">From (Pickup Locality)</label>
                            <div style="display: flex; gap: 8px;">
                                <input type="text" id="search-origin" class="form-input" value="Lanka, Varanasi" required placeholder="Enter pickup locality" />
                                <button type="button" onclick="window.app.useMyLocation()" class="btn btn-secondary" style="padding: 10px 14px; white-space: nowrap;" title="Detect GPS location">
                                    📍 GPS
                                </button>
                            </div>
                        </div>

                        <div style="margin-bottom: 14px;">
                            <label class="form-label" for="search-dest">To (Destination)</label>
                            <input type="text" id="search-dest" class="form-input" value="Varanasi Cantt Railway Station" required placeholder="Enter destination" />
                            <div style="display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap;">
                                <button type="button" onclick="document.getElementById('search-dest').value='BHU Gate'; window.app.handleHeroSearch(event)" style="font-size: 0.75rem; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 2px 8px; border-radius: 12px; cursor: pointer;">BHU Gate</button>
                                <button type="button" onclick="document.getElementById('search-dest').value='Assi Ghat'; window.app.handleHeroSearch(event)" style="font-size: 0.75rem; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 2px 8px; border-radius: 12px; cursor: pointer;">Assi Ghat</button>
                                <button type="button" onclick="document.getElementById('search-dest').value='Godowlia'; window.app.handleHeroSearch(event)" style="font-size: 0.75rem; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 2px 8px; border-radius: 12px; cursor: pointer;">Godowlia</button>
                                <button type="button" onclick="document.getElementById('search-dest').value='Sarnath'; window.app.handleHeroSearch(event)" style="font-size: 0.75rem; background: #F1F5F9; border: 1px solid #CBD5E1; padding: 2px 8px; border-radius: 12px; cursor: pointer;">Sarnath</button>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 18px;">
                            <div>
                                <label class="form-label" for="search-seats">Passengers</label>
                                <select id="search-seats" class="form-select">
                                    <option value="1">1 Passenger</option>
                                    <option value="2">2 Passengers</option>
                                    <option value="3">3 Passengers</option>
                                </select>
                            </div>
                            <div>
                                <label class="form-label" for="search-type">Vehicle Type</label>
                                <select id="search-type" class="form-select">
                                    <option value="all">Any EV Mode</option>
                                    <option value="ev_car">⚡ EV Car</option>
                                    <option value="e_auto">⚡ E-Auto</option>
                                    <option value="e_scooter">⚡ E-Scooter</option>
                                </select>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary" style="width: 100%; font-size: 1.05rem; padding: 14px;">
                            ⚡ FIND A SHARED RIDE
                        </button>
                    </form>
                </div>
            </div>
        </section>

        <div class="container">
            <!-- Visual Storytelling: 4 Cars vs 1 Shared EV -->
            <div class="story-comparison-widget">
                <div style="text-align: center; max-width: 700px; margin: 0 auto;">
                    <span class="brand-badge" style="background: #EFF6FF; border-color: #BFDBFE; color: #1D4ED8;">
                        THE CORE GREENRIDE PHILOSOPHY
                    </span>
                    <h2 style="font-size: 2rem; font-weight: 800; color: #0F172A; margin: 8px 0;">
                        Why Duplicate Journeys When We Can Share?
                    </h2>
                    <p style="color: #64748B; font-size: 1.05rem;">
                        Instead of 4 separate petrol vehicles making duplicate trips along the same road, GreenRide brings 4 commuters together into 1 shared zero-emission journey.
                    </p>
                </div>

                <div class="comparison-grid">
                    <div class="comparison-col traditional">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <span style="font-weight: 800; color: #991B1B; font-size: 0.9rem; text-transform: uppercase;">
                                ❌ Traditional Commuting
                            </span>
                            <span style="font-size: 1.5rem;">🚗🚗🚗🚗</span>
                        </div>
                        <h3 style="font-size: 1.3rem; font-weight: 700; color: #7F1D1D; margin-bottom: 8px;">
                            4 People • 4 Cars • 4x Congestion
                        </h3>
                        <ul style="color: #991B1B; font-size: 0.95rem; line-height: 1.7; padding-left: 18px;">
                            <li>4 separate vehicles burning fuel on the same Varanasi corridor.</li>
                            <li>High tailpipe emissions (approx. 768g CO₂/km combined).</li>
                            <li>Heavy traffic bottlenecks at Lanka, Sigra, and Cantt.</li>
                            <li>Spare vehicles sit idle at home 95% of the day.</li>
                            <li>High travel expense: ₹140 - ₹200 per solo cab ride.</li>
                        </ul>
                    </div>

                    <div class="comparison-col greenride">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <span style="font-weight: 800; color: #065F46; font-size: 0.9rem; text-transform: uppercase;">
                                ✅ GREENRIDE Community Mobility
                            </span>
                            <span style="font-size: 1.5rem;">⚡🚗👥👥👥👥</span>
                        </div>
                        <h3 style="font-size: 1.3rem; font-weight: 700; color: #064E3B; margin-bottom: 8px;">
                            4 People • 1 Shared EV • 75% Less Traffic
                        </h3>
                        <ul style="color: #065F46; font-size: 0.95rem; line-height: 1.7; padding-left: 18px;">
                            <li>Shared route matching combines trips along overlapping corridors.</li>
                            <li>Zero direct tailpipe emissions & cleaner local air quality.</li>
                            <li>3 cars removed from the road, easing city traffic.</li>
                            <li>Spare vehicle owner earns passive income (70/30 split).</li>
                            <li>Affordable shared fare: only ₹35 - ₹55 per passenger.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- How GreenRide Works -->
            <div style="margin: 50px 0;">
                <div style="text-align: center; margin-bottom: 36px;">
                    <span class="brand-badge">THREE-WAY COMMUNITY ECOSYSTEM</span>
                    <h2 style="font-size: 2rem; font-weight: 800; color: #0F172A; margin: 8px 0;">
                        How GreenRide Works for Everyone
                    </h2>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
                    <!-- Passenger -->
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 28px; box-shadow: var(--shadow-sm);">
                        <div style="font-size: 2.2rem; margin-bottom: 12px;">👤</div>
                        <h3 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 8px;">
                            1. Passengers
                        </h3>
                        <p style="color: #64748B; font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                            Find shared rides along your regular route. View route overlap score, split the travel fare, and track your CO₂ savings in real time.
                        </p>
                        <div style="background: #F8FAFC; border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #334155;">
                            🔍 Search Route → 🤝 Match Carpool → ⚡ Travel Clean
                        </div>
                    </div>

                    <!-- Driver -->
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 28px; box-shadow: var(--shadow-sm);">
                        <div style="font-size: 2.2rem; margin-bottom: 12px;">🚗</div>
                        <h3 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 8px;">
                            2. Drivers
                        </h3>
                        <p style="color: #64748B; font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                            Access employment opportunities even if you don't own an expensive vehicle. Get matched with spare vehicles and earn dignified income.
                        </p>
                        <div style="background: #F8FAFC; border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #334155;">
                            📋 Verified License → 🔑 Partner Vehicle → 💰 Fair Earnings
                        </div>
                    </div>

                    <!-- Vehicle Owner -->
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 28px; box-shadow: var(--shadow-sm);">
                        <div style="font-size: 2.2rem; margin-bottom: 12px;">🔑</div>
                        <h3 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 8px;">
                            3. Spare Vehicle Owners
                        </h3>
                        <p style="color: #64748B; font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                            Your vehicle sits parked during work hours. List it on GreenRide to be operated by background-verified drivers with transparent revenue splits.
                        </p>
                        <div style="background: #F8FAFC; border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #334155;">
                            🛋️ Idle Asset → 👥 Verified Driver Match → 📈 Passive Revenue
                        </div>
                    </div>
                </div>
            </div>

            <!-- Diverse Mobility Modes -->
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 36px; margin: 40px 0;">
                <div style="text-align: center; margin-bottom: 28px;">
                    <span class="brand-badge">MULTIMODAL SUSTAINABILITY</span>
                    <h2 style="font-size: 1.8rem; font-weight: 800; color: #0F172A; margin: 8px 0;">
                        One Platform. Many Ways to Move.
                    </h2>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px;">
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; text-align: center;">
                        <div style="font-size: 2rem;">⚡🚗</div>
                        <div style="font-weight: 800; margin: 8px 0 4px;">EV CARPOOL</div>
                        <div style="font-size: 0.8rem; color: #059669; font-weight: 600;">👥 3-4 SEATS • LONG DISTANCE</div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">Tata Nexon EV, MG ZS EV for intercity and college corridor commutes.</div>
                    </div>
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; text-align: center;">
                        <div style="font-size: 2rem;">⚡🛺</div>
                        <div style="font-weight: 800; margin: 8px 0 4px;">E-AUTO POOL</div>
                        <div style="font-size: 0.8rem; color: #D97706; font-weight: 600;">👥 3 SEATS • LAST-MILE</div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">Shared electric 3-wheelers navigating narrow ghats and bustling markets.</div>
                    </div>
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; text-align: center;">
                        <div style="font-size: 2rem;">⚡🛵</div>
                        <div style="font-weight: 800; margin: 8px 0 4px;">E-SCOOTER SHIFT</div>
                        <div style="font-size: 0.8rem; color: #0284C7; font-weight: 600;">👤 1 RIDER • QUICK ERRAND</div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">Zero-emission 2-wheelers for fast single-commuter campus links.</div>
                    </div>
                    <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; text-align: center;">
                        <div style="font-size: 2rem;">🚐⚡</div>
                        <div style="font-weight: 800; margin: 8px 0 4px;">COMMUNITY SHUTTLE</div>
                        <div style="font-size: 0.8rem; color: #7C3AED; font-weight: 600;">👥 8-12 SEATS • CAMPUS</div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">Scheduled high-occupancy EV shuttles for BHU campus scholars and staff.</div>
                    </div>
                </div>
            </div>
        </div>
    `,

    // 2. FIND A SHARED RIDE VIEW (Interactive Map + Route Overlap Cards)
    renderFindRide: (ridesData) => {
        const rides = (ridesData && ridesData.rides) || [];
        const count = rides.length;
        const origin = (ridesData && ridesData.searched_origin) || 'Lanka, Varanasi';
        const dest = (ridesData && ridesData.searched_destination) || 'Varanasi Cantt Station';

        return `
            <div class="container" style="padding-top: 16px;">
                <!-- Header with Quick Filter -->
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 20px 24px; box-shadow: var(--shadow-sm); margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                        <div>
                            <span class="match-badge">Intelligent Corridor Matching</span>
                            <h2 style="font-size: 1.45rem; font-weight: 800; color: #0F172A; margin-top: 4px;">
                                Shared Rides: <span style="color: #059669;">${origin.split(',')[0]}</span> → <span style="color: #0284C7;">${dest.split(',')[0]}</span>
                            </h2>
                            <p style="font-size: 0.9rem; color: #64748B;">
                                Found <strong>${count}</strong> verified low-impact rides along this corridor.
                            </p>
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <button onclick="window.app.reSearch()" class="btn btn-secondary" style="font-size: 0.85rem; padding: 8px 16px;">
                                🔄 Modify Search
                            </button>
                            <button onclick="window.demoTour.startTour()" class="btn btn-outline-primary" style="font-size: 0.85rem; padding: 8px 16px;">
                                ✨ Technofest Tour
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Explorer Split: Cards on Left, Map on Right -->
                <div class="map-ride-explorer">
                    <!-- Left: Rides List -->
                    <div class="rides-list-panel">
                        ${rides.length === 0 ? `
                            <div style="text-align: center; padding: 60px 20px; background: #fff; border-radius: 16px; border: 1px dashed #CBD5E1;">
                                <div style="font-size: 2.5rem; margin-bottom: 12px;">🌱</div>
                                <h3 style="font-size: 1.2rem; font-weight: 700; color: #0F172A;">No direct rides at this exact moment</h3>
                                <p style="color: #64748B; font-size: 0.9rem; margin: 8px 0 16px;">
                                    Try searching for Lanka, Assi Ghat, BHU, or Cantt Railway Station.
                                </p>
                                <button onclick="window.app.loadDemoRides()" class="btn btn-primary" style="padding: 8px 18px; font-size: 0.9rem;">
                                    Load Varanasi Corridor Rides
                                </button>
                            </div>
                        ` : rides.map(r => `
                            <div class="ride-card" id="card-${r.id}" onclick="window.app.highlightRide('${r.id}')">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                                    <span class="match-badge">
                                        ⚡ ${r.route_match_score}% Route Match
                                    </span>
                                    <span style="font-size: 1.25rem; font-weight: 800; color: #0F172A;">
                                        ₹${r.price_per_seat}<span style="font-size: 0.75rem; font-weight: 500; color: #64748B;">/seat</span>
                                    </span>
                                </div>

                                <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
                                    ${r.vehicle_title}
                                </h3>

                                <div style="font-size: 0.85rem; color: #475569; margin-bottom: 10px;">
                                    ${r.match_reason}
                                </div>

                                <!-- Route Waypoints -->
                                <div style="background: #F8FAFC; border-radius: 8px; padding: 10px; font-size: 0.82rem; margin-bottom: 12px;">
                                    <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                                        <span style="color: #059669; font-weight: 700;">🟢</span>
                                        <strong>From:</strong> ${r.origin_name}
                                    </div>
                                    <div style="display: flex; align-items: center; gap: 6px;">
                                        <span style="color: #DC2626; font-weight: 700;">🔴</span>
                                        <strong>To:</strong> ${r.dest_name}
                                    </div>
                                </div>

                                <!-- Driver & Vehicle Badges -->
                                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 14px;">
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <img src="${r.driver_avatar || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100'}" alt="Driver" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;" />
                                        <div>
                                            <div style="font-size: 0.85rem; font-weight: 700; color: #0F172A;">
                                                ${r.driver_name} ${r.driver_verified ? '🛡️' : ''}
                                            </div>
                                            <div style="font-size: 0.75rem; color: #64748B;">
                                                ⭐ ${r.driver_rating} (${r.driver_experience || 3} yrs exp)
                                            </div>
                                        </div>
                                    </div>

                                    <div style="text-align: right;">
                                        <div style="font-size: 0.75rem; font-weight: 700; color: #059669;">
                                            🌱 Saves ${r.co2_saved_kg} kg CO₂
                                        </div>
                                        <div style="font-size: 0.75rem; color: #64748B;">
                                            👥 ${r.available_seats} of ${r.total_seats} seats left
                                        </div>
                                    </div>
                                </div>

                                <!-- Action Buttons -->
                                <div style="display: flex; gap: 8px;">
                                    <button onclick="window.app.openBookingModal('${r.id}')" class="btn btn-primary" style="flex: 1; padding: 10px; font-size: 0.9rem;">
                                        Reserve Seat
                                    </button>
                                    <button onclick="window.app.trackRideLive('${r.id}')" class="btn btn-secondary" style="padding: 10px 14px; font-size: 0.9rem;" title="View Live Vehicle Tracking">
                                        📡 Live Map
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <!-- Right: Leaflet Map Container -->
                    <div class="map-container">
                        <div id="leaflet-map"></div>
                        <div style="position: absolute; bottom: 16px; left: 16px; z-index: 500; background: rgba(255,255,255,0.92); backdrop-filter: blur(4px); padding: 8px 14px; border-radius: 8px; border: 1px solid #CBD5E1; font-size: 0.78rem; display: flex; gap: 12px; align-items: center;">
                            <span>⚡🚗 <strong>Green:</strong> EV Car</span>
                            <span>⚡🛺 <strong>Amber:</strong> E-Auto</span>
                            <span>⚡🛵 <strong>Cyan:</strong> E-Scooter</span>
                            <span>📍 <strong>Blue:</strong> Your Route</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    // 3. LIVE RIDE TRACKING VIEW (Vehicle movement simulation, SOS alert, Rating)
    renderLiveTracking: (ride) => `
        <div class="container" style="padding-top: 16px;">
            <div style="display: grid; grid-template-columns: 440px 1fr; gap: 24px; min-height: 650px;">
                <!-- Telemetry & Ride Card -->
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 24px; box-shadow: var(--shadow-md); display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <span class="demo-badge" style="background: #ECFDF5; border-color: #10B981; color: #047857;">
                                🟢 LIVE TRACKING IN PROGRESS
                            </span>
                            <span style="font-size: 0.8rem; color: #64748B;">
                                Status: <strong>${ride.status.toUpperCase()}</strong>
                            </span>
                        </div>

                        <h2 style="font-size: 1.4rem; font-weight: 800; color: #0F172A; margin-bottom: 4px;">
                            ${ride.vehicle_title}
                        </h2>
                        <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 16px;">
                            Registration: <strong>${ride.reg_number}</strong> • Pure Electric
                        </div>

                        <!-- Driver Info -->
                        <div style="background: #F8FAFC; border-radius: 12px; padding: 14px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;">
                            <img src="${ride.driver_avatar || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100'}" alt="Driver" style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover;" />
                            <div>
                                <div style="font-weight: 800; color: #0F172A; font-size: 1rem;">
                                    ${ride.driver_name} 🛡️
                                </div>
                                <div style="font-size: 0.8rem; color: #64748B;">
                                    Police Verified • ⭐ ${ride.driver_rating} Rating
                                </div>
                                <div style="font-size: 0.78rem; color: #059669; font-weight: 600; margin-top: 2px;">
                                    📞 ${ride.driver_phone || '+91 98111 22334'}
                                </div>
                            </div>
                        </div>

                        <!-- Corridor Progress -->
                        <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
                            <div style="font-size: 0.75rem; font-weight: 700; color: #065F46; text-transform: uppercase;">
                                Active Travel Corridor
                            </div>
                            <div style="font-size: 0.95rem; font-weight: 700; color: #064E3B; margin: 4px 0;">
                                ${ride.origin_name.split(',')[0]} ➔ ${ride.dest_name.split(',')[0]}
                            </div>
                            <div style="font-size: 0.8rem; color: #047857;">
                                🌱 Saving <strong>${ride.co2_savings_kg} kg CO₂</strong> on this trip!
                            </div>
                        </div>

                        <!-- Exhibition Simulation Controls -->
                        <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 12px; padding: 14px; margin-bottom: 20px;">
                            <div style="font-size: 0.8rem; font-weight: 800; color: #92400E; margin-bottom: 6px;">
                                🕹️ Technofest Simulation Tool:
                            </div>
                            <p style="font-size: 0.8rem; color: #78350F; margin-bottom: 10px;">
                                Advance vehicle telemetry on the map to demonstrate live tracking to judges.
                            </p>
                            <button onclick="window.app.advanceSimulationStep('${ride.id}')" class="btn btn-primary" style="width: 100%; font-size: 0.85rem; padding: 8px;">
                                ⏩ Advance Vehicle 20% Along Route
                            </button>
                        </div>
                    </div>

                    <!-- Bottom Safety & Complete Actions -->
                    <div>
                        <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                            <button onclick="window.app.completeRideDemo('${ride.id}')" class="btn btn-secondary" style="flex: 1; font-size: 0.85rem; padding: 10px;">
                                ✅ Finish & Rate Trip
                            </button>
                            <button onclick="window.app.triggerSOSDemo('${ride.id}')" class="btn btn-danger" style="padding: 10px 16px; font-size: 0.85rem;" title="Simulate Emergency SOS Alert">
                                🚨 SOS
                            </button>
                        </div>
                        <div style="font-size: 0.72rem; color: #94A3B8; text-align: center;">
                            Safety tracking encrypted with 24/7 GreenRide Operations Room beacon.
                        </div>
                    </div>
                </div>

                <!-- Leaflet Map Live View -->
                <div class="map-container">
                    <div id="leaflet-map"></div>
                </div>
            </div>
        </div>
    `,

    // 4. DRIVER OPERATIONS DASHBOARD
    renderDriverDashboard: (data) => {
        const profile = data.profile || {};
        const earnings = data.earnings || {};
        const assignedVeh = profile.assigned_vehicle || {};

        return `
            <div class="container">
                <!-- Driver Header Card -->
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 24px; box-shadow: var(--shadow-sm); margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <img src="${profile.avatar || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150'}" alt="Driver" style="width: 64px; height: 64px; border-radius: 50%; object-fit: cover; border: 3px solid #10B981;" />
                            <div>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <h2 style="font-size: 1.45rem; font-weight: 800; color: #0F172A;">
                                        ${profile.name || 'Rahul Kumar'}
                                    </h2>
                                    <span class="match-badge">Verified Partner</span>
                                </div>
                                <div style="font-size: 0.85rem; color: #64748B;">
                                    License: <strong>${profile.license_number || 'UP-65-2019-008129'}</strong> • ⭐ ${profile.rating || 4.92} Rating (${profile.trips_completed || 184} Trips)
                                </div>
                            </div>
                        </div>

                        <!-- Online / Offline Toggle -->
                        <div style="display: flex; align-items: center; gap: 12px; background: #F8FAFC; padding: 8px 16px; border-radius: var(--radius-full); border: 1px solid #E2E8F0;">
                            <span style="font-size: 0.9rem; font-weight: 700; color: ${profile.is_online ? '#059669' : '#94A3B8'};">
                                ${profile.is_online ? '● Online & Accepting Carpools' : '○ Offline'}
                            </span>
                            <button onclick="window.app.toggleDriverOnline(${!profile.is_online})" class="btn ${profile.is_online ? 'btn-secondary' : 'btn-primary'}" style="padding: 6px 14px; font-size: 0.8rem;">
                                ${profile.is_online ? 'Go Offline' : 'Go Online'}
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Earnings & Metrics Grid -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px;">
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 20px;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Today's Payout</div>
                        <div class="stat-value" style="color: #059669;">₹${earnings.today_earnings_inr || '1,240'}</div>
                        <div style="font-size: 0.75rem; color: #10B981;">+ ₹210 vs yesterday</div>
                    </div>
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 20px;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Total Net Earnings</div>
                        <div class="stat-value">₹${earnings.net_driver_earnings_inr ? earnings.net_driver_earnings_inr.toLocaleString() : '24,150'}</div>
                        <div style="font-size: 0.75rem; color: #64748B;">Direct bank / UPI transfers</div>
                    </div>
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 20px;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Green Mobility Bonus</div>
                        <div class="stat-value" style="color: #0284C7;">₹${earnings.green_mobility_bonus_inr || '850'}</div>
                        <div style="font-size: 0.75rem; color: #0284C7;">Zero-emission incentive reward</div>
                    </div>
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 20px;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Completed Trips</div>
                        <div class="stat-value">${earnings.total_trips || '184'}</div>
                        <div style="font-size: 0.75rem; color: #64748B;">4.92 Customer Satisfaction</div>
                    </div>
                </div>

                <!-- Assigned Vehicle & Route Offer -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                    <!-- Assigned Spare Vehicle -->
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 24px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                            <h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">Assigned Vehicle</h3>
                            <span class="match-badge">Community Partnership</span>
                        </div>
                        ${assignedVeh.id ? `
                            <div style="display: flex; gap: 16px; align-items: center; margin-bottom: 16px;">
                                <img src="${assignedVeh.photo_url || 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=200'}" alt="Car" style="width: 90px; height: 70px; border-radius: 8px; object-fit: cover;" />
                                <div>
                                    <h4 style="font-size: 1.1rem; font-weight: 700; color: #0F172A;">${assignedVeh.title}</h4>
                                    <div style="font-size: 0.8rem; color: #64748B;">Reg: <strong>${assignedVeh.reg_number}</strong> • Range: <strong>${assignedVeh.ev_range_km} km</strong></div>
                                    <div style="font-size: 0.8rem; color: #059669; font-weight: 600;">Owner: ${assignedVeh.owner_name} (${assignedVeh.owner_share_pct || 70}% / ${assignedVeh.driver_share_pct || 30}% Split)</div>
                                </div>
                            </div>
                            <div style="background: #ECFDF5; border-radius: 8px; padding: 10px; font-size: 0.82rem; color: #065F46;">
                                💡 You do not need to pay vehicle purchase loans. You operate this vehicle and keep your 30% direct fare split on every completed ride!
                            </div>
                        ` : `
                            <div style="text-align: center; padding: 24px; color: #64748B;">
                                <p style="margin-bottom: 12px;">You currently have no partner vehicle assigned.</p>
                                <button onclick="window.app.navigate('marketplace')" class="btn btn-primary" style="font-size: 0.85rem; padding: 8px 16px;">
                                    Browse Spare Vehicles in Marketplace
                                </button>
                            </div>
                        `}
                    </div>

                    <!-- Offer a Ride Form -->
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 24px;">
                        <h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 14px;">
                            Publish Scheduled Shared Route
                        </h3>
                        <form onsubmit="window.app.handleCreateRide(event)">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                                <div>
                                    <label class="form-label">Pickup Point</label>
                                    <input type="text" id="offer-orig" class="form-input" value="Lanka Chauraha" required />
                                </div>
                                <div>
                                    <label class="form-label">Destination</label>
                                    <input type="text" id="offer-dest" class="form-input" value="BHU Gate" required />
                                </div>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                                <div>
                                    <label class="form-label">Time</label>
                                    <input type="text" id="offer-time" class="form-input" value="09:30 AM" required />
                                </div>
                                <div>
                                    <label class="form-label">Seats</label>
                                    <input type="number" id="offer-seats" class="form-input" value="3" min="1" max="4" required />
                                </div>
                                <div>
                                    <label class="form-label">Fare/Seat</label>
                                    <input type="number" id="offer-price" class="form-input" value="35" min="15" required />
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; padding: 10px;">
                                🚀 Publish Shared Ride to Commuters
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        `;
    },

    // 5. VEHICLE OWNER DASHBOARD
    renderOwnerDashboard: (vehicles) => `
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 24px;">
                <div>
                    <span class="brand-badge">SPARE VEHICLE ASSET HOSTING</span>
                    <h2 style="font-size: 1.8rem; font-weight: 800; color: #0F172A; margin-top: 4px;">
                        Vehicle Owner Dashboard: Vikram Singh
                    </h2>
                    <p style="color: #64748B; font-size: 0.95rem;">
                        Your spare vehicles are active sources of income instead of sitting idle.
                    </p>
                </div>
                <button onclick="window.app.openAddVehicleModal()" class="btn btn-primary">
                    ➕ List Another Spare Vehicle
                </button>
            </div>

            <!-- Revenue Summary Banner -->
            <div style="background: linear-gradient(135deg, #064E3B 0%, #0F172A 100%); color: #FFFFFF; border-radius: var(--radius-xl); padding: 28px; margin-bottom: 28px; box-shadow: var(--shadow-lg);">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                    <div>
                        <div style="font-size: 0.8rem; text-transform: uppercase; color: #A7F3D0; font-weight: 700;">Monthly Asset Income</div>
                        <div style="font-size: 2.2rem; font-weight: 800; margin: 4px 0;">₹18,450</div>
                        <div style="font-size: 0.8rem; color: #D1FAE5;">From 70% revenue split</div>
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; text-transform: uppercase; color: #A7F3D0; font-weight: 700;">Idle Hours Monetized</div>
                        <div style="font-size: 2.2rem; font-weight: 800; margin: 4px 0;">196 hrs</div>
                        <div style="font-size: 0.8rem; color: #D1FAE5;">Saved from depreciating parked</div>
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; text-transform: uppercase; color: #A7F3D0; font-weight: 700;">Emissions Avoided</div>
                        <div style="font-size: 2.2rem; font-weight: 800; margin: 4px 0;">284 kg</div>
                        <div style="font-size: 0.8rem; color: #D1FAE5;">By powering shared rides</div>
                    </div>
                    <div>
                        <div style="font-size: 0.8rem; text-transform: uppercase; color: #A7F3D0; font-weight: 700;">Partner Driver</div>
                        <div style="font-size: 1.4rem; font-weight: 800; margin: 8px 0 4px;">Rahul Kumar 🛡️</div>
                        <div style="font-size: 0.8rem; color: #D1FAE5;">4.92 Rating • 184 Trips</div>
                    </div>
                </div>
            </div>

            <!-- Vehicles List -->
            <h3 style="font-size: 1.3rem; font-weight: 800; color: #0F172A; margin-bottom: 16px;">
                Your Listed Vehicles (${vehicles.length})
            </h3>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
                ${vehicles.map(v => `
                    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 24px; box-shadow: var(--shadow-sm);">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span class="match-badge" style="background: ${v.status === 'assigned' ? '#ECFDF5' : '#FEF3C7'}; color: ${v.status === 'assigned' ? '#065F46' : '#92400E'};">
                                ${v.status === 'assigned' ? '● Active in Service' : '○ Seeking Driver in Marketplace'}
                            </span>
                            <span style="font-size: 0.75rem; font-weight: 700; color: #64748B;">
                                ${v.fuel_type}
                            </span>
                        </div>

                        <img src="${v.photo_url || 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400'}" alt="Vehicle" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px; margin-bottom: 14px;" />

                        <h4 style="font-size: 1.2rem; font-weight: 800; color: #0F172A; margin-bottom: 4px;">
                            ${v.title}
                        </h4>
                        <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 14px;">
                            Reg: <strong>${v.reg_number}</strong> • Range: <strong>${v.ev_range_km} km</strong> • Seats: <strong>${v.seats}</strong>
                        </div>

                        <div style="background: #F8FAFC; border-radius: 8px; padding: 12px; font-size: 0.82rem; margin-bottom: 16px;">
                            <div><strong>Revenue Model:</strong> ${v.revenue_share_owner}% Owner / ${v.revenue_share_driver}% Driver</div>
                            <div><strong>Assigned Driver:</strong> ${v.assigned_driver_name ? `${v.assigned_driver_name} (⭐ ${v.assigned_driver_rating})` : '<em style="color:#D97706;">None yet (Available in Marketplace)</em>'}</div>
                        </div>

                        <div style="display: flex; gap: 8px;">
                            <button onclick="window.app.toggleVehicleSeeking('${v.id}')" class="btn btn-secondary" style="flex: 1; font-size: 0.85rem; padding: 8px;">
                                ${v.seeking_driver ? 'Pause Seeking' : 'Seek Verified Driver'}
                            </button>
                            <button onclick="window.app.navigate('marketplace')" class="btn btn-outline-primary" style="font-size: 0.85rem; padding: 8px 12px;">
                                🤝 Match
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `,

    // 6. DRIVER + VEHICLE MARKETPLACE VIEW
    renderMarketplace: (data) => {
        const vehicles = data.vehicles || [];
        const drivers = data.drivers || [];
        const partnerships = data.partnerships || [];

        return `
            <div class="container">
                <div style="text-align: center; max-width: 760px; margin: 0 auto 36px;">
                    <span class="brand-badge">EMPLOYMENT & ASSET SHARING EXCHANGE</span>
                    <h2 style="font-size: 2.2rem; font-weight: 800; color: #0F172A; margin: 8px 0;">
                        Driver + Spare Vehicle Marketplace
                    </h2>
                    <p style="color: #64748B; font-size: 1.05rem;">
                        Connecting vehicle owners with spare EVs to verified drivers seeking livelihoods. Creating employment without demanding vehicle purchase debt.
                    </p>
                </div>

                <!-- Matchmaker Interactive Action Card -->
                <div style="background: #FFFFFF; border: 2px solid #10B981; border-radius: var(--radius-xl); padding: 28px; box-shadow: var(--shadow-lg); margin-bottom: 36px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span class="match-badge">Technofest Interactive Action</span>
                            <h3 style="font-size: 1.3rem; font-weight: 800; color: #0F172A; margin-top: 4px;">
                                Form a New Community Mobility Partnership
                            </h3>
                        </div>
                        <span style="font-size: 0.85rem; color: #059669; font-weight: 700;">
                            ✨ Zero Capital Barrier for Drivers
                        </span>
                    </div>

                    <form onsubmit="window.app.handleMarketplaceMatch(event)">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                            <div>
                                <label class="form-label" for="match-vehicle">Select Spare Vehicle</label>
                                <select id="match-vehicle" class="form-select" required>
                                    ${vehicles.map(v => `
                                        <option value="${v.id}">${v.title} (${v.reg_number}) - Owner: ${v.owner_name}</option>
                                    `).join('')}
                                </select>
                            </div>
                            <div>
                                <label class="form-label" for="match-driver">Select Verified Driver</label>
                                <select id="match-driver" class="form-select" required>
                                    ${drivers.map(d => `
                                        <option value="${d.user_id}">${d.driver_name} (⭐ ${d.rating} • ${d.experience_years} yrs exp)</option>
                                    `).join('')}
                                </select>
                            </div>
                        </div>

                        <!-- Revenue Split Configurator -->
                        <div class="split-slider-container">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-size: 0.85rem; font-weight: 700; color: #0F172A;">Configurable Revenue Split:</span>
                                <span id="split-label" style="font-size: 0.95rem; font-weight: 800; color: #059669;">
                                    70% Vehicle Owner / 30% Driver
                                </span>
                            </div>
                            <input type="range" id="split-slider" min="40" max="80" value="70" step="5" style="width: 100%; accent-color: #059669;" oninput="window.app.updateSplitLabel(this.value)" />
                            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748B; margin-top: 4px;">
                                <span>Higher Driver Share (40/60)</span>
                                <span>Standard Demo (70/30)</span>
                                <span>Higher Owner Share (80/20)</span>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 14px; font-size: 1rem;">
                            🤝 FORM COMMUNITY PARTNERSHIP & ASSIGN VEHICLE
                        </button>
                    </form>
                </div>

                <!-- Two Column Lists: Vehicles & Drivers -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 36px;">
                    <!-- Vehicles Column -->
                    <div>
                        <h3 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 14px;">
                            ⚡ Spare Vehicles Available (${vehicles.length})
                        </h3>
                        <div style="display: flex; flex-direction: column; gap: 14px;">
                            ${vehicles.map(v => `
                                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 18px; box-shadow: var(--shadow-sm);">
                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                                        <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A;">${v.title}</h4>
                                        <span class="match-badge">Available</span>
                                    </div>
                                    <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 8px;">
                                        Location: <strong>${v.locality}</strong> • Battery: <strong>${v.battery_kwh} kWh</strong> • Reg: <strong>${v.reg_number}</strong>
                                    </div>
                                    <div style="font-size: 0.8rem; color: #059669;">
                                        Owner: <strong>${v.owner_name}</strong> (⭐ ${v.owner_rating || 5.0})
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Drivers Column -->
                    <div>
                        <h3 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 14px;">
                            👥 Drivers Seeking Opportunities (${drivers.length})
                        </h3>
                        <div style="display: flex; flex-direction: column; gap: 14px;">
                            ${drivers.map(d => `
                                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 18px; box-shadow: var(--shadow-sm);">
                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                                        <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A;">${d.driver_name} 🛡️</h4>
                                        <span class="match-badge" style="background:#EFF6FF; color:#1D4ED8;">DL Verified</span>
                                    </div>
                                    <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 8px;">
                                        Experience: <strong>${d.experience_years} years</strong> • Area: <strong>${d.preferred_area || 'Varanasi'}</strong>
                                    </div>
                                    <div style="font-size: 0.8rem; color: #0284C7;">
                                        License: <strong>${d.license_number}</strong> • Rating: ⭐ ${d.rating}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <!-- Active Partnerships Stream -->
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 28px; box-shadow: var(--shadow-sm);">
                    <h3 style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-bottom: 16px;">
                        Live Active Partnerships (${partnerships.length})
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 12px;">
                        ${partnerships.map(p => `
                            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                                <div>
                                    <div style="font-size: 0.95rem; font-weight: 800; color: #0F172A;">
                                        ${p.vehicle_title} (${p.reg_number})
                                    </div>
                                    <div style="font-size: 0.8rem; color: #64748B;">
                                        Owner: <strong>${p.owner_name}</strong> ➔ Driven by: <strong>${p.driver_name}</strong>
                                    </div>
                                </div>
                                <div style="text-align: right;">
                                    <span class="match-badge">${p.owner_share_pct}% Owner / ${p.driver_share_pct}% Driver</span>
                                    <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">Assigned: ${p.assigned_at ? p.assigned_at.split(' ')[0] : 'Active'}</div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    },

    // 7. SUSTAINABILITY IMPACT DASHBOARD (Planet, People, Prosperity)
    renderImpactDashboard: (impactData) => {
        const p = impactData.planet || {};
        const peo = impactData.people || {};
        const pro = impactData.prosperity || {};
        const period = impactData.period || 'all';

        return `
            <div class="container">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 24px;">
                    <div>
                        <span class="brand-badge">THREE-DIMENSIONAL IMPACT METRICS</span>
                        <h2 style="font-size: 2.2rem; font-weight: 800; color: #0F172A; margin-top: 4px;">
                            GreenRide Sustainability Dashboard
                        </h2>
                        <p style="color: #64748B; font-size: 1rem;">
                            Quantifying real environmental, social, and economic change in Varanasi.
                        </p>
                    </div>

                    <!-- Period Filter Tabs -->
                    <div style="display: flex; gap: 6px; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 4px; border-radius: var(--radius-full); box-shadow: var(--shadow-sm);">
                        ${['today', 'week', 'month', 'all'].map(t => `
                            <button onclick="window.app.loadImpact('${t}')" style="background: ${period === t ? '#059669' : 'transparent'}; color: ${period === t ? '#FFFFFF' : '#475569'}; border: none; padding: 6px 16px; border-radius: var(--radius-full); font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: all 0.2s;">
                                ${t.toUpperCase()}
                            </button>
                        `).join('')}
                    </div>
                </div>

                <!-- 3 Pillars Grid -->
                <div class="pillars-grid">
                    <!-- PLANET -->
                    <div class="pillar-card planet">
                        <span class="brand-badge" style="background: #ECFDF5; border-color: #10B981; color: #047857;">
                            🌱 PLANET (ENVIRONMENT)
                        </span>
                        <div class="stat-value" style="color: #065F46;">
                            ${p.co2_avoided_kg ? p.co2_avoided_kg.toLocaleString() : '1,960'} <span style="font-size: 1rem; font-weight: 600;">kg</span>
                        </div>
                        <div style="font-weight: 700; color: #0F172A; margin-bottom: 8px;">Estimated CO₂ Avoided</div>
                        <p style="font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-bottom: 16px;">
                            Equivalent to planting <strong>${p.trees_equivalent || 93}</strong> mature trees absorbing emissions along the Ganges corridor.
                        </p>
                        <div style="background: #F8FAFC; border-radius: 8px; padding: 10px; font-size: 0.8rem; color: #334155;">
                            <div>🛣️ <strong>${(p.vehicle_km_avoided || 11928).toLocaleString()} km</strong> duplicate trips saved</div>
                            <div>⚡ <strong>${(p.zero_emission_ev_km || 13700).toLocaleString()} km</strong> powered by clean electricity</div>
                        </div>
                    </div>

                    <!-- PEOPLE -->
                    <div class="pillar-card people">
                        <span class="brand-badge" style="background: #EFF6FF; border-color: #38BDF8; color: #0284C7;">
                            👥 PEOPLE (SOCIAL MOBILITY)
                        </span>
                        <div class="stat-value" style="color: #0284C7;">
                            ${(peo.people_connected || 3890).toLocaleString()}
                        </div>
                        <div style="font-weight: 700; color: #0F172A; margin-bottom: 8px;">Commuters Connected</div>
                        <p style="font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-bottom: 16px;">
                            Empowering scholars, healthcare workers, and pilgrims with dependable, safe, verified community carpools.
                        </p>
                        <div style="background: #F8FAFC; border-radius: 8px; padding: 10px; font-size: 0.8rem; color: #334155;">
                            <div>💼 <strong>${peo.verified_drivers_employed || 28}</strong> verified driver jobs created</div>
                            <div>🎓 <strong>${(peo.student_commuters_supported || 1750).toLocaleString()}</strong> BHU student commutes shared</div>
                        </div>
                    </div>

                    <!-- PROSPERITY -->
                    <div class="pillar-card prosperity">
                        <span class="brand-badge" style="background: #FEF3C7; border-color: #F59E0B; color: #B45309;">
                            💰 PROSPERITY (CIRCULAR ECONOMY)
                        </span>
                        <div class="stat-value" style="color: #D97706;">
                            ₹${(pro.passenger_savings_inr || 96560).toLocaleString()}
                        </div>
                        <div style="font-weight: 700; color: #0F172A; margin-bottom: 8px;">Commuter Travel Savings</div>
                        <p style="font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-bottom: 16px;">
                            Money retained by local citizens compared to private solo surge-priced taxis.
                        </p>
                        <div style="background: #F8FAFC; border-radius: 8px; padding: 10px; font-size: 0.8rem; color: #334155;">
                            <div>💵 <strong>₹${(pro.driver_income_inr || 177500).toLocaleString()}</strong> driver income earned</div>
                            <div>🔑 <strong>₹${(pro.vehicle_owner_income_inr || 262700).toLocaleString()}</strong> earned by spare vehicle owners</div>
                        </div>
                    </div>
                </div>

                <!-- Historical Growth Chart -->
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 32px; margin-top: 32px; box-shadow: var(--shadow-sm);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div>
                            <h3 style="font-size: 1.25rem; font-weight: 800; color: #0F172A;">
                                Cumulative Monthly CO₂ Emissions Avoided (kg)
                            </h3>
                            <p style="font-size: 0.85rem; color: #64748B;">
                                Demonstrating exponential impact as more community members share journeys.
                            </p>
                        </div>
                        <span class="match-badge">Technofest Verified Data</span>
                    </div>
                    <div style="height: 320px; width: 100%;">
                        <canvas id="impact-chart"></canvas>
                    </div>
                </div>
            </div>
        `;
    },

    // 8. ADMIN OPERATIONS DASHBOARD
    renderAdminDashboard: (metrics, pendingDrivers, pendingVehicles, reports) => `
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 24px;">
                <div>
                    <span class="brand-badge">GREENRIDE OPERATIONS HQ</span>
                    <h2 style="font-size: 1.8rem; font-weight: 800; color: #0F172A; margin-top: 4px;">
                        Platform Administration & Safety Oversight
                    </h2>
                    <p style="color: #64748B; font-size: 0.95rem;">
                        Admin: Pooja Verma (Head of Mobility Operations, Varanasi)
                    </p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button onclick="window.app.resetDemoData()" class="btn btn-secondary" style="font-size: 0.85rem;">
                        🔄 Reset Demo Data
                    </button>
                    <span class="demo-badge" style="background:#ECFDF5; color:#065F46; padding: 8px 14px;">
                        Status: Healthy (99.98% Uptime)
                    </span>
                </div>
            </div>

            <!-- Stats Overview -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 28px;">
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 18px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Total Users</div>
                    <div class="stat-value" style="font-size: 1.8rem;">${metrics.total_users || 7}</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 18px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Active EV Drivers</div>
                    <div class="stat-value" style="font-size: 1.8rem; color: #059669;">${metrics.active_drivers || 3}</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 18px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Registered Vehicles</div>
                    <div class="stat-value" style="font-size: 1.8rem;">${metrics.total_vehicles || 5}</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 18px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Active Partnerships</div>
                    <div class="stat-value" style="font-size: 1.8rem; color: #0284C7;">${metrics.active_partnerships || 2}</div>
                </div>
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-lg); padding: 18px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Safety Alerts</div>
                    <div class="stat-value" style="font-size: 1.8rem; color: #DC2626;">0 Critical</div>
                </div>
            </div>

            <!-- Verification Queues -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                <!-- Driver Verifications -->
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 24px;">
                    <h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 14px;">
                        Driver Document Verification Queue
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        ${(pendingDrivers || []).map(d => `
                            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-weight: 700; color: #0F172A; font-size: 0.9rem;">${d.name}</div>
                                    <div style="font-size: 0.78rem; color: #64748B;">DL: <strong>${d.license_number}</strong> • Area: ${d.preferred_area || 'Varanasi'}</div>
                                </div>
                                <div>
                                    ${d.is_verified ? `
                                        <span class="match-badge" style="background:#ECFDF5; color:#065F46;">Verified ✓</span>
                                    ` : `
                                        <button onclick="window.app.verifyDriver('${d.id}')" class="btn btn-primary" style="padding: 4px 12px; font-size: 0.78rem;">
                                            Approve
                                        </button>
                                    `}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Vehicle Roadworthiness -->
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: var(--radius-xl); padding: 24px;">
                    <h3 style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 14px;">
                        Vehicle Inspection & Battery Certification
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        ${(pendingVehicles || []).map(v => `
                            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="font-weight: 700; color: #0F172A; font-size: 0.9rem;">${v.title} (${v.reg_number})</div>
                                    <div style="font-size: 0.78rem; color: #64748B;">Owner: ${v.owner_name} • ${v.battery_kwh} kWh Battery</div>
                                </div>
                                <div>
                                    ${v.is_verified ? `
                                        <span class="match-badge" style="background:#ECFDF5; color:#065F46;">Certified ✓</span>
                                    ` : `
                                        <button onclick="window.app.verifyVehicle('${v.id}')" class="btn btn-primary" style="padding: 4px 12px; font-size: 0.78rem;">
                                            Verify
                                        </button>
                                    `}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `
};

