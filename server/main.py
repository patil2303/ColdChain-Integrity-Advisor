import os
import sys
import tempfile
import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure server directory is in sys.path for relative imports on Vercel / serverless
server_dir = os.path.dirname(os.path.abspath(__file__))
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

from models import Shipment, RouteAdvisoryRequest, RouteAdvisoryResponse
from simulator import DATABASE, tick_simulation, create_new_shipment
from advisory_engine import evaluate_route_risk
from compliance_pdf import generate_shipment_audit_pdf

app = FastAPI(
    title="Cold-Chain Integrity Advisory Platform API",
    version="1.0.0",
    description="Real-Time Cold Chain Telemetry, Risk Advisory, and Compliance Engine"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Background simulation runner (only in persistent dev server, not on Vercel serverless)
if not os.environ.get("VERCEL"):
    @app.on_event("startup")
    async def start_simulation_loop():
        async def simulation_worker():
            while True:
                await asyncio.sleep(4)
                tick_simulation()

        asyncio.create_task(simulation_worker())

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
    
    shipment = DATABASE[shipment_id]
    pdf_filename = f"Audit_Cert_{shipment_id}.pdf"
    pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)
    
    generate_shipment_audit_pdf(shipment, pdf_path)
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=pdf_filename
    )

# Static UI serving
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

INDEX_HTML_CACHE = ""

def load_index_html():
    global INDEX_HTML_CACHE
    if INDEX_HTML_CACHE:
        return INDEX_HTML_CACHE
    
    candidates = [
        os.path.join(os.path.dirname(__file__), "static", "index.html"),
        os.path.join(os.getcwd(), "server", "static", "index.html"),
        os.path.join(os.getcwd(), "static", "index.html"),
        os.path.abspath("server/static/index.html")
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                INDEX_HTML_CACHE = f.read()
                return INDEX_HTML_CACHE
    return "<h1>Cold-Chain Advisory API Running</h1>"

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    return load_index_html()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
