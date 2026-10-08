/**
 * GREENRIDE - Main Application Controller
 * Handles Navigation, State, Role Switching, Simple Mode, Modals, and Microinteractions.
 */

class GreenRideApp {
    constructor() {
        this.currentView = 'home';
        this.activeRide = null;
        this.activeBooking = null;
        this.textScale = 'md';
        this.simpleMode = false;
        this.highContrast = false;
        this.chartInstance = null;
        this.lastSearchResults = null;
    }

    async init() {
        console.log("🌿 Initializing GreenRide Application...");
        
        // Restore user preferences
        if (localStorage.getItem('greenride_simple_mode') === 'true') {
            this.toggleSimpleMode(true);
        }
        if (localStorage.getItem('greenride_high_contrast') === 'true') {
            this.toggleHighContrast(true);
        }

        // Initialize user session (defaults to Passenger Ananya)
        try {
            if (!window.api.currentUser) {
                await window.api.demoSwitch('passenger');
            }
            this.updateHeaderUserInfo();
        } catch (e) {
            console.warn("API switch fallback:", e);
        }

        // Handle URL hash routing
        window.addEventListener('hashchange', () => this.handleRoute());
        this.handleRoute();
    }

    updateHeaderUserInfo() {
        const u = window.api.currentUser;
        if (!u) return;

        const nameEl = document.getElementById('nav-user-name');
        const roleEl = document.getElementById('nav-user-role');
        const avatarEl = document.getElementById('nav-user-avatar');

        if (nameEl) nameEl.textContent = u.name;
        if (roleEl) roleEl.textContent = (u.active_role || 'Passenger').toUpperCase();
        if (avatarEl && u.avatar) avatarEl.src = u.avatar;

        // Highlight active demo button
        document.querySelectorAll('.demo-role-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.role === u.active_role);
        });
    }

    async switchDemoRole(role) {
        try {
            const data = await window.api.demoSwitch(role);
            this.updateHeaderUserInfo();
            this.showToast(`Switched to ${data.role_title}`, 'success');

            // Intelligently route to the role's native dashboard
            if (role === 'passenger') this.navigate('find-ride');
            else if (role === 'driver') this.navigate('driver-dash');
            else if (role === 'owner') this.navigate('owner-dash');
            else if (role === 'admin') this.navigate('admin');
        } catch (err) {
            this.showToast('Could not switch demo role', 'error');
        }
    }

    navigate(viewName, params = {}) {
        window.location.hash = `#${viewName}`;
    }

    async handleRoute() {
        const hash = window.location.hash.replace('#', '') || 'home';
        this.currentView = hash;
        const main = document.getElementById('app-main');
        if (!main) return;

        // Update nav links active state
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === `#${hash}`);
        });

        // View Router
        if (hash === 'home') {
            main.innerHTML = window.components.renderHome();
        } 
        else if (hash === 'find-ride') {
            main.innerHTML = `<div class="container" style="text-align:center;padding:60px;"><div class="stat-value" style="font-size:2rem;color:#059669;">🌿 Loading GreenRide corridors...</div></div>`;
            try {
                const searchRes = this.lastSearchResults || await window.api.searchRides({
                    origin: 'Lanka, Varanasi',
                    destination: 'Varanasi Cantt Station',
                    seats: 1,
                    vehicle_type: 'all'
                });
                this.lastSearchResults = searchRes;
                main.innerHTML = window.components.renderFindRide(searchRes);
                window.mapManager.init();
                window.mapManager.renderRides(searchRes.rides);
                if (searchRes.user_coords) {
                    window.mapManager.renderUserRoute(
                        searchRes.user_coords.origin,
                        searchRes.user_coords.destination,
                        searchRes.searched_origin,
                        searchRes.searched_destination
                    );
                }
            } catch (e) {
                console.error(e);
                main.innerHTML = `<div class="container" style="padding:40px;color:red;">Error loading rides.</div>`;
            }
        }
        else if (hash === 'tracking') {
            if (!this.activeRide) {
                // Fetch first active ride for demo tracking
                const rides = await window.api.listRides();
                this.activeRide = rides[0] || null;
            }
            if (this.activeRide) {
                main.innerHTML = window.components.renderLiveTracking(this.activeRide);
                window.mapManager.init();
                window.mapManager.setupLiveTracking(this.activeRide);
            } else {
                this.navigate('find-ride');
            }
        }
        else if (hash === 'driver-dash') {
            main.innerHTML = `<div class="container" style="text-align:center;padding:60px;"><div class="stat-value" style="font-size:2rem;color:#059669;">🚗 Loading Driver Dashboard...</div></div>`;
            try {
                const profile = await window.api.getDriverProfile();
                const earnings = await window.api.getDriverEarnings();
                main.innerHTML = window.components.renderDriverDashboard({ profile, earnings });
            } catch (e) {
                console.error(e);
            }
        }
        else if (hash === 'owner-dash') {
            main.innerHTML = `<div class="container" style="text-align:center;padding:60px;"><div class="stat-value" style="font-size:2rem;color:#059669;">🔑 Loading Vehicle Owner Dashboard...</div></div>`;
            try {
                const vehicles = await window.api.getMyVehicles();
                main.innerHTML = window.components.renderOwnerDashboard(vehicles);
            } catch (e) {
                console.error(e);
            }
        }
        else if (hash === 'marketplace') {
            main.innerHTML = `<div class="container" style="text-align:center;padding:60px;"><div class="stat-value" style="font-size:2rem;color:#059669;">🤝 Loading Driver + Vehicle Marketplace...</div></div>`;
            try {
                const vehicles = await window.api.getMarketplaceVehicles();
                const drivers = await window.api.getMarketplaceDrivers();
                const partnerships = await window.api.getActivePartnerships();
                main.innerHTML = window.components.renderMarketplace({ vehicles, drivers, partnerships });
            } catch (e) {
                console.error(e);
            }
        }
        else if (hash === 'impact') {
            await this.loadImpact('all');
        }
        else if (hash === 'admin') {
            main.innerHTML = `<div class="container" style="text-align:center;padding:60px;"><div class="stat-value" style="font-size:2rem;color:#059669;">🛡️ Loading GreenRide Admin...</div></div>`;
            try {
                const metrics = await window.api.getAdminMetrics();
                const drivers = await window.api.getAdminDrivers();
                const vehicles = await window.api.getAdminVehicles();
                const reports = await window.api.getAdminReports();
                main.innerHTML = window.components.renderAdminDashboard(metrics, drivers, vehicles, reports);
            } catch (e) {
                console.error(e);
            }
        }

        window.scrollTo(0, 0);
    }

    async handleHeroSearch(e) {
        if (e) e.preventDefault();
        const origin = document.getElementById('search-origin')?.value || 'Lanka, Varanasi';
        const dest = document.getElementById('search-dest')?.value || 'Varanasi Cantt Station';
        const seats = parseInt(document.getElementById('search-seats')?.value || '1', 10);
        const type = document.getElementById('search-type')?.value || 'all';

        try {
            const results = await window.api.searchRides({
                origin,
                destination: dest,
                seats,
                vehicle_type: type
            });
            this.lastSearchResults = results;
            this.navigate('find-ride');
        } catch (err) {
            this.showToast('Could not search rides: ' + err.message, 'error');
        }
    }

    useMyLocation() {
        const input = document.getElementById('search-origin');
        if (!input) return;

        if (navigator.geolocation) {
            input.value = "Detecting GPS...";
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    input.value = `Lanka, Varanasi (GPS: ${pos.coords.latitude.toFixed(3)}, ${pos.coords.longitude.toFixed(3)})`;
                    this.showToast("Accurate GPS location locked!", "success");
                },
                (err) => {
                    // Graceful fallback for localhost / permissions
                    input.value = "Lanka, Varanasi (Demo GPS: 25.280° N, 82.999° E)";
                    this.showToast("Using verified Lanka Varanasi corridor GPS coordinates.", "success");
                },
                { timeout: 3000 }
            );
        } else {
            input.value = "Lanka Chauraha, Varanasi";
        }
    }

    highlightRide(rideId) {
        document.querySelectorAll('.ride-card').forEach(c => c.classList.remove('selected'));
        const card = document.getElementById(`card-${rideId}`);
        if (card) {
            card.classList.add('selected');
            card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    trackRideLive(rideId) {
        window.api.getRideDetails(rideId).then(ride => {
            this.activeRide = ride;
            this.navigate('tracking');
        });
    }

    // Modal Operations
    async openBookingModal(rideId) {
        try {
            const ride = await window.api.getRideDetails(rideId);
            let modal = document.getElementById('booking-modal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'booking-modal';
                modal.className = 'modal-overlay';
                document.body.appendChild(modal);
            }

            modal.innerHTML = `
                <div class="modal-dialog">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <span class="match-badge">Confirm Carpool Seat</span>
                        <button onclick="document.getElementById('booking-modal').remove()" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748B;">&times;</button>
                    </div>

                    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin-bottom: 4px;">
                        ${ride.vehicle_title}
                    </h3>
                    <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 16px;">
                        Driver: <strong>${ride.driver_name}</strong> (⭐ ${ride.driver_rating}) • Reg: <strong>${ride.reg_number}</strong>
                    </div>

                    <div style="background: #ECFDF5; border-radius: 8px; padding: 12px; font-size: 0.85rem; color: #065F46; margin-bottom: 16px;">
                        <div>🟢 <strong>Pickup:</strong> ${ride.origin_name}</div>
                        <div style="margin-top: 4px;">🔴 <strong>Drop-off:</strong> ${ride.dest_name}</div>
                        <div style="margin-top: 6px; font-weight: 700;">🌱 Environmental impact: Avoids ~${ride.co2_savings_kg} kg CO₂</div>
                    </div>

                    <form onsubmit="window.app.confirmBooking(event, '${ride.id}', ${ride.price_per_seat})">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                            <div>
                                <label class="form-label" for="book-seats">Number of Seats</label>
                                <select id="book-seats" class="form-select" onchange="document.getElementById('total-fare-calc').textContent = '₹' + (this.value * ${ride.price_per_seat})">
                                    <option value="1">1 Seat</option>
                                    <option value="2">2 Seats</option>
                                    <option value="3">3 Seats</option>
                                </select>
                            </div>
                            <div>
                                <label class="form-label">Total Shared Fare</label>
                                <div id="total-fare-calc" style="font-size: 1.5rem; font-weight: 800; color: #059669; padding-top: 6px;">
                                    ₹${ride.price_per_seat}
                                </div>
                            </div>
                        </div>

                        <div style="margin-bottom: 16px;">
                            <label class="form-label" for="book-pickup">Your Exact Boarding Landmark</label>
                            <input type="text" id="book-pickup" class="form-input" value="Lanka Chauraha (Near MMV Gate)" required />
                        </div>

                        <div style="background: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 8px; padding: 10px; font-size: 0.78rem; color: #64748B; margin-bottom: 20px;">
                            💳 <strong>Payment Architecture:</strong> Demo UPI / Cashless Green Wallet ready. No deduction during Technofest test mode.
                        </div>

                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 12px; font-size: 1rem;">
                            CONFIRM & START LIVE TRACKING ⚡
                        </button>
                    </form>
                </div>
            `;
        } catch (e) {
            this.showToast('Could not open booking modal: ' + e.message, 'error');
        }
    }

    async confirmBooking(e, rideId, pricePerSeat) {
        e.preventDefault();
        const seats = parseInt(document.getElementById('book-seats').value, 10);
        const pickup = document.getElementById('book-pickup').value;

        try {
            const res = await window.api.createBooking({
                ride_id: rideId,
                seats_booked: seats,
                pickup_name: pickup,
                dropoff_name: "Selected Destination"
            });

            document.getElementById('booking-modal')?.remove();
            this.showToast("🎉 Seat booked successfully! Your carpool is confirmed.", "success");

            // Open Live Tracking for this ride
            this.trackRideLive(rideId);
        } catch (err) {
            this.showToast("Booking failed: " + err.message, "error");
        }
    }

    async advanceSimulationStep(rideId) {
        try {
            const stepRes = await window.api.simulateRideStep(rideId);
            window.mapManager.updateVehiclePosition(stepRes.current_lat, stepRes.current_lng);
            this.showToast(`Vehicle telemetry updated! Distance remaining: ${stepRes.remaining_dist_km} km`, "success");

            if (stepRes.status === 'completed') {
                this.showToast("Trip reached destination!", "success");
                this.completeRideDemo(rideId);
            }
        } catch (e) {
            this.showToast("Simulation advance: " + e.message, "error");
        }
    }

    completeRideDemo(rideId) {
        let modal = document.getElementById('rating-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'rating-modal';
            modal.className = 'modal-overlay';
            document.body.appendChild(modal);
        }

        modal.innerHTML = `
            <div class="modal-dialog" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 12px;">🎉</div>
                <h3 style="font-size: 1.5rem; font-weight: 800; color: #0F172A; margin-bottom: 6px;">
                    Shared Ride Completed!
                </h3>
                <p style="color: #64748B; font-size: 0.95rem; margin-bottom: 20px;">
                    You saved <strong>3.1 kg of CO₂</strong> and avoided 1 duplicate car on Varanasi's roads.
                </p>

                <div style="background: #ECFDF5; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #065F46; text-transform: uppercase;">Rate Driver: Rahul Kumar</div>
                    <div style="font-size: 2rem; color: #F59E0B; margin: 8px 0; cursor: pointer;">
                        ⭐⭐⭐⭐⭐
                    </div>
                    <textarea id="rate-comment" class="form-input" rows="2" placeholder="Write a kind word about your clean EV carpool..."></textarea>
                </div>

                <div style="display: flex; gap: 10px;">
                    <button onclick="window.app.submitRating('${rideId}')" class="btn btn-primary" style="flex: 1; padding: 12px;">
                        Submit Feedback & Impact
                    </button>
                    <button onclick="document.getElementById('rating-modal').remove(); window.app.navigate('impact')" class="btn btn-secondary" style="padding: 12px 18px;">
                        View Impact
                    </button>
                </div>
            </div>
        `;
    }

    async submitRating(rideId) {
        const comment = document.getElementById('rate-comment')?.value || "Great electric carpool!";
        try {
            await window.api.rateRide({
                ride_id: rideId,
                score: 5.0,
                comment
            });
            document.getElementById('rating-modal')?.remove();
            this.showToast("⭐ Thank you! Your review promotes trusted community mobility.", "success");
            this.navigate('impact');
        } catch (e) {
            document.getElementById('rating-modal')?.remove();
            this.navigate('impact');
        }
    }

    async triggerSOSDemo(rideId) {
        try {
            const data = await window.api.triggerSOS(rideId, 25.2910, 83.0030);
            let modal = document.getElementById('sos-modal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'sos-modal';
                modal.className = 'modal-overlay';
                document.body.appendChild(modal);
            }

            modal.innerHTML = `
                <div class="modal-dialog" style="border-top: 6px solid #DC2626;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                        <span class="match-badge" style="background: #FEE2E2; color: #991B1B;">
                            🚨 SIMULATED EMERGENCY SOS BEACON
                        </span>
                        <button onclick="document.getElementById('sos-modal').remove()" style="background: none; border: none; font-size: 1.4rem; cursor: pointer;">&times;</button>
                    </div>

                    <h3 style="font-size: 1.35rem; font-weight: 800; color: #991B1B; margin-bottom: 12px;">
                        Emergency Protocol Activated
                    </h3>

                    <ul style="padding-left: 18px; line-height: 1.7; font-size: 0.9rem; color: #1E293B; margin-bottom: 20px;">
                        ${data.simulated_actions.map(a => `<li>${a}</li>`).join('')}
                    </ul>

                    <div style="background: #FEF2F2; border: 1px solid #FECACA; padding: 12px; border-radius: 8px; font-size: 0.8rem; color: #7F1D1D; margin-bottom: 20px;">
                        <strong>Note for Technofest Judges:</strong> ${data.disclaimer}
                    </div>

                    <button onclick="document.getElementById('sos-modal').remove()" class="btn btn-secondary" style="width: 100%; padding: 10px;">
                        Dismiss Emergency Simulation
                    </button>
                </div>
            `;
        } catch (e) {
            this.showToast("SOS error: " + e.message, "error");
        }
    }

    // Marketplace Actions
    updateSplitLabel(ownerVal) {
        const owner = parseInt(ownerVal, 10);
        const driver = 100 - owner;
        const el = document.getElementById('split-label');
        if (el) el.textContent = `${owner}% Vehicle Owner / ${driver}% Driver`;
    }

    async handleMarketplaceMatch(e) {
        e.preventDefault();
        const vehId = document.getElementById('match-vehicle').value;
        const drvId = document.getElementById('match-driver').value;
        const ownerShare = parseFloat(document.getElementById('split-slider').value);
        const driverShare = 100.0 - ownerShare;

        try {
            const res = await window.api.matchDriverVehicle({
                vehicle_id: vehId,
                driver_id: drvId,
                owner_share_pct: ownerShare,
                driver_share_pct: driverShare,
                notes: "Exhibition match partnership"
            });
            this.showToast(`✨ ${res.message}`, "success");
            this.handleRoute(); // Refresh marketplace
        } catch (err) {
            this.showToast("Marketplace match error: " + err.message, "error");
        }
    }

    // Owner Add Spare Vehicle
    openAddVehicleModal() {
        let modal = document.getElementById('add-veh-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'add-veh-modal';
            modal.className = 'modal-overlay';
            document.body.appendChild(modal);
        }

        modal.innerHTML = `
            <div class="modal-dialog">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span class="match-badge">Monetize Unused Vehicle</span>
                    <button onclick="document.getElementById('add-veh-modal').remove()" style="background: none; border: none; font-size: 1.5rem; cursor: pointer;">&times;</button>
                </div>

                <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin-bottom: 12px;">
                    List a Spare / Unused Vehicle
                </h3>

                <form onsubmit="window.app.submitNewVehicle(event)">
                    <div style="margin-bottom: 12px;">
                        <label class="form-label" for="veh-title">Vehicle Make & Model</label>
                        <input type="text" id="veh-title" class="form-input" value="Tata Tiago EV Long Range" required />
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                        <div>
                            <label class="form-label" for="veh-cat">Category</label>
                            <select id="veh-cat" class="form-select">
                                <option value="ev_car">⚡ Electric Car</option>
                                <option value="e_auto">⚡ Electric Auto-Rickshaw</option>
                                <option value="e_scooter">⚡ Electric Scooter</option>
                                <option value="ev_van">⚡ Electric Van</option>
                            </select>
                        </div>
                        <div>
                            <label class="form-label" for="veh-reg">Registration Number</label>
                            <input type="text" id="veh-reg" class="form-input" value="UP-65-EV-7721" required />
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                        <div>
                            <label class="form-label" for="veh-range">Range per Charge (km)</label>
                            <input type="number" id="veh-range" class="form-input" value="315" required />
                        </div>
                        <div>
                            <label class="form-label" for="veh-seats">Seats</label>
                            <input type="number" id="veh-seats" class="form-input" value="4" required />
                        </div>
                    </div>

                    <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; padding: 12px; margin-bottom: 18px; font-size: 0.85rem; color: #334155;">
                        ☑️ <strong>Default Revenue Share:</strong> 70% to you (Vehicle Owner) / 30% to the verified partner driver.
                    </div>

                    <button type="submit" class="btn btn-primary" style="width: 100%; padding: 12px;">
                        LIST IN GREENRIDE MARKETPLACE 🚀
                    </button>
                </form>
            </div>
        `;
    }

    async submitNewVehicle(e) {
        e.preventDefault();
        const title = document.getElementById('veh-title').value;
        const vehicle_type = document.getElementById('veh-cat').value;
        const reg_number = document.getElementById('veh-reg').value;
        const ev_range_km = parseInt(document.getElementById('veh-range').value, 10);
        const seats = parseInt(document.getElementById('veh-seats').value, 10);

        try {
            await window.api.registerVehicle({
                title,
                vehicle_type,
                make_model: title,
                reg_number,
                ev_range_km,
                seats,
                seeking_driver: true,
                revenue_share_owner: 70.0,
                revenue_share_driver: 30.0,
                locality: "Lanka, Varanasi"
            });

            document.getElementById('add-veh-modal')?.remove();
            this.showToast(`✨ ${title} successfully listed!`, "success");
            this.handleRoute();
        } catch (err) {
            this.showToast("Failed to list vehicle: " + err.message, "error");
        }
    }

    async toggleVehicleSeeking(vehicleId) {
        try {
            const res = await window.api.toggleSeekingDriver(vehicleId);
            this.showToast(res.message, "success");
            this.handleRoute();
        } catch (e) {
            this.showToast("Toggle error: " + e.message, "error");
        }
    }

    // Driver Operations
    async toggleDriverOnline(isOnline) {
        try {
            await window.api.toggleDriverStatus(isOnline);
            this.showToast(`Driver status set to ${isOnline ? 'Online' : 'Offline'}`, "success");
            this.handleRoute();
        } catch (e) {
            this.showToast("Status toggle: " + e.message, "error");
        }
    }

    async handleCreateRide(e) {
        e.preventDefault();
        const orig = document.getElementById('offer-orig').value;
        const dest = document.getElementById('offer-dest').value;
        const time = document.getElementById('offer-time').value;
        const seats = parseInt(document.getElementById('offer-seats').value, 10);
        const price = parseFloat(document.getElementById('offer-price').value);

        try {
            await window.api.createRide({
                origin_name: orig,
                origin_lat: 25.2800,
                origin_lng: 82.9995,
                dest_name: dest,
                dest_lat: 25.2720,
                dest_lng: 82.9975,
                departure_time: time,
                total_seats: seats,
                price_per_seat: price,
                vehicle_id: "veh_1",
                ride_type: "shared_ev"
            });
            this.showToast("🚀 Shared ride offered! Commuters along this corridor will now see it.", "success");
            this.handleRoute();
        } catch (err) {
            this.showToast("Failed to offer ride: " + err.message, "error");
        }
    }

    // Sustainability Impact Dashboard Loader
    async loadImpact(period = 'all') {
        const main = document.getElementById('app-main');
        if (!main) return;

        try {
            const impactData = await window.api.getImpactSummary(period);
            main.innerHTML = window.components.renderImpactDashboard(impactData);

            // Render Chart.js
            setTimeout(() => {
                const ctx = document.getElementById('impact-chart');
                if (ctx && typeof Chart !== 'undefined') {
                    if (this.chartInstance) {
                        this.chartInstance.destroy();
                    }
                    const labels = impactData.historical_trend.map(t => t.month);
                    const co2Data = impactData.historical_trend.map(t => t.co2_kg);
                    const tripsData = impactData.historical_trend.map(t => t.trips);

                    this.chartInstance = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [
                                {
                                    label: 'CO₂ Avoided (kg)',
                                    data: co2Data,
                                    borderColor: '#059669',
                                    backgroundColor: 'rgba(5, 150, 105, 0.1)',
                                    fill: true,
                                    tension: 0.35,
                                    yAxisID: 'y'
                                },
                                {
                                    label: 'Shared Commutes Completed',
                                    data: tripsData,
                                    borderColor: '#0284C7',
                                    backgroundColor: 'rgba(2, 132, 199, 0.1)',
                                    fill: true,
                                    tension: 0.35,
                                    yAxisID: 'y1'
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    type: 'linear',
                                    position: 'left',
                                    title: { display: true, text: 'CO₂ Emissions Saved (kg)' }
                                },
                                y1: {
                                    type: 'linear',
                                    position: 'right',
                                    grid: { drawOnChartArea: false },
                                    title: { display: true, text: 'Shared Commutes' }
                                }
                            }
                        }
                    });
                }
            }, 100);
        } catch (e) {
            console.error("Impact load error:", e);
        }
    }

    // Admin Actions
    async verifyDriver(driverId) {
        try {
            await window.api.verifyDriver(driverId);
            this.showToast("✓ Driver background & DL verified!", "success");
            this.handleRoute();
        } catch (e) {
            this.showToast("Verify driver: " + e.message, "error");
        }
    }

    async verifyVehicle(vehicleId) {
        try {
            await window.api.verifyVehicle(vehicleId);
            this.showToast("✓ Vehicle inspection & battery certified!", "success");
            this.handleRoute();
        } catch (e) {
            this.showToast("Verify vehicle: " + e.message, "error");
        }
    }

    async resetDemoData() {
        if (!confirm("Reset database to fresh Technofest demo state?")) return;
        try {
            await window.api.resetDemoData();
            this.showToast("Demo database re-seeded successfully!", "success");
            this.handleRoute();
        } catch (e) {
            this.showToast("Reset failed: " + e.message, "error");
        }
    }

    // Accessibility & Simple Mode Toggles
    toggleSimpleMode(forcedState = null) {
        this.simpleMode = forcedState !== null ? forcedState : !this.simpleMode;
        document.body.classList.toggle('simple-mode', this.simpleMode);
        localStorage.setItem('greenride_simple_mode', this.simpleMode);

        const btn = document.getElementById('simple-mode-btn');
        if (btn) {
            btn.classList.toggle('active', this.simpleMode);
            btn.textContent = this.simpleMode ? '⚡ Standard Mode' : '👓 Simple Mode';
        }
    }

    toggleHighContrast(forcedState = null) {
        this.highContrast = forcedState !== null ? forcedState : !this.highContrast;
        document.body.classList.toggle('high-contrast', this.highContrast);
        localStorage.setItem('greenride_high_contrast', this.highContrast);
    }

    changeTextScale(scale) {
        this.textScale = scale;
        document.documentElement.style.fontSize = scale === 'lg' ? '18px' : scale === 'xl' ? '20px' : '16px';
        document.querySelectorAll('.font-scale-btn').forEach(b => {
            b.classList.toggle('active', b.dataset.scale === scale);
        });
    }

    // Toast Notifications
    showToast(message, type = 'info') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:99999;display:flex;flex-direction:column;gap:8px;';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.style.cssText = `
            background: ${type === 'success' ? '#065F46' : type === 'error' ? '#991B1B' : '#0F172A'};
            color: #FFFFFF;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: fadeIn 0.2s ease;
        `;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3500);
    }
}

window.app = new GreenRideApp();
document.addEventListener('DOMContentLoaded', () => window.app.init());

