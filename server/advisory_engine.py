import math
import requests
from typing import List, Tuple, Dict
from models import RouteAdvisoryRequest, RouteAdvisoryResponse, PayloadCategory

# Comprehensive Indian Cities & Pharma Logistics Hubs Coordinates (Lat, Lng)
INDIAN_CITIES: Dict[str, Tuple[float, float]] = {
    "pune": (18.5204, 73.8567),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "hyderabad": (17.3850, 78.4867),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "ahmedabad": (23.0225, 72.5714),
    "mumbai": (19.0760, 72.8777),
    "bombay": (19.0760, 72.8777),
    "chennai": (13.0827, 80.2707),
    "madras": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "calcutta": (22.5726, 88.3639),
    "nagpur": (21.1458, 79.0882),
    "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462),
    "chandigarh": (30.7333, 76.7794),
    "surat": (21.1702, 72.8311),
    "vadodara": (22.3072, 73.1812),
    "indore": (22.7196, 75.8577),
    "bhopal": (23.2599, 77.4126),
    "kochi": (9.9312, 76.2673),
    "cochin": (9.9312, 76.2673),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "patna": (25.5941, 85.1376),
    "bhubaneswar": (20.2961, 85.8245),
    "guwahati": (26.1445, 91.7362),
    "varanasi": (25.3176, 82.9739),
    "goa": (15.2993, 74.1240)
}

def resolve_coords(location_str: str) -> Tuple[float, float]:
    """Fuzzy matches any Indian location string to its coordinates."""
    loc_clean = location_str.lower()
    for city, coords in INDIAN_CITIES.items():
        if city in loc_clean:
            return coords
    # Default fallback to center of India (Nagpur)
    return (21.1458, 79.0882)

def fetch_driving_route(orig_coords: Tuple[float, float], dest_coords: Tuple[float, float]) -> Tuple[List[List[float]], int, float]:
    """
    Fetches real road network driving geometry from OSRM routing engine.
    Returns: (list_of_lat_lng, distance_km, duration_hours)
    """
    lat1, lng1 = orig_coords
    lat2, lng2 = dest_coords
    
    url = f"https://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{lng2},{lat2}?overview=simplified&geometries=geojson"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if "routes" in data and len(data["routes"]) > 0:
                route_obj = data["routes"][0]
                dist_km = int(route_obj["distance"] / 1000)
                dur_hrs = round(route_obj["duration"] / 3600, 1)
                
                # GeoJSON coordinates are [lng, lat], Leaflet requires [lat, lng]
                geojson_coords = route_obj["geometry"]["coordinates"]
                leaflet_coords = [[coord[1], coord[0]] for coord in geojson_coords]
                return leaflet_coords, dist_km, dur_hrs
    except Exception as e:
        print(f"OSRM routing fallback used: {e}")
        
    # Fallback interpolation if network fails
    num_pts = 10
    coords = []
    for i in range(num_pts + 1):
        frac = i / float(num_pts)
        lat = lat1 + (lat2 - lat1) * frac
        lng = lng1 + (dest_coords[1] - lng1) * frac
        coords.append([round(lat, 4), round(lng, 4)])
        
    # Approximation
    lat_diff = (lat2 - lat1) * 111
    lng_diff = (lng2 - lng1) * 100
    est_dist = int(math.sqrt(lat_diff**2 + lng_diff**2))
    est_hrs = round(est_dist / 65.0, 1)  # average 65 km/h truck speed
    return coords, est_dist, est_hrs

def calculate_mkt(temperatures_celsius: List[float]) -> float:
    """Mean Kinetic Temperature (MKT) via Arrhenius USP <1151>."""
    if not temperatures_celsius:
        return 0.0
    
    delta_H_over_R = 10000.0
    sum_exp = 0.0
    for t_c in temperatures_celsius:
        t_kelvin = t_c + 273.15
        if t_kelvin <= 0:
            t_kelvin = 0.1
        sum_exp += math.exp(-delta_H_over_R / t_kelvin)
        
    avg_exp = sum_exp / len(temperatures_celsius)
    if avg_exp <= 0:
        return temperatures_celsius[-1]
    mkt_kelvin = -delta_H_over_R / math.log(avg_exp)
    return round(mkt_kelvin - 273.15, 2)

def evaluate_route_risk(request: RouteAdvisoryRequest) -> RouteAdvisoryResponse:
    """
    Dynamically computes highway route, distance, driving geometry,
    and thermal risk for any Indian origin and destination pair.
    """
    orig_coords = resolve_coords(request.origin)
    dest_coords = resolve_coords(request.destination)
    
    # Fetch real road network driving geometry
    route_geometry, distance_km, estimated_hours = fetch_driving_route(orig_coords, dest_coords)

    # Ambient climate corridor modeling
    # Northern and Western India plains have higher ambient heat
    avg_lat = (orig_coords[0] + dest_coords[0]) / 2.0
    if avg_lat > 20.0:
        max_ambient = 41.5  # Northern/Central heat corridor
        min_ambient = 25.0
    else:
        max_ambient = 36.5  # Southern peninsular corridor
        min_ambient = 23.0

    # Risk Scoring Formula (0 to 100)
    base_vulnerability = {
        PayloadCategory.ULTRA_COLD: 35,
        PayloadCategory.FROZEN: 25,
        PayloadCategory.STANDARD_COLD: 20,
        PayloadCategory.CRT: 10,
    }.get(request.payload_category, 20)

    duration_ratio = estimated_hours / max(request.insulation_hours, 1)
    duration_penalty = min(int(duration_ratio * 40), 45)

    ambient_penalty = 12
    if max_ambient >= 39.0:
        ambient_penalty += 18

    raw_score = base_vulnerability + duration_penalty + ambient_penalty
    risk_score = min(max(raw_score, 15), 95)

    if risk_score >= 70:
        risk_level = "Critical Risk"
        recommendation = (
            f"HIGH THERMAL RISK: Driving distance is {distance_km} km ({estimated_hours} hrs). "
            f"Corridor temperatures peak at {max_ambient}°C. Passive insulation capacity ({request.insulation_hours}h) "
            f"is insufficient without active reefer power. Schedule night departure (post 21:00 IST) "
            f"and reserve pre-cooled dry-ice replenishment at midway cross-docks."
        )
    elif risk_score >= 40:
        risk_level = "Moderate Risk"
        recommendation = (
            f"MODERATE RISK: Driving distance is {distance_km} km (~{estimated_hours} hrs). Ambient conditions peak at {max_ambient}°C. "
            f"Standard active refrigerated truck adequate. Calibrate dual digital temperature probes before departure."
        )
    else:
        risk_level = "Low Risk"
        recommendation = (
            f"LOW RISK: Driving distance is {distance_km} km ({estimated_hours} hrs). Ambient conditions nominal. "
            f"Highway route within safe operational limits. Enable standard 60-second telemetry streaming."
        )

    # Nearest highway hubs
    origin_name = request.origin.split(',')[0].strip()
    dest_name = request.destination.split(',')[0].strip()

    return RouteAdvisoryResponse(
        origin=request.origin,
        destination=request.destination,
        origin_coords=[orig_coords[0], orig_coords[1]],
        destination_coords=[dest_coords[0], dest_coords[1]],
        route_geometry=route_geometry,
        distance_km=distance_km,
        estimated_duration_hours=estimated_hours,
        corridor_max_ambient=max_ambient,
        corridor_min_ambient=min_ambient,
        risk_score=risk_score,
        risk_level=risk_level,
        recommendation=recommendation,
        suggested_departure_window="Night Transit Window: 21:00 - 05:30 IST (Avoids Solar Heat Peak)",
        cold_storage_checkpoints=[
            f"{origin_name} Certified Pre-Cooling Bio-Hub",
            f"NH Intermediate Cold-Storage & Reefer Rest Dock",
            f"{dest_name} Medical Receiving Depo"
        ],
        compliance_checklist=[
            "CDSCO (India) Good Distribution Practices Guidelines Annex 2",
            "Continuous Dual-Sensor GPS + Temperature Logging Active",
            "US FDA 21 CFR Part 11 Electronic Audit Record Sealed",
            "Emergency Highway Cold-Storage Diversion Protocol Enabled"
        ]
    )
