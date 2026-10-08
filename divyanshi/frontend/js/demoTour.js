/**
 * GREENRIDE - Technofest Guided Walkthrough & Exhibition Tour
 * Provides a structured 5-step presentation flow for judges and evaluators.
 */

class GreenRideDemoTour {
    constructor() {
        this.currentStep = 0;
        this.tourSteps = [
            {
                title: "1. The Urban Problem: Too Many Empty Vehicles",
                badge: "URBAN CONGESTION & ASSET IDLE TIME",
                content: `
                    <p style="margin-bottom: 12px; font-size: 1.05rem; color: #334155;">
                        In Indian cities like Varanasi, roads suffer from acute congestion because multiple commuters travel along similar corridors in separate personal vehicles.
                    </p>
                    <div style="background: #FEF2F2; border-left: 4px solid #EF4444; padding: 12px 16px; border-radius: 6px; margin: 12px 0;">
                        <strong>The Inefficiency Paradox:</strong> While roads are choked with single-occupant cars, millions of vehicles sit parked <strong>95% of the day</strong>. Meanwhile, skilled drivers seek honest employment.
                    </div>
                `,
                actionLabel: "Next: The GreenRide Innovation →",
                targetView: "home"
            },
            {
                title: "2. The Innovation: Community Mobility & Spare EV Sharing",
                badge: "NOT A CAB APP — A COMMUNITY NETWORK",
                content: `
                    <p style="margin-bottom: 12px; font-size: 1.05rem; color: #334155;">
                        GREENRIDE is fundamentally different from Uber or Ola. It is a <strong>tri-party community platform</strong> connecting:
                    </p>
                    <ul style="padding-left: 20px; line-height: 1.8; color: #1E293B;">
                        <li><strong>Spare Vehicle Owners:</strong> Put idle EVs and E-Autos to work to earn passive revenue.</li>
                        <li><strong>Verified Drivers:</strong> Get access to partner vehicles and dignified driving livelihoods without loan debt.</li>
                        <li><strong>Passengers:</strong> Enjoy affordable, clean shared carpools along their regular commute.</li>
                    </ul>
                `,
                actionLabel: "Next: Route Matching in Action →",
                targetView: "find-ride"
            },
            {
                title: "3. Intelligent Carpool Route Matching Engine",
                badge: "86% - 96% ROUTE OVERLAP",
                content: `
                    <p style="margin-bottom: 12px; font-size: 1.05rem; color: #334155;">
                        When a passenger searches for a ride from <strong>Lanka to Cantt Railway Station</strong>:
                    </p>
                    <div style="background: #ECFDF5; border-left: 4px solid #10B981; padding: 12px 16px; border-radius: 6px; margin: 12px 0;">
                        Our corridor matching algorithm compares the travel vectors and detects:
                        <div style="font-size: 1.2rem; font-weight: 800; color: #065F46; margin: 6px 0;">
                            ✨ 94% Route Match with Rahul's Nexon EV!
                        </div>
                        Instead of hailing a solo ₹160 cab, the passenger pays ₹45 and saves <strong>3.2 kg CO₂</strong>!
                    </div>
                `,
                actionLabel: "Next: Driver-Vehicle Marketplace →",
                targetView: "marketplace"
            },
            {
                title: "4. Driver + Spare Vehicle Marketplace",
                badge: "CREATING LIVELIHOODS WITHOUT CAPITAL BARRIERS",
                content: `
                    <p style="margin-bottom: 12px; font-size: 1.05rem; color: #334155;">
                        How can someone work as an EV driver if they cannot afford a ₹15 Lakh electric car?
                    </p>
                    <div style="background: #F0FDF4; border: 1px solid #BBF7D0; padding: 14px; border-radius: 8px;">
                        <strong>Vikram owns a spare Tata Nexon EV</strong> that sits in his driveway during office hours.<br>
                        <strong>Rahul is a verified driver</strong> seeking opportunities.<br>
                        With 1-click in the GreenRide Marketplace, they form a partnership with a transparent <strong>70% Owner / 30% Driver</strong> revenue split.
                    </div>
                `,
                actionLabel: "Next: 3D Sustainability Impact →",
                targetView: "marketplace"
            },
            {
                title: "5. Measuring Impact: Planet, People, Prosperity",
                badge: "PROVING SUSTAINABILITY BEYOND BUZZWORDS",
                content: `
                    <p style="margin-bottom: 12px; font-size: 1.05rem; color: #334155;">
                        We do not simply say "EVs are good." We track measurable impact across three pillars:
                    </p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin: 12px 0; text-align: center;">
                        <div style="background: #ECFDF5; padding: 10px; border-radius: 8px;">
                            <div style="font-size: 0.75rem; font-weight: 700; color: #047857;">🌱 PLANET</div>
                            <div style="font-size: 1rem; font-weight: 800; color: #065F46;">Avoided CO₂</div>
                        </div>
                        <div style="background: #EFF6FF; padding: 10px; border-radius: 8px;">
                            <div style="font-size: 0.75rem; font-weight: 700; color: #1D4ED8;">👥 PEOPLE</div>
                            <div style="font-size: 1rem; font-weight: 800; color: #1E40AF;">Driver Jobs</div>
                        </div>
                        <div style="background: #FFFBEB; padding: 10px; border-radius: 8px;">
                            <div style="font-size: 0.75rem; font-weight: 700; color: #B45309;">💰 PROSPERITY</div>
                            <div style="font-size: 1rem; font-weight: 800; color: #92400E;">Asset Income</div>
                        </div>
                    </div>
                `,
                actionLabel: "Finish Tour & Explore Freely 🎉",
                targetView: "impact"
            }
        ];
    }

    startTour() {
        this.currentStep = 0;
        this.renderStep();
    }

    renderStep() {
        const step = this.tourSteps[this.currentStep];
        if (!step) {
            this.closeTour();
            return;
        }

        // Navigate to appropriate view for this step
        if (window.app && step.targetView) {
            window.app.navigate(step.targetView);
        }

        let modal = document.getElementById('demo-tour-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'demo-tour-modal';
            modal.className = 'modal-overlay';
            document.body.appendChild(modal);
        }

        modal.innerHTML = `
            <div class="modal-dialog" style="max-width: 640px; border-top: 5px solid #10B981;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span class="demo-badge" style="background: #ECFDF5; border-color: #10B981; color: #065F46; font-size: 0.8rem;">
                        ${step.badge}
                    </span>
                    <button onclick="window.demoTour.closeTour()" style="background: none; border: none; font-size: 1.4rem; color: #64748B; cursor: pointer;">
                        &times;
                    </button>
                </div>
                <h3 style="font-size: 1.45rem; font-weight: 800; color: #0F172A; margin-bottom: 12px;">
                    ${step.title}
                </h3>
                <div style="margin-bottom: 24px;">
                    ${step.content}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #E2E8F0; padding-top: 16px;">
                    <div style="font-size: 0.85rem; color: #64748B;">
                        Step <strong>${this.currentStep + 1}</strong> of ${this.tourSteps.length}
                    </div>
                    <div style="display: flex; gap: 8px;">
                        ${this.currentStep > 0 ? `
                            <button onclick="window.demoTour.prevStep()" class="btn btn-secondary" style="padding: 8px 16px; font-size: 0.9rem;">
                                ← Previous
                            </button>
                        ` : ''}
                        <button onclick="window.demoTour.nextStep()" class="btn btn-primary" style="padding: 8px 20px; font-size: 0.95rem;">
                            ${step.actionLabel}
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    nextStep() {
        if (this.currentStep < this.tourSteps.length - 1) {
            this.currentStep++;
            this.renderStep();
        } else {
            this.closeTour();
        }
    }

    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.renderStep();
        }
    }

    closeTour() {
        const modal = document.getElementById('demo-tour-modal');
        if (modal) modal.remove();
    }
}

window.demoTour = new GreenRideDemoTour();

