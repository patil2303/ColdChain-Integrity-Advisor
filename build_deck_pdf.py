import os
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_PATH = "D:/Internship/ColdChain_Integrity_Advisor_12_Page_Business_Deck.pdf"

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

    def draw_page_decorations(self, total_pages):
        self.saveState()
        # Top banner line
        self.setStrokeColor(colors.HexColor("#0284c7"))
        self.setLineWidth(2)
        self.line(40, 570, 752, 570)
        
        # Bottom footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 35, 752, 35)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(40, 22, "COLD-CHAIN INTEGRITY ADVISOR | CONFIDENTIAL BUSINESS PITCH DECK")
        self.drawRightString(752, 22, f"Slide {self._pageNumber} of {total_pages}")
        self.restoreState()

def build_pdf():
    # Landscape letter: 792 x 612
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(letter),
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor('#0f172a')
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#0284c7')
    )

    slide_cat = ParagraphStyle(
        'SlideCat',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#0284c7')
    )

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a')
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#334155')
    )

    bold_body = ParagraphStyle(
        'SlideBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f172a')
    )

    card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0369a1')
    )

    slides_data = [
        # Slide 1
        {
            "cat": "EXECUTIVE PITCH DECK",
            "title": "Cold-Chain Integrity Advisor",
            "subtitle": "Predictive Route Thermal Risk Modeling & GxP Compliance for Biopharma Logistics",
            "content": [
                ("Founders & Development Team", "Antigravity Engineering | Serum & Biopharma Advisory Taskforce"),
                ("Core Innovation", "Physics-based Arrhenius MKT degradation modeling + Real-time IoT Highway Telematics"),
                ("Regulatory Conformance", "CDSCO Draft Guidelines 2023, WHO GDP TRS 961 Annex 9, US FDA 21 CFR Part 11"),
                ("Production Architecture", "Frontend: Next.js | Backend: Node.js + Express.js | Database: MongoDB | Telemetry: MQTT/REST"),
                ("Live Deployment", "Vercel Cloud Serverless + GitHub Enterprise Continuous Delivery")
            ]
        },
        # Slide 2
        {
            "cat": "PROBLEM STATEMENT",
            "title": "The $35 Billion Vulnerability in Global Pharma Logistics",
            "subtitle": "Temperature-sensitive biologics suffer devastating spoilage due to reactive monitoring",
            "content": [
                ("Annual Economic Waste", "Over $35 Billion lost globally every year due to in-transit cold-chain excursions and spoilage."),
                ("Post-Mortem Blindness", "Legacy USB/NFC data loggers only reveal thermal failures after the vaccines have already arrived ruined at hospitals."),
                ("Extreme Ambient Climates", "Indian highway corridors regularly exceed 42°C-46°C ambient heat, overwhelming standard passive reefers."),
                ("Catastrophic Regulatory Liability", "A single unmonitored excursion batch forces mandatory CDSCO quarantine, audit failures, and complete batch destruction."),
                ("Core Flaw of Status Quo", "Logistics providers act reactively. The market requires predictive pre-departure dispatch advisory.")
            ]
        },
        # Slide 3
        {
            "cat": "MARKET OPPORTUNITY",
            "title": "Total Addressable Market (TAM, SAM & SOM)",
            "subtitle": "High-growth tailwinds driven by biopharma expansion and mandatory CDSCO 2023 regulations",
            "content": [
                ("TAM: Global Cold-Chain Logistics", "$382 Billion by 2030 (CAGR: 16.2%), driven by mRNA vaccines, GLP-1 biologics, and cellular therapies."),
                ("SAM: India Pharma Cold-Chain Market", "$4.8 Billion by 2028 (CAGR: 19.4%), powered by the 'Pharmacy of the World' vaccine manufacturing hub."),
                ("SOM: High-Assurance IoT Integrity Advisory", "$620 Million beachhead market targeting Tier-1 CDMOs, vaccine manufacturers, and specialized 3PLs."),
                ("Regulatory Catalyst", "Mandatory CDSCO Good Distribution Practices (GDP) requires continuous tamper-proof digital thermal logging."),
                ("Growth Velocity", "Indian refrigerated vehicle fleet growing from 15,000 to 45,000+ units over the next 4 years.")
            ]
        },
        # Slide 4
        {
            "cat": "THE SOLUTION",
            "title": "Cold-Chain Integrity Advisor: Proactive & Automated",
            "subtitle": "Transforming blind transportation into an intelligent, self-healing biopharma cold chain",
            "content": [
                ("Pre-Departure Advisory", "Simulates highway surface temperatures, solar irradiance, and traffic jams before the truck leaves the warehouse."),
                ("Arrhenius MKT Analytics", "Calculates Mean Kinetic Temperature across all points to measure genuine biological shelf-life degradation."),
                ("Dynamic OSRM Highway Routing", "Calculates real turn-by-turn road waypoints across Indian National Highways (NH 48, NH 44, Western Corridor)."),
                ("Instant Excursion Mitigation", "Automated real-time rerouting to nearest certified highway dry-ice hubs and pre-cooling depots upon cooling failure."),
                ("Zero-Trust Digital Auditing", "One-click generation of CDSCO & WHO compliant inspection certificates signed with SHA-256 digital digests.")
            ]
        },
        # Slide 5
        {
            "cat": "PLATFORM WORKFLOW",
            "title": "End-to-End Operational Workflow",
            "subtitle": "How the advisory engine protects biopharma from origin synthesis to patient administration",
            "content": [
                ("Step 1: Order & Dispatch Formulation", "Supply chain planner inputs payload type (Covishield, Covaxin, Insulin), origin hub, and destination clinic."),
                ("Step 2: Physics-Based Thermal Assessment", "Algorithm evaluates ambient heat, corridor delays, insulation R-values, producing an actionable 0-100 Risk Score."),
                ("Step 3: Real-Time IoT Telematics Stream", "Reefer GPS and calibrated BLE sensors transmit temperature, ambient heat, door-status, and battery health."),
                ("Step 4: Autonomous Breach Detection", "Immediate alerts triggered via SMS/Email if temperature drifts beyond narrow target limits (e.g. +2°C to +8°C)."),
                ("Step 5: Automated GxP Delivery Sign-Off", "Consignee receives cryptographic batch release certificate verifying unbroken chain-of-custody.")
            ]
        },
        # Slide 6
        {
            "cat": "ARCHITECTURE & TECHNICAL MOAT",
            "title": "Production Tech Stack & Competitive Moat",
            "subtitle": "Engineered on the senior-mandated enterprise stack for hyper-scale and strict compliance",
            "content": [
                ("Frontend Layer: Next.js (React 18)", "Server-side rendering, low-latency telematics dashboards, interactive Leaflet geo-tracking, Chart.js telemetry curves."),
                ("Backend Engine: Node.js + Express.js", "High-throughput asynchronous REST microservices, real-time WebSockets, and mathematical Arrhenius calculation modules."),
                ("Data Persistence: MongoDB Atlas", "Time-series collections for sub-second IoT sensor ingest, immutable GxP audit trail logs, and shipment metadata."),
                ("IoT Telematics Gateway", "Support for MQTT, CoAP, and Cellular 4G/5G GPS beacon ingestion with encrypted TLS 1.3 payloads."),
                ("Our Technical Moat", "Proprietary Indian highway corridor thermal microclimate maps + Arrhenius biological degradation modeling.")
            ]
        },
        # Slide 7
        {
            "cat": "REGULATORY & COMPLIANCE CONFORMANCE",
            "title": "Built for Global Audits & CDSCO Mandates",
            "subtitle": "Eliminating manual paper logs with tamper-evident, audit-ready compliance certificates",
            "content": [
                ("CDSCO Good Distribution Practices 2023", "Full adherence to Indian regulatory mandates for continuous cold-chain temperature mapping and documentation."),
                ("WHO GDP (TRS 961, Annex 9)", "Meets World Health Organization standards for temperature-sensitive pharmaceutical product storage and transit."),
                ("US FDA 21 CFR Part 11 Compliance", "Electronic records, cryptographic SHA-256 digital verification digests, and immutable chronological audit trails."),
                ("ALCOA+ Data Integrity Principles", "Attributable, Legible, Contemporaneous, Original, and Accurate telemetry logging."),
                ("Instant PDF Audit Export", "One-click generation of inspector-ready compliance dossiers with excursion root-cause analysis.")
            ]
        },
        # Slide 8
        {
            "cat": "GO-TO-MARKET & TARGET PERSONAS",
            "title": "GTM Strategy & Customer Personas",
            "subtitle": "Targeting high-margin biopharma manufacturers and specialized healthcare 3PLs",
            "content": [
                ("Persona 1: Biopharma QA & Regulatory VP", "Pain: Audit findings, batch rejections, CDSCO regulatory notices. Value: 100% automated GxP digital sign-off."),
                ("Persona 2: Cold-Chain Logistics Director", "Pain: In-transit refrigeration breakdowns, driver negligence, dry-ice depletion. Value: Predictive route planning."),
                ("Persona 3: Hospital & Depot Chief Pharmacist", "Pain: Receiving compromised vaccines without proof of potency. Value: Instant QR-code batch release acceptance."),
                ("GTM Phase 1 (Months 1-6): Direct CDMO Outreach", "Pilots with Serum Institute, Bharat Biotech, and Zydus Cadila corridor lanes."),
                ("GTM Phase 2 (Months 7-18): 3PL Integrations", "Strategic partnerships with Blue Dart Medipak, Snowman Logistics, and DHL Supply Chain.")
            ]
        },
        # Slide 9
        {
            "cat": "COMPETITIVE BENCHMARKING",
            "title": "Why Cold-Chain Integrity Advisor Wins",
            "subtitle": "Moving past legacy tracking to automated predictive intelligence",
            "content": [
                ("Legacy Data Loggers (Sensitech, TempTale)", "Passive, post-trip analysis only. Zero pre-trip risk modeling. High manual labor to download data."),
                ("Generic Fleet Telematics (Trakmatic, Samsara)", "Monitors truck GPS and fuel, but lacks Arrhenius biological MKT modeling and CDSCO GxP compliance templates."),
                ("Cold-Chain Integrity Advisor", "Holistic solution: Pre-trip route climate simulation + Real-time IoT telematics + Automated GxP audit certificate generation."),
                ("Speed-to-Value", "Zero-friction customer onboarding portal allowing enterprise workspace setup in under 60 seconds."),
                ("Cost Advantage", "70% lower total cost of ownership compared to expensive proprietary hardware lock-in.")
            ]
        },
        # Slide 10
        {
            "cat": "BUSINESS MODEL & UNIT ECONOMICS",
            "title": "B2B SaaS Subscription + Usage Revenue",
            "subtitle": "Predictable recurring revenue with exceptional gross margins",
            "content": [
                ("Tier 1: Growth Tier ($1,499 / mo)", "Up to 50 active monitored shipments/month, core predictive route advisory, email excursion alerts, PDF audit certs."),
                ("Tier 2: Enterprise Biopharma ($4,999 / mo)", "Unlimited shipments, dedicated SLA, custom ERP/SAP integration, custom telematics hardware webhooks."),
                ("Per-Consignment Metered Add-On ($25 / shipment)", "Single-trip high-value biologic audit certificate generation for ad-hoc 3PL contractors."),
                ("Gross Margin Profile", "84% gross margins enabled by serverless microservices and automated server-side PDF generation."),
                ("Projected ARR", "Reaching $2.4M ARR by Month 18 with 45 enterprise biopharma accounts.")
            ]
        },
        # Slide 11
        {
            "cat": "EXECUTION ROADMAP",
            "title": "18-Month Product & Growth Roadmap",
            "subtitle": "From live prototype to national standard for biopharma cold chains",
            "content": [
                ("Q1-Q2: Prototype & Pilot Validation (Completed)", "FastAPI simulator deployed, customer onboarding portal built, Leaflet routing active, ReportLab audit certs verified."),
                ("Q3: Production Stack Port (Next.js + Express + Mongo)", "Migrating to enterprise stack: Next.js frontend, Node.js/Express backend, MongoDB Atlas time-series database."),
                ("Q4: Hardware Agnostic Sensor SDK", "Plug-and-play integrations with Teltonika, Queclink, and CalAmp BLE/MQTT temperature gateways."),
                ("Q5: AI Autonomous Rerouting Engine", "Reinforcement learning for real-time dynamic rerouting around severe Indian highway weather disruptions."),
                ("Q6: Pan-India National Rollout", "Expansion across 500+ distribution routes covering every state medical supply depot.")
            ]
        },
        # Slide 12
        {
            "cat": "THE ASK & STRATEGIC VISION",
            "title": "The Ask & Future Outlook",
            "subtitle": "Ensuring every single dose of life-saving medicine reaches the patient at 100% potency",
            "content": [
                ("Strategic Funding Ask", "Seeking $750,000 Seed Investment / Enterprise Pilot Sponsorship to accelerate commercialization."),
                ("Use of Funds", "45% Core Software Engineering & Stack Migration | 30% Hardware Testing & CDSCO Validation | 25% GTM & CDMO Sales."),
                ("Target Milestones", "100,000 Monitored Biopharma Shipments, 0 Uncaught Temperature Excursions, 50 Enterprise Clients within 18 Months."),
                ("Long-Term Vision", "To establish the universal digital trust layer for sovereign healthcare and vaccine resilience across the Global South."),
                ("Contact & Demo Access", "Live Platform: Vercel Cloud | GitHub: patil2303/ColdChain-Integrity-Advisor | Lead: Shreyas Patil")
            ]
        }
    ]

    story = []
    
    for i, slide in enumerate(slides_data):
        # Category Banner
        story.append(Paragraph(slide["cat"], slide_cat))
        story.append(Spacer(1, 4))
        
        # Title
        story.append(Paragraph(slide["title"], slide_title))
        story.append(Spacer(1, 4))
        
        # Subtitle
        story.append(Paragraph(slide["subtitle"], subtitle_style))
        story.append(Spacer(1, 14))
        
        # Card / Content Table
        table_data = []
        for header, detail in slide["content"]:
            p_hdr = Paragraph(f"<b>{header}</b>", bold_body)
            p_det = Paragraph(detail, body_style)
            table_data.append([p_hdr, p_det])
            
        t = Table(table_data, colWidths=[200, 500])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        
        story.append(t)
        
        if i < len(slides_data) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Deck generated successfully at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
