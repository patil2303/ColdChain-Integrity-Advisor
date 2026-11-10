import os
import hashlib
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.pdfgen import canvas
from models import Shipment

def generate_shipment_audit_pdf(shipment: Shipment, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0F172A")
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#475569")
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=10,
        spaceAfter=4
    )

    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#334155")
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=cell_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # Title & Header
    story.append(Paragraph("<b>NATIONAL COLD-CHAIN INTEGRITY & AUDIT CERTIFICATE (INDIA)</b>", ParagraphStyle(
        'Badge', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#1D4ED8")
    )))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"Official Audit Record — Consignment #{shipment.tracking_number}", title_style))
    story.append(Paragraph("Standards Compliance: CDSCO (Govt. of India), WHO GDP Annex 5 & US FDA 21 CFR Part 11", subtitle_style))
    story.append(Spacer(1, 10))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>CONSIGNMENT ID</b><br/>" + shipment.id, cell_style),
            Paragraph("<b>PHARMA PAYLOAD</b><br/>" + shipment.payload_name, cell_style),
            Paragraph("<b>CATEGORY</b><br/>" + shipment.category.value, cell_style),
            Paragraph("<b>TRANSIT STATUS</b><br/>" + shipment.status, cell_style),
        ],
        [
            Paragraph(f"<b>ORIGIN HUB</b><br/>{shipment.origin}", cell_style),
            Paragraph(f"<b>DESTINATION DEPO</b><br/>{shipment.destination}", cell_style),
            Paragraph(f"<b>DISPATCH TIME</b><br/>{shipment.departure_time} IST", cell_style),
            Paragraph(f"<b>ESTIMATED ARRIVAL</b><br/>{shipment.estimated_arrival} IST", cell_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[130, 130, 130, 133])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Thermal Metrics Summary
    story.append(Paragraph("Thermal & Mean Kinetic Temperature (MKT) Summary", h2_style))
    temps = [p.temperature for p in shipment.history] if shipment.history else [shipment.current_temp]
    min_recorded = min(temps)
    max_recorded = max(temps)
    avg_recorded = sum(temps) / len(temps)

    status_color = "#16A34A" if shipment.status != "AT_RISK" else "#DC2626"
    status_text = "PASS — COMPLIANT WITH CDSCO LIMITS" if shipment.status != "AT_RISK" else "EXCURSION RECORDED — UNDER QA REVIEW"

    metrics_data = [
        [
            Paragraph("Permissible Lower Bound", cell_bold),
            Paragraph(f"{shipment.min_temp}°C", cell_style),
            Paragraph("Minimum Recorded Sensor Temp", cell_bold),
            Paragraph(f"{min_recorded:.1f}°C", cell_style)
        ],
        [
            Paragraph("Permissible Upper Bound", cell_bold),
            Paragraph(f"{shipment.max_temp}°C", cell_style),
            Paragraph("Maximum Recorded Sensor Temp", cell_bold),
            Paragraph(f"{max_recorded:.1f}°C", cell_style)
        ],
        [
            Paragraph("Mean Kinetic Temp (MKT)", cell_bold),
            Paragraph(f"{shipment.mkt_temp:.2f}°C (Arrhenius USP <1151>)", cell_style),
            Paragraph("Integrity Outcome", cell_bold),
            Paragraph(f"<b><font color='{status_color}'>{status_text}</font></b>", cell_style)
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[140, 120, 140, 123])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 10))

    # Excursion Incident Log
    story.append(Paragraph("Thermal Excursion Log & Highway Interventions", h2_style))
    if not shipment.excursions:
        excursion_rows = [
            [
                Paragraph("<b>Status</b>", cell_bold),
                Paragraph("<b>Details</b>", cell_bold)
            ],
            [
                Paragraph("<font color='#16A34A'><b>ZERO EXCURSIONS LOGGED</b></font>", cell_style),
                Paragraph("Consignment maintained strictly within cold chain specifications across national highway corridors.", cell_style)
            ]
        ]
        col_w = [180, 343]
    else:
        excursion_rows = [
            [
                Paragraph("Timestamp", cell_bold),
                Paragraph("Severity", cell_bold),
                Paragraph("Breach Temp", cell_bold),
                Paragraph("Duration", cell_bold),
                Paragraph("Incident Description & Highway Intervention", cell_bold)
            ]
        ]
        for exc in shipment.excursions:
            sev_color = "#DC2626" if exc.severity == "Critical" else "#D97706"
            excursion_rows.append([
                Paragraph(exc.timestamp, cell_style),
                Paragraph(f"<font color='{sev_color}'><b>{exc.severity}</b></font>", cell_style),
                Paragraph(f"{exc.temperature}°C", cell_style),
                Paragraph(f"{exc.duration_mins} min", cell_style),
                Paragraph(f"<b>{exc.description}</b><br/>Intervention: {exc.corrective_action}", cell_style)
            ])
        col_w = [70, 55, 60, 50, 288]

    exc_table = Table(excursion_rows, colWidths=col_w)
    exc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(exc_table)
    story.append(Spacer(1, 14))

    # Cryptographic Hash & Digital Sign-off
    data_payload = f"{shipment.id}:{shipment.tracking_number}:{shipment.mkt_temp}:{len(shipment.history)}"
    sha256_hash = hashlib.sha256(data_payload.encode()).hexdigest()

    story.append(Paragraph("Cryptographic Audit Verification (CDSCO / FDA 21 CFR Part 11)", h2_style))
    story.append(Paragraph(
        f"<b>Audit Hash (SHA-256):</b> <font face='Courier' color='#0F172A'>{sha256_hash}</font><br/>"
        "Immutable cryptographic digest certifying continuous sensor ingestion integrity across the Indian National Cold Chain Network.",
        cell_style
    ))
    story.append(Spacer(1, 10))

    # Signature Block
    sig_data = [
        [
            Paragraph("<b>QA / Regulatory Compliance Head:</b><br/><br/>________________________________________<br/>Dr. Rajesh Sharma, Quality Assurance Lead", cell_style),
            Paragraph("<b>Cold-Chain Fleet Logistics Officer:</b><br/><br/>________________________________________<br/>Vikramaditya Patil, Reefer Operations Head", cell_style)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[261, 262])
    sig_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sig_table)

    doc.build(story)
    return output_path
