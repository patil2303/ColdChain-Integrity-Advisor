from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class PayloadCategory(str, Enum):
    ULTRA_COLD = "Ultra-Cold (-80°C to -60°C)"
    FROZEN = "Frozen (-25°C to -15°C)"
    STANDARD_COLD = "Refrigerated (2°C to 8°C)"
    CRT = "Controlled Room Temp (15°C to 25°C)"

class TelemetryPoint(BaseModel):
    timestamp: str
    lat: float
    lng: float
    temperature: float
    humidity: float
    ambient_temp: float
    door_open: bool = False
    refrigeration_active: bool = True
    battery_pct: int = 95

class ExcursionEvent(BaseModel):
    event_id: str
    timestamp: str
    temperature: float
    duration_mins: int
    severity: str  # "Warning", "Critical"
    description: str
    corrective_action: str

class Shipment(BaseModel):
    id: str
    tracking_number: str
    payload_name: str
    category: PayloadCategory
    min_temp: float
    max_temp: float
    origin: str
    destination: str
    origin_coords: List[float]
    destination_coords: List[float]
    status: str  # "IN_TRANSIT", "AT_RISK", "DELIVERED"
    current_temp: float
    current_humidity: float
    current_ambient: float
    mkt_temp: float
    current_lat: float
    current_lng: float
    battery_pct: int
    door_open: bool
    refrigeration_active: bool
    risk_score: int  # 0 to 100
    risk_level: str  # "Low", "Moderate", "Critical"
    departure_time: str
    estimated_arrival: str
    route_waypoints: List[List[float]]
    history: List[TelemetryPoint] = []
    excursions: List[ExcursionEvent] = []

class RouteAdvisoryRequest(BaseModel):
    origin: str
    destination: str
    payload_category: PayloadCategory
    insulation_hours: int = 36
    vehicle_type: str = "Active Refrigerated Reefer"

class RouteAdvisoryResponse(BaseModel):
    origin: str
    destination: str
    origin_coords: List[float] = []
    destination_coords: List[float] = []
    route_geometry: List[List[float]] = []
    distance_km: int
    estimated_duration_hours: float
    corridor_max_ambient: float
    corridor_min_ambient: float
    risk_score: int
    risk_level: str
    recommendation: str
    suggested_departure_window: str
    cold_storage_checkpoints: List[str]
    compliance_checklist: List[str]
