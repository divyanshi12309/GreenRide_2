/**
 * GREENRIDE - Leaflet Interactive Map Manager
 * Handles Varanasi map rendering, EV vehicle pins, route polylines, and live simulation.
 */

class GreenRideMapManager {
    constructor(elementId = 'leaflet-map') {
        this.elementId = elementId;
        this.map = null;
        this.markersLayer = null;
        this.routesLayer = null;
        this.activeVehicleMarker = null;
        this.activePolyline = null;
        this.defaultCenter = [25.2950, 82.9980]; // Central Varanasi / Lanka - Assi corridor
        this.defaultZoom = 13;
    }

    init() {
        const container = document.getElementById(this.elementId);
        if (!container) return;

        // Clean up previous instance if needed
        if (this.map) {
            this.map.remove();
            this.map = null;
        }

        // Initialize Leaflet map
        if (typeof L === 'undefined') {
            console.warn('Leaflet library not loaded.');
            container.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#64748B;">Interactive Map (Leaflet Offline Preview)</div>';
            return;
        }

        this.map = L.map(this.elementId, {
            zoomControl: true,
            scrollWheelZoom: true
        }).setView(this.defaultCenter, this.defaultZoom);

        // Standard OpenStreetMap tiles with fast response
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors | GreenRide Community Mobility',
            maxZoom: 18
        }).addTo(this.map);

        this.markersLayer = L.layerGroup().addTo(this.map);
        this.routesLayer = L.layerGroup().addTo(this.map);

        // Fix leaflet tile sizing on load
        setTimeout(() => {
            if (this.map) this.map.invalidateSize();
        }, 250);
    }

    createCustomIcon(type, label = '') {
        let bgColor = '#059669';
        let svgIcon = '⚡🚗';
        let borderColor = '#34D399';

        if (type === 'e_auto') {
            bgColor = '#D97706';
            borderColor = '#FCD34D';
            svgIcon = '⚡🛺';
        } else if (type === 'e_scooter') {
            bgColor = '#0284C7';
            borderColor = '#7DD3FC';
            svgIcon = '⚡🛵';
        } else if (type === 'pickup') {
            bgColor = '#0F172A';
            borderColor = '#38BDF8';
            svgIcon = '📍A';
        } else if (type === 'destination') {
            bgColor = '#DC2626';
            borderColor = '#FCA5A5';
            svgIcon = '🎯B';
        }

        const html = `
            <div style="
                background: ${bgColor};
                border: 2px solid ${borderColor};
                color: #FFFFFF;
                width: 38px;
                height: 38px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                cursor: pointer;
                transition: transform 0.2s;
            ">
                ${svgIcon}
            </div>
        `;

        return L.divIcon({
            html: html,
            className: 'custom-ev-marker',
            iconSize: [38, 38],
            iconAnchor: [19, 19],
            popupAnchor: [0, -20]
        });
    }

    renderRides(rides, onSelectRide = null) {
        if (!this.map || !this.markersLayer) return;

        this.markersLayer.clearLayers();
        this.routesLayer.clearLayers();

        if (!rides || rides.length === 0) return;

        const bounds = [];

        rides.forEach(ride => {
            const vLat = ride.current_lat || ride.origin_lat;
            const vLng = ride.current_lng || ride.origin_lng;

            if (!vLat || !vLng) return;

            bounds.push([vLat, vLng]);
            bounds.push([ride.dest_lat, ride.dest_lng]);

            // Vehicle marker
            const icon = this.createCustomIcon(ride.vehicle_type, ride.vehicle_title);
            const marker = L.marker([vLat, vLng], { icon }).addTo(this.markersLayer);

            const popupContent = `
                <div style="font-family: var(--font-sans); min-width: 220px; padding: 4px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase;">
                        ${ride.vehicle_type === 'e_auto' ? '⚡ E-Auto Pool' : '⚡ Shared EV Car'}
                    </div>
                    <div style="font-size: 1rem; font-weight: 700; color: #0F172A; margin: 2px 0;">
                        ${ride.vehicle_title}
                    </div>
                    <div style="font-size: 0.85rem; color: #475569; margin-bottom: 6px;">
                        Driver: <strong>${ride.driver_name}</strong> (⭐ ${ride.driver_rating})
                    </div>
                    <div style="font-size: 0.8rem; background: #ECFDF5; padding: 6px; border-radius: 6px; color: #065F46;">
                        Route: <strong>${ride.origin_name.split(',')[0]}</strong> → <strong>${ride.dest_name.split(',')[0]}</strong><br>
                        Route Match: <strong>${ride.route_match_score || 92}%</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                        <span style="font-size: 1.1rem; font-weight: 800; color: #0F172A;">₹${ride.price_per_seat}<span style="font-size: 0.75rem; font-weight: 500;">/seat</span></span>
                        <button onclick="window.app.openBookingModal('${ride.id}')" style="background: #059669; color: #fff; border: none; padding: 5px 12px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.85rem;">
                            Book Seat
                        </button>
                    </div>
                </div>
            `;
            marker.bindPopup(popupContent);

            if (onSelectRide) {
                marker.on('click', () => onSelectRide(ride));
            }

            // Draw route polyline between origin and destination
            const polyline = L.polyline([
                [ride.origin_lat, ride.origin_lng],
                [ride.dest_lat, ride.dest_lng]
            ], {
                color: ride.vehicle_type === 'e_auto' ? '#D97706' : '#10B981',
                weight: 4,
                opacity: 0.65,
                dashArray: '8, 8'
            }).addTo(this.routesLayer);
        });

        if (bounds.length > 0) {
            this.map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 });
        }
    }

    renderUserRoute(userOrigCoords, userDestCoords, originName = 'Your Pickup', destName = 'Your Destination') {
        if (!this.map || !this.markersLayer) return;

        // Pickup Marker
        const pIcon = this.createCustomIcon('pickup');
        L.marker(userOrigCoords, { icon: pIcon })
            .addTo(this.markersLayer)
            .bindPopup(`<strong>Pickup:</strong> ${originName}`);

        // Destination Marker
        const dIcon = this.createCustomIcon('destination');
        L.marker(userDestCoords, { icon: dIcon })
            .addTo(this.markersLayer)
            .bindPopup(`<strong>Drop-off:</strong> ${destName}`);

        // Solid Corridor line
        L.polyline([userOrigCoords, userDestCoords], {
            color: '#0284C7',
            weight: 5,
            opacity: 0.85
        }).addTo(this.routesLayer);

        this.map.fitBounds([userOrigCoords, userDestCoords], { padding: [60, 60] });
    }

    setupLiveTracking(ride) {
        if (!this.map) return;

        this.markersLayer.clearLayers();
        this.routesLayer.clearLayers();

        const origin = [ride.origin_lat, ride.origin_lng];
        const dest = [ride.dest_lat, ride.dest_lng];
        const current = [ride.current_lat || ride.origin_lat, ride.current_lng || ride.origin_lng];

        // Draw path
        this.activePolyline = L.polyline([origin, dest], {
            color: '#10B981',
            weight: 6,
            opacity: 0.9
        }).addTo(this.routesLayer);

        // Vehicle marker
        const vIcon = this.createCustomIcon(ride.vehicle_type);
        this.activeVehicleMarker = L.marker(current, { icon: vIcon }).addTo(this.markersLayer);
        this.activeVehicleMarker.bindPopup(`<strong>${ride.vehicle_title}</strong> (Live Position)`).openPopup();

        // Destination flag
        const dIcon = this.createCustomIcon('destination');
        L.marker(dest, { icon: dIcon }).addTo(this.markersLayer).bindPopup(`Destination: ${ride.dest_name}`);

        this.map.fitBounds([origin, dest], { padding: [60, 60] });
    }

    updateVehiclePosition(newLat, newLng) {
        if (this.activeVehicleMarker) {
            this.activeVehicleMarker.setLatLng([newLat, newLng]);
        }
    }
}

window.mapManager = new GreenRideMapManager();

