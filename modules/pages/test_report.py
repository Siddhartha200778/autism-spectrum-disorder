import streamlit as st
import datetime
from modules.theme import render_section_header, render_disclaimer, render_html

def get_default_sample_report(risk_type="elevated"):
    """Generates a realistic clinical sample report for instant testing & printing."""
    if risk_type == "elevated":
        return {
            "patient_name": "Liam Davis",
            "mrn": "MRN-ASD-2026-0842",
            "date": datetime.date.today().strftime("%B %d, %Y"),
            "examiner": "Dr. Sarah Jenkins, MD, FAAP",
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
            "mrn": "MRN-TYP-2026-0199",
            "date": datetime.date.today().strftime("%B %d, %Y"),
            "examiner": "Dr. Sarah Jenkins, MD, FAAP",
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
            <td><strong>{qtitle}</strong><br><span style="font-size: 0.85rem; color: #64748B;">{qdesc}</span></td>
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
            color: #0F172A;
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
            border-bottom: 2px solid #1D4ED8;
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
            background: #F1F5F9;
            color: #0F172A;
            text-align: left;
            padding: 8px 12px;
            border-bottom: 2px solid #CBD5E1;
            font-size: 0.88rem;
        }}
        .info-table td {{
            padding: 8px 12px;
            border-bottom: 1px solid #E2E8F0;
            font-size: 0.9rem;
        }}
        .eval-grid {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }}
        .eval-card {{
            flex: 1;
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            padding: 14px;
            background: #F8FAFC;
        }}
        .eval-title {{
            font-size: 0.85rem;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}
        .eval-val {{
            font-size: 1.6rem;
            font-weight: 800;
            color: #1D4ED8;
        }}
        .signature-section {{
            margin-top: 30px;
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #E2E8F0;
            padding-top: 20px;
        }}
        .sig-line {{
            width: 250px;
            border-top: 1px solid #0F172A;
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
    <div class="no-print" style="margin-bottom: 20px; text-align: right;">
        <button onclick="window.print()" style="background: #1D4ED8; color: #FFFFFF; font-weight: bold; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer;">
            🖨️ Print This Clinical Report
        </button>
    </div>

    <div class="report-header">
        <div>
            <div style="font-size: 0.78rem; font-weight: 800; color: #1D4ED8; letter-spacing: 0.08em; text-transform: uppercase;">
                OFFICIAL CLINICAL SCREENING ASSESSMENT
            </div>
            <h1 style="font-size: 1.6rem; font-weight: 800; margin: 4px 0 0 0; color: #0A192F;">
                Pediatric Autism Spectrum Developmental Evaluation
            </h1>
            <div style="font-size: 0.88rem; color: #64748B; margin-top: 3px;">
                {data.get('institution', 'Pediatric Neurodevelopmental Research Center')}
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.82rem; color: #64748B;">MRN: <strong>{data.get('mrn', 'N/A')}</strong></div>
            <div style="font-size: 0.82rem; color: #64748B;">Date: <strong>{data.get('date', datetime.date.today().strftime('%B %d, %Y'))}</strong></div>
        </div>
    </div>

    <div class="status-box">
        <div class="status-title">{status_text}</div>
        <p style="margin: 0; font-size: 0.95rem; color: #334155;">
            Multivariate screening based on standardized <strong>Q-CHAT-10</strong> protocol combined with calibrated deep tabular models (TabNet Attentive Learning & Multi-Layer Perceptron).
        </p>
    </div>

    <table class="info-table">
        <tr>
            <th colspan="4" style="background: #E2E8F0; font-size: 0.95rem;">1. PATIENT DEMOGRAPHICS & CLINICAL HISTORY</th>
        </tr>
        <tr>
            <td><strong>Child's Name / ID:</strong> {data.get('patient_name', 'Liam Davis')}</td>
            <td><strong>Chronological Age:</strong> {data.get('Age', 24)} Months</td>
            <td><strong>Biological Sex:</strong> {'Male' if data.get('Sex') == 'm' else 'Female'}</td>
            <td><strong>Ethnicity:</strong> {str(data.get('Ethnicity', 'N/A')).title()}</td>
        </tr>
        <tr>
            <td><strong>Neonatal Jaundice:</strong> {str(data.get('Jaundice', 'no')).title()}</td>
            <td><strong>Immediate Family ASD History:</strong> {str(data.get('Family_ASD', 'no')).title()}</td>
            <td><strong>Informant / Screener:</strong> {str(data.get('Screener', 'Family Member')).title()}</td>
            <td><strong>Assessment Instrument:</strong> Q-CHAT-10 Protocol</td>
        </tr>
    </table>

    <div class="eval-grid">
        <div class="eval-card">
            <div class="eval-title">TabNet Attentive Output</div>
            <div class="eval-val">{data.get('tabnet_prob', 0) * 100:.1f}%</div>
            <div style="font-size: 0.82rem; color: #64748B;">Risk Confidence (Sparse Attention)</div>
        </div>
        <div class="eval-card">
            <div class="eval-title">MLP Neural Net Output</div>
            <div class="eval-val" style="color: #7C3AED;">{data.get('mlp_prob', 0) * 100:.1f}%</div>
            <div style="font-size: 0.82rem; color: #64748B;">Sigmoid Prob (Cutoff &ge; 0.60)</div>
        </div>
        <div class="eval-card">
            <div class="eval-title">Q-CHAT Total Score</div>
            <div class="eval-val" style="color: #0F172A;">{data.get('aq10_score', 0)} / 10</div>
            <div style="font-size: 0.82rem; color: #64748B;">Domain A: {data.get('a_domain', 0)}/9 &bull; Domain B: {data.get('b_domain', 0)}/1</div>
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
        <h4 style="margin: 0 0 8px 0; font-size: 1rem; color: #0A192F;">Clinical Recommendation & Referral Plan:</h4>
        <ul style="margin: 0; padding-left: 20px; font-size: 0.92rem; color: #334155;">
            {'<li><strong>Priority Pediatric Referral:</strong> Schedule comprehensive multidisciplinary developmental diagnostic evaluation (ADOS-2 / ADI-R).</li><li><strong>Immediate Early Intervention:</strong> Refer to state/regional early intervention services for communication and occupational support.</li><li><strong>Audiological Clearance:</strong> Complete formal hearing examination to rule out sensory peripheral deficits.</li>' if is_elevated else '<li><strong>Developmental Surveillance:</strong> Continue routine 18- and 24-month well-child pediatric developmental monitoring.</li><li><strong>Milestone Tracking:</strong> Follow standard communication and social play milestones with pediatrician.</li>'}
        </ul>
    </div>

    <div class="signature-section">
        <div>
            <div style="font-size: 0.85rem; color: #64748B;">Evaluating Clinician / Informant:</div>
            <div style="font-weight: 700; color: #0F172A; margin-top: 4px;">{data.get('examiner', 'Dr. Sarah Jenkins, MD, FAAP')}</div>
            <div style="font-size: 0.82rem; color: #64748B;">Board Certified Pediatric Specialist</div>
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
    
    t_col1, t_col2, t_col3, t_col4 = st.columns([1.5, 1.5, 1.2, 1.2])
    
    with t_col1:
        if st.button("📋 Load Elevated Risk Sample", use_container_width=True, help="Load representative toddler case with ASD traits"):
            st.session_state["latest_patient_report"] = get_default_sample_report("elevated")
            st.rerun()

    with t_col2:
        if st.button("📋 Load Typical Child Sample", use_container_width=True, help="Load representative toddler case with typical development"):
            st.session_state["latest_patient_report"] = get_default_sample_report("typical")
            st.rerun()

    report_data = st.session_state["latest_patient_report"]

    with st.expander("✏️ Customize Patient Identification & Clinic Information", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Patient Name / Child Identifier", value=report_data.get("patient_name", "Liam Davis"))
            p_mrn = st.text_input("Medical Record Number (MRN)", value=report_data.get("mrn", "MRN-ASD-2026-0842"))
            p_date = st.date_input("Evaluation Date", value=datetime.date.today()).strftime("%B %d, %Y")
        with c2:
            p_examiner = st.text_input("Evaluating Specialist / Clinician", value=report_data.get("examiner", "Dr. Sarah Jenkins, MD, FAAP"))
            p_inst = st.text_input("Clinical Facility / Hospital", value=report_data.get("institution", "Pediatric Neurodevelopmental Research Center"))
        
        report_data["patient_name"] = p_name
        report_data["mrn"] = p_mrn
        report_data["date"] = p_date
        report_data["examiner"] = p_examiner
        report_data["institution"] = p_inst

    # Print & Download Controls Bar
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("2. Export & Print Options")
    
    html_content = generate_standalone_html_report(report_data)
    
    p_col1, p_col2, p_spacer = st.columns([1.8, 2.2, 3.5])
    with p_col1:
        # Browser print trigger using HTML iframe
        st.download_button(
            label="📥 Download Official HTML Report",
            data=html_content,
            file_name=f"ASD_Screening_Report_{report_data.get('patient_name', 'Patient').replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True,
            type="primary"
        )
    with p_col2:
        # Client side JavaScript print helper
        st.markdown("""
        <button onclick="window.print()" style="background: linear-gradient(135deg, #0A192F 0%, #1D4ED8 100%); color: #FFFFFF; font-weight: 700; padding: 10px 20px; border-radius: 10px; border: none; cursor: pointer; width: 100%; box-shadow: 0 4px 12px rgba(29,78,216,0.3);">
            🖨️ Open Print Dialog (PDF)
        </button>
        """, unsafe_allow_html=True)

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
                <h2 style="font-size: 1.65rem; font-weight: 800; color: #0A192F; margin: 4px 0 2px 0;">
                    Pediatric Autism Spectrum Developmental Evaluation
                </h2>
                <div style="font-size: 0.92rem; color: #64748B;">
                    {report_data.get('institution', 'Pediatric Neurodevelopmental Research Center')}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.88rem; color: #0F172A;"><strong>MRN:</strong> {report_data.get('mrn', 'N/A')}</div>
                <div style="font-size: 0.88rem; color: #64748B;"><strong>Date:</strong> {report_data.get('date', datetime.date.today().strftime('%B %d, %Y'))}</div>
                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">Protocol: Q-CHAT-10 / DeepScreen AI</div>
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
                <div style="font-size: 2.8rem; margin-left: 20px;">
                    {'⚠️' if is_elevated else '✅'}
                </div>
            </div>
        </div>

        <!-- Patient Demographics Table -->
        <h4 style="color: #0A192F; font-size: 1.05rem; font-weight: 700; margin-bottom: 8px;">
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
                <td><strong>Neonatal Jaundice:</strong> {str(report_data.get('Jaundice', 'no')).title()}</td>
                <td><strong>Family ASD History:</strong> {str(report_data.get('Family_ASD', 'no')).title()}</td>
                <td><strong>Informant / Screener:</strong> {str(report_data.get('Screener', 'Family Member')).title()}</td>
                <td><strong>Assessment Type:</strong> Early Toddler Screening</td>
            </tr>
        </table>

        <!-- Model Predictions -->
        <h4 style="color: #0A192F; font-size: 1.05rem; font-weight: 700; margin: 24px 0 8px 0;">
            2. Deep Learning Multimodal Risk Scoring
        </h4>
        <div style="display: flex; gap: 16px; margin-bottom: 24px;">
            <div style="flex: 1; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #1D4ED8; text-transform: uppercase;">TabNet Attentive Output</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #1D4ED8; margin: 4px 0;">
                    {report_data.get('tabnet_prob', 0) * 100:.1f}%
                </div>
                <div style="font-size: 0.82rem; color: #475569;">
                    Status: <strong>{'ASD Positive' if report_data.get('tabnet_pred') == 1 else 'ASD Negative'}</strong><br>
                    Sequential Sparse Attention
                </div>
            </div>

            <div style="flex: 1; background: #F3E8FF; border: 1px solid #DDD6FE; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #7C3AED; text-transform: uppercase;">MLP Neural Net Output</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #7C3AED; margin: 4px 0;">
                    {report_data.get('mlp_prob', 0) * 100:.1f}%
                </div>
                <div style="font-size: 0.82rem; color: #475569;">
                    Status: <strong>{'ASD Positive' if report_data.get('mlp_pred') == 1 else 'ASD Negative'}</strong><br>
                    Calibrated Sigmoid (Cutoff &ge; 0.60)
                </div>
            </div>

            <div style="flex: 1; background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #0F172A; text-transform: uppercase;">Cumulative Q-CHAT Score</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 4px 0;">
                    {report_data.get('aq10_score', 0)} / 10
                </div>
                <div style="font-size: 0.82rem; color: #475569;">
                    Domain A (Social): <strong>{report_data.get('a_domain', 0)}/9</strong><br>
                    Domain B (Repetitive): <strong>{report_data.get('b_domain', 0)}/1</strong>
                </div>
            </div>
        </div>

        <!-- Domain Meter Bars -->
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; margin-bottom: 24px;">
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
        <h4 style="color: #0A192F; font-size: 1.05rem; font-weight: 700; margin-bottom: 8px;">
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
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 35px; border-top: 1px solid #E2E8F0; padding-top: 24px;">
            <div>
                <div style="font-size: 0.82rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Evaluating Clinician</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #0A192F; margin-top: 2px;">
                    {report_data.get('examiner', 'Dr. Sarah Jenkins, MD, FAAP')}
                </div>
                <div style="font-size: 0.85rem; color: #64748B;">
                    Pediatric Neurodevelopmental Specialist &bull; License #PEDI-48291
                </div>
            </div>
            <div style="text-align: center;">
                <div style="width: 240px; border-top: 1px solid #0F172A; padding-top: 6px; font-size: 0.85rem; color: #475569;">
                    Authorized Signature & Date
                </div>
            </div>
        </div>
    </div>
    """)

    render_disclaimer()
