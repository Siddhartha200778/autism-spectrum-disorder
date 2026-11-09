import streamlit as st
import datetime
import io
from modules.theme import render_section_header, render_disclaimer, render_html

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.pdfgen import canvas
    _REPORTLAB_AVAILABLE = True
except Exception:
    _REPORTLAB_AVAILABLE = False


if _REPORTLAB_AVAILABLE:
    class NumberedCanvas(canvas.Canvas):
        """Two-pass canvas to dynamically compute and draw total page numbers and clinical footer."""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_number(num_pages)
                super().showPage()
            super().save()

        def draw_page_number(self, page_count):
            self.saveState()
            self.setFont('Helvetica', 7)
            self.setFillColor(colors.HexColor('#667085'))
            text = f"CONFIDENTIAL CLINICAL DOCUMENT  •  Generated: {datetime.date.today().strftime('%Y-%m-%d')}  •  Page {self._pageNumber} of {page_count}"
            self.drawRightString(A4[0] - 36, 18, text)
            self.drawString(36, 18, "ASD DeepScreen  •  Interpretable Clinical Research Platform")
            self.setStrokeColor(colors.HexColor('#E3E8EE'))
            self.setLineWidth(0.5)
            self.line(36, 26, A4[0] - 36, 26)
            self.restoreState()


def generate_clinical_pdf_report(data: dict) -> bytes:
    """
    Constructs a high-fidelity, publication-grade clinical PDF diagnostic dossier
    matching the exact structure and visual standards of the medical report.
    """
    if not _REPORTLAB_AVAILABLE:
        raise RuntimeError("ReportLab engine is initializing. Please refresh in a moment.")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    printable_width = A4[0] - 72

    styles = getSampleStyleSheet()

    style_badge = ParagraphStyle(
        'Badge', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=colors.HexColor('#167C80'), textTransform='uppercase', spaceAfter=3
    )
    style_main_title = ParagraphStyle(
        'MainTitle', fontName='Helvetica-Bold', fontSize=15, leading=18,
        textColor=colors.HexColor('#202B36'), spaceAfter=2
    )
    style_subtitle = ParagraphStyle(
        'Subtitle', fontName='Helvetica', fontSize=8.5, leading=11,
        textColor=colors.HexColor('#667085'), spaceAfter=0
    )
    style_header_meta = ParagraphStyle(
        'HeaderMeta', fontName='Helvetica', fontSize=8, leading=11,
        alignment=TA_RIGHT, textColor=colors.HexColor('#667085')
    )
    style_status_title = ParagraphStyle(
        'StatusTitle', fontName='Helvetica-Bold', fontSize=11.5, leading=14, alignment=TA_CENTER
    )
    style_status_body = ParagraphStyle(
        'StatusBody', fontName='Helvetica', fontSize=8, leading=11,
        alignment=TA_CENTER, textColor=colors.HexColor('#202B36')
    )
    style_section_title = ParagraphStyle(
        'SectionTitle', fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=colors.HexColor('#202B36'), spaceAfter=4
    )
    style_body = ParagraphStyle(
        'Body', fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#202B36')
    )
    style_body_bold = ParagraphStyle(
        'BodyBold', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.HexColor('#202B36')
    )
    style_small = ParagraphStyle(
        'Small', fontName='Helvetica', fontSize=7, leading=9.5, textColor=colors.HexColor('#667085')
    )
    style_metric_val = ParagraphStyle(
        'MetricVal', fontName='Helvetica-Bold', fontSize=14, leading=17, alignment=TA_CENTER
    )
    style_metric_label = ParagraphStyle(
        'MetricLabel', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
        alignment=TA_CENTER, textColor=colors.HexColor('#667085')
    )
    style_metric_sub = ParagraphStyle(
        'MetricSub', fontName='Helvetica', fontSize=6.5, leading=8.5,
        alignment=TA_CENTER, textColor=colors.HexColor('#667085')
    )

    story = []

    # 1. Header Row
    institution = data.get('institution', 'Pediatric Neurodevelopmental Research Center')
    mrn = data.get('mrn', 'MRN-ASD-2026-0842')
    eval_date = data.get('date', datetime.date.today().strftime('%B %d, %Y'))

    left_header = [
        Paragraph("CONFIDENTIAL MEDICAL SCREENING DOCUMENT", style_badge),
        Paragraph("Pediatric Autism Spectrum Developmental Evaluation", style_main_title),
        Paragraph(institution, style_subtitle)
    ]
    right_header = [
        Paragraph(f"<strong>MRN:</strong> {mrn}", style_header_meta),
        Paragraph(f"<strong>Evaluation Date:</strong> {eval_date}", style_header_meta),
        Paragraph("<strong>Protocol:</strong> Q-CHAT-10 Toddler", style_header_meta),
        Paragraph("<strong>Status:</strong> Completed Assessment Record", style_header_meta)
    ]
    header_table = Table([[left_header, right_header]], colWidths=[printable_width * 0.70, printable_width * 0.30])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#167C80'), spaceBefore=2, spaceAfter=8))

    # 2. Risk Banner
    is_elevated = (data.get("tabnet_pred") == 1) or (data.get("mlp_pred") == 1) or (data.get("aq10_score", 0) >= 3)
    if is_elevated:
        status_text = "ELEVATED ASD RISK PROFILE"
        status_bg = colors.HexColor('#FEF2F2')
        status_border = colors.HexColor('#EF4444')
        status_color = colors.HexColor('#991B1B')
    else:
        status_text = "TYPICAL DEVELOPMENTAL PROFILE"
        status_bg = colors.HexColor('#F0FDF4')
        status_border = colors.HexColor('#10B981')
        status_color = colors.HexColor('#065F46')

    style_status_title.textColor = status_color
    status_content = [
        Paragraph(status_text, style_status_title),
        Spacer(1, 2),
        Paragraph(
            "Multivariate screening based on standardized <strong>Q-CHAT-10</strong> behavioral markers "
            "evaluated through calibrated deep neural architectures (TabNet Attentive Learning &amp; Multi-Layer Perceptron).",
            style_status_body
        )
    ]
    status_table = Table([[status_content]], colWidths=[printable_width])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), status_bg),
        ('BOX', (0,0), (-1,-1), 1.5, status_border),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(status_table)
    story.append(Spacer(1, 8))

    # 3. Patient Demographics & History
    patient_name = data.get('patient_name', 'Liam Davis')
    age_mons = data.get('Age', 24)
    sex_str = 'Male' if str(data.get('Sex', 'm')).lower() in ['m', 'male'] else 'Female'
    ethnicity = str(data.get('Ethnicity', 'N/A')).title()
    guardian = str(data.get('guardian_name', 'Sarah Davis (Mother)')).title()
    jaundice = str(data.get('Jaundice', 'no')).title()
    fam_asd = str(data.get('Family_ASD', 'no')).title()
    screener = str(data.get('Screener', 'Family Member')).title()

    demo_title_row = [
        Paragraph("1. PATIENT DEMOGRAPHICS &amp; CLINICAL EPIDEMIOLOGY", style_section_title),
        "", "", ""
    ]
    demo_row1 = [
        Paragraph(f"<strong>Patient ID:</strong> {patient_name}", style_body),
        Paragraph(f"<strong>Chronological Age:</strong> {age_mons} Months", style_body),
        Paragraph(f"<strong>Biological Sex:</strong> {sex_str}", style_body),
        Paragraph(f"<strong>Ethnicity:</strong> {ethnicity}", style_body)
    ]
    demo_row2 = [
        Paragraph(f"<strong>Informant / Guardian:</strong> {guardian}", style_body),
        Paragraph(f"<strong>Neonatal Jaundice:</strong> {jaundice}", style_body),
        Paragraph(f"<strong>Family ASD History:</strong> {fam_asd}", style_body),
        Paragraph(f"<strong>Test Administrator:</strong> {screener}", style_body)
    ]
    col_w4 = printable_width / 4.0
    demo_table = Table([demo_title_row, demo_row1, demo_row2], colWidths=[col_w4]*4)
    demo_table.setStyle(TableStyle([
        ('SPAN', (0,0), (3,0)),
        ('BACKGROUND', (0,0), (3,0), colors.HexColor('#F4F6F8')),
        ('BOTTOMPADDING', (0,0), (3,0), 3),
        ('TOPPADDING', (0,0), (3,0), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,1), (-1,-1), 4),
        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#C5D0DA')),
        ('INNERGRID', (0,1), (-1,-1), 0.5, colors.HexColor('#E3E8EE')),
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 8))

    # 4. Deep Learning Risk Stratification
    tabnet_prob = data.get('tabnet_prob', 0) * 100.0
    mlp_prob = data.get('mlp_prob', 0) * 100.0
    aq10_score = data.get('aq10_score', 0)
    a_dom = data.get('a_domain', 0)
    b_dom = data.get('b_domain', 0)

    card1 = [
        Paragraph("TABNET ATTENTIVE NETWORK", style_metric_label),
        Spacer(1, 2),
        Paragraph(f"{tabnet_prob:.1f}%", ParagraphStyle('TVal', parent=style_metric_val, textColor=colors.HexColor('#167C80'))),
        Spacer(1, 1),
        Paragraph("Risk Probability (Sparse Attention)", style_metric_sub)
    ]
    card2 = [
        Paragraph("MLP NEURAL BASELINE", style_metric_label),
        Spacer(1, 2),
        Paragraph(f"{mlp_prob:.1f}%", ParagraphStyle('MVal', parent=style_metric_val, textColor=colors.HexColor('#167C80'))),
        Spacer(1, 1),
        Paragraph("Sigmoid Output (Threshold &ge; 60%)", style_metric_sub)
    ]
    card3 = [
        Paragraph("Q-CHAT-10 SCORE", style_metric_label),
        Spacer(1, 2),
        Paragraph(f"{aq10_score} / 10", ParagraphStyle('QVal', parent=style_metric_val, textColor=colors.HexColor('#202B36'))),
        Spacer(1, 1),
        Paragraph(f"Domain A: {a_dom}/9 &bull; Domain B: {b_dom}/1", style_metric_sub)
    ]
    col_w3 = printable_width / 3.0
    eval_table = Table([[card1, card2, card3]], colWidths=[col_w3]*3)
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F6F8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#C5D0DA')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#C5D0DA')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(eval_table)
    story.append(Spacer(1, 8))

    # 5. Itemized Q-CHAT-10 Behavioral Matrix
    questions_info = [
        ("Q1", "Name Orientation", "Does child respond / turn when called by name?", data.get("Q1", 0), "Domain A"),
        ("Q2", "Eye Contact", "Ease of establishing sustained mutual eye contact?", data.get("Q2", 0), "Domain A"),
        ("Q3", "Proto-Imperative Point", "Points to indicate desire for objects?", data.get("Q3", 0), "Domain A"),
        ("Q4", "Proto-Declarative Point", "Points to share interest in objects / events?", data.get("Q4", 0), "Domain A"),
        ("Q5", "Pretend Play", "Engages in symbolic pretend play (e.g. phone, doll)?", data.get("Q5", 0), "Domain A"),
        ("Q6", "Gaze Following", "Follows adult looking direction across room?", data.get("Q6", 0), "Domain A"),
        ("Q7", "Affective Empathy", "Consoles or reacts to visibly upset family members?", data.get("Q7", 0), "Domain A"),
        ("Q8", "Early Vocalization", "Frequency and communicative quality of words?", data.get("Q8", 0), "Domain A"),
        ("Q9", "Gestural Repertoire", "Uses communicative gestures (e.g. waving bye-bye)?", data.get("Q9", 0), "Domain A"),
        ("Q10", "Repetitive Mannerisms", "Repetitive motor mannerisms or object spinning?", data.get("Q10", 0), "Domain B")
    ]
    matrix_title_row = [
        Paragraph("2. ITEMIZED Q-CHAT-10 BEHAVIORAL MARKER ATTRIBUTION MATRIX", style_section_title),
        "", "", ""
    ]
    matrix_header_row = [
        Paragraph("<strong>Item</strong>", style_body_bold),
        Paragraph("<strong>Clinical Marker &amp; Behavioral Inquiry</strong>", style_body_bold),
        Paragraph("<strong>Domain</strong>", style_body_bold),
        Paragraph("<strong>Attribution Score</strong>", style_body_bold)
    ]
    matrix_rows = [matrix_title_row, matrix_header_row]
    row_styles = [
        ('SPAN', (0,0), (3,0)),
        ('BACKGROUND', (0,0), (3,0), colors.HexColor('#F4F6F8')),
        ('BACKGROUND', (0,1), (3,1), colors.HexColor('#E3E8EE')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#C5D0DA')),
        ('INNERGRID', (0,1), (-1,-1), 0.5, colors.HexColor('#E3E8EE')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]
    col_w_matrix = [printable_width * 0.08, printable_width * 0.54, printable_width * 0.18, printable_width * 0.20]

    for idx, (qid, qtitle, qdesc, val, dom) in enumerate(questions_info, start=2):
        val_int = 1 if str(val).lower() in ['1', 'yes', 'true'] else 0
        if val_int == 1:
            score_text = "<strong>Atypical (1)</strong>"
            score_color = colors.HexColor('#991B1B')
        else:
            score_text = "Typical (0)"
            score_color = colors.HexColor('#065F46')

        desc_para = Paragraph(f"<strong>{qtitle}</strong> &bull; <font color='#667085'>{qdesc}</font>", style_body)
        dom_para = Paragraph(f"<font color='#667085'>{dom}</font>", style_body)
        score_para = Paragraph(f"<font color='{score_color.hexval()}'>{score_text}</font>", style_body)

        matrix_rows.append([
            Paragraph(f"<strong>{qid}</strong>", style_body),
            desc_para,
            dom_para,
            score_para
        ])
        if idx % 2 == 1:
            row_styles.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor('#F4F6F8')))

    matrix_table = Table(matrix_rows, colWidths=col_w_matrix)
    matrix_table.setStyle(TableStyle(row_styles))
    story.append(matrix_table)
    story.append(Spacer(1, 8))

    # 6. Recommendations
    if is_elevated:
        recs = [
            "<strong>Priority Pediatric Referral:</strong> Schedule comprehensive multidisciplinary diagnostic evaluation (ADOS-2 / ADI-R / CARS-2).",
            "<strong>Early Intervention Services:</strong> Connect with state/regional early developmental intervention for speech, language, and occupational therapy.",
            "<strong>Audiological Evaluation:</strong> Complete formal pediatric hearing screening to rule out peripheral sensory deficits."
        ]
    else:
        recs = [
            "<strong>Developmental Surveillance:</strong> Continue standard 18-, 24-, and 30-month well-child pediatric checkups.",
            "<strong>Milestone Tracking:</strong> Monitor continuous social communication and language acquisition milestones with primary pediatrician."
        ]
    rec_paras = [Paragraph("3. CLINICAL RECOMMENDATIONS &amp; ACTION PLAN", style_section_title)]
    for r in recs:
        rec_paras.append(Paragraph(f"&bull; {r}", style_body))
        rec_paras.append(Spacer(1, 1.5))
    rec_table = Table([[rec_paras]], colWidths=[printable_width])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F6F8')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#C5D0DA')),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 8))

    # 7. Signatures
    examiner = data.get('examiner', 'Evaluating Specialist (Clinical Assessment)')
    sig_left = [
        Paragraph("Evaluating Specialist / Clinician:", style_small),
        Spacer(1, 2),
        Paragraph(f"<strong>{examiner}</strong>", style_body_bold),
        Paragraph("Pediatric Assessment Protocol &bull; Clinical Screening Evaluation Record", style_small),
        Paragraph(institution, style_small)
    ]
    sig_right = [
        Spacer(1, 14),
        HRFlowable(width="80%", thickness=1, color=colors.HexColor('#202B36'), spaceBefore=0, spaceAfter=2, hAlign='RIGHT'),
        Paragraph("Physician / Licensed Examiner Signature &amp; Date", ParagraphStyle('SigCap', parent=style_small, alignment=TA_RIGHT))
    ]
    sig_table = Table([[sig_left, sig_right]], colWidths=[printable_width * 0.60, printable_width * 0.40])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))

    # 8. Disclaimer
    disclaimer_p = Paragraph(
        "<strong>MEDICAL DISCLAIMER:</strong> This document is generated as an academic screening decision support output. "
        "It does NOT constitute a definitive psychiatric or medical diagnosis. Final diagnostic determination must be conducted "
        "by qualified healthcare professionals following direct clinical assessment (e.g. DSM-5 / ICD-11 criteria).",
        ParagraphStyle('Disc', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#7F1D1D'))
    )
    disc_table = Table([[disclaimer_p]], colWidths=[printable_width])
    disc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#FCA5A5')),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    story.append(KeepTogether([sig_table, Spacer(1, 6), disc_table]))

    doc.build(story, canvasmaker=NumberedCanvas)
    return buf.getvalue()


def get_default_sample_report(risk_type="elevated"):
    """Generates a realistic clinical sample report for instant testing & printing."""
    if risk_type == "elevated":
        return {
            "patient_name": "Liam Davis",
            "guardian_name": "Sarah Davis (Mother)",
            "mrn": "MRN-ASD-2026-0842",
            "date": datetime.date.today().strftime("%B %d, %Y"),
            "examiner": "Evaluating Specialist (Clinical Assessment)",
            "institution": "Pediatric Neurodevelopmental & Clinical AI Research Center",
            "Age": 24,
            "Sex": "m",
            "Ethnicity": "White-European",
            "Jaundice": "yes",
            "Family_ASD": "yes",
            "Screener": "family member",
            "Q1": 1, "Q2": 1, "Q3": 1, "Q4": 1, "Q5": 1,
            "Q6": 1, "Q7": 0, "Q8": 1, "Q9": 0, "Q10": 1,
            "tabnet_prob": 0.9998,
            "tabnet_pred": 1,
            "mlp_prob": 0.9991,
            "mlp_pred": 1,
            "aq10_score": 8,
            "a_domain": 7,
            "b_domain": 1,
            "is_sample": True
        }
    else:
        return {
            "patient_name": "Emma Watson",
            "guardian_name": "David Watson (Father)",
            "mrn": "MRN-TYP-2026-0199",
            "date": datetime.date.today().strftime("%B %d, %Y"),
            "examiner": "Evaluating Specialist (Clinical Assessment)",
            "institution": "Pediatric Neurodevelopmental & Clinical AI Research Center",
            "Age": 28,
            "Sex": "f",
            "Ethnicity": "Asian",
            "Jaundice": "no",
            "Family_ASD": "no",
            "Screener": "family member",
            "Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0, "Q5": 0,
            "Q6": 0, "Q7": 0, "Q8": 0, "Q9": 0, "Q10": 0,
            "tabnet_prob": 0.0003,
            "tabnet_pred": 0,
            "mlp_prob": 0.0012,
            "mlp_pred": 0,
            "aq10_score": 0,
            "a_domain": 0,
            "b_domain": 0,
            "is_sample": True
        }

def generate_standalone_html_report(data):
    """Constructs a complete, standalone printable HTML document for downloading."""
    is_elevated = (data.get("tabnet_pred") == 1) or (data.get("mlp_pred") == 1) or (data.get("aq10_score", 0) >= 3)
    status_text = "ELEVATED ASD RISK PROFILE" if is_elevated else "TYPICAL DEVELOPMENTAL PROFILE"
    status_bg = "#FEF2F2" if is_elevated else "#F0FDF4"
    status_color = "#991B1B" if is_elevated else "#065F46"
    status_border = "#EF4444" if is_elevated else "#10B981"

    questions_info = [
        ("Q1", "Name Orientation / Attention", "Does child look when called by name?", data.get("Q1", 0), "Domain A"),
        ("Q2", "Eye Gaze Contact", "Ease of establishing mutual eye contact?", data.get("Q2", 0), "Domain A"),
        ("Q3", "Proto-Imperative Pointing", "Points to indicate desire for objects?", data.get("Q3", 0), "Domain A"),
        ("Q4", "Proto-Declarative Pointing", "Points to share interest with others?", data.get("Q4", 0), "Domain A"),
        ("Q5", "Pretend / Symbolic Play", "Engages in pretend play (e.g. phone, doll)?", data.get("Q5", 0), "Domain A"),
        ("Q6", "Gaze Tracking / Shared Attention", "Follows adult's looking direction?", data.get("Q6", 0), "Domain A"),
        ("Q7", "Affective Empathy Response", "Consoles visibly upset family members?", data.get("Q7", 0), "Domain A"),
        ("Q8", "Early Vocalization / Communicative Speech", "Nature of early vocalizations / words?", data.get("Q8", 0), "Domain A"),
        ("Q9", "Communicative Gestural Repertoire", "Uses simple gestures (e.g. waving bye-bye)?", data.get("Q9", 0), "Domain A"),
        ("Q10", "Repetitive Mannerisms / Visual Fixation", "Repetitive motor mannerisms or staring?", data.get("Q10", 0), "Domain B")
    ]

    table_rows = ""
    for qid, qtitle, qdesc, val, dom in questions_info:
        badge_style = "background: #FEE2E2; color: #991B1B;" if val == 1 else "background: #DCFCE7; color: #065F46;"
        val_text = "Atypical Trait (1)" if val == 1 else "Typical Response (0)"
        table_rows += f"""
        <tr>
            <td style="font-weight: 700;">{qid}</td>
            <td><strong>{qtitle}</strong><br><span style="font-size: 0.85rem; color: #667085;">{qdesc}</span></td>
            <td><span style="font-size: 0.78rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px; {badge_style}">{dom}</span></td>
            <td><span style="font-size: 0.82rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; {badge_style}">{val_text}</span></td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ASD Clinical Screening Report - {data.get('patient_name', 'Patient')}</title>
    <style>
        @page {{ size: A4; margin: 20mm; }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            color: #202B36;
            background: #FFFFFF;
            margin: 0;
            padding: 25px;
            font-size: 11pt;
            line-height: 1.5;
        }}
        .report-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid #167C80;
            padding-bottom: 14px;
            margin-bottom: 20px;
        }}
        .status-box {{
            background: {status_bg};
            border: 2px solid {status_border};
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
        }}
        .status-title {{
            font-size: 1.3rem;
            font-weight: 800;
            color: {status_color};
            margin: 0 0 6px 0;
        }}
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        .info-table th {{
            background: #F4F6F8;
            color: #202B36;
            text-align: left;
            padding: 8px 12px;
            border-bottom: 2px solid #C5D0DA;
            font-size: 0.88rem;
        }}
        .info-table td {{
            padding: 8px 12px;
            border-bottom: 1px solid #E3E8EE;
            font-size: 0.9rem;
        }}
        .eval-grid {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }}
        .eval-card {{
            flex: 1;
            border: 1px solid #C5D0DA;
            border-radius: 10px;
            padding: 14px;
            background: #F4F6F8;
        }}
        .eval-title {{
            font-size: 0.85rem;
            font-weight: 700;
            color: #667085;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}
        .eval-val {{
            font-size: 1.6rem;
            font-weight: 800;
            color: #167C80;
        }}
        .signature-section {{
            margin-top: 30px;
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #E3E8EE;
            padding-top: 20px;
        }}
        .sig-line {{
            width: 250px;
            border-top: 1px solid #202B36;
            margin-top: 40px;
            text-align: center;
            font-size: 0.85rem;
        }}
        .disclaimer {{
            margin-top: 25px;
            padding: 12px 16px;
            background: #FEF2F2;
            border-left: 4px solid #EF4444;
            font-size: 0.82rem;
            color: #7F1D1D;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            body {{ padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="no-print" style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; background: #F4F6F8; border: 1.5px solid #E3E8EE; padding: 12px 18px; border-radius: 12px;">
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="https://autism-spectrum-disorder.streamlit.app" style="display: inline-flex; align-items: center; gap: 6px; background: #202B36; color: #FFFFFF; font-weight: 700; text-decoration: none; padding: 8px 18px; border-radius: 8px; font-size: 0.9rem;">
                &larr; Back to Platform Website
            </a>
            <button onclick="if(window.history.length &gt; 1) {{ window.history.back(); }} else {{ window.location.href='https://autism-spectrum-disorder.streamlit.app'; }}" style="background: #FFFFFF; color: #202B36; font-weight: 700; padding: 8px 16px; border: 1.5px solid #C5D0DA; border-radius: 8px; cursor: pointer; font-size: 0.9rem;">
                &larr; Previous Page
            </button>
        </div>
        <div>
            <button onclick="window.print()" style="background: #167C80; color: #FFFFFF; font-weight: 700; padding: 8px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 0.9rem; box-shadow: 0 2px 8px rgba(22,124,128,0.25);">
                Print Clinical Report
            </button>
        </div>
    </div>

    <div class="report-header">
        <div>
            <div style="font-size: 0.78rem; font-weight: 800; color: #167C80; letter-spacing: 0.08em; text-transform: uppercase;">
                OFFICIAL CLINICAL SCREENING ASSESSMENT
            </div>
            <h1 style="font-size: 1.6rem; font-weight: 800; margin: 4px 0 0 0; color: #202B36;">
                Pediatric Autism Spectrum Developmental Evaluation
            </h1>
            <div style="font-size: 0.88rem; color: #667085; margin-top: 3px;">
                {data.get('institution', 'Pediatric Neurodevelopmental Research Center')}
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.82rem; color: #667085;">MRN: <strong>{data.get('mrn', 'N/A')}</strong></div>
            <div style="font-size: 0.82rem; color: #667085;">Date: <strong>{data.get('date', datetime.date.today().strftime('%B %d, %Y'))}</strong></div>
        </div>
    </div>

    <div class="status-box">
        <div class="status-title">{status_text}</div>
        <p style="margin: 0; font-size: 0.95rem; color: #202B36;">
            Multivariate screening based on standardized <strong>Q-CHAT-10</strong> protocol combined with calibrated deep tabular models (TabNet Attentive Learning & Multi-Layer Perceptron).
        </p>
    </div>

    <table class="info-table">
        <tr>
            <th colspan="4" style="background: #E3E8EE; font-size: 0.95rem;">1. PATIENT DEMOGRAPHICS & CLINICAL HISTORY</th>
        </tr>
        <tr>
            <td><strong>Child's Name / ID:</strong> {data.get('patient_name', 'Liam Davis')}</td>
            <td><strong>Chronological Age:</strong> {data.get('Age', 24)} Months</td>
            <td><strong>Biological Sex:</strong> {'Male' if data.get('Sex') == 'm' else 'Female'}</td>
            <td><strong>Ethnicity:</strong> {str(data.get('Ethnicity', 'N/A')).title()}</td>
        </tr>
        <tr>
            <td><strong>Parent / Guardian:</strong> {str(data.get('guardian_name', 'Sarah Davis (Mother)')).title()}</td>
            <td><strong>Neonatal Jaundice:</strong> {str(data.get('Jaundice', 'no')).title()}</td>
            <td><strong>Immediate Family ASD History:</strong> {str(data.get('Family_ASD', 'no')).title()}</td>
            <td><strong>Informant / Screener:</strong> {str(data.get('Screener', 'Family Member')).title()}</td>
        </tr>
    </table>

    <div class="eval-grid">
        <div class="eval-card">
            <div class="eval-title">TabNet Attentive Output</div>
            <div class="eval-val">{data.get('tabnet_prob', 0) * 100:.1f}%</div>
            <div style="font-size: 0.82rem; color: #667085;">Risk Confidence (Sparse Attention)</div>
        </div>
        <div class="eval-card">
            <div class="eval-title">MLP Neural Net Output</div>
            <div class="eval-val" style="color: #167C80;">{data.get('mlp_prob', 0) * 100:.1f}%</div>
            <div style="font-size: 0.82rem; color: #667085;">Sigmoid Prob (Cutoff &ge; 0.60)</div>
        </div>
        <div class="eval-card">
            <div class="eval-title">Q-CHAT Total Score</div>
            <div class="eval-val" style="color: #202B36;">{data.get('aq10_score', 0)} / 10</div>
            <div style="font-size: 0.82rem; color: #667085;">Domain A: {data.get('a_domain', 0)}/9 &bull; Domain B: {data.get('b_domain', 0)}/1</div>
        </div>
    </div>

    <table class="info-table">
        <thead>
            <tr>
                <th style="width: 8%;">Item</th>
                <th style="width: 52%;">Clinical Trait & Questionnaire Inquiry</th>
                <th style="width: 20%;">Clinical Domain</th>
                <th style="width: 20%;">Score Attribution</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>

    <div style="margin-top: 20px;">
        <h4 style="margin: 0 0 8px 0; font-size: 1rem; color: #202B36;">Clinical Recommendation & Referral Plan:</h4>
        <ul style="margin: 0; padding-left: 20px; font-size: 0.92rem; color: #202B36;">
            {'<li><strong>Priority Pediatric Referral:</strong> Schedule comprehensive multidisciplinary developmental diagnostic evaluation (ADOS-2 / ADI-R).</li><li><strong>Immediate Early Intervention:</strong> Refer to state/regional early intervention services for communication and occupational support.</li><li><strong>Audiological Clearance:</strong> Complete formal hearing examination to rule out sensory peripheral deficits.</li>' if is_elevated else '<li><strong>Developmental Surveillance:</strong> Continue routine 18- and 24-month well-child pediatric developmental monitoring.</li><li><strong>Milestone Tracking:</strong> Follow standard communication and social play milestones with pediatrician.</li>'}
        </ul>
    </div>

    <div class="signature-section">
        <div>
            <div style="font-size: 0.85rem; color: #667085;">Evaluating Clinician / Informant:</div>
            <div style="font-weight: 700; color: #202B36; margin-top: 4px;">{data.get('examiner', 'Evaluating Specialist (Clinical Assessment)')}</div>
            <div style="font-size: 0.82rem; color: #667085;">Board Certified Pediatric Specialist</div>
        </div>
        <div>
            <div class="sig-line">
                Physician / Specialist Signature & Date
            </div>
        </div>
    </div>

    <div class="disclaimer">
        <strong>MEDICAL DISCLAIMER:</strong> This document is generated as an academic screening decision support output. It does NOT constitute a definitive psychiatric or medical diagnosis. Final diagnostic confirmation must be conducted by qualified healthcare professionals.
    </div>
</body>
</html>"""
    return html

def render():
    render_section_header(
        "Clinical Diagnostic Test Report",
        "Official pediatric screening report with itemized behavioral matrix, dual deep learning risk stratification, and one-click print/export.",
        badge="PATIENT TEST REPORT"
    )

    # Check if latest report is in session state
    if "latest_patient_report" not in st.session_state:
        st.session_state["latest_patient_report"] = get_default_sample_report("elevated")

    # Action Toolbar
    st.subheader("1. Report Settings & Patient Case")
    
    t_col1, t_col2, t_col3, t_col4 = st.columns([1.5, 1.5, 1.3, 1.3])
    
    with t_col1:
        if st.button("Load Elevated Risk Sample", use_container_width=True, help="Load representative toddler case with ASD traits"):
            st.session_state["latest_patient_report"] = get_default_sample_report("elevated")
            st.rerun()

    with t_col2:
        if st.button("Load Typical Child Sample", use_container_width=True, help="Load representative toddler case with typical development"):
            st.session_state["latest_patient_report"] = get_default_sample_report("typical")
            st.rerun()

    with t_col3:
        if st.button("Return to Home", use_container_width=True, help="Navigate back to the main homepage"):
            st.session_state["nav_target"] = "Home"
            st.rerun()

    with t_col4:
        if st.button("Back to Screener", use_container_width=True, help="Return to the ASD screening wizard"):
            st.session_state["nav_target"] = "Early ASD Detection"
            st.rerun()

    report_data = st.session_state["latest_patient_report"]

    with st.expander("Customize Patient Identification & Clinic Information", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Patient Name / Child Identifier", value=report_data.get("patient_name", "Liam Davis"))
            p_mrn = st.text_input("Medical Record Number (MRN)", value=report_data.get("mrn", "MRN-ASD-2026-0842"))
            p_date = st.date_input("Evaluation Date", value=datetime.date.today()).strftime("%B %d, %Y")
        with c2:
            p_examiner = st.text_input("Evaluating Specialist / Clinician", value=report_data.get("examiner", "Evaluating Specialist (Clinical Assessment)"))
            p_inst = st.text_input("Clinical Facility / Hospital", value=report_data.get("institution", "Pediatric Neurodevelopmental Research Center"))
        
        report_data["patient_name"] = p_name
        report_data["mrn"] = p_mrn
        report_data["date"] = p_date
        report_data["examiner"] = p_examiner
        report_data["institution"] = p_inst

    # Print & Download Controls Bar
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("2. Export & Print Options")

    # Generate Clinical PDF Report (Medical-grade format)
    pdf_bytes = None
    pdf_error = None
    try:
        pdf_bytes = generate_clinical_pdf_report(report_data)
    except Exception as _pdf_err:
        pdf_error = str(_pdf_err)

    html_content = generate_standalone_html_report(report_data)

    patient_slug = str(report_data.get('patient_name', 'Patient')).strip().replace(' ', '_')
    mrn_slug = str(report_data.get('mrn', 'MRN')).strip().replace(' ', '_')
    file_base = f"Clinical_ASD_Report_{patient_slug}_{mrn_slug}"

    p_col1, p_col2, p_col3, p_spacer = st.columns([2.4, 2.0, 1.8, 1.8])

    with p_col1:
        if pdf_bytes is not None:
            st.download_button(
                label="Download Clinical Report (PDF)",
                data=pdf_bytes,
                file_name=f"{file_base}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
                help="Official high-fidelity clinical diagnostic screening report in PDF format matching medical records standard"
            )
        else:
            st.button(
                "PDF Compiling...",
                disabled=True,
                use_container_width=True,
                type="primary"
            )
            if pdf_error:
                st.caption(f"PDF note: {pdf_error}")

    with p_col2:
        st.download_button(
            label="Download HTML Report",
            data=html_content,
            file_name=f"{file_base}.html",
            mime="text/html",
            use_container_width=True,
            help="Download standalone browser-viewable HTML version"
        )

    with p_col3:
        render_html("""
        <button onclick="window.print()" style="background: #F4F6F8; color: #202B36; font-weight: 700; padding: 9px 16px; border-radius: 8px; border: 1px solid #C5D0DA; cursor: pointer; width: 100%; font-size: 0.9rem; transition: all 0.2s ease;">
            Print Document
        </button>
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("3. Document Preview (Official Clinical Screening Report)")

    # Render Clean High-Fidelity Medical Document Preview
    is_elevated = (report_data.get("tabnet_pred") == 1) or (report_data.get("mlp_pred") == 1) or (report_data.get("aq10_score", 0) >= 3)
    
    render_html(f"""
    <div class="printable-report">
        <!-- Header -->
        <div class="report-header-banner">
            <div>
                <span class="clinical-brand-badge" style="margin-bottom: 6px;">CONFIDENTIAL MEDICAL SCREENING DOCUMENT</span>
                <h2 style="font-size: 1.65rem; font-weight: 800; color: #202B36; margin: 4px 0 2px 0;">
                    Pediatric Autism Spectrum Developmental Evaluation
                </h2>
                <div style="font-size: 0.92rem; color: #667085;">
                    {report_data.get('institution', 'Pediatric Neurodevelopmental Research Center')}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.88rem; color: #202B36;"><strong>MRN:</strong> {report_data.get('mrn', 'N/A')}</div>
                <div style="font-size: 0.88rem; color: #667085;"><strong>Date:</strong> {report_data.get('date', datetime.date.today().strftime('%B %d, %Y'))}</div>
                <div style="font-size: 0.78rem; color: #8899A6; margin-top: 4px;">Protocol: Q-CHAT-10 / DeepScreen AI</div>
            </div>
        </div>

        <!-- Risk Status Banner -->
        <div style="background: {'#FEF2F2' if is_elevated else '#F0FDF4'}; border: 2px solid {'#EF4444' if is_elevated else '#10B981'}; border-radius: 14px; padding: 18px 24px; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span class="pill-badge" style="background: {'#DC2626' if is_elevated else '#059669'}; color: #FFFFFF; font-size: 0.82rem;">
                        {'ELEVATED ASD RISK PROFILE' if is_elevated else 'TYPICAL DEVELOPMENT PROFILE'}
                    </span>
                    <h3 style="color: {'#991B1B' if is_elevated else '#065F46'}; margin: 10px 0 4px 0; font-size: 1.35rem; font-weight: 800;">
                        {'Developmental Autism Spectrum Traits Indicated' if is_elevated else 'Normative Developmental Trajectory Indicated'}
                    </h3>
                    <p style="color: {'#7F1D1D' if is_elevated else '#064E3B'}; margin: 0; font-size: 0.94rem;">
                        {'Atypical response patterns identified across early social communication and motor behavioral markers. Multidisciplinary clinical evaluation is advised.' if is_elevated else 'Response distribution falls within typical normative milestones. Continue routine pediatric surveillance.'}
                    </p>
                </div>
                <div style="margin-left: 20px; align-self: center;">
                    <span style="display: inline-block; padding: 6px 14px; border-radius: 6px; font-size: 11px; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; background: {'#FEF2F2' if is_elevated else '#ECFDF5'}; color: {'#991B1B' if is_elevated else '#065F46'}; border: 1px solid {'#FCA5A5' if is_elevated else '#A7F3D0'};">
                        {'HIGH RISK' if is_elevated else 'LOW RISK'}
                    </span>
                </div>
            </div>
        </div>

        <!-- Patient Demographics Table -->
        <h4 style="color: #202B36; font-size: 1.05rem; font-weight: 700; margin-bottom: 8px;">
            1. Patient Demographics & Clinical History
        </h4>
        <table class="report-table">
            <tr>
                <td style="width: 25%;"><strong>Child's Name / ID:</strong> {report_data.get('patient_name', 'Liam Davis')}</td>
                <td style="width: 25%;"><strong>Age:</strong> {report_data.get('Age', 24)} Months</td>
                <td style="width: 25%;"><strong>Biological Sex:</strong> {'Male' if report_data.get('Sex') == 'm' else 'Female'}</td>
                <td style="width: 25%;"><strong>Ethnicity:</strong> {str(report_data.get('Ethnicity', 'N/A')).title()}</td>
            </tr>
            <tr>
                <td><strong>Parent / Guardian:</strong> {str(report_data.get('guardian_name', 'Sarah Davis (Mother)')).title()}</td>
                <td><strong>Neonatal Jaundice:</strong> {str(report_data.get('Jaundice', 'no')).title()}</td>
                <td><strong>Family ASD History:</strong> {str(report_data.get('Family_ASD', 'no')).title()}</td>
                <td><strong>Informant / Screener:</strong> {str(report_data.get('Screener', 'Family Member')).title()}</td>
            </tr>
        </table>

        <!-- Model Predictions -->
        <h4 style="color: #202B36; font-size: 1.05rem; font-weight: 700; margin: 24px 0 8px 0;">
            2. Deep Learning Multimodal Risk Scoring
        </h4>
        <div style="display: flex; gap: 16px; margin-bottom: 24px;">
            <div style="flex: 1; background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #167C80; text-transform: uppercase;">TabNet Attentive Output</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #167C80; margin: 4px 0;">
                    {report_data.get('tabnet_prob', 0) * 100:.1f}%
                </div>
                <div style="font-size: 0.82rem; color: #667085;">
                    Status: <strong>{'ASD Positive' if report_data.get('tabnet_pred') == 1 else 'ASD Negative'}</strong><br>
                    Sequential Sparse Attention
                </div>
            </div>

            <div style="flex: 1; background: #F3E8FF; border: 1px solid #DDD6FE; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #167C80; text-transform: uppercase;">MLP Neural Net Output</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #167C80; margin: 4px 0;">
                    {report_data.get('mlp_prob', 0) * 100:.1f}%
                </div>
                <div style="font-size: 0.82rem; color: #667085;">
                    Status: <strong>{'ASD Positive' if report_data.get('mlp_pred') == 1 else 'ASD Negative'}</strong><br>
                    Calibrated Sigmoid (Cutoff &ge; 0.60)
                </div>
            </div>

            <div style="flex: 1; background: #F4F6F8; border: 1px solid #C5D0DA; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #202B36; text-transform: uppercase;">Cumulative Q-CHAT Score</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #202B36; margin: 4px 0;">
                    {report_data.get('aq10_score', 0)} / 10
                </div>
                <div style="font-size: 0.82rem; color: #667085;">
                    Domain A (Social): <strong>{report_data.get('a_domain', 0)}/9</strong><br>
                    Domain B (Repetitive): <strong>{report_data.get('b_domain', 0)}/1</strong>
                </div>
            </div>
        </div>

        <!-- Domain Meter Bars -->
        <div style="background: #FFFFFF; border: 1px solid #E3E8EE; border-radius: 12px; padding: 18px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600;">
                <span>Domain A: Social Communication & Reciprocal Interaction ({report_data.get('a_domain', 0)} / 9)</span>
                <span>{report_data.get('a_domain', 0) / 9 * 100:.0f}%</span>
            </div>
            <div class="domain-meter-container">
                <div class="domain-meter-fill" style="width: {report_data.get('a_domain', 0) / 9 * 100}%; background: {'#EF4444' if report_data.get('a_domain', 0) >= 3 else '#10B981'};"></div>
            </div>

            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; margin-top: 10px;">
                <span>Domain B: Repetitive Motor Mannerisms & Stereotypies ({report_data.get('b_domain', 0)} / 1)</span>
                <span>{report_data.get('b_domain', 0) * 100:.0f}%</span>
            </div>
            <div class="domain-meter-container">
                <div class="domain-meter-fill" style="width: {report_data.get('b_domain', 0) * 100}%; background: {'#EF4444' if report_data.get('b_domain', 0) == 1 else '#10B981'};"></div>
            </div>
        </div>

        <!-- Itemized Matrix Table -->
        <h4 style="color: #202B36; font-size: 1.05rem; font-weight: 700; margin-bottom: 8px;">
            3. Q-CHAT-10 Itemized Behavioral Assessment Matrix
        </h4>
        <table class="report-table">
            <thead>
                <tr>
                    <th style="width: 8%;">Item</th>
                    <th style="width: 52%;">Clinical Trait Inquiry</th>
                    <th style="width: 20%;">Clinical Domain</th>
                    <th style="width: 20%;">Observed Trait</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Q1</strong></td>
                    <td>Response to Name / Orientation</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q1') == 1 else 'Typical / Present (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q2</strong></td>
                    <td>Establishing Mutual Eye Contact</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Difficult / Rare (1)' if report_data.get('Q2') == 1 else 'Easy / Typical (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q3</strong></td>
                    <td>Proto-Imperative Pointing (Wants)</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q3') == 1 else 'Typical / Regular (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q4</strong></td>
                    <td>Proto-Declarative Pointing (Shared Interest)</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q4') == 1 else 'Typical / Regular (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q5</strong></td>
                    <td>Pretend & Symbolic Play</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q5') == 1 else 'Typical / Active (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q6</strong></td>
                    <td>Gaze Following / Joint Attention Tracking</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q6') == 1 else 'Typical / Active (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q7</strong></td>
                    <td>Affective Empathy / Consoling Behavior</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q7') == 1 else 'Typical / Active (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q8</strong></td>
                    <td>Early Communicative Words / Vocalizations</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q8') == 1 else 'Typical / Active (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q9</strong></td>
                    <td>Communicative Gestures (Waving, Nodding)</td>
                    <td><span class="pill-badge pill-blue">Domain A</span></td>
                    <td>{'Atypical / Absent (1)' if report_data.get('Q9') == 1 else 'Typical / Active (0)'}</td>
                </tr>
                <tr>
                    <td><strong>Q10</strong></td>
                    <td>Repetitive Motor Stereotypies or Fixation</td>
                    <td><span class="pill-badge pill-purple">Domain B</span></td>
                    <td>{'Present / Frequent (1)' if report_data.get('Q10') == 1 else 'Absent / Rare (0)'}</td>
                </tr>
            </tbody>
        </table>

        <!-- Sign-off Block -->
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 35px; border-top: 1px solid #E3E8EE; padding-top: 24px;">
            <div>
                <div style="font-size: 0.82rem; color: #526071; text-transform: uppercase; font-weight: 700;">Evaluating Clinician</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #202B36; margin-top: 2px;">
                    {report_data.get('examiner', 'Evaluating Clinician / Specialist')}
                </div>
                <div style="font-size: 0.85rem; color: #526071;">
                    Pediatric Assessment Protocol &bull; Clinical Screening Evaluation Record
                </div>
            </div>
            <div style="text-align: center;">
                <div style="width: 240px; border-top: 1px solid #202B36; padding-top: 6px; font-size: 0.85rem; color: #526071;">
                    Authorized Signature & Date
                </div>
            </div>
        </div>
    </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    b_col1, b_col2, b_spacer = st.columns([1.6, 2.0, 3.4])
    with b_col1:
        if st.button("Return to Home Page", use_container_width=True, type="primary"):
            st.session_state["nav_target"] = "Home"
            st.rerun()
    with b_col2:
        if st.button("Start New Screening Test", use_container_width=True):
            st.session_state["nav_target"] = "Early ASD Detection"
            st.session_state["wiz_step"] = 1
            st.rerun()

    render_disclaimer()
