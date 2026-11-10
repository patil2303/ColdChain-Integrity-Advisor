import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def create_system_architecture_diagram(output_path="D:/Internship/diag_system_arch.png"):
    fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=300)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title Banner
    ax.text(0.3, 5.85, "SYSTEM ARCHITECTURE & TECH STACK", fontsize=12, fontweight='bold', color='#0F294A', va='top')
    ax.text(0.3, 5.55, "End-to-End Real-Time Ingestion, Climate Advisory & Compliance Pipeline", fontsize=9, color='#64748B', va='top')

    # Columns / Layers
    layers = [
        {"title": "1. EDGE & SENSORS", "color": "#0284C7", "bg": "#F0F9FF", "x": 0.3, "w": 2.0},
        {"title": "2. INGESTION GATEWAY", "color": "#2563EB", "bg": "#EFF6FF", "x": 2.55, "w": 2.0},
        {"title": "3. ADVISORY & LOGIC", "color": "#7C3AED", "bg": "#FAF5FF", "x": 4.8, "w": 2.1},
        {"title": "4. DATA & PERSISTENCE", "color": "#0D9488", "bg": "#F0FDFA", "x": 7.15, "w": 1.95},
        {"title": "5. CLIENT & AUDIT", "color": "#EA580C", "bg": "#FFF7ED", "x": 9.35, "w": 1.95},
    ]

    for lyr in layers:
        # Layer Header Box
        hdr_rect = patches.FancyBboxPatch(
            (lyr["x"], 4.9), lyr["w"], 0.38,
            boxstyle="round,pad=0.03,rounding_size=0.06",
            facecolor=lyr["color"], edgecolor=lyr["color"], linewidth=1
        )
        ax.add_patch(hdr_rect)
        ax.text(lyr["x"] + lyr["w"]/2, 5.09, lyr["title"], color='white', fontsize=7.8, fontweight='bold', ha='center', va='center')

        # Layer Container
        body_rect = patches.FancyBboxPatch(
            (lyr["x"], 0.3), lyr["w"], 4.45,
            boxstyle="round,pad=0.04,rounding_size=0.06",
            facecolor=lyr["bg"], edgecolor=lyr["color"], linewidth=0.8, alpha=0.9
        )
        ax.add_patch(body_rect)

    # Component cards helper with precise top-down placement
    def add_card(x, y, w, h, title, subtitle_lines, tag, color):
        # Card background
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.05",
                                      facecolor='#FFFFFF', edgecolor=color, linewidth=0.9)
        ax.add_patch(card)
        
        # Title at the top with va='top'
        ax.text(x + 0.1, y + h - 0.12, title, fontsize=7.8, fontweight='bold', color='#0F172A', va='top')
        
        # Subtitle lines clearly separated
        subtitle_text = "\n".join(subtitle_lines)
        ax.text(x + 0.1, y + h - 0.40, subtitle_text, fontsize=6.6, color='#475569', va='top', linespacing=1.35)
        
        # Tag at the bottom right
        tag_w = 0.72
        tag_h = 0.22
        tag_bg = patches.FancyBboxPatch((x + w - tag_w - 0.08, y + 0.08), tag_w, tag_h,
                                        boxstyle="round,pad=0.02,rounding_size=0.04",
                                        facecolor=color, edgecolor='none', alpha=0.15)
        ax.add_patch(tag_bg)
        ax.text(x + w - tag_w/2 - 0.08, y + 0.08 + tag_h/2, tag, fontsize=6.0, fontweight='bold', color=color, ha='center', va='center')

    # Layer 1 Cards (x = 0.42, w = 1.76)
    add_card(0.42, 3.55, 1.76, 1.05, "IoT Sensor Pods", ["• BLE Temp / Humidity", "• Shock & Light Sensors"], "Hardware", "#0284C7")
    add_card(0.42, 2.30, 1.76, 1.05, "Cellular Gateway", ["• 4G/5G Telematics", "• GPS Route Stream (60s)"], "Field Hub", "#0284C7")
    add_card(0.42, 0.45, 1.76, 1.65, "Fleet Simulator", ["• Virtual Vehicle Fleet", "• Ambient Temp Drift", "• Refrigeration Failures", "• Route GPS Emulation"], "Testing", "#0284C7")

    # Layer 2 Cards (x = 2.67, w = 1.76)
    add_card(2.67, 3.40, 1.76, 1.20, "FastAPI / NestJS", ["• Async Ingestion Engine", "• MQTT & REST Brokers", "• JWT Auth & Rate Limit"], "Ingestion", "#2563EB")
    add_card(2.67, 1.95, 1.76, 1.25, "Packet Validation", ["• Sensor Sanitization", "• Checksum Verification", "• Timestamp Sequencing"], "Validation", "#2563EB")
    add_card(2.67, 0.45, 1.76, 1.30, "Event Bus", ["• Pub/Sub Streaming", "• Decoupled Pipelines", "• Redis Streams / Kafka"], "Streaming", "#2563EB")

    # Layer 3 Cards (x = 4.92, w = 1.86)
    add_card(4.92, 3.50, 1.86, 1.10, "Route Climate Engine", ["• Weather API Corridor Map", "• 0-100 Thermal Risk Index", "• Safe Departure Advisory"], "Advisory", "#7C3AED")
    add_card(4.92, 2.15, 1.86, 1.15, "Excursion Monitor", ["• Mean Kinetic Temp (MKT)", "• Dynamic Threshold Alerts", "• Rapid Anomaly Detection"], "Analytics", "#7C3AED")
    add_card(4.92, 0.45, 1.86, 1.50, "Alert Dispatcher", ["• Instant SMS (Twilio)", "• Push Webhook Alerts", "• Nearest Cold-Storage Hub", "• Driver Reroute Guidance"], "Alerts", "#7C3AED")

    # Layer 4 Cards (x = 7.27, w = 1.71)
    add_card(7.27, 3.35, 1.71, 1.25, "TimescaleDB", ["• PostgreSQL Extension", "• Telemetry Time-Series", "• Hypertable Compression"], "Timeseries", "#0D9488")
    add_card(7.27, 1.95, 1.71, 1.20, "PostgreSQL Core", ["• Shipments & Payloads", "• Carrier & Vehicle Profiles", "• Immutable Audit Trails"], "Relational", "#0D9488")
    add_card(7.27, 0.45, 1.71, 1.30, "Redis Cache", ["• Current Vehicle State", "• Active Geo-fencing", "• Rate-Limit Counters"], "In-Memory", "#0D9488")

    # Layer 5 Cards (x = 9.47, w = 1.71)
    add_card(9.47, 3.45, 1.71, 1.15, "Operations Portal", ["• Next.js 14 / React", "• Live Vehicle Telemetry", "• Excursion Incident Log"], "Web UI", "#EA580C")
    add_card(9.47, 2.05, 1.71, 1.20, "Mapbox GL / GIS", ["• Live Polyline Map View", "• Corridor Heatmap Overlay", "• Checkpoint Milestones"], "GIS Map", "#EA580C")
    add_card(9.47, 0.45, 1.71, 1.40, "Audit PDF Engine", ["• One-Click Trip Certificate", "• FDA 21 CFR Part 11 Spec", "• WHO GDP Compliance", "• SHA-256 Tamper Proof"], "Reporting", "#EA580C")

    # Inter-layer Connection Arrows
    def add_arrow(x1, y, x2):
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=1.3, mutation_scale=11))

    add_arrow(2.22, 4.05, 2.67)
    add_arrow(2.22, 2.80, 2.67)
    add_arrow(4.47, 4.00, 4.92)
    add_arrow(4.47, 2.60, 4.92)
    add_arrow(6.82, 4.00, 7.27)
    add_arrow(6.82, 2.55, 7.27)
    add_arrow(9.02, 4.00, 9.47)
    add_arrow(9.02, 2.65, 9.47)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print("Saved Architecture Diagram:", output_path)

def create_workflow_diagram(output_path="D:/Internship/diag_workflow.png"):
    fig, ax = plt.subplots(figsize=(10.5, 2.6), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 2.6)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title
    ax.text(0.2, 2.35, "END-TO-END OPERATIONAL LIFECYCLE", fontsize=10, fontweight='bold', color='#0F294A', va='top')

    steps = [
        {"num": "STAGE 1", "title": "Route & Thermal Planning", "desc": "Dispatcher selects payload (e.g. 2-8°C).\nEngine models weather across route\n& outputs pre-transit Risk Score.", "color": "#1E40AF"},
        {"num": "STAGE 2", "title": "Sensor Commissioning", "desc": "Device paired to cargo package.\nThreshold limits set & validated.\nDeparture ping logged in database.", "color": "#0284C7"},
        {"num": "STAGE 3", "title": "Real-Time Telemetry", "desc": "Live coordinates, temp, humidity\nstreamed every 60s. Live polyline\nrendered on Mapbox dashboard.", "color": "#0D9488"},
        {"num": "STAGE 4", "title": "Excursion & Advisory", "desc": "If temp rises near limit or cooling fails,\nsystem dispatches instant SMS\n& identifies nearest cold storage.", "color": "#DC2626"},
        {"num": "STAGE 5", "title": "Delivery & Audit Cert", "desc": "Upon destination arrival, one-click\nFDA 21 CFR Part 11 compliant PDF\nis signed and archived immutably.", "color": "#7C3AED"},
    ]

    step_w = 1.85
    spacing = 0.22
    for i, s in enumerate(steps):
        x = 0.2 + i * (step_w + spacing)
        
        card = patches.FancyBboxPatch((x, 0.2), step_w, 1.85, boxstyle="round,pad=0.03,rounding_size=0.06",
                                      facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1)
        ax.add_patch(card)

        bar = patches.FancyBboxPatch((x, 1.82), step_w, 0.23, boxstyle="round,pad=0.02,rounding_size=0.04",
                                     facecolor=s["color"], edgecolor=s["color"])
        ax.add_patch(bar)
        ax.text(x + step_w/2, 1.93, s["num"], color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')

        ax.text(x + 0.1, 1.70, s["title"], fontsize=7.5, fontweight='bold', color='#0F172A', va='top')
        ax.text(x + 0.1, 1.35, s["desc"], fontsize=6.2, color='#475569', linespacing=1.35, va='top')

        if i < len(steps) - 1:
            arr_x = x + step_w + 0.04
            ax.annotate('', xy=(arr_x + spacing - 0.08, 1.1), xytext=(arr_x, 1.1),
                        arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=1.5, mutation_scale=12))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print("Saved Workflow Diagram:", output_path)

def create_thermal_excursion_graph(output_path="D:/Internship/diag_thermal_graph.png"):
    fig, ax = plt.subplots(figsize=(10.5, 3.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFBFD')

    hours = np.linspace(0, 24, 200)
    ambient_temp = 22 + 13 * np.sin((hours - 6) * np.pi / 14)
    ambient_temp = np.clip(ambient_temp, 18, 36)

    cargo_temp = 4.5 + 0.5 * np.sin(hours)
    excursion_mask = (hours >= 13) & (hours <= 20)
    cargo_temp[excursion_mask] += 4.5 * np.sin((hours[excursion_mask] - 13) * np.pi / 7)

    ax.axhspan(2, 8, color='#DCFCE7', alpha=0.55, label='Safe Specification Band (2°C to 8°C)')
    ax.axhline(8, color='#DC2626', linestyle='--', linewidth=1.2, label='Upper Critical Limit (8.0°C)')
    ax.axhline(2, color='#2563EB', linestyle='--', linewidth=1.2, label='Lower Critical Limit (2.0°C)')
    ax.axhline(7.0, color='#D97706', linestyle=':', linewidth=1.0, label='Early Warning Threshold (7.0°C)')

    ax.plot(hours, ambient_temp, color='#94A3B8', linestyle='-.', linewidth=1.4, label='Ambient Highway Weather (°C)')
    ax.plot(hours, cargo_temp, color='#0F172A', linewidth=2.2, label='Payload Sensor Temperature (°C)')

    breach_hours = hours[cargo_temp > 8.0]
    breach_temps = cargo_temp[cargo_temp > 8.0]
    if len(breach_hours) > 0:
        ax.fill_between(breach_hours, 8.0, breach_temps, color='#EF4444', alpha=0.35, label='Excursion Breach Zone')
        ax.annotate('EXCURSION TRIGGERED!\nInstant SMS & Re-route Advisory',
                    xy=(breach_hours[len(breach_hours)//2], max(breach_temps)),
                    xytext=(breach_hours[len(breach_hours)//2] - 3.5, max(breach_temps) + 2.0),
                    arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.2, headwidth=6),
                    fontsize=7.5, fontweight='bold', color='#B91C1C',
                    bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#DC2626", lw=1))

    ax.set_title("Thermal Trajectory Simulation & Real-Time Excursion Detection", fontsize=10, fontweight='bold', color='#0F294A', pad=10)
    ax.set_xlabel("Transit Elapsed Time (Hours)", fontsize=8, color='#475569')
    ax.set_ylabel("Temperature (°C)", fontsize=8, color='#475569')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 38)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper right', fontsize=6.8, framealpha=0.9, ncol=2)
    ax.tick_params(axis='both', which='major', labelsize=7.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='#FFFFFF', bbox_inches='tight')
    plt.close()
    print("Saved Thermal Graph:", output_path)

if __name__ == '__main__':
    create_system_architecture_diagram()
    create_workflow_diagram()
    create_thermal_excursion_graph()
