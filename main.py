import os
import sys
import tempfile
import random
import asyncio
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure server directory is in sys.path for relative imports on Vercel / serverless
server_dir = os.path.dirname(os.path.abspath(__file__))
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

from models import Shipment, RouteAdvisoryRequest, RouteAdvisoryResponse
from simulator import DATABASE, tick_simulation, create_new_shipment
from advisory_engine import evaluate_route_risk

# Embed dashboard and landing page HTML directly in Python for zero file-system dependency
try:
    from dashboard_html import INDEX_HTML
except ImportError:
    INDEX_HTML = "<h1>Cold-Chain Operations Tower Running</h1>"

try:
    from landing_html import LANDING_HTML
except ImportError:
    LANDING_HTML = "<h1>Cold-Chain Customer Onboarding Portal</h1>"

app = FastAPI(
    title="Cold-Chain Integrity Advisory Platform API",
    version="1.0.0",
    description="Real-Time Cold Chain Telemetry, Risk Advisory, and Compliance Engine"
)

# Enable CORS for local development and Vercel domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- ONBOARDING SCHEMA & ENDPOINT -----------------

class OnboardingRequest(BaseModel):
    organization_name: str
    sector: str
    contact_person: str
    email: str
    origin_hub: str
    destination_hub: str
    temp_band: str
    hardware_type: str
    phone_number: str
    compliance_standard: str

@app.post("/api/onboard")
def handle_onboarding(request: OnboardingRequest):
    """Processes customer onboarding submissions and provisions their workspace."""
    client_id = f"CLT-IND-{random.randint(1000, 9999)}"
    return {
        "status": "PROVISIONED",
        "client_id": client_id,
        "organization_name": request.organization_name,
        "sector": request.sector,
        "origin_hub": request.origin_hub,
        "destination_hub": request.destination_hub,
        "message": "Enterprise workspace provisioned successfully on the National Cold-Chain Network."
    }

# ----------------- REST ENDPOINTS -----------------

@app.get("/api/shipments", response_model=List[Shipment])
def get_shipments():
    """Retrieve all actively monitored cold-chain shipments."""
    tick_simulation()
    return list(DATABASE.values())

@app.get("/api/shipments/{shipment_id}", response_model=Shipment)
def get_shipment_detail(shipment_id: str):
    """Retrieve full telemetry history and metrics for a specific shipment."""
    if shipment_id not in DATABASE:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return DATABASE[shipment_id]

@app.post("/api/advisory/plan", response_model=RouteAdvisoryResponse)
def plan_route_advisory(request: RouteAdvisoryRequest):
    """Run pre-transit route climate simulation and thermal risk assessment."""
    return evaluate_route_risk(request)

@app.post("/api/shipments/dispatch", response_model=Shipment)
def dispatch_planned_shipment(request: RouteAdvisoryRequest):
    """Dispatches a newly planned route into active monitoring."""
    advisory = evaluate_route_risk(request)
    new_shipment = create_new_shipment(
        origin=request.origin,
        destination=request.destination,
        category=request.payload_category,
        risk_score=advisory.risk_score,
        risk_level=advisory.risk_level,
        route_geometry=advisory.route_geometry,
        orig_coords=advisory.origin_coords,
        dest_coords=advisory.destination_coords
    )
    return new_shipment

@app.post("/api/shipments/{shipment_id}/trigger-excursion")
def trigger_excursion(shipment_id: str):
    """Demo control: simulate refrigeration failure on a truck."""
    if shipment_id not in DATABASE:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipment = DATABASE[shipment_id]
    shipment.refrigeration_active = False
    return {"status": "SUCCESS", "message": f"Refrigeration failure injected on {shipment_id}"}

@app.post("/api/shipments/{shipment_id}/resolve-excursion")
def resolve_excursion(shipment_id: str):
    """Demo control: restore refrigeration on a truck."""
    if shipment_id not in DATABASE:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipment = DATABASE[shipment_id]
    shipment.refrigeration_active = True
    return {"status": "SUCCESS", "message": f"Refrigeration restored on {shipment_id}"}

@app.get("/api/shipments/{shipment_id}/audit-pdf")
def download_audit_pdf(shipment_id: str):
    """Generate and download FDA 21 CFR Part 11 & WHO GDP compliance PDF."""
    if shipment_id not in DATABASE:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    try:
        from compliance_pdf import generate_shipment_audit_pdf
        shipment = DATABASE[shipment_id]
        pdf_filename = f"Audit_Cert_{shipment_id}.pdf"
        pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)
        generate_shipment_audit_pdf(shipment, pdf_path)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=pdf_filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {str(e)}")

# ----------------- PAGE ROUTES -----------------

@app.get("/", response_class=HTMLResponse)
def serve_landing_page():
    """Serves the Customer Onboarding Landing Page."""
    return HTMLResponse(content=LANDING_HTML)

@app.get("/operations", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def serve_operations_tower():
    """Serves the Live Operations Tower (Map & Telemetry)."""
    return HTMLResponse(content=INDEX_HTML)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
