import streamlit as st
import pandas as pd
import datetime
from modules.theme import render_section_header, render_disclaimer, render_html
from modules.ml_pipeline import run_single_patient_inference

def init_wizard_state(reset=False):
    """Initializes session state for the step-by-step screening wizard without pre-filling user answers."""
    if reset:
        st.session_state["wiz_step"] = 1
        st.session_state["wiz_patient_name"] = ""
        st.session_state["wiz_guardian_name"] = ""
        st.session_state["wiz_mrn"] = "MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01"
        st.session_state["wiz_age"] = 24
        st.session_state["wiz_sex"] = None
        st.session_state["wiz_ethnicity"] = None
        st.session_state["wiz_jaundice"] = None
        st.session_state["wiz_family_asd"] = None
        st.session_state["wiz_screener"] = None
        st.session_state["wiz_q"] = {f"Q{i}": None for i in range(1, 11)}
        st.session_state["wiz_results"] = None
        for i in range(1, 11):
            st.session_state.pop(f"radio_Q{i}", None)
        st.session_state.pop("radio_jaundice", None)
        st.session_state.pop("radio_family_asd", None)
        return

    if "wiz_step" not in st.session_state:
        st.session_state["wiz_step"] = 1
    if "wiz_patient_name" not in st.session_state:
        st.session_state["wiz_patient_name"] = ""
    if "wiz_guardian_name" not in st.session_state:
        st.session_state["wiz_guardian_name"] = ""
    if "wiz_mrn" not in st.session_state:
        st.session_state["wiz_mrn"] = "MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01"
    if "wiz_age" not in st.session_state:
        st.session_state["wiz_age"] = 24
    if "wiz_sex" not in st.session_state:
        st.session_state["wiz_sex"] = None
    if "wiz_ethnicity" not in st.session_state:
        st.session_state["wiz_ethnicity"] = None
    if "wiz_jaundice" not in st.session_state:
        st.session_state["wiz_jaundice"] = None
    if "wiz_family_asd" not in st.session_state:
        st.session_state["wiz_family_asd"] = None
    if "wiz_screener" not in st.session_state:
        st.session_state["wiz_screener"] = None
    if "wiz_q" not in st.session_state:
        st.session_state["wiz_q"] = {f"Q{i}": None for i in range(1, 11)}
    if "wiz_results" not in st.session_state:
        st.session_state["wiz_results"] = None

def render_stepper(current_step):
    """Renders visual multi-step progress indicator at the top."""
    steps = [
        (1, "1. Patient", "👤"),
        (2, "2. Age", "👶"),
        (3, "3. Gender", "🚻"),
        (4, "4. History", "📋"),
        (5, "5. Social", "🗣️"),
        (6, "6. Motor", "🔄"),
        (7, "7. Risk Analysis", "🩺"),
        (8, "8. Stage & Plan", "📊"),
        (9, "9. Precautions", "🛡️")
    ]
    
    html = '<div class="stepper-container">'
    for step_num, label, icon in steps:
        if step_num == current_step:
            cls = "step-node active"
        elif step_num < current_step:
            cls = "step-node completed"
        else:
            cls = "step-node"
        
        circle_content = "✓" if step_num < current_step else str(step_num)
        html += f"""<div class="{cls}">
<div class="step-circle">{circle_content}</div>
<span>{icon} {label}</span>
</div>"""
        if step_num < 9:
            html += '<span style="color: #CBD5E1; font-weight: bold; margin: 0 4px;">➔</span>'
    html += '</div>'
    render_html(html)

def calculate_asd_stage(tabnet_prob, mlp_prob, aq10_score, is_elevated):
    """Calculates clinically grounded ASD stage and affection metrics."""
    affection_pct = tabnet_prob * 100
    
    if not is_elevated:
        return {
            "status_label": "Typical Developmental Profile",
            "status_chip": "NON-ASD AFFECTED (TYPICAL)",
            "is_affected": False,
            "affection_pct": affection_pct,
            "stage_num": 0,
            "stage_name": "Normative Milestone Stage",
            "support_level": "Typical Development - Routine Pediatric Surveillance",
            "color": "#059669",
            "bg_color": "#F0FDF4",
            "border_color": "#10B981",
            "badge_class": "pill-green",
            "description": "Behavioral responses and social communication milestones fall within normative developmental expectations for this age group. Continue standard routine pediatric well-child visits.",
            "meter_pct": min(max(affection_pct, 5), 25)
        }
    
    # Composite severity score balancing behavioral questionnaire (50%) and deep learning attention probability (50%)
    severity_index = (aq10_score / 10.0) * 0.5 + (tabnet_prob) * 0.5
    
    if severity_index < 0.62:
        return {
            "status_label": "ASD Traits Indicated (Mild Presentation)",
            "status_chip": "ASD AFFECTED: STAGE 1 (MILD)",
            "is_affected": True,
            "affection_pct": affection_pct,
            "stage_num": 1,
            "stage_name": "Stage 1: Mild Presentation (Requiring Support)",
            "support_level": "DSM-5 Level 1 Support Required",
            "color": "#D97706",
            "bg_color": "#FEF3C7",
            "border_color": "#F59E0B",
            "badge_class": "pill-amber",
            "description": "Mild divergence observed in social communication initiation, subtle difficulties in peer joint attention, or specific sensory preferences. With early speech and play support, toddlers in Stage 1 adapt rapidly and achieve high communicative independence.",
            "meter_pct": max(35, min(severity_index * 100, 65))
        }
    elif severity_index < 0.82:
        return {
            "status_label": "ASD Traits Indicated (Moderate Presentation)",
            "status_chip": "ASD AFFECTED: STAGE 2 (MODERATE)",
            "is_affected": True,
            "affection_pct": affection_pct,
            "stage_num": 2,
            "stage_name": "Stage 2: Moderate Presentation (Requiring Substantial Support)",
            "support_level": "DSM-5 Level 2 Substantial Support Required",
            "color": "#EA580C",
            "bg_color": "#FFEDD5",
            "border_color": "#FB923C",
            "badge_class": "pill-amber",
            "description": "Notable challenges in reciprocal verbal/non-verbal communication, reduced eye gaze contact, distress during routine transitions, and observable repetitive motor mannerisms. Benefits significantly from multi-disciplinary early intervention (speech-language therapy, occupational therapy, and structured developmental play).",
            "meter_pct": max(68, min(severity_index * 100, 85))
        }
    else:
        return {
            "status_label": "ASD Traits Indicated (Substantial Presentation)",
            "status_chip": "ASD AFFECTED: STAGE 3 (SUBSTANTIAL)",
            "is_affected": True,
            "affection_pct": affection_pct,
            "stage_num": 3,
            "stage_name": "Stage 3: Substantial Presentation (Requiring Very Substantial Support)",
            "support_level": "DSM-5 Level 3 Very Substantial Support Required",
            "color": "#DC2626",
            "bg_color": "#FEE2E2",
            "border_color": "#EF4444",
            "badge_class": "pill-red",
            "description": "Marked divergence in verbal expressive speech, limited social smiling or response to name, intense focus on specific objects, and frequent repetitive motor traits (hand-flapping, spinning). Requires comprehensive, intensive early developmental support programs.",
            "meter_pct": max(86, min(severity_index * 100, 98))
        }

def render():
    render_section_header(
        "Step-by-Step Guided ASD Clinical Screener",
        "Interactive developmental assessment guiding you sequentially from patient information and demographics to behavioral evaluation, clinical action planning, and protective precautions.",
        badge="STEP-BY-STEP CLINICAL WIZARD"
    )

    if "models_result" not in st.session_state or "prepared_data" not in st.session_state:
        st.info("💡 The predictive AI models are initializing on the research benchmark dataset...")
        return

    init_wizard_state()
    step = st.session_state["wiz_step"]

    # Top Stepper Ribbon
    render_stepper(step)

    # -------------------------------------------------------------
    # STEP 1: PATIENT & CAREGIVER IDENTIFICATION
    # -------------------------------------------------------------
    if step == 1:
        render_html("""<div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
<div class="med-card-header">
<div class="med-card-icon">👤</div>
<span class="pill-badge pill-blue">Step 1 of 9 &bull; Identification</span>
</div>
<div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
Patient & Caregiver Identification
</div>
<div class="med-card-body" style="font-size: 1rem; color: #475569;">
Please enter the child's identity details and caregiver information. These will be linked to the clinical evaluation profile, risk stratification report, and printable medical dossier.
</div>
</div>""")

        st.markdown("""<style>
div[data-testid="stTextInput"],
div[data-testid="stTextInput"] div,
div[data-testid="stTextInput"] div *,
div[data-testid="stTextInput"] [data-baseweb="input"],
div[data-testid="stTextInput"] [data-baseweb="input"] *,
div[data-testid="stTextInput"] [data-baseweb="base-input"],
div[data-testid="stTextInput"] [data-baseweb="base-input"] *,
div[data-baseweb="input"],
div[data-baseweb="input"] *,
div[data-baseweb="base-input"],
div[data-baseweb="base-input"] *,
.main input,
.main textarea,
input[type="text"] {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #202B36 !important;
    -webkit-text-fill-color: #202B36 !important;
    caret-color: #202B36 !important;
}
div[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #202B36 !important;
    -webkit-text-fill-color: #202B36 !important;
    caret-color: #202B36 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
div[data-testid="stTextInput"] [data-baseweb="input"] {
    border: 1.5px solid #C5D0DA !important;
    border-radius: 8px !important;
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #8899A6 !important;
    -webkit-text-fill-color: #8899A6 !important;
    opacity: 1 !important;
}
</style>""", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            render_html("<p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Child's Full Name / Identifier (Optional):</p>")
            p_name = st.text_input(
                "Child's Full Name / Identifier:",
                value=st.session_state.get("wiz_patient_name", ""),
                placeholder="Enter child's full name (leave blank if preferred)...",
                label_visibility="collapsed"
            )
            st.session_state["wiz_patient_name"] = p_name.strip()

            render_html("<div style='margin-top: 14px;'></div><p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Medical Record Number (MRN) / Evaluation ID (Auto-Generated):</p>")
            mrn_val = st.text_input(
                "MRN / Evaluation ID:",
                value=st.session_state.get("wiz_mrn", "MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01"),
                label_visibility="collapsed"
            )
            st.session_state["wiz_mrn"] = mrn_val.strip() if mrn_val.strip() else ("MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01")

        with c2:
            render_html("<p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Parent / Guardian Name (Optional):</p>")
            g_name = st.text_input(
                "Parent / Guardian Name:",
                value=st.session_state.get("wiz_guardian_name", ""),
                placeholder="Enter parent or guardian name...",
                label_visibility="collapsed"
            )
            st.session_state["wiz_guardian_name"] = g_name.strip()

            render_html("""<div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 14px 18px; margin-top: 18px;">
<div style="font-size: 0.78rem; font-weight: 700; color: #1D4ED8; text-transform: uppercase;">Assessment Protocol</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #0A192F; margin: 4px 0;">Q-CHAT-10 Toddler Protocol</div>
<div style="font-size: 0.82rem; color: #475569;">Calibrated with TabNet Sparse Attention & Deep MLP Classifiers</div>
</div>""")

        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_spacer = st.columns([1.5, 1.8, 3.5])
        with nav_col1:
            if st.button("🏠 Return to Home", use_container_width=True):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col2:
            if st.button("Next: Child's Age ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 2
                st.rerun()

    # -------------------------------------------------------------
    # STEP 2: CHILD'S AGE
    # -------------------------------------------------------------
    elif step == 2:
        render_html("""<div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
<div class="med-card-header">
<div class="med-card-icon">👶</div>
<span class="pill-badge pill-blue">Step 2 of 9 &bull; Chronological Age</span>
</div>
<div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
What is the child's chronological age in months?
</div>
<div class="med-card-body" style="font-size: 1rem; color: #475569;">
Standardized pediatric screening via the Q-CHAT protocol is calibrated for toddlers between <strong>12 and 36 months</strong> of age. 
This period represents the golden developmental window of maximal neural plasticity.
</div>
</div>""")

        col_input, col_info = st.columns([2, 1.5])
        with col_input:
            render_html("<p style='font-size: 1.05rem; font-weight: 800; color: #0A192F !important; margin-bottom: 8px;'>Select Child's Age (in Months):</p>")
            age_val = st.slider(
                "Select Child's Age (in Months):",
                min_value=12,
                max_value=36,
                value=int(st.session_state.get("wiz_age", 24)),
                step=1,
                label_visibility="collapsed",
                help="Select the exact age in months of the child at the time of screening."
            )
            st.session_state["wiz_age"] = age_val

        with col_info:
            render_html(f"""<div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 18px; margin-top: 5px;">
<div style="font-size: 0.8rem; font-weight: 700; color: #1D4ED8; text-transform: uppercase;">Selected Milestone</div>
<div style="font-size: 2rem; font-weight: 800; color: #1D4ED8; margin: 4px 0;">{age_val} Months</div>
<div style="font-size: 0.85rem; color: #334155;">
Approx. <strong>{age_val // 12} year(s) and {age_val % 12} month(s)</strong> old.
</div>
</div>""")

        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1.5, 1.5, 1.8, 2.2])
        with nav_col1:
            if st.button("⬅️ Back: Patient Info", use_container_width=True):
                st.session_state["wiz_step"] = 1
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step2_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("Next: Biological Sex ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 3
                st.rerun()

    # -------------------------------------------------------------
    # STEP 3: BIOLOGICAL SEX
    # -------------------------------------------------------------
    elif step == 3:
        render_html("""<div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
<div class="med-card-header">
<div class="med-card-icon">🚻</div>
<span class="pill-badge pill-blue">Step 3 of 9 &bull; Biological Sex</span>
</div>
<div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
What is the child's biological sex?
</div>
<div class="med-card-body" style="font-size: 1rem; color: #475569;">
Biological sex is evaluated by the models to normalize normative developmental behavioral trajectories and account for known prevalence ratios.
</div>
</div>""")

        c_sex1, c_sex2 = st.columns(2)
        curr_sex = st.session_state.get("wiz_sex")
        with c_sex1:
            is_male = (curr_sex == "m")
            render_html(f"""<div style="border: 2px solid {'#1D4ED8' if is_male else '#CBD5E1'}; background: {'#EFF6FF' if is_male else '#FFFFFF'}; border-radius: 14px; padding: 22px; text-align: center; transition: all 0.2s ease;">
<div style="font-size: 2.5rem; margin-bottom: 6px;">👦</div>
<div style="font-size: 1.25rem; font-weight: 800; color: {'#1D4ED8' if is_male else '#0A192F'};">Male</div>
<div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">Biological Male</div>
</div>""")
            if st.button("Select Male", use_container_width=True, type="primary" if is_male else "secondary", key="btn_sex_male"):
                st.session_state["wiz_sex"] = "m"
                st.rerun()

        with c_sex2:
            is_female = (curr_sex == "f")
            render_html(f"""<div style="border: 2px solid {'#1D4ED8' if is_female else '#CBD5E1'}; background: {'#EFF6FF' if is_female else '#FFFFFF'}; border-radius: 14px; padding: 22px; text-align: center; transition: all 0.2s ease;">
<div style="font-size: 2.5rem; margin-bottom: 6px;">👧</div>
<div style="font-size: 1.25rem; font-weight: 800; color: {'#1D4ED8' if is_female else '#0A192F'};">Female</div>
<div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">Biological Female</div>
</div>""")
            if st.button("Select Female", use_container_width=True, type="primary" if is_female else "secondary", key="btn_sex_female"):
                st.session_state["wiz_sex"] = "f"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1.5, 1.5, 1.8, 2.2])
        with nav_col1:
            if st.button("⬅️ Back: Age", use_container_width=True):
                st.session_state["wiz_step"] = 2
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step3_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("Next: Clinical History ➔", type="primary", use_container_width=True):
                if st.session_state.get("wiz_sex") is None:
                    st.warning("⚠️ Please select the child's biological sex (Male or Female) before proceeding.")
                else:
                    st.session_state["wiz_step"] = 4
                    st.rerun()

    # -------------------------------------------------------------
    # STEP 4: CLINICAL & PERINATAL BACKGROUND
    # -------------------------------------------------------------
    elif step == 4:
        render_html("""<div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
<div class="med-card-header">
<div class="med-card-icon">📋</div>
<span class="pill-badge pill-blue">Step 4 of 9 &bull; Clinical Background</span>
</div>
<div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
Clinical, Perinatal & Family Background
</div>
<div class="med-card-body" style="font-size: 1rem; color: #475569;">
Please select demographic and clinical history details. These are encoded as non-linear priors by TabNet and MLP neural networks.
</div>
</div>""")

        st.markdown("""<style>
div[data-testid="stSelectbox"],
div[data-testid="stSelectbox"] div,
div[data-testid="stSelectbox"] div *,
div[data-testid="stSelectbox"] [data-baseweb="select"],
div[data-testid="stSelectbox"] [data-baseweb="select"] *,
div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
div[data-baseweb="select"],
div[data-baseweb="select"] * {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #202B36 !important;
    -webkit-text-fill-color: #202B36 !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    border: 1.5px solid #C5D0DA !important;
    border-radius: 8px !important;
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
}
div[data-testid="stSelectbox"] svg,
div[data-baseweb="select"] svg {
    fill: #202B36 !important;
    color: #202B36 !important;
}
div[data-baseweb="popover"],
div[data-baseweb="popover"] *,
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] ul li {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #202B36 !important;
    -webkit-text-fill-color: #202B36 !important;
}
div[data-baseweb="popover"] ul li:hover,
div[data-baseweb="popover"] ul li[aria-selected="true"] {
    background-color: #EDF4F4 !important;
    background: #EDF4F4 !important;
    color: #167C80 !important;
    -webkit-text-fill-color: #167C80 !important;
}
</style>""", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            render_html("<p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Ethnicity / Cultural Background:</p>")
            eth_options = [
                "-- Select Ethnicity --",
                "White-European", "Asian", "Middle Eastern", "black",
                "South Asian", "Hispanic", "Latino", "mixed", "others"
            ]
            current_eth = st.session_state.get("wiz_ethnicity")
            eth_idx = eth_options.index(current_eth) if current_eth in eth_options else 0
            selected_eth = st.selectbox(
                "Ethnicity:",
                options=eth_options,
                index=eth_idx,
                format_func=lambda x: x.title() if x != "-- Select Ethnicity --" else x,
                label_visibility="collapsed"
            )
            st.session_state["wiz_ethnicity"] = selected_eth if selected_eth != "-- Select Ethnicity --" else None

            render_html("<div style='margin-top: 14px;'></div><p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Who is completing this screening questionnaire?</p>")
            screener_options = ["-- Select Screener --", "family member", "Health Care Professional", "Others"]
            curr_scr = st.session_state.get("wiz_screener")
            scr_idx = screener_options.index(curr_scr) if curr_scr in screener_options else 0
            selected_scr = st.selectbox(
                "Who is completing this screening questionnaire?",
                options=screener_options,
                index=scr_idx,
                format_func=lambda x: x.title() if x != "-- Select Screener --" else x,
                label_visibility="collapsed"
            )
            st.session_state["wiz_screener"] = selected_scr if selected_scr != "-- Select Screener --" else None

        with col2:
            render_html("<p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Was the child born with neonatal jaundice?</p>")
            curr_j = st.session_state.get("wiz_jaundice")
            j_idx = ["no", "yes"].index(curr_j) if curr_j in ["no", "yes"] else None
            j_choice = st.radio(
                "Was the child born with neonatal jaundice?",
                options=["no", "yes"],
                index=j_idx,
                horizontal=True,
                format_func=lambda x: "Yes (Jaundice diagnosed)" if x == "yes" else "No (Typical birth)",
                key="radio_jaundice",
                label_visibility="collapsed"
            )
            st.session_state["wiz_jaundice"] = j_choice

            render_html("<div style='margin-top: 14px;'></div><p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Does any immediate family member have diagnosed ASD?</p>")
            curr_f = st.session_state.get("wiz_family_asd")
            f_idx = ["no", "yes"].index(curr_f) if curr_f in ["no", "yes"] else None
            f_choice = st.radio(
                "Does any immediate family member have diagnosed ASD?",
                options=["no", "yes"],
                index=f_idx,
                horizontal=True,
                format_func=lambda x: "Yes (Parent or sibling)" if x == "yes" else "No (No diagnosed family ASD)",
                key="radio_family_asd",
                label_visibility="collapsed"
            )
            st.session_state["wiz_family_asd"] = f_choice

        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1.5, 1.5, 2.2, 1.8])
        with nav_col1:
            if st.button("⬅️ Back: Gender", use_container_width=True):
                st.session_state["wiz_step"] = 3
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step4_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("Next: Social Questions (Q1-Q5) ➔", type="primary", use_container_width=True):
                missing = []
                if not st.session_state.get("wiz_ethnicity"):
                    missing.append("Ethnicity")
                if not st.session_state.get("wiz_screener"):
                    missing.append("Screener")
                if st.session_state.get("wiz_jaundice") is None:
                    missing.append("Neonatal Jaundice")
                if st.session_state.get("wiz_family_asd") is None:
                    missing.append("Family ASD History")
                
                if missing:
                    st.warning(f"⚠️ Please complete all required clinical history selections: {', '.join(missing)}.")
                else:
                    st.session_state["wiz_step"] = 5
                    st.rerun()

    # -------------------------------------------------------------
    # STEP 5: SOCIAL COMMUNICATION QUESTIONS (Q1 TO Q5)
    # -------------------------------------------------------------
    elif step == 5:
        render_html("""<div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
<div class="med-card-header">
<div class="med-card-icon">🗣️</div>
<span class="pill-badge pill-blue">Step 5 of 9 &bull; Domain A</span>
</div>
<div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
Social Communication & Interaction (Q1 to Q5)
</div>
<div class="med-card-body" style="font-size: 1rem; color: #475569;">
Evaluate the child's typical communicative behaviors. Please select your answer for each question below.
</div>
</div>""")

        q_list_1 = [
            ("Q1", "Does your child look at you when you call his/her name?", "Always / Usually (0)", "Rarely or Never (1)"),
            ("Q2", "How easy is it for you to establish mutual eye contact with your child?", "Very easy / Typical (0)", "Difficult / Rare (1)"),
            ("Q3", "Does your child point to indicate that s/he wants something (e.g. out of reach)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q4", "Does your child point to share interest with you (e.g. pointing at an airplane)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q5", "Does your child engage in pretend play (e.g. caring for a doll, talking on a toy phone)?", "Frequently / Often (0)", "Rarely or Never (1)")
        ]

        for qid, qtext, opt0, opt1 in q_list_1:
            curr_val = st.session_state["wiz_q"].get(qid)
            idx = curr_val if curr_val in [0, 1] else None
            render_html(f"""<div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 12px; padding: 14px 18px 12px 18px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
<div style="font-size: 1.05rem; font-weight: 800; color: #0A192F !important; line-height: 1.5;">
<span style="background: #1D4ED8; color: #FFFFFF !important; padding: 3px 10px; border-radius: 6px; font-weight: 800; font-size: 0.88rem; margin-right: 8px;">{qid}</span>
<span style="color: #0A192F !important;">{qtext}</span>
</div>
</div>""")
            choice = st.radio(
                f"Selection for {qid}",
                options=[0, 1],
                index=idx,
                format_func=lambda x, o0=opt0, o1=opt1: o0 if x == 0 else o1,
                horizontal=True,
                key=f"radio_{qid}",
                label_visibility="collapsed"
            )
            st.session_state["wiz_q"][qid] = choice
            st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

        nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1.5, 1.5, 2.2, 1.8])
        with nav_col1:
            if st.button("⬅️ Back: History", use_container_width=True):
                st.session_state["wiz_step"] = 4
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step5_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("Next: Motor Traits (Q6-Q10) ➔", type="primary", use_container_width=True):
                unanswered = [qid for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"] if st.session_state["wiz_q"].get(qid) is None]
                if unanswered:
                    st.warning(f"⚠️ Please answer all questions before proceeding. Unanswered: {', '.join(unanswered)}.")
                else:
                    st.session_state["wiz_step"] = 6
                    st.rerun()

    # -------------------------------------------------------------
    # STEP 6: MOTOR & BEHAVIORAL QUESTIONS (Q6 TO Q10)
    # -------------------------------------------------------------
    elif step == 6:
        render_html("""<div class="med-card" style="border-left: 5px solid #7C3AED; margin-bottom: 20px;">
<div class="med-card-header">
<div class="med-card-icon">🔄</div>
<span class="pill-badge pill-purple">Step 6 of 9 &bull; Domains A & B</span>
</div>
<div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
Affective, Motor & Communicative Traits (Q6 to Q10)
</div>
<div class="med-card-body" style="font-size: 1rem; color: #475569;">
Final screening indicators assessing gaze tracking, empathy, speech sounds, communicative gestures, and repetitive motor mannerisms. Please select your answer for each question below.
</div>
</div>""")

        q_list_2 = [
            ("Q6", "Does your child follow where you look (gaze tracking)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q7", "If someone in the family is upset, does the child show empathy or try to comfort them?", "Frequently (0)", "Rarely or Never (1)"),
            ("Q8", "Would you describe your child's first words or vocalizations as:", "Typical & communicative (0)", "Absent or atypical echoes (1)"),
            ("Q9", "Does your child use simple communicative gestures (e.g. waving bye-bye, shaking head)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q10", "Does your child stare at objects with no apparent purpose or show repetitive motor mannerisms?", "Never or Rarely (0)", "Frequently or Constantly (1)")
        ]

        for qid, qtext, opt0, opt1 in q_list_2:
            curr_val = st.session_state["wiz_q"].get(qid)
            idx = curr_val if curr_val in [0, 1] else None
            render_html(f"""<div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 12px; padding: 14px 18px 12px 18px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
<div style="font-size: 1.05rem; font-weight: 800; color: #0A192F !important; line-height: 1.5;">
<span style="background: #7C3AED; color: #FFFFFF !important; padding: 3px 10px; border-radius: 6px; font-weight: 800; font-size: 0.88rem; margin-right: 8px;">{qid}</span>
<span style="color: #0A192F !important;">{qtext}</span>
</div>
</div>""")
            choice = st.radio(
                f"Selection for {qid}",
                options=[0, 1],
                index=idx,
                format_func=lambda x, o0=opt0, o1=opt1: o0 if x == 0 else o1,
                horizontal=True,
                key=f"radio_{qid}",
                label_visibility="collapsed"
            )
            st.session_state["wiz_q"][qid] = choice
            st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

        nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1.5, 1.5, 2.5, 1.5])
        with nav_col1:
            if st.button("⬅️ Back: Q1–Q5", use_container_width=True):
                st.session_state["wiz_step"] = 5
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step6_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("🧠 Evaluate Developmental Risk with AI ➔", type="primary", use_container_width=True):
                unanswered = [qid for qid in ["Q6", "Q7", "Q8", "Q9", "Q10"] if st.session_state["wiz_q"].get(qid) is None]
                if unanswered:
                    st.warning(f"⚠️ Please answer all questions before evaluating. Unanswered: {', '.join(unanswered)}.")
                else:
                    # Execute inference
                    patient_dict = {
                        "Age": st.session_state["wiz_age"],
                        "Sex": st.session_state["wiz_sex"],
                        "Ethnicity": st.session_state["wiz_ethnicity"],
                        "Jaundice": st.session_state["wiz_jaundice"],
                        "Family_ASD": st.session_state["wiz_family_asd"],
                        "Screener": st.session_state["wiz_screener"],
                        **st.session_state["wiz_q"]
                    }
                    models_dict = st.session_state["models_result"]
                    prepared_data = st.session_state["prepared_data"]

                    with st.spinner("Executing dual-model inference across TabNet and MLP networks..."):
                        res = run_single_patient_inference(patient_dict, models_dict, prepared_data)

                    p_display_name = st.session_state.get("wiz_patient_name", "").strip() or "Patient (Unspecified)"
                    g_display_name = st.session_state.get("wiz_guardian_name", "").strip() or "Caregiver (Unspecified)"
                    mrn_display = st.session_state.get("wiz_mrn", "").strip() or ("MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01")

                    # Save results & patient report for the Clinical Test Report page
                    st.session_state["wiz_results"] = res
                    st.session_state["latest_patient_report"] = {
                        "patient_name": p_display_name,
                        "guardian_name": g_display_name,
                        "mrn": mrn_display,
                        "date": datetime.date.today().strftime("%B %d, %Y"),
                        "examiner": "Pediatric Screening Specialist",
                        "institution": "Pediatric Neurodevelopmental Clinical Center",
                        **patient_dict,
                        **res
                    }
                    st.session_state["wiz_step"] = 7
                    st.rerun()

    # -------------------------------------------------------------
    # STEP 7: DEDICATED CLINICAL RISK EVALUATION & PATIENT DOSSIER
    # -------------------------------------------------------------
    elif step == 7:
        res = st.session_state.get("wiz_results")
        if res is None:
            st.warning("No evaluation results found. Please start from Step 1.")
            if st.button("Start Screening"):
                st.session_state["wiz_step"] = 1
                st.rerun()
            return

        p_name = st.session_state.get("wiz_patient_name", "").strip() or "Patient (Unspecified)"
        g_name = st.session_state.get("wiz_guardian_name", "").strip() or "Caregiver (Unspecified)"
        mrn = st.session_state.get("wiz_mrn", "").strip() or ("MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01")
        age = st.session_state.get("wiz_age", 24)
        sex = st.session_state.get("wiz_sex", "m")
        ethnicity = st.session_state.get("wiz_ethnicity") or "Unspecified"
        jaundice = st.session_state.get("wiz_jaundice") or "no"
        family_asd = st.session_state.get("wiz_family_asd") or "no"
        screener = st.session_state.get("wiz_screener") or "family member"
        eval_date = datetime.date.today().strftime("%B %d, %Y")

        is_elevated = (res["tabnet_pred"] == 1) or (res["mlp_pred"] == 1) or (res["aq10_score"] >= 3)
        stage_info = calculate_asd_stage(res["tabnet_prob"], res["mlp_prob"], res["aq10_score"], is_elevated)

        # 1. Prominent Patient Information Card
        render_html(f"""<div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 16px; padding: 22px 26px; margin-bottom: 24px; box-shadow: 0 4px 16px rgba(15,23,42,0.04);">
<div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1.5px solid #F1F5F9; padding-bottom: 14px; margin-bottom: 16px;">
<div>
<span class="clinical-brand-badge" style="margin-bottom: 4px;">OFFICIAL PEDIATRIC SCREENING DOSSIER</span>
<h3 style="font-size: 1.6rem; font-weight: 800; color: #0A192F; margin: 4px 0 2px 0;">{p_name}</h3>
<div style="font-size: 0.9rem; color: #64748B;">Caregiver: <strong style="color: #0F172A;">{g_name}</strong> &bull; Screener: <strong style="color: #0F172A;">{screener.title()}</strong></div>
</div>
<div style="text-align: right;">
<div style="font-size: 0.88rem; color: #0F172A;"><strong>MRN:</strong> {mrn}</div>
<div style="font-size: 0.82rem; color: #64748B;"><strong>Date:</strong> {eval_date}</div>
<div style="font-size: 0.78rem; color: #1D4ED8; font-weight: 700; margin-top: 4px;">Validated Q-CHAT-10 Protocol</div>
</div>
</div>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; font-size: 0.9rem;">
<div style="background: #F8FAFC; border-radius: 10px; padding: 12px 14px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Chronological Age</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0A192F;">{age} Months</div>
<div style="font-size: 0.76rem; color: #475569;">({age // 12}y {age % 12}m old)</div>
</div>
<div style="background: #F8FAFC; border-radius: 10px; padding: 12px 14px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Biological Sex</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0A192F;">{'Male (Boy)' if sex=='m' else 'Female (Girl)'}</div>
<div style="font-size: 0.76rem; color: #475569;">Normative profile</div>
</div>
<div style="background: #F8FAFC; border-radius: 10px; padding: 12px 14px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Ethnicity Background</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0A192F;">{ethnicity.title()}</div>
<div style="font-size: 0.76rem; color: #475569;">Demographic baseline</div>
</div>
<div style="background: #F8FAFC; border-radius: 10px; padding: 12px 14px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Perinatal & History</div>
<div style="font-size: 0.95rem; font-weight: 800; color: #0A192F;">Jaundice: {jaundice.title()}</div>
<div style="font-size: 0.8rem; color: #475569;">Family ASD: {family_asd.title()}</div>
</div>
</div>
</div>""")

        # 2. Prominent Full-Width Clinical Risk Stratification Banner
        if is_elevated:
            render_html("""<div style="background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 50%, #FEE2E2 100%); border: 2.5px solid #EF4444; border-radius: 18px; padding: 28px 32px; margin-bottom: 26px; box-shadow: 0 8px 24px rgba(239,68,68,0.12);">
<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 20px;">
<div>
<span style="background: #DC2626; color: #FFFFFF; font-weight: 800; font-size: 0.88rem; padding: 6px 14px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em; display: inline-block;">
⚠️ ELEVATED DEVELOPMENTAL RISK DETECTED
</span>
<h2 style="color: #991B1B; font-size: 1.85rem; font-weight: 800; margin: 12px 0 8px 0; letter-spacing: -0.01em;">
Developmental Autism Spectrum Traits Indicated
</h2>
<p style="color: #7F1D1D; font-size: 1.05rem; line-height: 1.6; margin: 0; max-width: 860px;">
Multimodal inference across <strong>TabNet Sparse Attentive Learning</strong> and <strong>Multi-Layer Perceptrons</strong> indicates significant behavioral divergence consistent with elevated Autism Spectrum traits. Responses across early joint attention, eye gaze contact, and communicative gestures suggest that this toddler will benefit from comprehensive developmental pediatric evaluation.
</p>
</div>
<div style="background: #FFFFFF; border: 2px solid #FCA5A5; border-radius: 16px; padding: 18px 24px; text-align: center; min-width: 170px; box-shadow: 0 4px 12px rgba(239,68,68,0.1);">
<div style="font-size: 0.78rem; font-weight: 800; color: #DC2626; text-transform: uppercase;">Clinical Stratum</div>
<div style="font-size: 2.2rem; font-weight: 900; color: #991B1B; margin: 4px 0;">Tier 3</div>
<div style="font-size: 0.78rem; color: #7F1D1D; font-weight: 600;">Elevated Clinical Priority</div>
</div>
</div>
</div>""")
        else:
            render_html("""<div style="background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 50%, #BBF7D0 100%); border: 2.5px solid #10B981; border-radius: 18px; padding: 28px 32px; margin-bottom: 26px; box-shadow: 0 8px 24px rgba(16,185,129,0.12);">
<div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 20px;">
<div>
<span style="background: #059669; color: #FFFFFF; font-weight: 800; font-size: 0.88rem; padding: 6px 14px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em; display: inline-block;">
✅ TYPICAL DEVELOPMENTAL TRAJECTORY
</span>
<h2 style="color: #065F46; font-size: 1.85rem; font-weight: 800; margin: 12px 0 8px 0; letter-spacing: -0.01em;">
Normative Toddler Behavioral Milestones Observed
</h2>
<p style="color: #064E3B; font-size: 1.05rem; line-height: 1.6; margin: 0; max-width: 860px;">
The deep learning models identified behavioral and communicative response patterns consistent with typical early childhood development. Social communication, mutual gaze, and play markers fall within expected normative distributions. Continue standard routine pediatric surveillance.
</p>
</div>
<div style="background: #FFFFFF; border: 2px solid #86EFAC; border-radius: 16px; padding: 18px 24px; text-align: center; min-width: 170px; box-shadow: 0 4px 12px rgba(16,185,129,0.1);">
<div style="font-size: 0.78rem; font-weight: 800; color: #059669; text-transform: uppercase;">Clinical Stratum</div>
<div style="font-size: 2.2rem; font-weight: 900; color: #065F46; margin: 4px 0;">Tier 1</div>
<div style="font-size: 0.78rem; color: #064E3B; font-weight: 600;">Normative Surveillance</div>
</div>
</div>
</div>""")

        # 3. Model Metric Breakdown Cards
        c1, c2, c3 = st.columns(3)
        with c1:
            render_html(f"""<div class="med-card">
<div class="med-card-header">
<div class="med-card-icon">🧠</div>
<span class="pill-badge {'pill-amber' if res['tabnet_pred'] == 1 else 'pill-green'}">
{'ASD Positive' if res['tabnet_pred'] == 1 else 'ASD Negative'}
</span>
</div>
<div class="med-card-title">TabNet Attentive Model</div>
<div style="font-size: 1.85rem; font-weight: 800; color: #1D4ED8; margin-bottom: 6px;">
{res['tabnet_prob'] * 100:.1f}%
</div>
<div class="med-card-body">
Sequential sparse attention model confidence for ASD behavioral traits.
</div>
</div>""")

        with c2:
            render_html(f"""<div class="med-card">
<div class="med-card-header">
<div class="med-card-icon">⚡</div>
<span class="pill-badge {'pill-amber' if res['mlp_pred'] == 1 else 'pill-green'}">
{'ASD Positive' if res['mlp_pred'] == 1 else 'ASD Negative'}
</span>
</div>
<div class="med-card-title">MLP Neural Network</div>
<div style="font-size: 1.85rem; font-weight: 800; color: #7C3AED; margin-bottom: 6px;">
{res['mlp_prob'] * 100:.1f}%
</div>
<div class="med-card-body">
Dense non-linear classifier probability with decision threshold calibrated at 0.60.
</div>
</div>""")

        with c3:
            render_html(f"""<div class="med-card">
<div class="med-card-header">
<div class="med-card-icon">📋</div>
<span class="pill-badge pill-blue">Q-CHAT Total</span>
</div>
<div class="med-card-title">Behavioral Domain Scores</div>
<div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin-bottom: 6px;">
{res['aq10_score']} / 10
</div>
<div class="med-card-body">
<strong>Domain A (Social Communication):</strong> {res['a_domain']} / 9<br>
<strong>Domain B (Repetitive Behaviors):</strong> {res['b_domain']} / 1
</div>
</div>""")

        # 4. Behavioral Response Summary Audit Table
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Behavioral Questionnaire Response Audit")
        
        q_meta = [
            ("Q1", "Name Orientation", "Does child look when name is called?", "Domain A"),
            ("Q2", "Eye Contact", "Ease of establishing mutual eye contact?", "Domain A"),
            ("Q3", "Pointing for Wants", "Points to indicate desired objects?", "Domain A"),
            ("Q4", "Shared Interest", "Points to share interest (e.g. airplane)?", "Domain A"),
            ("Q5", "Pretend Play", "Engages in pretend play (doll, toy phone)?", "Domain A"),
            ("Q6", "Gaze Following", "Follows where adult looks (gaze tracking)?", "Domain A"),
            ("Q7", "Empathy & Comfort", "Shows empathy or comforts upset family member?", "Domain A"),
            ("Q8", "Speech & Vocalization", "Are first words communicative or atypical echoes?", "Domain A"),
            ("Q9", "Communicative Gestures", "Uses simple communicative gestures (waving)?", "Domain A"),
            ("Q10", "Repetitive Mannerisms", "Stares blankly or shows repetitive motor mannerisms?", "Domain B"),
        ]

        table_rows = ""
        for qid, short_label, inquiry, domain in q_meta:
            score = st.session_state["wiz_q"].get(qid, 0)
            status_badge = '<span style="background: #FEE2E2; color: #DC2626; font-weight: 800; padding: 4px 10px; border-radius: 9999px; font-size: 0.8rem;">Atypical Trait (1)</span>' if score == 1 else '<span style="background: #DCFCE7; color: #059669; font-weight: 800; padding: 4px 10px; border-radius: 9999px; font-size: 0.8rem;">Typical Response (0)</span>'
            table_rows += f"""<tr>
<td style="font-weight: 800; color: #0A192F;">{qid}</td>
<td><strong>{short_label}</strong><br><span style="font-size: 0.82rem; color: #64748B;">{inquiry}</span></td>
<td><span style="background: #EFF6FF; color: #1D4ED8; font-weight: 700; padding: 3px 8px; border-radius: 6px; font-size: 0.78rem;">{domain}</span></td>
<td>{status_badge}</td>
</tr>"""

        render_html(f"""<table class="report-table" style="margin-top: 10px;">
<thead>
<tr>
<th style="width: 8%;">Item</th>
<th style="width: 52%;">Clinical Trait & Questionnaire Inquiry</th>
<th style="width: 18%;">Domain</th>
<th style="width: 22%;">Recorded Attribution</th>
</tr>
</thead>
<tbody>
{table_rows}
</tbody>
</table>""")

        # Navigation Controls
        st.markdown("<br>", unsafe_allow_html=True)
        r_col1, r_col2, r_col3, r_spacer = st.columns([1.6, 1.6, 2.8, 1.5])
        with r_col1:
            if st.button("⬅️ Back: Questions (Q6-Q10)", use_container_width=True):
                st.session_state["wiz_step"] = 6
                st.rerun()
        with r_col2:
            if st.button("🏠 Home", use_container_width=True, key="step7_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with r_col3:
            if st.button("🌟 Proceed to ASD Staging & Action Plan ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 8
                st.rerun()

    # -------------------------------------------------------------
    # STEP 8: CLINICAL ASD STAGING & ACTION PLAN
    # -------------------------------------------------------------
    elif step == 8:
        res = st.session_state.get("wiz_results")
        if res is None:
            st.warning("No evaluation results found. Please start from Step 1.")
            if st.button("Start Screening"):
                st.session_state["wiz_step"] = 1
                st.rerun()
            return

        p_name = st.session_state.get("wiz_patient_name", "").strip() or "Patient (Unspecified)"
        g_name = st.session_state.get("wiz_guardian_name", "").strip() or "Caregiver (Unspecified)"
        mrn = st.session_state.get("wiz_mrn", "").strip() or ("MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01")
        age = st.session_state.get("wiz_age", 24)
        sex = st.session_state.get("wiz_sex", "m")
        is_elevated = (res["tabnet_pred"] == 1) or (res["mlp_pred"] == 1) or (res["aq10_score"] >= 3)
        stage_info = calculate_asd_stage(res["tabnet_prob"], res["mlp_prob"], res["aq10_score"], is_elevated)
        eval_date = datetime.date.today().strftime("%B %d, %Y")

        # 1. Clinical ASD Stage, Affection Percentage & Severity Meter
        render_html(f"""<div style="background: #FFFFFF; border: 2px solid #CBD5E1; border-radius: 18px; padding: 26px 30px; margin-bottom: 28px; box-shadow: 0 6px 22px rgba(15,23,42,0.06);">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #F1F5F9; padding-bottom: 14px; margin-bottom: 18px;">
<div>
<div style="font-size: 0.8rem; font-weight: 800; color: #1D4ED8; text-transform: uppercase; letter-spacing: 0.08em;">PEDIATRIC CLINICAL STAGING & AFFECTION ANALYSIS</div>
<h2 style="font-size: 1.7rem; font-weight: 800; color: #0A192F; margin: 4px 0 2px 0;">{stage_info['stage_name']}</h2>
<div style="font-size: 0.9rem; color: #64748B;">Patient: <strong style="color: #0F172A;">{p_name}</strong> &bull; Caregiver: <strong style="color: #0F172A;">{g_name}</strong></div>
</div>
<div>
<span style="background: {stage_info['bg_color']}; color: {stage_info['color']}; border: 1.5px solid {stage_info['border_color']}; font-weight: 800; font-size: 0.88rem; padding: 7px 16px; border-radius: 9999px; text-transform: uppercase; display: inline-block;">
{stage_info['status_chip']}
</span>
</div>
</div>

<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px;">
<div style="background: #F8FAFC; border-radius: 12px; padding: 14px 16px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.74rem; color: #64748B; font-weight: 700; text-transform: uppercase;">ASD Affection Rate</div>
<div style="font-size: 1.75rem; font-weight: 900; color: {stage_info['color']}; margin: 2px 0;">{stage_info['affection_pct']:.1f}%</div>
<div style="font-size: 0.76rem; color: #64748B;">Model risk probability</div>
</div>
<div style="background: #F8FAFC; border-radius: 12px; padding: 14px 16px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.74rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Identified ASD Stage</div>
<div style="font-size: 1.25rem; font-weight: 800; color: #0A192F; margin: 4px 0;">{'Stage ' + str(stage_info['stage_num']) if stage_info['stage_num'] > 0 else 'Normative'}</div>
<div style="font-size: 0.76rem; color: #64748B;">Pediatric Severity Tier</div>
</div>
<div style="background: #F8FAFC; border-radius: 12px; padding: 14px 16px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.74rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Support Recommendation</div>
<div style="font-size: 0.95rem; font-weight: 800; color: #334155; margin: 4px 0;">{stage_info['support_level']}</div>
<div style="font-size: 0.76rem; color: #64748B;">Clinical action criteria</div>
</div>
<div style="background: #F8FAFC; border-radius: 12px; padding: 14px 16px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.74rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Domain Distribution</div>
<div style="font-size: 1.15rem; font-weight: 800; color: #0A192F; margin: 4px 0;">A: {res['a_domain']}/9 &bull; B: {res['b_domain']}/1</div>
<div style="font-size: 0.76rem; color: #64748B;">Social vs Repetitive markers</div>
</div>
</div>

<div style="margin-top: 14px; margin-bottom: 8px;">
<div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-weight: 700; color: #64748B; margin-bottom: 6px;">
<span>🟢 Baseline (0–25%)</span>
<span>🟡 Stage 1: Mild (26–65%)</span>
<span>🟠 Stage 2: Moderate (66–85%)</span>
<span>🔴 Stage 3: Substantial (86–100%)</span>
</div>
<div style="background: #E2E8F0; border-radius: 9999px; height: 16px; width: 100%; overflow: hidden; position: relative;">
<div style="background: linear-gradient(90deg, #10B981 0%, #F59E0B 50%, #EA580C 75%, #DC2626 100%); height: 100%; width: {stage_info['meter_pct']}%; border-radius: 9999px; transition: width 0.8s ease;"></div>
</div>
<div style="font-size: 0.82rem; color: #64748B; margin-top: 6px; text-align: right;">
Calibrated Patient Affection Marker: <strong>{stage_info['affection_pct']:.1f}%</strong> ({'Elevated Risk' if is_elevated else 'Normative Expectation'})
</div>
</div>

<div style="background: #F8FAFC; border-radius: 12px; padding: 14px 18px; border-left: 4px solid {stage_info['color']}; margin-top: 14px;">
<div style="font-size: 0.92rem; color: #334155; line-height: 1.6;">
{stage_info['description']}
</div>
</div>
</div>""")

        # 2. 4-Pillar Clinical Action Plan
        st.subheader("Clinical Action Plan & Support Pathway")
        p1, p2 = st.columns(2)
        with p1:
            render_html("""<div class="med-card" style="border-left: 5px solid #1D4ED8;">
<div class="med-card-header">
<div class="med-card-icon">🩺</div>
<span class="pill-badge pill-blue">Pillar 1 &bull; Clinical Medical Care</span>
</div>
<div class="med-card-title">1. Pediatric Consultation & Diagnostic Referral</div>
<div class="med-card-body">
<ul>
<li><strong>Schedule Pediatric Follow-up:</strong> Bring a copy of this staging dossier to your child's pediatrician or developmental doctor.</li>
<li><strong>Request Formal Diagnostic Evaluation:</strong> Ask for multidisciplinary evaluation using gold-standard diagnostic instruments (ADOS-2, Bayley-4, ADI-R).</li>
<li><strong>Audiology / Hearing Screen:</strong> Rule out hearing fluid variations that frequently mimic reduced social name orientation.</li>
</ul>
</div>
</div>""")

            render_html("""<div class="med-card" style="border-left: 5px solid #059669;">
<div class="med-card-header">
<div class="med-card-icon">💡</div>
<span class="pill-badge pill-green">Pillar 3 &bull; Home Play Strategies</span>
</div>
<div class="med-card-title">3. Interactive Floor-Time & Joint Attention Games</div>
<div class="med-card-body">
<ul>
<li><strong>Eye-Level Play:</strong> Sit face-to-face during play to naturally foster reciprocal eye gaze.</li>
<li><strong>Turn-Taking Games:</strong> Play rolling balls, popping soap bubbles, and passing colorful toys.</li>
<li><strong>Language Expansion:</strong> Model 2-3 word descriptive phrases that narrate what the child is actively watching.</li>
<li><strong>Positive Reinforcement:</strong> Enthusiastically praise every smile, gesture, and pointing attempt.</li>
</ul>
</div>
</div>""")

        with p2:
            render_html("""<div class="med-card" style="border-left: 5px solid #7C3AED;">
<div class="med-card-header">
<div class="med-card-icon">🧸</div>
<span class="pill-badge pill-purple">Pillar 2 &bull; Early Support Services</span>
</div>
<div class="med-card-title">2. Early Intervention (No Diagnosis Required!)</div>
<div class="med-card-body">
<ul>
<li><strong>Start Services Immediately:</strong> State and county Early Intervention (EI) services do not require a medical hospital diagnosis to begin.</li>
<li><strong>Speech-Language Pathology:</strong> Builds intentional communication, gesture imitation, and social sound play.</li>
<li><strong>Occupational Therapy:</strong> Enhances sensory regulation, fine motor grasp, and transitions between activities.</li>
<li><strong>Developmental Play Therapy:</strong> Supports peer engagement and shared social play.</li>
</ul>
</div>
</div>""")

            render_html("""<div class="med-card" style="border-left: 5px solid #D97706;">
<div class="med-card-header">
<div class="med-card-icon">🤝</div>
<span class="pill-badge pill-amber">Pillar 4 &bull; Community & Guidance</span>
</div>
<div class="med-card-title">4. Family Guidance & Trusted Resources</div>
<div class="med-card-body">
<ul>
<li><strong>CDC Learn the Signs. Act Early:</strong> Free milestone tracker app with research-backed developmental guides.</li>
<li><strong>Autism Navigator Video Glossary:</strong> Side-by-side video clips showing typical vs atypical toddler communication.</li>
<li><strong>Caregiver Empowerment:</strong> Connect with local pediatric parent support groups and early childhood playgroups.</li>
<li><strong>Parent Well-Being:</strong> Remember that self-care and caregiver emotional balance provide the stable foundation for your child.</li>
</ul>
</div>
</div>""")

        # Navigation Controls to Step 9
        st.markdown("<br>", unsafe_allow_html=True)
        r_col1, r_col2, r_col3, r_spacer = st.columns([1.6, 1.6, 2.8, 1.5])
        with r_col1:
            if st.button("⬅️ Back: Risk Analysis", use_container_width=True):
                st.session_state["wiz_step"] = 7
                st.rerun()
        with r_col2:
            if st.button("🏠 Home", use_container_width=True, key="step8_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with r_col3:
            if st.button("🌟 Proceed to Precautions & Protective Care Guide (\"Beautiful Ending\") ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 9
                st.rerun()

    # -------------------------------------------------------------
    # STEP 9: CLINICAL PRECAUTIONS & CAREGIVER PROTECTIVE GUIDANCE
    # ("THE BEAUTIFUL ENDING")
    # -------------------------------------------------------------
    elif step == 9:
        res = st.session_state.get("wiz_results")
        if res is None:
            st.warning("No evaluation results found. Please start from Step 1.")
            if st.button("Start Screening"):
                st.session_state["wiz_step"] = 1
                st.rerun()
            return

        p_name = st.session_state.get("wiz_patient_name", "").strip() or "Patient (Unspecified)"
        g_name = st.session_state.get("wiz_guardian_name", "").strip() or "Caregiver (Unspecified)"
        mrn = st.session_state.get("wiz_mrn", "").strip() or ("MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01")
        age = st.session_state.get("wiz_age", 24)
        sex = st.session_state.get("wiz_sex", "m")
        is_elevated = (res["tabnet_pred"] == 1) or (res["mlp_pred"] == 1) or (res["aq10_score"] >= 3)
        stage_info = calculate_asd_stage(res["tabnet_prob"], res["mlp_prob"], res["aq10_score"], is_elevated)
        eval_date = datetime.date.today().strftime("%B %d, %Y")

        # 1. Breathtaking Royal Hero Banner
        st.markdown(f"""<style>
.precautions-hero-banner,
.precautions-hero-banner *,
.precautions-hero-banner div,
.precautions-hero-banner span,
.precautions-hero-banner h1,
.precautions-hero-banner p,
.precautions-hero-banner strong,
.precautions-hero-title,
.precautions-hero-desc,
.main .precautions-hero-banner,
.main .precautions-hero-banner *,
.main .precautions-hero-banner div,
.main .precautions-hero-banner span,
.main .precautions-hero-banner p,
.main .precautions-hero-banner strong,
[data-testid="stMain"] .precautions-hero-banner,
[data-testid="stMain"] .precautions-hero-banner *,
[data-testid="stMarkdownContainer"] .precautions-hero-banner,
[data-testid="stMarkdownContainer"] .precautions-hero-banner * {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}}
.precautions-hero-desc,
.precautions-hero-banner .precautions-hero-desc,
.precautions-hero-banner p,
.main .precautions-hero-banner p {{
    color: #E2E8F0 !important;
    -webkit-text-fill-color: #E2E8F0 !important;
}}
.precautions-hero-banner .hero-pill-badge,
.main .precautions-hero-banner .hero-pill-badge {{
    color: #93C5FD !important;
    -webkit-text-fill-color: #93C5FD !important;
}}
</style>
<div class="precautions-hero-banner" style="background: linear-gradient(135deg, #071326 0%, #0F284E 45%, #1E3A8A 100%); border-radius: 22px; padding: 40px 42px; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; margin-bottom: 30px; box-shadow: 0 20px 40px rgba(7,19,38,0.3); border: 1.5px solid rgba(255,255,255,0.12); position: relative; overflow: hidden;">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
<span class="hero-pill-badge" style="background: rgba(255,255,255,0.16); color: #93C5FD !important; -webkit-text-fill-color: #93C5FD !important; font-size: 0.84rem; font-weight: 800; padding: 6px 16px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.08em; border: 1px solid rgba(255,255,255,0.2); display: inline-block;">
CLINICAL PRECAUTIONS &amp; PROTECTIVE PARENTING GUIDE
</span>
</div>
<div class="precautions-hero-title" style="font-size: 28px; font-weight: 800; color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; margin: 8px 0 14px 0; letter-spacing: -0.02em; line-height: 1.25;">
Essential Protective Precautions &amp; Everyday Guidance for {p_name}
</div>
<div class="precautions-hero-desc" style="font-size: 15px; line-height: 1.7; color: #E2E8F0 !important; -webkit-text-fill-color: #E2E8F0 !important; max-width: 900px; margin: 0;">
Parenting a young toddler with developmental differences is an act of deep attentiveness. Below are evidence-based medical, environmental, and behavioral precautions formulated by pediatric developmental specialists to protect <strong style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; font-weight: 700;">{p_name}</strong>'s sensory balance, physical safety, emotional security, and overall developmental flourishing.
</div>
</div>""", unsafe_allow_html=True)

        # 2. 6 Comprehensive Precaution Cards
        st.subheader("Crucial Precautions & Caregiver Protective Practices")
        pr1, pr2 = st.columns(2)
        with pr1:
            render_html("""<div class="med-card" style="border-left: 5px solid #1D4ED8;">
<div class="med-card-header">
<div class="med-card-icon">🌿</div>
<span class="pill-badge pill-blue">Precaution 1 &bull; Sensory Environment</span>
</div>
<div class="med-card-title">1. Sensory Overload & Meltdown Prevention</div>
<div class="med-card-body">
<ul>
<li><strong>Recognize Early Distress Cues:</strong> Watch for subtle pre-meltdown signs: covering ears, rapid blinking, gaze aversion, or sudden vocal agitation. Intervene before overload occurs.</li>
<li><strong>Design a Quiet Sensory Corner:</strong> Set up a low-stimulation calming zone at home with soft lighting, weighted pillows or blankets, and noise-dampening earmuffs.</li>
<li><strong>Prepare for Noisy Environments:</strong> When attending grocery stores, airports, or clinics, equip the child with sunglasses, familiar fidget toys, and noise-canceling headphones.</li>
</ul>
</div>
</div>""")

            render_html("""<div class="med-card" style="border-left: 5px solid #EF4444;">
<div class="med-card-header">
<div class="med-card-icon">🚪</div>
<span class="pill-badge pill-amber" style="background: #FEE2E2; color: #DC2626;">Precaution 3 &bull; Physical Safety</span>
</div>
<div class="med-card-title">3. Safety, Wandering (Elopement) & Water Precautions</div>
<div class="med-card-body">
<ul>
<li><strong>Enhanced Home Security:</strong> Toddlers with ASD traits frequently lack intuitive danger awareness and may bolt unexpectedly. Install high secondary deadbolts and audible door-chime alarms.</li>
<li><strong>Strict Water Supervision:</strong> Statistics show toddlers with developmental traits are disproportionately drawn to water. Maintain direct "touch supervision" around bathtubs, ponds, and pools.</li>
<li><strong>Wearable Identification:</strong> In public parks or busy transport hubs, use an ID wristband or embroidered tag with parent phone contact information.</li>
</ul>
</div>
</div>""")

            render_html("""<div class="med-card" style="border-left: 5px solid #059669;">
<div class="med-card-header">
<div class="med-card-icon">🥗</div>
<span class="pill-badge pill-green">Precaution 5 &bull; Nutrition & Sleep</span>
</div>
<div class="med-card-title">5. Nutritional Sensitivity & Sleep Rhythm Precautions</div>
<div class="med-card-body">
<ul>
<li><strong>Gentle Mealtime Strategies:</strong> Sensory oral aversions (refusing crunchy, slimy, or mixed textures) are common. Never turn meals into power struggles; introduce tiny sample bites next to safe preferred foods.</li>
<li><strong>Consistent Circadian Routine:</strong> Melatonin production is often delayed in neurodivergent toddlers. Implement a predictable 4-step bedtime routine: warm bath &bull; dim room &bull; soft massage &bull; white noise machine.</li>
<li><strong>Monitor Gastrointestinal Comfort:</strong> Toddlers with ASD traits have higher rates of constipation or food intolerances. Consult your pediatrician if chronic bowel distress is observed.</li>
</ul>
</div>
</div>""")

        with pr2:
            render_html("""<div class="med-card" style="border-left: 5px solid #7C3AED;">
<div class="med-card-header">
<div class="med-card-icon">📱</div>
<span class="pill-badge pill-purple">Precaution 2 &bull; Media & Devices</span>
</div>
<div class="med-card-title">2. Screen Time & Digital Device Precautions</div>
<div class="med-card-body">
<ul>
<li><strong>Zero Passive Screens for Toddlers:</strong> The American Academy of Pediatrics (AAP) recommends eliminating passive smartphone, tablet, and TV viewing for children under 24 months.</li>
<li><strong>Prevent Synaptic Displacement:</strong> Fast-paced digital animations overstimulate immature neural pathways and displace critical real-world 3D joint attention and human eye gaze.</li>
<li><strong>Replace with Tactile Interaction:</strong> Swap touchscreen time for interactive floor games, playdough sculpting, bubble popping, and face-to-face vocal imitation.</li>
</ul>
</div>
</div>""")

            render_html("""<div class="med-card" style="border-left: 5px solid #D97706;">
<div class="med-card-header">
<div class="med-card-icon">⏰</div>
<span class="pill-badge pill-amber">Precaution 4 &bull; Daily Transitions</span>
</div>
<div class="med-card-title">4. Routine Consistency & Transition Precautions</div>
<div class="med-card-body">
<ul>
<li><strong>Consistent Daily Predictability:</strong> Neurodivergent brains consume high cognitive energy processing change. Keeping waking, feeding, and playing routines predictable reduces anxiety.</li>
<li><strong>Visual Schedule Cards:</strong> Use visual picture sequences (e.g. Card 1: Shoes &bull; Card 2: Park &bull; Card 3: Home) so the child anticipates what is happening next.</li>
<li><strong>Transitional Verbal Warnings:</strong> Provide gentle countdown warnings: "In 2 minutes, we say bye-bye to bubbles and wash hands for snack."</li>
</ul>
</div>
</div>""")

            render_html("""<div class="med-card" style="border-left: 5px solid #BE185D;">
<div class="med-card-header">
<div class="med-card-icon">💖</div>
<span class="pill-badge pill-purple" style="background: #FCE7F3; color: #9D174D;">Precaution 6 &bull; Emotional Mindset</span>
</div>
<div class="med-card-title">6. Caregiver Mental Well-Being & Protective Mindset</div>
<div class="med-card-body">
<ul>
<li><strong>Avoid Milestone Comparisons:</strong> Never compare your toddler's developmental timeline with siblings or peers. Every child develops according to their own biological blueprint.</li>
<li><strong>Do Not Force Prolonged Eye Contact:</strong> Forcing eye contact can trigger fight-or-flight anxiety. Many children listen and learn best while looking slightly to the side or holding a sensory toy.</li>
<li><strong>Protect Your Emotional Reserves:</strong> A calm, supported caregiver co-regulates a developing child's nervous system. Seek support, take restorative breaks, and connect with peer parent communities.</li>
</ul>
</div>
</div>""")

        # 3. The "Very Beautiful Ending" Climax — Heartfelt Golden Love Letter
        render_html(f"""<div style="background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 50%, #FDE68A 100%); border: 2.5px solid #F59E0B; border-radius: 22px; padding: 36px 42px; margin: 30px 0; box-shadow: 0 12px 32px rgba(245,158,11,0.15);">
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
<span style="background: #D97706; color: #FFFFFF; font-size: 0.82rem; font-weight: 800; padding: 5px 14px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.06em;">
🌟 A LOVE LETTER TO PARENTS & CAREGIVERS
</span>
</div>
<h2 style="font-size: 1.95rem; font-weight: 800; color: #78350F; margin: 8px 0 14px 0; letter-spacing: -0.01em; line-height: 1.3;">
Your Child is Not Broken — They Experience the World in a Beautiful, Distinct Frequency
</h2>
<p style="font-size: 1.08rem; line-height: 1.75; color: #92400E; margin-bottom: 18px;">
Neurodiversity is a natural, profound variation of the human mind. The traits identified today do not define <strong>{p_name}</strong>'s destiny; they illuminate how they process sound, sight, language, emotion, and connection. Today, you took the single most courageous, proactive step a caregiver can take: seeking understanding early during the golden window of childhood neuroplasticity.
</p>
<div style="background: rgba(255,255,255,0.75); border-radius: 14px; padding: 20px 24px; border-left: 5px solid #D97706; font-style: italic; color: #78350F; font-size: 1.05rem; line-height: 1.65;">
"Autism is not a tragedy. The tragedy is lack of understanding, delayed intervention, and lost time. By acting early, you gave {p_name} the greatest gift possible: time, understanding, and the unwavering foundation of your love. With the right early support, their future holds limitless brilliance, warmth, and joy."
</div>
</div>""")

        # 4. Official Gold-Seal Certificate of Parental Dedication & Screening Completion
        render_html(f"""<div style="background: #FFFFFF; border: 2px solid #CBD5E1; border-radius: 18px; padding: 26px 30px; box-shadow: 0 8px 24px rgba(15,23,42,0.06); margin-bottom: 30px;">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1D4ED8; padding-bottom: 16px; margin-bottom: 18px;">
<div>
<div style="font-size: 0.78rem; font-weight: 800; color: #1D4ED8; text-transform: uppercase; letter-spacing: 0.08em;">OFFICIAL CLINICAL RECORD CERTIFICATE OF COMPLETION</div>
<h3 style="font-size: 1.65rem; font-weight: 800; color: #0A192F; margin: 4px 0 2px 0;">{p_name}</h3>
<div style="font-size: 0.92rem; color: #64748B;">Dedicated Caregiver: <strong style="color: #0F172A;">{g_name}</strong> &bull; MRN: <strong>{mrn}</strong></div>
</div>
<div style="text-align: right;">
<div style="font-size: 2.8rem; line-height: 1;">🎖️</div>
<div style="font-size: 0.78rem; font-weight: 800; color: #059669; text-transform: uppercase; margin-top: 4px;">Completed Screening Dossier</div>
</div>
</div>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; font-size: 0.92rem;">
<div style="background: #F8FAFC; border-radius: 10px; padding: 14px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Assessment Date & Protocol</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #0A192F;">{eval_date}</div>
<div style="font-size: 0.76rem; color: #64748B;">Standardized Q-CHAT-10</div>
</div>
<div style="background: #F8FAFC; border-radius: 10px; padding: 14px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Clinical Staging Classification</div>
<div style="font-size: 1.05rem; font-weight: 800; color: {stage_info['color']};">{stage_info['stage_name']}</div>
<div style="font-size: 0.76rem; color: #64748B;">Affection Rate: {stage_info['affection_pct']:.1f}%</div>
</div>
<div style="background: #F8FAFC; border-radius: 10px; padding: 14px; border: 1px solid #E2E8F0;">
<div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Clinical Pathway Status</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #1D4ED8;">Action & Precautions Complete</div>
<div style="font-size: 0.76rem; color: #64748B;">Pediatric Referral Package Ready</div>
</div>
</div>
</div>""")

        # 5. Final Action Controls
        f_col1, f_col2, f_col3, f_col4 = st.columns([2.5, 1.8, 1.8, 1.5])
        with f_col1:
            if st.button("📄 View & Print Full Official Medical Report", type="primary", use_container_width=True):
                st.session_state["nav_target"] = "Clinical Test Report"
                st.rerun()
        with f_col2:
            if st.button("⬅️ Back: Action Plan & Stage", use_container_width=True):
                st.session_state["wiz_step"] = 8
                st.rerun()
        with f_col3:
            if st.button("🔄 Start New Screening", use_container_width=True):
                init_wizard_state(reset=True)
                st.rerun()
        with f_col4:
            if st.button("🏠 Home", use_container_width=True, key="step9_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()

    render_disclaimer()
