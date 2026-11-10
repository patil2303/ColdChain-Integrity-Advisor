import math
import random
from datetime import datetime, timedelta
from typing import Dict, List
from models import Shipment, PayloadCategory, TelemetryPoint, ExcursionEvent
from advisory_engine import calculate_mkt, resolve_coords, fetch_driving_route

# Pre-baked highway waypoints for instant startup with ZERO network latency
DEFAULT_ROUTES = {
    "PUNE_DELHI": [
        [18.5204, 73.8567], [19.0760, 72.8777], [19.8762, 73.0125],
        [20.3893, 72.9106], [21.1702, 72.8311], [21.7051, 72.9959],
        [22.3072, 73.1812], [23.0225, 72.5714], [23.8345, 73.1124],
        [24.5854, 73.7125], [25.7512, 74.6231], [26.9124, 75.7873],
        [27.5612, 76.1245], [28.2145, 76.8123], [28.6139, 77.2090]
    ],
    "HYDERABAD_BENGALURU": [
        [17.3850, 78.4867], [17.0124, 78.2145], [16.7388, 77.9974],
        [16.2145, 78.0124], [15.8281, 78.0373], [15.1245, 77.8124],
        [14.6819, 77.6006], [14.1245, 77.6541], [13.7380, 77.7289],
        [13.2541, 77.6512], [12.9716, 77.5946]
    ],
    "AHMEDABAD_MUMBAI": [
        [23.0225, 72.5714], [22.7541, 72.7812], [22.5645, 72.9289],
        [22.3072, 73.1812], [21.9541, 73.0512], [21.7051, 72.9959],
        [21.1702, 72.8311], [20.7541, 72.8512], [20.3893, 72.9106],
        [19.8124, 72.8941], [19.2183, 72.9781], [19.0760, 72.8777]
    ]
}

DATABASE: Dict[str, Shipment] = {}

def init_database():
    global DATABASE
    now = datetime.now()

    # Shipment 1: Serum Institute Covishield (Pune -> Delhi)
    pts1 = DEFAULT_ROUTES["PUNE_DELHI"]
    s1_history = []
    base_t = 4.2
    for i in range(12):
        t_stamp = (now - timedelta(minutes=(12-i)*15)).strftime("%H:%M:%S")
        temp = base_t + random.uniform(-0.4, 0.4)
        pt_idx = min(int(len(pts1) * (i / 30.0)), len(pts1) - 1)
        s1_history.append(TelemetryPoint(
            timestamp=t_stamp,
            lat=pts1[pt_idx][0],
            lng=pts1[pt_idx][1],
            temperature=round(temp, 1),
            humidity=round(45.0 + random.uniform(-2, 2), 1),
            ambient_temp=round(34.0 + random.uniform(-1, 2), 1),
            door_open=False,
            refrigeration_active=True,
            battery_pct=96 - i//4
        ))

    curr_idx_1 = min(int(len(pts1) * 0.4), len(pts1) - 1)
    s1 = Shipment(
        id="SHP-SII-101",
        tracking_number="IND-VAC-9821-MH",
        payload_name="Serum Institute Covishield & Pentavalent Vaccines",
        category=PayloadCategory.STANDARD_COLD,
        min_temp=2.0,
        max_temp=8.0,
        origin="Pune SII Bio-Hub, Maharashtra",
        destination="New Delhi AIIMS Central Medical Depot",
        origin_coords=pts1[0],
        destination_coords=pts1[-1],
        status="IN_TRANSIT",
        current_temp=s1_history[-1].temperature,
        current_humidity=s1_history[-1].humidity,
        current_ambient=s1_history[-1].ambient_temp,
        mkt_temp=calculate_mkt([p.temperature for p in s1_history]),
        current_lat=pts1[curr_idx_1][0],
        current_lng=pts1[curr_idx_1][1],
        battery_pct=94,
        door_open=False,
        refrigeration_active=True,
        risk_score=26,
        risk_level="Low Risk",
        departure_time=(now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
        estimated_arrival=(now + timedelta(hours=14)).strftime("%Y-%m-%d %H:%M"),
        route_waypoints=pts1,
        history=s1_history,
        excursions=[]
    )

    # Shipment 2: Bharat Biotech Covaxin (Hyderabad -> Bengaluru)
    pts2 = DEFAULT_ROUTES["HYDERABAD_BENGALURU"]
    s2_history = []
    base_t2 = 4.8
    for i in range(10):
        t_stamp = (now - timedelta(minutes=(10-i)*15)).strftime("%H:%M:%S")
        temp = base_t2 + random.uniform(-0.3, 0.3)
        pt_idx = min(int(len(pts2) * (i / 25.0)), len(pts2) - 1)
        s2_history.append(TelemetryPoint(
            timestamp=t_stamp,
            lat=pts2[pt_idx][0],
            lng=pts2[pt_idx][1],
            temperature=round(temp, 1),
            humidity=round(50.0 + random.uniform(-3, 3), 1),
            ambient_temp=round(33.5 + random.uniform(-1, 2), 1),
            door_open=False,
            refrigeration_active=True,
            battery_pct=98 - i//3
        ))

    curr_idx_2 = min(int(len(pts2) * 0.45), len(pts2) - 1)
    s2 = Shipment(
        id="SHP-BB-204",
        tracking_number="IND-BBX-4410-TS",
        payload_name="Bharat Biotech Covaxin & Rotavirus Vaccine",
        category=PayloadCategory.STANDARD_COLD,
        min_temp=2.0,
        max_temp=8.0,
        origin="Hyderabad Genome Valley, Telangana",
        destination="Bengaluru Biocon Cluster, Karnataka",
        origin_coords=pts2[0],
        destination_coords=pts2[-1],
        status="IN_TRANSIT",
        current_temp=s2_history[-1].temperature,
        current_humidity=s2_history[-1].humidity,
        current_ambient=s2_history[-1].ambient_temp,
        mkt_temp=calculate_mkt([p.temperature for p in s2_history]),
        current_lat=pts2[curr_idx_2][0],
        current_lng=pts2[curr_idx_2][1],
        battery_pct=96,
        door_open=False,
        refrigeration_active=True,
        risk_score=19,
        risk_level="Low Risk",
        departure_time=(now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
        estimated_arrival=(now + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
        route_waypoints=pts2,
        history=s2_history,
        excursions=[]
    )

    # Shipment 3: Zydus Biologics (Ahmedabad -> Mumbai)
    pts3 = DEFAULT_ROUTES["AHMEDABAD_MUMBAI"]
    s3_history = []
    base_t3 = 5.2
    for i in range(12):
        t_stamp = (now - timedelta(minutes=(12-i)*15)).strftime("%H:%M:%S")
        temp = base_t3 + (i * 0.18) + random.uniform(-0.2, 0.2)
        pt_idx = min(int(len(pts3) * (i / 20.0)), len(pts3) - 1)
        s3_history.append(TelemetryPoint(
            timestamp=t_stamp,
            lat=pts3[pt_idx][0],
            lng=pts3[pt_idx][1],
            temperature=round(temp, 1),
            humidity=round(68.0 + random.uniform(-2, 2), 1),
            ambient_temp=round(38.2 + random.uniform(-1, 2), 1),
            door_open=False,
            refrigeration_active=True,
            battery_pct=84 - i//2
        ))

    curr_idx_3 = min(int(len(pts3) * 0.55), len(pts3) - 1)
    s3 = Shipment(
        id="SHP-ZYD-308",
        tracking_number="IND-ZYD-1198-GJ",
        payload_name="Zydus Biologics & Clinical Blood Plasma",
        category=PayloadCategory.STANDARD_COLD,
        min_temp=2.0,
        max_temp=8.0,
        origin="Ahmedabad Biotech Hub, Gujarat",
        destination="Mumbai Central Cold Storage, Maharashtra",
        origin_coords=pts3[0],
        destination_coords=pts3[-1],
        status="IN_TRANSIT",
        current_temp=s3_history[-1].temperature,
        current_humidity=s3_history[-1].humidity,
        current_ambient=s3_history[-1].ambient_temp,
        mkt_temp=calculate_mkt([p.temperature for p in s3_history]),
        current_lat=pts3[curr_idx_3][0],
        current_lng=pts3[curr_idx_3][1],
        battery_pct=81,
        door_open=False,
        refrigeration_active=True,
        risk_score=76,
        risk_level="Critical Risk",
        departure_time=(now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
        estimated_arrival=(now + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M"),
        route_waypoints=pts3,
        history=s3_history,
        excursions=[]
    )

    DATABASE[s1.id] = s1
    DATABASE[s2.id] = s2
    DATABASE[s3.id] = s3

def create_new_shipment(origin: str, destination: str, category: PayloadCategory, 
                        risk_score: int, risk_level: str, 
                        route_geometry: List[List[float]] = None,
                        orig_coords: List[float] = None,
                        dest_coords: List[float] = None) -> Shipment:
    now = datetime.now()
    new_id = f"SHP-IND-{random.randint(400, 999)}"
    
    specs = {
        PayloadCategory.ULTRA_COLD: ("mRNA Vaccine Batch", -80.0, -60.0, -70.0),
        PayloadCategory.FROZEN: ("Frozen Plasma & Diagnostics", -25.0, -15.0, -20.0),
        PayloadCategory.STANDARD_COLD: ("Insulin & Vaccine Consignment (2-8°C)", 2.0, 8.0, 4.5),
        PayloadCategory.CRT: ("Controlled Room Temp Formulations (15-25°C)", 15.0, 25.0, 20.0),
    }.get(category, ("Clinical Pharma Batch", 2.0, 8.0, 4.5))
    
    payload_name, min_t, max_t, init_t = specs
    
    if not route_geometry or len(route_geometry) < 2:
        c1 = resolve_coords(origin)
        c2 = resolve_coords(destination)
        route_geometry, _, _ = fetch_driving_route(c1, c2)
        orig_coords = [c1[0], c1[1]]
        dest_coords = [c2[0], c2[1]]
    
    start_lat, start_lng = route_geometry[0]
    
    init_pt = TelemetryPoint(
        timestamp=now.strftime("%H:%M:%S"),
        lat=start_lat,
        lng=start_lng,
        temperature=init_t,
        humidity=50.0,
        ambient_temp=33.0,
        door_open=False,
        refrigeration_active=True,
        battery_pct=100
    )
    
    origin_short = origin.split(',')[0].strip()
    dest_short = destination.split(',')[0].strip()
    
    shipment = Shipment(
        id=new_id,
        tracking_number=f"IND-EXP-{random.randint(10000, 99999)}",
        payload_name=f"{payload_name} ({origin_short} → {dest_short})",
        category=category,
        min_temp=min_t,
        max_temp=max_t,
        origin=origin,
        destination=destination,
        origin_coords=orig_coords or [start_lat, start_lng],
        destination_coords=dest_coords or [route_geometry[-1][0], route_geometry[-1][1]],
        status="IN_TRANSIT",
        current_temp=init_t,
        current_humidity=50.0,
        current_ambient=33.0,
        mkt_temp=init_t,
        current_lat=start_lat,
        current_lng=start_lng,
        battery_pct=100,
        door_open=False,
        refrigeration_active=True,
        risk_score=risk_score,
        risk_level=risk_level,
        departure_time=now.strftime("%Y-%m-%d %H:%M"),
        estimated_arrival=(now + timedelta(hours=10)).strftime("%Y-%m-%d %H:%M"),
        route_waypoints=route_geometry,
        history=[init_pt],
        excursions=[]
    )
    
    DATABASE[new_id] = shipment
    return shipment

def tick_simulation():
    now_str = datetime.now().strftime("%H:%M:%S")
    for s_id, shipment in DATABASE.items():
        if shipment.status == "DELIVERED":
            continue

        if shipment.route_waypoints and len(shipment.route_waypoints) > 1:
            min_dist = float('inf')
            closest_idx = 0
            for idx, pt in enumerate(shipment.route_waypoints):
                d = (pt[0] - shipment.current_lat)**2 + (pt[1] - shipment.current_lng)**2
                if d < min_dist:
                    min_dist = d
                    closest_idx = idx
            
            next_idx = min(closest_idx + 1, len(shipment.route_waypoints) - 1)
            shipment.current_lat = shipment.route_waypoints[next_idx][0]
            shipment.current_lng = shipment.route_waypoints[next_idx][1]

        if not shipment.refrigeration_active:
            drift = 0.7 if shipment.current_temp < shipment.current_ambient else -0.2
            shipment.current_temp = round(shipment.current_temp + drift, 1)
        else:
            target = (shipment.min_temp + shipment.max_temp) / 2
            diff = target - shipment.current_temp
            shipment.current_temp = round(shipment.current_temp + (diff * 0.15) + random.uniform(-0.15, 0.15), 1)

        shipment.current_ambient = round(shipment.current_ambient + random.uniform(-0.2, 0.2), 1)

        if shipment.current_temp > shipment.max_temp or shipment.current_temp < shipment.min_temp:
            shipment.status = "AT_RISK"
            if not shipment.excursions or (shipment.excursions and shipment.excursions[-1].severity != "Critical"):
                shipment.excursions.append(ExcursionEvent(
                    event_id=f"EXC-{len(shipment.excursions)+1:03d}",
                    timestamp=now_str,
                    temperature=shipment.current_temp,
                    duration_mins=15,
                    severity="Critical",
                    description=f"Temperature breached limit ({shipment.current_temp}°C vs threshold {shipment.max_temp}°C)",
                    corrective_action="Driver directed to nearest highway cold storage hub. Dry-ice top-up initiated."
                ))
        else:
            if shipment.status == "AT_RISK" and shipment.refrigeration_active:
                shipment.status = "IN_TRANSIT"

        new_pt = TelemetryPoint(
            timestamp=now_str,
            lat=shipment.current_lat,
            lng=shipment.current_lng,
            temperature=shipment.current_temp,
            humidity=round(shipment.current_humidity + random.uniform(-0.5, 0.5), 1),
            ambient_temp=shipment.current_ambient,
            door_open=shipment.door_open,
            refrigeration_active=shipment.refrigeration_active,
            battery_pct=shipment.battery_pct
        )
        shipment.history.append(new_pt)
        if len(shipment.history) > 30:
            shipment.history.pop(0)

        shipment.mkt_temp = calculate_mkt([p.temperature for p in shipment.history])

init_database()
