import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Image
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.drawString(36, 810, "Supply Chain Cold-Chain Integrity Advisory — Product Requirements Document (PRD)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)
        
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 42, 559, 42)
        
        self.drawString(36, 30, "Confidential — Startup Engineering & Product Specification | Ref: CC-PRD-2026-V1")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 30, page_text)
        self.restoreState()

def build_pdf(filename="D:/Internship/PRD_Cold_Chain_Integrity_Advisory.pdf"):
    # Target 595.27 x 841.89 (A4)
    # margins: 36pt (0.5 in) left/right -> usable width = 523.27 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=colors.HexColor("#0F172A")
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#475569")
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1D4ED8")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F294A"),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=13,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.2,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=2.5
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.3,
        leading=12,
        textColor=colors.HexColor("#1E3A8A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor("#334155")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ==================== PAGE 1 ====================
    # Title & Metadata
    story.append(Paragraph("<b>PRODUCT REQUIREMENTS SPECIFICATION (PRD)</b>", badge_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Supply Chain Cold-Chain Integrity Advisory", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Predictive Route Climate Engineering & Real-Time In-Transit Compliance Platform", subtitle_style))
    story.append(Spacer(1, 8))

    meta_data = [
        [
            Paragraph("<b>VERSION</b><br/>1.0 (MVP Scope)", table_cell_style),
            Paragraph("<b>TARGET DOMAIN</b><br/>Vaccines, Biopharma, Food", table_cell_style),
            Paragraph("<b>COMPLIANCE STANDARDS</b><br/>FDA 21 CFR Part 11 / WHO GDP", table_cell_style),
            Paragraph("<b>STATUS</b><br/>Ready for Engineering Sign-off", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[130, 130, 140, 123])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "<b>Context:</b> High-potency biopharmaceuticals (vaccines, biologics, gene therapies) and fresh perishable foods "
        "require strict, unbroken temperature control throughout the supply chain. A single thermal breach (excursion) "
        "can irreversibly spoil entire batches, causing massive financial write-offs and risking patient safety.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Problem:</b> Existing solutions rely on passive loggers (where temperature data is only extracted after delivery, "
        "when cargo is already ruined) or generic GPS telematics that fail to predict thermal degradation or route climate risks.",
        body_style
    ))

    # Callout
    callout_data = [[
        Paragraph(
            "<b>The 'Advisory' Advantage:</b> Rather than just alerting after an excursion occurs, our platform provides "
            "<b>predictive route risk engineering</b>. By combining digital route mapping with real-time ambient weather forecasts "
            "and vehicle insulation decay models, the platform proactively calculates departure windows, detects transit heatwaves, "
            "and routes trucks to certified re-icing and cold-storage facilities before product degradation occurs.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[523])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93C5FD")),
        ('LINELEFT', (0, 0), (-1, -1), 3.5, colors.HexColor("#1D4ED8")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 8))

    # Section 2: Competitor Benchmarking
    story.append(Paragraph("2. Competitor Benchmarking & Gap Analysis", h1_style))
    comp_data = [
        [
            Paragraph("Competitor", table_header_style),
            Paragraph("Focus Market", table_header_style),
            Paragraph("Hardware Model", table_header_style),
            Paragraph("Key Strengths", table_header_style),
            Paragraph("Market Gaps / Disadvantages", table_header_style)
        ],
        [
            Paragraph("<b>Controlant</b>", table_cell_bold),
            Paragraph("Tier-1 Biopharma (Pfizer Vaccine partner)", table_cell_style),
            Paragraph("Proprietary reusable IoT loggers (Saga Card)", table_cell_style),
            Paragraph("Deep pharma validation, automated reverse logistics.", table_cell_style),
            Paragraph("High cost, hardware lock-in, slow onboarding for mid-market distributors.", table_cell_style)
        ],
        [
            Paragraph("<b>Roambee</b>", table_cell_bold),
            Paragraph("Multimodal Global Supply Chain", table_cell_style),
            Paragraph("BLE beacon swarm + cellular gateway", table_cell_style),
            Paragraph("Condition monitoring, dynamic ETA, item-level tracking.", table_cell_style),
            Paragraph("Complex UI, steep learning curve, requires extensive configuration.", table_cell_style)
        ],
        [
            Paragraph("<b>Sensitech</b><br/>(Carrier)", table_cell_bold),
            Paragraph("Enterprise Life Sciences & Food", table_cell_style),
            Paragraph("TempTale loggers (USB & Real-time)", table_cell_style),
            Paragraph("Massive global footprint and proven audit history.", table_cell_style),
            Paragraph("Legacy UI/UX, proprietary closed ecosystem, sluggish API integrations.", table_cell_style)
        ],
        [
            Paragraph("<b>Tive</b>", table_cell_bold),
            Paragraph("Multi-industry freight visibility", table_cell_style),
            Paragraph("Single-use & Multi-use 5G Trackers", table_cell_style),
            Paragraph("Modern web dashboard, multi-sensor (Temp, Humidity, Shock, Light).", table_cell_style),
            Paragraph("Primarily tracking; lacks algorithmic route climate modeling and advisory.", table_cell_style)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[70, 100, 105, 124, 124])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 8))

    # Section 3: Operational Workflow with Diagram
    story.append(Paragraph("3. Operational Workflow Lifecycle", h1_style))
    if os.path.exists("D:/Internship/diag_workflow.png"):
        story.append(Image("D:/Internship/diag_workflow.png", width=523, height=130))
    story.append(Spacer(1, 6))

    # Page Break to Page 2
    story.append(PageBreak())

    # ==================== PAGE 2 ====================
    story.append(Paragraph("4. Recommended System Architecture & Tech Stack", h1_style))
    story.append(Paragraph(
        "The system is built as a microservice-ready cloud architecture designed for high-frequency IoT streaming, "
        "algorithmic route calculation, and tamper-proof compliance generation.",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    # System Architecture Diagram
    if os.path.exists("D:/Internship/diag_system_arch.png"):
        story.append(Image("D:/Internship/diag_system_arch.png", width=523, height=282))
    story.append(Spacer(1, 8))

    # Tech Stack Table
    tech_data = [
        [
            Paragraph("Layer", table_header_style),
            Paragraph("Selected Technology", table_header_style),
            Paragraph("Architectural Purpose & Rationale", table_header_style)
        ],
        [
            Paragraph("<b>Frontend UI</b>", table_cell_bold),
            Paragraph("Next.js 14 / React + Tailwind CSS + Mapbox GL", table_cell_style),
            Paragraph("High-performance operations control tower, live polyline rendering, telemetry charting.", table_cell_style)
        ],
        [
            Paragraph("<b>Backend API</b>", table_cell_bold),
            Paragraph("FastAPI (Python) or NestJS (Node.js)", table_cell_style),
            Paragraph("Async ingestion of IoT telemetry packets, route advisory math, webhook dispatch.", table_cell_style)
        ],
        [
            Paragraph("<b>Database</b>", table_cell_bold),
            Paragraph("PostgreSQL with TimescaleDB extension", table_cell_style),
            Paragraph("Time-series hypertable compression for telemetry + relational tables for shipments & audit logs.", table_cell_style)
        ],
        [
            Paragraph("<b>In-Memory Cache</b>", table_cell_bold),
            Paragraph("Redis 7.x", table_cell_style),
            Paragraph("Real-time geofence indexing and latest-device-state fast lookup.", table_cell_style)
        ],
        [
            Paragraph("<b>Field Simulator</b>", table_cell_bold),
            Paragraph("Python Fleet Simulator Script", table_cell_style),
            Paragraph("Emulates active truck runs, GPS movements, and dynamic temperature drift for demo/testing.", table_cell_style)
        ]
    ]
    tech_table = Table(tech_data, colWidths=[90, 165, 268])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(tech_table)

    # Page Break to Page 3
    story.append(PageBreak())

    # ==================== PAGE 3 ====================
    story.append(Paragraph("5. MVP Functional Requirements Scope", h1_style))

    story.append(Paragraph("Module 1: Pre-Transit Route & Risk Advisory Engine", h2_style))
    story.append(Paragraph("• <b>Standard Payload Profiles:</b> Ultra-Cold (-80°C to -60°C), Standard Cold (2°C to 8°C), Controlled Room Temp (15°C to 25°C), and Frozen Food (-20°C to -10°C).", bullet_style))
    story.append(Paragraph("• <b>Corridor Weather Forecasting:</b> Ingests ambient route weather at 50-mile increments to identify ambient heatwaves or sub-zero freezing zones.", bullet_style))
    story.append(Paragraph("• <b>Advisory Risk Scoring:</b> Computes a 0–100 risk index factoring transit duration, vehicle cooling rating, and re-icing station proximity.", bullet_style))

    story.append(Paragraph("Module 2: In-Transit Real-Time Telemetry Dashboard", h2_style))
    story.append(Paragraph("• <b>Hardware-Agnostic Telemetry API:</b> Lightweight REST/MQTT endpoint accepting JSON packets (Device ID, Lat/Lng, Temp, Humidity, Battery, Door Sensor).", bullet_style))
    story.append(Paragraph("• <b>Interactive Transit Map:</b> Color-coded route path (Green = Safe, Amber = Warning, Red = Excursion) powered by Mapbox GL / Leaflet.", bullet_style))

    story.append(Paragraph("Module 3: Excursion Detection & Mean Kinetic Temperature (MKT)", h2_style))
    story.append(Paragraph("• <b>Dynamic Threshold Triggers:</b> Instant alerting when readings exceed limits for > 15 cumulative minutes.", bullet_style))
    story.append(Paragraph("• <b>Mean Kinetic Temperature (MKT):</b> Calculates actual biological degradation via Arrhenius kinetics to evaluate product stability.", bullet_style))
    
    # Excursion Graph Diagram
    if os.path.exists("D:/Internship/diag_thermal_graph.png"):
        story.append(Spacer(1, 3))
        story.append(Image("D:/Internship/diag_thermal_graph.png", width=523, height=174))
        story.append(Spacer(1, 4))

    story.append(Paragraph("Module 4: Regulatory Compliance & Audit Reporting", h2_style))
    story.append(Paragraph("• <b>One-Click Trip Audit Certificate:</b> Automated generation of signed, tamper-evident PDF inspection summaries with temperature curves.", bullet_style))
    story.append(Paragraph("• <b>Regulatory Conformance:</b> Built to comply with <b>FDA 21 CFR Part 11</b> (audit trail immutability) and <b>WHO Good Distribution Practices (GDP) Annex 5</b>.", bullet_style))

    story.append(Spacer(1, 6))

    # Section 6: Roadmap
    story.append(Paragraph("6. 4-Week MVP Milestone Roadmap", h1_style))
    story.append(Paragraph("• <b>Week 1 (Data Foundation):</b> Relational & time-series schemas, Ingestion API, and realistic mock IoT sensor data generator.", bullet_style))
    story.append(Paragraph("• <b>Week 2 (Route Advisory & Weather):</b> Route corridor calculation API, weather forecast integration, and thermal risk scoring.", bullet_style))
    story.append(Paragraph("• <b>Week 3 (Live Operations UI):</b> Mapbox visualizer, live sensor graphs via WebSockets, and threshold excursion alerting.", bullet_style))
    story.append(Paragraph("• <b>Week 4 (Compliance & Hardening):</b> PDF audit report generator, FDA/WHO compliance validation, end-to-end demo testing.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Updated PDF generated successfully at: {filename}")

if __name__ == '__main__':
    build_pdf()
