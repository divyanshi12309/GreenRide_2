/**
 * GREENRIDE - REST API Client
 */

const API_BASE = window.location.origin;

class GreenRideAPI {
    constructor() {
        this.token = localStorage.getItem('greenride_token') || '';
        this.currentUser = JSON.parse(localStorage.getItem('greenride_user') || 'null');
    }

    setAuth(token, user) {
        this.token = token;
        this.currentUser = user;
        localStorage.setItem('greenride_token', token);
        localStorage.setItem('greenride_user', JSON.stringify(user));
    }

    clearAuth() {
        this.token = '';
        this.currentUser = null;
        localStorage.removeItem('greenride_token');
        localStorage.removeItem('greenride_user');
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...(this.token ? { 'Authorization': `Bearer ${this.token}` } : {}),
            ...options.headers
        };

        try {
            const res = await fetch(`${API_BASE}${endpoint}`, {
                ...options,
                headers
            });

            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || `Request failed with status ${res.status}`);
            }

            return await res.json();
        } catch (err) {
            console.error(`API Error on ${endpoint}:`, err);
            throw err;
        }
    }

    // Auth & Demo Switcher
    async demoSwitch(role) {
        const data = await this.request(`/api/auth/demo-switch/${role}`);
        this.setAuth(data.token, data.user);
        return data;
    }

    async getCurrentUser() {
        return await this.request('/api/auth/me');
    }

    async switchRole(role) {
        const data = await this.request('/api/auth/switch-active-role', {
            method: 'POST',
            body: JSON.stringify({ role })
        });
        this.setAuth(data.token, data.user);
        return data;
    }

    // Rides & Carpooling
    async listRides(status = null) {
        const q = status ? `?status=${status}` : '';
        return await this.request(`/api/rides/list${q}`);
    }

    async searchRides(params) {
        return await this.request('/api/rides/search', {
            method: 'POST',
            body: JSON.stringify(params)
        });
    }

    async getRideDetails(rideId) {
        return await this.request(`/api/rides/${rideId}`);
    }

    async createRide(rideData) {
        return await this.request('/api/rides/create', {
            method: 'POST',
            body: JSON.stringify(rideData)
        });
    }

    async simulateRideStep(rideId) {
        return await this.request(`/api/rides/${rideId}/simulate-step`, {
            method: 'POST'
        });
    }

    // Bookings
    async createBooking(bookingData) {
        return await this.request('/api/bookings/create', {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });
    }

    async getMyBookings() {
        return await this.request('/api/bookings/my-bookings');
    }

    async cancelBooking(bookingId) {
        return await this.request(`/api/bookings/${bookingId}/cancel`, {
            method: 'POST'
        });
    }

    async rateRide(rateData) {
        return await this.request('/api/bookings/rate', {
            method: 'POST',
            body: JSON.stringify(rateData)
        });
    }

    // Vehicles
    async getMyVehicles() {
        return await this.request('/api/vehicles/my-vehicles');
    }

    async registerVehicle(vehData) {
        return await this.request('/api/vehicles/register', {
            method: 'POST',
            body: JSON.stringify(vehData)
        });
    }

    async toggleSeekingDriver(vehicleId) {
        return await this.request(`/api/vehicles/${vehicleId}/toggle-seeking-driver`, {
            method: 'POST'
        });
    }

    // Drivers
    async getDriverProfile() {
        return await this.request('/api/drivers/profile');
    }

    async toggleDriverStatus(isOnline) {
        return await this.request('/api/drivers/toggle-status', {
            method: 'POST',
            body: JSON.stringify({ is_online: isOnline })
        });
    }

    async getDriverEarnings() {
        return await this.request('/api/drivers/earnings');
    }

    async getDriverRides() {
        return await this.request('/api/drivers/assigned-rides');
    }

    // Marketplace
    async getMarketplaceVehicles() {
        return await this.request('/api/marketplace/vehicles-seeking-drivers');
    }

    async getMarketplaceDrivers() {
        return await this.request('/api/marketplace/drivers-seeking-vehicles');
    }

    async getActivePartnerships() {
        return await this.request('/api/marketplace/active-partnerships');
    }

    async matchDriverVehicle(matchData) {
        return await this.request('/api/marketplace/match', {
            method: 'POST',
            body: JSON.stringify(matchData)
        });
    }

    // Impact Dashboard
    async getImpactSummary(period = 'all') {
        return await this.request(`/api/impact/summary?period=${period}`);
    }

    // Admin
    async getAdminMetrics() {
        return await this.request('/api/admin/metrics');
    }

    async getAdminDrivers() {
        return await this.request('/api/admin/drivers');
    }

    async verifyDriver(driverId) {
        return await this.request(`/api/admin/verify-driver/${driverId}`, { method: 'POST' });
    }

    async getAdminVehicles() {
        return await this.request('/api/admin/vehicles');
    }

    async verifyVehicle(vehicleId) {
        return await this.request(`/api/admin/verify-vehicle/${vehicleId}`, { method: 'POST' });
    }

    async getAdminReports() {
        return await this.request('/api/admin/reports');
    }

    async resolveReport(reportId) {
        return await this.request(`/api/admin/resolve-report/${reportId}`, { method: 'POST' });
    }

    async getAdminAuditLogs() {
        return await this.request('/api/admin/audit-logs');
    }

    async resetDemoData() {
        return await this.request('/api/admin/reset-demo-database', { method: 'POST' });
    }

    // Safety & SOS
    async triggerSOS(rideId, lat, lng) {
        return await this.request(`/api/safety/sos-alert?ride_id=${rideId}&lat=${lat}&lng=${lng}`, {
            method: 'POST'
        });
    }

    async submitReport(reportData) {
        return await this.request('/api/safety/report', {
            method: 'POST',
            body: JSON.stringify(reportData)
        });
    }

    async getCommunities() {
        return await this.request('/api/safety/communities');
    }
}

window.api = new GreenRideAPI();

