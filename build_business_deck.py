import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_pptx_deck(output_path="D:/Internship/ColdChain_Integrity_Advisor_12_Page_Business_Deck.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Corporate Color Palette
    NAVY = RGBColor(15, 35, 65)         # Primary Dark #0F2341
    DEEP_BLUE = RGBColor(29, 78, 216)    # Brand Accent #1D4ED8
    CYAN = RGBColor(2, 132, 199)        # Secondary #0284C7
    EMERALD = RGBColor(16, 185, 129)    # Success #10B981
    DARK_TEXT = RGBColor(30, 41, 59)    # Slate 800
    MUTED_TEXT = RGBColor(100, 116, 139)# Slate 500
    LIGHT_BG = RGBColor(248, 250, 252)  # Slate 50
    CARD_BG = RGBColor(255, 255, 255)   # White
    CARD_BORDER = RGBColor(226, 232, 240) # Slate 200

    def add_header(slide, slide_num, title, category="COLDCHAIN INTEGRITY ADVISOR"):
        # Header banner
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        shape.fill.solid()
        shape.fill.fore_color.rgb = NAVY
        shape.line.fill.background()

        # Category / Subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.18), Inches(10), Inches(0.3))
        tf = cat_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = CYAN

        # Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(10), Inches(0.55))
        tf2 = t_box.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = title
        p2.font.size = Pt(20)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(255, 255, 255)

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.8), Inches(0.4), Inches(1.0), Inches(0.4))
        p3 = num_box.text_frame.paragraphs[0]
        p3.text = f"{slide_num:02d} / 12"
        p3.alignment = PP_ALIGN.RIGHT
        p3.font.size = Pt(11)
        p3.font.bold = True
        p3.font.color.rgb = RGBColor(148, 163, 184)

        # Bottom footer line
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.02))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = CARD_BORDER
        footer_line.line.fill.background()

        # Footer text
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(8), Inches(0.3))
        pf = f_box.text_frame.paragraphs[0]
        pf.text = "ColdChain Integrity Advisor — Enterprise Life-Science Pitch Deck | Confidential"
        pf.font.size = Pt(8)
        pf.font.color.rgb = MUTED_TEXT

    def add_card(slide, left, top, width, height, title="", fill_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = NAVY
        return card

    # ==========================================
    # SLIDE 1: Title Slide (Cover)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Brand badge
    b_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.6), Inches(3.6), Inches(0.4))
    b_badge.fill.solid()
    b_badge.fill.fore_color.rgb = DEEP_BLUE
    b_badge.line.fill.background()
    bp = b_badge.text_frame.paragraphs[0]
    bp.text = "ENTERPRISE BUSINESS DECK (12 PAGES)"
    bp.font.size = Pt(9.5)
    bp.font.bold = True
    bp.font.color.rgb = RGBColor(255, 255, 255)
    bp.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(1.5))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "ColdChain Integrity Advisor"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Predictive Route Climate Advisory & Real-Time In-Transit Compliance for Life Sciences"
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = CYAN
    p1_sub.space_before = Pt(8)

    # Core Value Prop summary box
    summary_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.3), Inches(11.3), Inches(1.4))
    summary_box.fill.solid()
    summary_box.fill.fore_color.rgb = RGBColor(23, 49, 87)
    summary_box.line.color.rgb = RGBColor(40, 80, 140)
    stf = summary_box.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = "MISSION: Eliminating vaccine and biopharmaceutical spoilage across Indian national highway corridors through pre-transit climate prediction, dynamic IoT sensor streaming, and instant CDSCO/WHO GDP audit certification."
    sp1.font.size = Pt(12)
    sp1.font.color.rgb = RGBColor(226, 232, 240)

    # Metadata footer
    m_box = s1.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.6))
    mp = m_box.text_frame.paragraphs[0]
    mp.text = "Target Sectors: Vaccines (Serum Institute, Bharat Biotech) • Biologics (Biocon, Zydus) • 3PL Reefer Fleets • Hospital Depots\nRegulatory Compliance: CDSCO Schedule M • WHO GDP Annex 5 • US FDA 21 CFR Part 11"
    mp.font.size = Pt(9.5)
    mp.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================
    # SLIDE 2: Problem Statement
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, 2, "The Billion-Dollar Problem: The Broken Cold Chain", "Market Pain Points")

    # 3 Column Problem Cards
    col_w = 3.65
    gap = 0.38
    left_start = 0.8
    y_start = 1.45

    # Problem 1
    add_card(s2, left_start, y_start, col_w, 5.3, "1. Massive Financial Spoilage", fill_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    p1_tb = s2.shapes.add_textbox(Inches(left_start + 0.25), Inches(y_start + 0.65), Inches(col_w - 0.5), Inches(4.3))
    p1_tf = p1_tb.text_frame
    p1_tf.word_wrap = True
    p = p1_tf.paragraphs[0]
    p.text = "• $35 Billion lost annually worldwide due to temperature failures in pharmaceutical transit.\n\n• Over 25% of vaccines arrive degraded due to cold-chain excursions.\n\n• 1 single broken container can cost ₹1.5 Cr to ₹12 Cr in direct product write-offs."
    p.font.size = Pt(10.5)
    p.font.color.rgb = DARK_TEXT

    # Problem 2
    add_card(s2, left_start + col_w + gap, y_start, col_w, 5.3, "2. Extreme Indian Climate", fill_color=RGBColor(255, 251, 235), border_color=RGBColor(254, 240, 138))
    p2_tb = s2.shapes.add_textbox(Inches(left_start + col_w + gap + 0.25), Inches(y_start + 0.65), Inches(col_w - 0.5), Inches(4.3))
    p2_tf = p2_tb.text_frame
    p2_tf.word_wrap = True
    p2_t = p2_tf.paragraphs[0]
    p2_t.text = "• Summer highway temperatures frequently peak at 42°C to 48°C across Rajasthan, Gujarat, and Maharashtra.\n\n• Passive box insulation (dry ice / gel packs) depletes 300% faster under afternoon sun.\n\n• Traffic bottlenecks and toll delays turn minor temperature drifts into total cargo ruin."
    p2_t.font.size = Pt(10.5)
    p2_t.font.color.rgb = DARK_TEXT

    # Problem 3
    add_card(s2, left_start + 2*(col_w + gap), y_start, col_w, 5.3, "3. Legacy Passive Loggers", fill_color=RGBColor(248, 250, 252), border_color=CARD_BORDER)
    p3_tb = s2.shapes.add_textbox(Inches(left_start + 2*(col_w + gap) + 0.25), Inches(y_start + 0.65), Inches(col_w - 0.5), Inches(4.3))
    p3_tf = p3_tb.text_frame
    p3_tf.word_wrap = True
    p3_t = p3_tf.paragraphs[0]
    p3_t.text = "• The 'Post-Mortem' Fallacy: Standard USB thermometers only reveal spoilage after arrival at the receiving hospital.\n\n• Zero Pre-Trip Advisory: Dispatchers blindly send trucks without highway climate risk forecasting.\n\n• Regulatory Penalty: CDSCO & WHO audits reject uncertified consignments, risking license cancellations."
    p3_t.font.size = Pt(10.5)
    p3_t.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 3: Market Opportunity & TAM / SAM / SOM
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, 3, "Market Opportunity: Rapidly Expanding Cold Chain", "Market Size & Growth")

    # 3 Stat Cards on top
    stat_w = 3.65
    add_card(s3, 0.8, 1.45, stat_w, 2.2, "Total Addressable Market (TAM)", fill_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    s3_t1 = s3.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(stat_w - 0.3), Inches(1.4))
    p = s3_t1.text_frame.paragraphs[0]
    p.text = "$10.2 Billion\nGlobal Biopharma Cold-Chain Logistics Market (Growing at 8.9% CAGR)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = DEEP_BLUE

    add_card(s3, 0.8 + stat_w + gap, 1.45, stat_w, 2.2, "Serviceable Addressable (SAM)", fill_color=RGBColor(240, 253, 250), border_color=RGBColor(153, 246, 228))
    s3_t2 = s3.shapes.add_textbox(Inches(0.8 + stat_w + gap + 0.15), Inches(2.05), Inches(stat_w - 0.3), Inches(1.4))
    p2 = s3_t2.text_frame.paragraphs[0]
    p2.text = "$2.4 Billion\nIndian & South-East Asian Pharmaceutical Cold Chain & Reefer Transit"
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(13, 148, 136)

    add_card(s3, 0.8 + 2*(stat_w + gap), 1.45, stat_w, 2.2, "Serviceable Obtainable (SOM)", fill_color=RGBColor(254, 243, 199), border_color=RGBColor(253, 230, 138))
    s3_t3 = s3.shapes.add_textbox(Inches(0.8 + 2*(stat_w + gap) + 0.15), Inches(2.05), Inches(stat_w - 0.3), Inches(1.4))
    p3 = s3_t3.text_frame.paragraphs[0]
    p3.text = "$280 Million\nHigh-Risk Vaccine, Monoclonal & Plasma Transit Corridors (Initial 3-Year Target)"
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(180, 83, 9)

    # Growth Drivers Container
    add_card(s3, 0.8, 3.9, 11.733, 2.9, "Key Market Catalysts Driving Accelerated Adoption")
    driver_tb = s3.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(11.3), Inches(2.1))
    dtf = driver_tb.text_frame
    dtf.word_wrap = True
    dp1 = dtf.paragraphs[0]
    dp1.text = "1. India as the 'Pharmacy of the World': India produces 60% of global vaccines (Serum Institute, Bharat Biotech) and is expanding into temperature-sensitive biologics, mRNA therapies, and biosimilars requiring strict 2°C–8°C and -80°C logistics.\n\n2. Stringent Regulatory Enforcement: CDSCO Schedule M mandate and revised Good Distribution Practices (GDP) require continuous electronic temperature logging and verifiable audit trails for pharmaceutical licenses.\n\n3. Surge in Cold Chain Infrastructure: Rapid expansion of dedicated freight corridors and temperature-controlled reefer fleets seeking modern software layers to replace dumb GPS trackers."
    dp1.font.size = Pt(10)
    dp1.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 4: The Solution
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, 4, "Our Solution: Shifting from Reactive Tracking to Predictive Advisory", "Value Proposition")

    # 3 Pillars
    c_w = 3.65
    add_card(s4, 0.8, 1.45, c_w, 5.3, "1. PRE-TRANSIT ADVISORY", fill_color=RGBColor(240, 249, 255), border_color=RGBColor(186, 230, 253))
    t1 = s4.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(c_w - 0.4), Inches(4.4))
    t1.text_frame.word_wrap = True
    t1.text_frame.paragraphs[0].text = "• Route-Level Climate Modeling: Ingests origin, destination, and payload sensitivity to model ambient highway weather.\n\n• 0-100 Thermal Risk Index: Factors container insulation life against highway heatwaves.\n\n• Safe Departure Advisory: Recommends night departure windows (post 21:00 IST) to avoid peak daytime solar radiation.\n\n• Contingency Pre-Booking: Pre-reserves re-icing checkpoints at highway hubs."
    t1.text_frame.paragraphs[0].font.size = Pt(10)
    t1.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s4, 0.8 + c_w + gap, 1.45, c_w, 5.3, "2. IN-TRANSIT TELEMETRICS", fill_color=RGBColor(238, 242, 255), border_color=RGBColor(199, 210, 254))
    t2 = s4.shapes.add_textbox(Inches(0.8 + c_w + gap + 0.2), Inches(2.1), Inches(c_w - 0.4), Inches(4.4))
    t2.text_frame.word_wrap = True
    t2.text_frame.paragraphs[0].text = "• Live IoT Telemetry: Streams temperature, humidity, GPS, and door breach pings every 60 seconds.\n\n• Dynamic Highway Routing: OSRM engine renders real road polylines across NH 48, NH 44, etc.\n\n• Mean Kinetic Temp (MKT): Automated Arrhenius USP <1151> calculation to determine actual biological degradation.\n\n• Instant Driver Alerts: Multi-channel SMS/WhatsApp alerts directing drivers to the nearest cold-storage hub."
    t2.text_frame.paragraphs[0].font.size = Pt(10)
    t2.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s4, 0.8 + 2*(c_w + gap), 1.45, c_w, 5.3, "3. POST-TRANSIT AUDIT", fill_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    t3 = s4.shapes.add_textbox(Inches(0.8 + 2*(c_w + gap) + 0.2), Inches(2.1), Inches(c_w - 0.4), Inches(4.4))
    t3.text_frame.word_wrap = True
    t3.text_frame.paragraphs[0].text = "• 1-Click Compliance PDF: Instant generation of tamper-evident inspection reports upon hospital arrival.\n\n• Cryptographic Integrity: SHA-256 digital digest guarantees zero sensor record manipulation.\n\n• CDSCO & WHO GDP Compliant: Approved format for government hospital deliveries and international export customs.\n\n• Digital Sign-off: Embedded QA and fleet lead verification signatures."
    t3.text_frame.paragraphs[0].font.size = Pt(10)
    t3.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 5: Operational Workflow & Architecture
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, 5, "End-to-End Operational Lifecycle & Workflow", "Product Workflow")

    steps = [
        ("STAGE 1", "Route & Thermal Planning", "Dispatcher inputs origin, destination & payload (e.g. 2-8°C). Engine simulates highway corridor climate & outputs 0-100 Risk Score.", DEEP_BLUE),
        ("STAGE 2", "Sensor Commissioning", "IoT pod paired to vaccine consignment. Upper/lower breach thresholds verified. Initial departure ping logged in immutable database.", CYAN),
        ("STAGE 3", "In-Transit Telemetry", "Live GPS, temperature & ambient weather streamed every 60s. Real-time road polyline dynamically rendered on operations map.", RGBColor(13, 148, 136)),
        ("STAGE 4", "Excursion Intervention", "If reefer power fails or temp drifts near 8°C, automated SMS dispatched with turn-by-turn guidance to nearest certified cold hub.", RGBColor(220, 38, 38)),
        ("STAGE 5", "Delivery & Audit Cert", "Upon arrival at receiving hospital, 1-click FDA 21 CFR Part 11 / CDSCO compliant certificate generated with complete MKT graph.", RGBColor(124, 58, 237))
    ]

    card_h = 0.95
    card_gap = 0.15
    for idx, (stage, stitle, sdesc, scolor) in enumerate(steps):
        top_pos = 1.45 + idx * (card_h + card_gap)
        card = add_card(s5, 0.8, top_pos, 11.733, card_h)
        
        # Color bar
        bar = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(top_pos), Inches(1.5), Inches(card_h))
        bar.fill.solid()
        bar.fill.fore_color.rgb = scolor
        bar.line.fill.background()
        bp = bar.text_frame.paragraphs[0]
        bp.text = stage
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = RGBColor(255, 255, 255)
        bp.alignment = PP_ALIGN.CENTER

        # Title & desc
        tb = s5.shapes.add_textbox(Inches(2.5), Inches(top_pos + 0.1), Inches(9.8), Inches(card_h - 0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p_desc = tf.add_paragraph()
        p_desc.text = sdesc
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 6: Technology Stack & Moat
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, 6, "Mandated Enterprise Architecture & Technical Moat", "Engineering Stack")

    # 4 Tech Cards (Frontend, Backend, Database, Algorithms)
    t_w = 2.75
    t_gap = 0.24
    
    add_card(s6, 0.8, 1.45, t_w, 5.3, "FRONTEND", fill_color=RGBColor(248, 250, 252))
    tb = s6.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(t_w - 0.3), Inches(4.5))
    tb.text_frame.word_wrap = True
    tb.text_frame.paragraphs[0].text = "• Next.js 14 / React\n\n• Server-Side Rendering (SSR)\n\n• Tailwind CSS Design System\n\n• Leaflet / Mapbox GL GIS\n\n• Chart.js Time-Series Engine\n\n• Real-Time WebSocket Feeds"
    tb.text_frame.paragraphs[0].font.size = Pt(9.5)
    tb.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s6, 0.8 + t_w + t_gap, 1.45, t_w, 5.3, "BACKEND", fill_color=RGBColor(248, 250, 252))
    tb2 = s6.shapes.add_textbox(Inches(0.8 + t_w + t_gap + 0.15), Inches(2.05), Inches(t_w - 0.3), Inches(4.5))
    tb2.text_frame.word_wrap = True
    tb2.text_frame.paragraphs[0].text = "• Node.js + Express.js\n\n• High-Throughput REST APIs\n\n• Hardware-Agnostic Ingestion\n\n• Multi-Channel Alert Engine\n\n• Twilio / SMS Gateways\n\n• PDF Certificate Generator"
    tb2.text_frame.paragraphs[0].font.size = Pt(9.5)
    tb2.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s6, 0.8 + 2*(t_w + t_gap), 1.45, t_w, 5.3, "DATABASE", fill_color=RGBColor(248, 250, 252))
    tb3 = s6.shapes.add_textbox(Inches(0.8 + 2*(t_w + t_gap) + 0.15), Inches(2.05), Inches(t_w - 0.3), Inches(4.5))
    tb3.text_frame.word_wrap = True
    tb3.text_frame.paragraphs[0].text = "• MongoDB (Mongoose)\n\n• Time-Series Collections for Sensor Telemetry\n\n• GeoJSON Indexing for Highway Corridors\n\n• Immutable Audit Records\n\n• Dynamic Schema for Multi-Sensor Hardware"
    tb3.text_frame.paragraphs[0].font.size = Pt(9.5)
    tb3.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s6, 0.8 + 3*(t_w + t_gap), 1.45, t_w, 5.3, "PROPRIETARY IP", fill_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    tb4 = s6.shapes.add_textbox(Inches(0.8 + 3*(t_w + t_gap) + 0.15), Inches(2.05), Inches(t_w - 0.3), Inches(4.5))
    tb4.text_frame.word_wrap = True
    tb4.text_frame.paragraphs[0].text = "• OSRM Highway Routing: Computes turn-by-turn road network coordinates across India.\n\n• Arrhenius MKT Engine: USP <1151> mathematical biological degradation modeling.\n\n• Thermal Risk Index: Multi-factor ambient heat wave & insulation decay scoring."
    tb4.text_frame.paragraphs[0].font.size = Pt(9.5)
    tb4.text_frame.paragraphs[0].font.color.rgb = DEEP_BLUE

    # ==========================================
    # SLIDE 7: Regulatory Compliance
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, 7, "Regulatory Compliance: Audit-Proof Pharmaceutical Operations", "Regulatory Standards")

    c_box_w = 3.65
    add_card(s7, 0.8, 1.45, c_box_w, 5.3, "CDSCO (Govt. of India)", fill_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    t1 = s7.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(c_box_w - 0.3), Inches(4.5))
    t1.text_frame.word_wrap = True
    t1.text_frame.paragraphs[0].text = "• Schedule M Compliance: Adheres to Good Manufacturing & Distribution Practices for pharmaceuticals.\n\n• Temperature Monitoring Mandate: Requires unbroken records for vaccines, biologicals, and blood products.\n\n• Ready for State Drug Inspector Audits: Eliminates manual logbooks with legally verified electronic certificates."
    t1.text_frame.paragraphs[0].font.size = Pt(10)
    t1.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s7, 0.8 + c_box_w + gap, 1.45, c_box_w, 5.3, "WHO GDP Annex 5", fill_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    t2 = s7.shapes.add_textbox(Inches(0.8 + c_box_w + gap + 0.15), Inches(2.05), Inches(c_box_w - 0.3), Inches(4.5))
    t2.text_frame.word_wrap = True
    t2.text_frame.paragraphs[0].text = "• TRS 961 Annex 5: Standard for good distribution practices for pharmaceutical products.\n\n• Mean Kinetic Temp (MKT): Automated computation according to Arrhenius kinetics (USP <1151>).\n\n• Global Export Grade: Ensures Indian vaccine exports clear customs in Europe, North America, and Africa without consignment rejection."
    t2.text_frame.paragraphs[0].font.size = Pt(10)
    t2.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s7, 0.8 + 2*(c_box_w + gap), 1.45, c_box_w, 5.3, "US FDA 21 CFR Part 11", fill_color=RGBColor(255, 251, 235), border_color=RGBColor(254, 240, 138))
    t3 = s7.shapes.add_textbox(Inches(0.8 + 2*(c_box_w + gap) + 0.15), Inches(2.05), Inches(c_box_w - 0.3), Inches(4.5))
    t3.text_frame.word_wrap = True
    t3.text_frame.paragraphs[0].text = "• Immutable Electronic Signatures: Digitally sealed inspection reports with QA and driver verification blocks.\n\n• Tamper-Evident SHA-256 Digest: Mathematical proof that no telemetry reading has been altered or deleted.\n\n• Complete Audit Trail: Retains every temperature sample, excursion duration, and corrective intervention."
    t3.text_frame.paragraphs[0].font.size = Pt(10)
    t3.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 8: Target Customers & GTM
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, 8, "Target Customer Segments & Go-To-Market Strategy", "Market Execution")

    # 3 Segments
    add_card(s8, 0.8, 1.45, 3.65, 3.0, "Tier 1: Vaccine & Pharma Giants")
    tb = s8.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(3.35), Inches(2.2))
    tb.text_frame.word_wrap = True
    tb.text_frame.paragraphs[0].text = "• Targets: Serum Institute, Bharat Biotech, Zydus, Biocon, Dr. Reddy's.\n• Need: High-volume domestic distribution and export compliance.\n• Deal Size: ₹40L – ₹1.2 Cr / year enterprise contracts."
    tb.text_frame.paragraphs[0].font.size = Pt(9.5)
    tb.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s8, 0.8 + 3.65 + gap, 1.45, 3.65, 3.0, "Tier 2: 3PL Reefer Fleets")
    tb = s8.shapes.add_textbox(Inches(0.8 + 3.65 + gap + 0.15), Inches(2.05), Inches(3.35), Inches(2.2))
    tb.text_frame.word_wrap = True
    tb.text_frame.paragraphs[0].text = "• Targets: Specialized cold-chain logistics providers & reefer operators.\n• Need: Proactive route risk advisory & SLA breach prevention.\n• Deal Size: ₹15L – ₹45L / year fleet subscriptions."
    tb.text_frame.paragraphs[0].font.size = Pt(9.5)
    tb.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s8, 0.8 + 2*(3.65 + gap), 1.45, 3.65, 3.0, "Tier 3: Hospital & State Depots")
    tb = s8.shapes.add_textbox(Inches(0.8 + 2*(3.65 + gap) + 0.15), Inches(2.05), Inches(3.35), Inches(2.2))
    tb.text_frame.word_wrap = True
    tb.text_frame.paragraphs[0].text = "• Targets: AIIMS, Apollo, Fortis, State Medical Corporation depots.\n• Need: Inbound consignment inspection & 1-click audit sign-offs.\n• Deal Size: ₹10L – ₹25L / year portal licenses."
    tb.text_frame.paragraphs[0].font.size = Pt(9.5)
    tb.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    # GTM Flywheel Box
    add_card(s8, 0.8, 4.7, 11.733, 2.1, "Go-To-Market Execution Flywheel", fill_color=RGBColor(240, 249, 255), border_color=RGBColor(186, 230, 253))
    tb_gtm = s8.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.3), Inches(1.5))
    tb_gtm.text_frame.word_wrap = True
    tb_gtm.text_frame.paragraphs[0].text = "1. Direct Enterprise Sales: Target heads of supply chain & QA at top 20 Indian pharma manufacturers.\n2. Ecosystem Partnerships: Integrate with refrigerated truck OEMs (Tata Motors, Ashok Leyland) and cold-storage parks.\n3. Product-Led Onboarding: Self-service Customer Onboarding Landing Page allowing mid-size fleets to activate within 10 minutes."
    tb_gtm.text_frame.paragraphs[0].font.size = Pt(10)
    tb_gtm.text_frame.paragraphs[0].font.color.rgb = DEEP_BLUE

    # ==========================================
    # SLIDE 9: Competitive Landscape
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, 9, "Competitive Benchmarking & Defensible Moat", "Market Differentiation")

    # Table of Competitors
    # Rows: Metric, Controlant, Sensitech, Roambee, Tive, OUR PLATFORM
    add_card(s9, 0.8, 1.45, 11.733, 5.3)
    c_table = s9.shapes.add_table(6, 6, Inches(1.0), Inches(1.6), Inches(11.333), Inches(4.8)).table
    
    headers = ["Feature / Capability", "Controlant", "Sensitech", "Roambee", "Tive", "ColdChain Advisor"]
    for i, h in enumerate(headers):
        c_table.cell(0, i).text = h
        p = c_table.cell(0, i).text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255) if i == 5 else NAVY

    data_rows = [
        ["Pre-Transit Route Climate Risk", "❌ No", "❌ No", "⚠️ Partial", "❌ No", "✅ Yes (0-100 Index)"],
        ["Dynamic Road Network Routing", "❌ Straight-line", "❌ No", "⚠️ Waypoints", "❌ Straight-line", "✅ Yes (Real Highways)"],
        ["Hardware Strategy", "Proprietary", "Proprietary", "Sensor Swarm", "Proprietary", "✅ Hardware-Agnostic"],
        ["Indian Corridor Optimization", "❌ Global generic", "❌ Weak in India", "⚠️ Limited", "❌ Low presence", "✅ Built for India"],
        ["Total Cost of Ownership (TCO)", "Very High ($$$)", "High ($$)", "High ($$)", "Moderate ($$)", "✅ 60-70% Lower Cost"]
    ]

    for r_idx, row in enumerate(data_rows):
        for c_idx, val in enumerate(row):
            c_table.cell(r_idx + 1, c_idx).text = val
            p = c_table.cell(r_idx + 1, c_idx).text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if c_idx == 5:
                p.font.bold = True
                p.font.color.rgb = DEEP_BLUE
            else:
                p.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 10: Business Model
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, 10, "Business Model & Unit Economics", "Monetization Strategy")

    m_w = 3.65
    add_card(s10, 0.8, 1.45, m_w, 3.2, "1. Enterprise SaaS Tier", fill_color=RGBColor(248, 250, 252))
    tb = s10.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(m_w - 0.3), Inches(2.4))
    tb.text_frame.word_wrap = True
    tb.text_frame.paragraphs[0].text = "• Annual Platform License\n• Includes Operations Tower, Route Advisory Engine & User Management\n• ₹12 Lakh to ₹48 Lakh / year per enterprise enterprise customer."
    tb.text_frame.paragraphs[0].font.size = Pt(10)
    tb.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    add_card(s10, 0.8 + m_w + gap, 1.45, m_w, 3.2, "2. Per-Trip Micro-Fee", fill_color=RGBColor(240, 249, 255), border_color=RGBColor(186, 230, 253))
    tb = s10.shapes.add_textbox(Inches(0.8 + m_w + gap + 0.15), Inches(2.05), Inches(m_w - 0.3), Inches(2.4))
    tb.text_frame.word_wrap = True
    tb.text_frame.paragraphs[0].text = "• Pay-as-you-ship Model\n• ₹450 ($5.50) per monitored consignment trip\n• Includes continuous 60s ingestion & signed PDF audit certificate\n• Aligns directly with 3PL reefer volume."
    tb.text_frame.paragraphs[0].font.size = Pt(10)
    tb.text_frame.paragraphs[0].font.color.rgb = DEEP_BLUE

    add_card(s10, 0.8 + 2*(m_w + gap), 1.45, m_w, 3.2, "3. Hardware Integration", fill_color=RGBColor(248, 250, 252))
    tb = s10.shapes.add_textbox(Inches(0.8 + 2*(m_w + gap) + 0.15), Inches(2.05), Inches(m_w - 0.3), Inches(2.4))
    tb.text_frame.word_wrap = True
    tb.text_frame.paragraphs[0].text = "• Hardware-Agnostic Gateway API\n• Optional certified BLE beacon starter packs (₹1,800/unit)\n• Calibration & reverse-logistics management fee."
    tb.text_frame.paragraphs[0].font.size = Pt(10)
    tb.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    # Financial Projections Summary
    add_card(s10, 0.8, 4.9, 11.733, 1.9, "Target Unit Economics & Margins")
    tb_m = s10.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.3))
    tb_m.text_frame.word_wrap = True
    tb_m.text_frame.paragraphs[0].text = "• Gross SaaS Margin: 78% – 82% (High-leverage cloud software, low cloud hosting costs).\n• Customer Lifetime Value (LTV): ₹38 Lakh across 3-year enterprise contracts.\n• Customer Acquisition Cost (CAC): ₹6.5 Lakh via direct enterprise sales."
    tb_m.text_frame.paragraphs[0].font.size = Pt(10.5)
    tb_m.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 11: 18-Month Roadmap
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, 11, "18-Month Execution Roadmap & Milestones", "Strategic Horizons")

    quarters = [
        ("PHASE 1 (M 1-3)", "Stack Migration & Core MVP", "• Next.js + Node/Express + MongoDB migration\n• Live dynamic OSRM routing across NH 48 / NH 44\n• Initial pilot with 2 reefer logistics fleets", DEEP_BLUE),
        ("PHASE 2 (M 4-8)", "Commercial Pilots", "• Onboard 3 Tier-1 Pharma manufacturers\n• CDSCO Schedule M compliance audit sign-offs\n• Scale to 2,000 active monthly trips", CYAN),
        ("PHASE 3 (M 9-14)", "Cryogenic & Rail Expansion", "• Ultra-cold (-80°C) dry ice depletion sensors\n• Integration with Indian Dedicated Freight Corridors (DFCs)\n• Multi-tenant enterprise dashboard", RGBColor(13, 148, 136)),
        ("PHASE 4 (M 15-18)", "International Air-Cargo", "• Expansion into Frankfurt, Dubai, Singapore air lanes\n• Automated customs clearance API integration\n• Series A institutional funding round", RGBColor(124, 58, 237))
    ]

    q_w = 2.75
    q_gap = 0.24
    for idx, (q_title, q_sub, q_desc, q_col) in enumerate(quarters):
        left_pos = 0.8 + idx * (q_w + q_gap)
        card = add_card(s11, left_pos, 1.45, q_w, 5.3, q_title, fill_color=RGBColor(248, 250, 252))
        
        # Subtitle
        sub_tb = s11.shapes.add_textbox(Inches(left_pos + 0.2), Inches(2.0), Inches(q_w - 0.4), Inches(0.5))
        sp = sub_tb.text_frame.paragraphs[0]
        sp.text = q_sub
        sp.font.size = Pt(11)
        sp.font.bold = True
        sp.font.color.rgb = q_col

        # Details
        dtb = s11.shapes.add_textbox(Inches(left_pos + 0.2), Inches(2.6), Inches(q_w - 0.4), Inches(4.0))
        dtb.text_frame.word_wrap = True
        dp = dtb.text_frame.paragraphs[0]
        dp.text = q_desc
        dp.font.size = Pt(9.5)
        dp.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 12: The Ask & Vision
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, 12, "The Vision & Next Steps: The Digital Backbone of Cold Chain", "Call to Action")

    # Left Box: The Ask / Milestones
    add_card(s12, 0.8, 1.45, 5.7, 5.3, "Next Immediate Deliverables & Milestones", fill_color=RGBColor(240, 249, 255), border_color=RGBColor(186, 230, 253))
    tb_l = s12.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.2), Inches(4.4))
    tb_l.text_frame.word_wrap = True
    tb_l.text_frame.paragraphs[0].text = "1. Technical Transition:\n• Finalize Next.js App Router frontend scaffolding\n• Deploy Node.js + Express REST API with MongoDB Atlas\n\n2. Pilot Deployment:\n• Deploy 50 IoT sensor pods on Pune-Delhi and Hyderabad-Bengaluru corridors\n• Partner with 1 primary vaccine distribution carrier\n\n3. Regulatory Verification:\n• Submit sample compliance audit reports for CDSCO & WHO GDP validation\n• Secure zero-excursion certification baseline."
    tb_l.text_frame.paragraphs[0].font.size = Pt(10)
    tb_l.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    # Right Box: The Grand Vision
    add_card(s12, 6.833, 1.45, 5.7, 5.3, "The Long-Term Vision", fill_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    tb_r = s12.shapes.add_textbox(Inches(7.08), Inches(2.1), Inches(5.2), Inches(4.4))
    tb_r.text_frame.word_wrap = True
    tb_r.text_frame.paragraphs[0].text = "“Every vial of vaccine, every insulin dose, and every critical therapeutic delivered anywhere across India should arrive at 100% biological potency with cryptographic compliance proof.”\n\nBy uniting predictive climate routing, live IoT telematics, and automated audit certification into one seamless software platform, ColdChain Integrity Advisor is poised to become the digital operating system for global cold-chain logistics.\n\nThank you!\nWebsite: https://coldchainintegrityadvisor-phi.vercel.app\nGitHub: https://github.com/patil2303/ColdChain-Integrity-Advisor"
    tb_r.text_frame.paragraphs[0].font.size = Pt(10)
    tb_r.text_frame.paragraphs[0].font.color.rgb = DARK_TEXT

    prs.save(output_path)
    print(f"PowerPoint Presentation generated successfully at: {output_path}")

if __name__ == '__main__':
    create_pptx_deck()
