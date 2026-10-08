"""
GREENRIDE - Safety, SOS Simulation & Community Router
"""

from fastapi import APIRouter, HTTPException, Depends
from ..database import get_db
from ..models import ReportCreateRequest
from .auth import get_current_user_from_token
import uuid

router = APIRouter(prefix="/api/safety", tags=["safety"])

@router.post("/sos-alert")
def trigger_sos(ride_id: str, lat: float = 25.2910, lng: float = 83.0030, current_user: dict = Depends(get_current_user_from_token)):
    """
    Demonstration Emergency SOS simulation.
    Logs event, simulates SMS alert to emergency contact & GreenRide Safety Desk.
    """
    sos_id = f"sos_{uuid.uuid4().hex[:8]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, 'EMERGENCY_SOS_TRIGGERED', ?, ?)
        """, (
            sos_id, current_user["id"],
            f"[DEMO SIMULATION] Emergency SOS triggered on Ride {ride_id} at coordinates ({lat}, {lng}). Emergency contacts alerted with live tracking link."
        ))

        return {
            "sos_id": sos_id,
            "status": "active_alert",
            "simulated_actions": [
                "Dispatched live GPS beacon to GreenRide 24/7 Operations Room",
                f"Simulated SMS alert with tracking link sent to emergency contact for {current_user['name']}",
                "Nearest GreenRide community patrol on Lanka-Assi corridor notified",
                "Trip audio/telemetry snapshot recorded for passenger safety verification"
            ],
            "disclaimer": "TECHNOLOGY EXHIBITION DEMONSTRATION: In a real emergency in India, dial 112 directly."
        }

@router.post("/report")
def create_report(req: ReportCreateRequest, current_user: dict = Depends(get_current_user_from_token)):
    rep_id = f"rep_{uuid.uuid4().hex[:8]}"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO reports (id, reporter_id, target_type, target_id, category, description, status)
        VALUES (?, ?, ?, ?, ?, ?, 'under_review')
        """, (rep_id, current_user["id"], req.target_type, req.target_id, req.category, req.description))

        cursor.execute("""
        INSERT INTO system_logs (id, event_type, actor_id, details)
        VALUES (?, 'USER_REPORT_FILED', ?, ?)
        """, (f"log_{uuid.uuid4().hex[:8]}", current_user["id"], f"Reported {req.target_type} ({req.category})."))

        return {
            "report_id": rep_id,
            "status": "under_review",
            "message": "Report logged with GreenRide Safety & Operations team. We will review within 2 hours."
        }

@router.get("/communities")
def get_communities():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM communities ORDER BY members_count DESC")
        return [dict(r) for r in cursor.fetchall()]

