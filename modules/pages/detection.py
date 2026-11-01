import streamlit as st
import pandas as pd
import datetime
from modules.theme import render_section_header, render_disclaimer, render_html
from modules.ml_pipeline import run_single_patient_inference

def init_wizard_state():
    """Initializes session state for the step-by-step screening wizard."""
    if "wiz_step" not in st.session_state:
        st.session_state["wiz_step"] = 1
    if "wiz_age" not in st.session_state:
        st.session_state["wiz_age"] = 24
    if "wiz_sex" not in st.session_state:
        st.session_state["wiz_sex"] = "m"
    if "wiz_ethnicity" not in st.session_state:
        st.session_state["wiz_ethnicity"] = "White-European"
    if "wiz_jaundice" not in st.session_state:
        st.session_state["wiz_jaundice"] = "no"
    if "wiz_family_asd" not in st.session_state:
        st.session_state["wiz_family_asd"] = "no"
    if "wiz_screener" not in st.session_state:
        st.session_state["wiz_screener"] = "family member"
    if "wiz_q" not in st.session_state:
        st.session_state["wiz_q"] = {f"Q{i}": 0 for i in range(1, 11)}
    if "wiz_results" not in st.session_state:
        st.session_state["wiz_results"] = None

def render_stepper(current_step):
    """Renders visual multi-step progress indicator at the top."""
    steps = [
        (1, "1. Age", "👶"),
        (2, "2. Gender", "🚻"),
        (3, "3. History", "📋"),
        (4, "4. Social (Q1-Q5)", "🗣️"),
        (5, "5. Motor (Q6-Q10)", "🔄"),
        (6, "6. AI Results", "🧠")
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
        html += f"""
        <div class="{cls}">
            <div class="step-circle">{circle_content}</div>
            <span>{icon} {label}</span>
        </div>
        """
        if step_num < 6:
            html += '<span style="color: #CBD5E1; font-weight: bold; margin: 0 4px;">➔</span>'
    html += '</div>'
    render_html(html)

def render():
    render_section_header(
        "Step-by-Step Guided ASD Clinical Screener",
        "Interactive developmental assessment guiding you sequentially from child age and demographics to behavioral screening.",
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
    # STEP 1: CHILD'S AGE
    # -------------------------------------------------------------
    if step == 1:
        render_html("""
        <div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
            <div class="med-card-header">
                <div class="med-card-icon">👶</div>
                <span class="pill-badge pill-blue">Step 1 of 5</span>
            </div>
            <div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
                What is the child's chronological age in months?
            </div>
            <div class="med-card-body" style="font-size: 1rem; color: #475569;">
                Standardized pediatric screening via the Q-CHAT protocol is calibrated for toddlers between <strong>12 and 36 months</strong> of age. 
                This period represents the golden developmental window of maximal neural plasticity.
            </div>
        </div>
        """)

        col_input, col_info = st.columns([2, 1.5])
        with col_input:
            render_html("<p style='font-size: 1.05rem; font-weight: 800; color: #0A192F !important; margin-bottom: 8px;'>Select Child's Age (in Months):</p>")
            age_val = st.slider(
                "Select Child's Age (in Months):",
                min_value=12,
                max_value=36,
                value=int(st.session_state["wiz_age"]),
                step=1,
                label_visibility="collapsed",
                help="Select the exact age in months of the child at the time of screening."
            )
            st.session_state["wiz_age"] = age_val

        with col_info:
            render_html(f"""
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 18px; margin-top: 5px;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #1D4ED8; text-transform: uppercase;">Selected Milestone</div>
                <div style="font-size: 2rem; font-weight: 800; color: #1D4ED8; margin: 4px 0;">{age_val} Months</div>
                <div style="font-size: 0.85rem; color: #334155;">
                    Approx. <strong>{age_val // 12} year(s) and {age_val % 12} month(s)</strong> old.
                </div>
            </div>
            """)

        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_spacer = st.columns([1.5, 1.8, 3.5])
        with nav_col1:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col2:
            if st.button("Next: Biological Sex ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 2
                st.rerun()

    # -------------------------------------------------------------
    # STEP 2: BIOLOGICAL SEX
    # -------------------------------------------------------------
    elif step == 2:
        render_html("""
        <div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
            <div class="med-card-header">
                <div class="med-card-icon">🚻</div>
                <span class="pill-badge pill-blue">Step 2 of 5</span>
            </div>
            <div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
                What is the child's biological sex?
            </div>
            <div class="med-card-body" style="font-size: 1rem; color: #475569;">
                Biological sex is evaluated by the models to normalize normative developmental behavioral trajectories and account for known prevalence ratios.
            </div>
        </div>
        """)

        c_sex1, c_sex2 = st.columns(2)
        curr_sex = st.session_state["wiz_sex"]
        with c_sex1:
            is_male = (curr_sex == "m")
            render_html(f"""
            <div style="border: 2px solid {'#1D4ED8' if is_male else '#E2E8F0'}; background: {'#EFF6FF' if is_male else '#FFFFFF'}; border-radius: 14px; padding: 22px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 6px;">👦</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0A192F;">Male</div>
                <div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">Biological Male</div>
            </div>
            """)
            if st.button("Select Male", use_container_width=True, type="primary" if is_male else "secondary"):
                st.session_state["wiz_sex"] = "m"
                st.rerun()

        with c_sex2:
            is_female = (curr_sex == "f")
            render_html(f"""
            <div style="border: 2px solid {'#1D4ED8' if is_female else '#E2E8F0'}; background: {'#EFF6FF' if is_female else '#FFFFFF'}; border-radius: 14px; padding: 22px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 6px;">👧</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0A192F;">Female</div>
                <div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">Biological Female</div>
            </div>
            """)
            if st.button("Select Female", use_container_width=True, type="primary" if is_female else "secondary"):
                st.session_state["wiz_sex"] = "f"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1.5, 1.5, 1.8, 2.2])
        with nav_col1:
            if st.button("⬅️ Back: Age", use_container_width=True):
                st.session_state["wiz_step"] = 1
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step2_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("Next: Clinical History ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 3
                st.rerun()

    # -------------------------------------------------------------
    # STEP 3: CLINICAL & PERINATAL BACKGROUND
    # -------------------------------------------------------------
    elif step == 3:
        render_html("""
        <div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
            <div class="med-card-header">
                <div class="med-card-icon">📋</div>
                <span class="pill-badge pill-blue">Step 3 of 5</span>
            </div>
            <div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
                Clinical, Perinatal & Family Background
            </div>
            <div class="med-card-body" style="font-size: 1rem; color: #475569;">
                Please provide demographic and clinical history details. These are encoded as non-linear priors by TabNet and MLP neural networks.
            </div>
        </div>
        """)

        col1, col2 = st.columns(2)
        with col1:
            render_html("<p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Ethnicity / Cultural Background:</p>")
            eth_options = [
                "White-European", "Asian", "Middle Eastern", "black",
                "South Asian", "Hispanic", "Latino", "mixed", "others"
            ]
            current_eth = st.session_state["wiz_ethnicity"]
            eth_idx = eth_options.index(current_eth) if current_eth in eth_options else 0
            st.session_state["wiz_ethnicity"] = st.selectbox(
                "Ethnicity:",
                options=eth_options,
                index=eth_idx,
                format_func=lambda x: x.title(),
                label_visibility="collapsed"
            )

            render_html("<div style='margin-top: 14px;'></div><p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Who is completing this screening questionnaire?</p>")
            screener_options = ["family member", "Health Care Professional", "Others"]
            curr_scr = st.session_state["wiz_screener"]
            scr_idx = screener_options.index(curr_scr) if curr_scr in screener_options else 0
            st.session_state["wiz_screener"] = st.selectbox(
                "Who is completing this screening questionnaire?",
                options=screener_options,
                index=scr_idx,
                format_func=lambda x: x.title(),
                label_visibility="collapsed"
            )

        with col2:
            render_html("<p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Was the child born with neonatal jaundice?</p>")
            st.session_state["wiz_jaundice"] = st.radio(
                "Was the child born with neonatal jaundice?",
                options=["no", "yes"],
                index=0 if st.session_state["wiz_jaundice"] == "no" else 1,
                horizontal=True,
                format_func=lambda x: "Yes (Jaundice diagnosed)" if x == "yes" else "No",
                label_visibility="collapsed"
            )

            render_html("<div style='margin-top: 14px;'></div><p style='font-size: 0.95rem; font-weight: 800; color: #0A192F !important; margin-bottom: 6px;'>Does any immediate family member have diagnosed ASD?</p>")
            st.session_state["wiz_family_asd"] = st.radio(
                "Does any immediate family member have diagnosed ASD?",
                options=["no", "yes"],
                index=0 if st.session_state["wiz_family_asd"] == "no" else 1,
                horizontal=True,
                format_func=lambda x: "Yes (Parent or sibling)" if x == "yes" else "No",
                label_visibility="collapsed"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_col3, nav_spacer = st.columns([1.5, 1.5, 2.2, 1.8])
        with nav_col1:
            if st.button("⬅️ Back: Gender", use_container_width=True):
                st.session_state["wiz_step"] = 2
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step3_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("Next: Social Questions (Q1-Q5) ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 4
                st.rerun()

    # -------------------------------------------------------------
    # STEP 4: SOCIAL COMMUNICATION QUESTIONS (Q1 TO Q5)
    # -------------------------------------------------------------
    elif step == 4:
        render_html("""
        <div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 20px;">
            <div class="med-card-header">
                <div class="med-card-icon">🗣️</div>
                <span class="pill-badge pill-blue">Step 4 of 5 &bull; Domain A</span>
            </div>
            <div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
                Social Communication & Interaction (Q1 to Q5)
            </div>
            <div class="med-card-body" style="font-size: 1rem; color: #475569;">
                Evaluate the child's typical communicative behaviors. Select whether the response indicates a <strong>typical developmental trait (0)</strong> or an <strong>atypical screening marker (1)</strong>.
            </div>
        </div>
        """)

        q_list_1 = [
            ("Q1", "Does your child look at you when you call his/her name?", "Always / Usually (0)", "Rarely or Never (1)"),
            ("Q2", "How easy is it for you to establish mutual eye contact with your child?", "Very easy / Typical (0)", "Difficult / Rare (1)"),
            ("Q3", "Does your child point to indicate that s/he wants something (e.g. out of reach)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q4", "Does your child point to share interest with you (e.g. pointing at an airplane)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q5", "Does your child engage in pretend play (e.g. caring for a doll, talking on a toy phone)?", "Frequently / Often (0)", "Rarely or Never (1)")
        ]

        for qid, qtext, opt0, opt1 in q_list_1:
            curr_val = st.session_state["wiz_q"].get(qid, 0)
            render_html(f"""
            <div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 12px; padding: 14px 18px 12px 18px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                <div style="font-size: 1.05rem; font-weight: 800; color: #0A192F !important; line-height: 1.5;">
                    <span style="background: #1D4ED8; color: #FFFFFF !important; padding: 3px 10px; border-radius: 6px; font-weight: 800; font-size: 0.88rem; margin-right: 8px;">{qid}</span>
                    <span style="color: #0A192F !important;">{qtext}</span>
                </div>
            </div>
            """)
            choice = st.radio(
                f"Selection for {qid}",
                options=[0, 1],
                index=curr_val,
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
                st.session_state["wiz_step"] = 3
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step4_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("Next: Motor Traits (Q6-Q10) ➔", type="primary", use_container_width=True):
                st.session_state["wiz_step"] = 5
                st.rerun()

    # -------------------------------------------------------------
    # STEP 5: MOTOR & BEHAVIORAL QUESTIONS (Q6 TO Q10)
    # -------------------------------------------------------------
    elif step == 5:
        render_html("""
        <div class="med-card" style="border-left: 5px solid #7C3AED; margin-bottom: 20px;">
            <div class="med-card-header">
                <div class="med-card-icon">🔄</div>
                <span class="pill-badge pill-purple">Step 5 of 5 &bull; Domains A & B</span>
            </div>
            <div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
                Affective, Motor & Communicative Traits (Q6 to Q10)
            </div>
            <div class="med-card-body" style="font-size: 1rem; color: #475569;">
                Final screening indicators assessing gaze tracking, empathy, speech sounds, communicative gestures, and repetitive motor mannerisms.
            </div>
        </div>
        """)

        q_list_2 = [
            ("Q6", "Does your child follow where you look (gaze tracking)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q7", "If someone in the family is upset, does the child show empathy or try to comfort them?", "Frequently (0)", "Rarely or Never (1)"),
            ("Q8", "Would you describe your child's first words or vocalizations as:", "Typical & communicative (0)", "Absent or atypical echoes (1)"),
            ("Q9", "Does your child use simple communicative gestures (e.g. waving bye-bye, shaking head)?", "Many times a day (0)", "Rarely or Never (1)"),
            ("Q10", "Does your child stare at objects with no apparent purpose or show repetitive motor mannerisms?", "Never or Rarely (0)", "Frequently or Constantly (1)")
        ]

        for qid, qtext, opt0, opt1 in q_list_2:
            curr_val = st.session_state["wiz_q"].get(qid, 0)
            render_html(f"""
            <div style="background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 12px; padding: 14px 18px 12px 18px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                <div style="font-size: 1.05rem; font-weight: 800; color: #0A192F !important; line-height: 1.5;">
                    <span style="background: #7C3AED; color: #FFFFFF !important; padding: 3px 10px; border-radius: 6px; font-weight: 800; font-size: 0.88rem; margin-right: 8px;">{qid}</span>
                    <span style="color: #0A192F !important;">{qtext}</span>
                </div>
            </div>
            """)
            choice = st.radio(
                f"Selection for {qid}",
                options=[0, 1],
                index=curr_val,
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
                st.session_state["wiz_step"] = 4
                st.rerun()
        with nav_col2:
            if st.button("🏠 Home", use_container_width=True, key="step5_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()
        with nav_col3:
            if st.button("🧠 Evaluate Developmental Risk with AI ➔", type="primary", use_container_width=True):
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

                # Save results & patient report for the Clinical Test Report page
                st.session_state["wiz_results"] = res
                st.session_state["latest_patient_report"] = {
                    "patient_name": f"Patient ({'Male' if patient_dict['Sex']=='m' else 'Female'}, {patient_dict['Age']}m)",
                    "mrn": "MRN-ASD-" + datetime.date.today().strftime("%Y%m%d") + "-01",
                    "date": datetime.date.today().strftime("%B %d, %Y"),
                    "examiner": "Pediatric Screening Specialist",
                    "institution": "Pediatric Neurodevelopmental Clinical Center",
                    **patient_dict,
                    **res
                }
                st.session_state["wiz_step"] = 6
                st.rerun()

    # -------------------------------------------------------------
    # STEP 6: AI CLINICAL RESULTS & PRINT REPORT
    # -------------------------------------------------------------
    elif step == 6:
        res = st.session_state.get("wiz_results")
        if res is None:
            st.warning("No evaluation results found. Please start from Step 1.")
            if st.button("Start Screening"):
                st.session_state["wiz_step"] = 1
                st.rerun()
            return

        is_elevated = (res["tabnet_pred"] == 1) or (res["mlp_pred"] == 1) or (res["aq10_score"] >= 3)
        
        if is_elevated:
            render_html("""
            <div style="background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); border: 2px solid #EF4444; border-radius: 16px; padding: 24px; margin-bottom: 25px;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span class="pill-badge pill-amber" style="background: #DC2626; color: #FFFFFF; font-size: 0.85rem;">ELEVATED RISK DETECTED</span>
                        <h3 style="color: #991B1B; margin: 10px 0 6px 0; font-size: 1.45rem; font-weight: 800;">
                            Developmental ASD Traits Indicated
                        </h3>
                        <p style="color: #7F1D1D; margin: 0; font-size: 0.98rem; line-height: 1.5;">
                            The deep learning models identified behavioral response patterns consistent with elevated Autism Spectrum traits. A comprehensive multidisciplinary pediatric evaluation is advised.
                        </p>
                    </div>
                    <div style="font-size: 3rem; margin-left: 20px;">⚠️</div>
                </div>
            </div>
            """)
        else:
            render_html("""
            <div style="background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border: 2px solid #10B981; border-radius: 16px; padding: 24px; margin-bottom: 25px;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span class="pill-badge pill-green" style="background: #059669; color: #FFFFFF; font-size: 0.85rem;">LOW RISK PROFILE</span>
                        <h3 style="color: #065F46; margin: 10px 0 6px 0; font-size: 1.45rem; font-weight: 800;">
                            Typical Developmental Trajectory Indicated
                        </h3>
                        <p style="color: #064E3B; margin: 0; font-size: 0.98rem; line-height: 1.5;">
                            Responses fall within normative developmental expectations for this age group. Continue routine pediatric surveillance and developmental milestone checkups.
                        </p>
                    </div>
                    <div style="font-size: 3rem; margin-left: 20px;">✅</div>
                </div>
            </div>
            """)

        # Model Metric Breakdown Cards
        c1, c2, c3 = st.columns(3)
        with c1:
            render_html(f"""
            <div class="med-card">
                <div class="med-card-header">
                    <div class="med-card-icon">🧠</div>
                    <span class="pill-badge {'pill-amber' if res['tabnet_pred'] == 1 else 'pill-green'}">
                        {'ASD Positive' if res['tabnet_pred'] == 1 else 'ASD Negative'}
                    </span>
                </div>
                <div class="med-card-title">TabNet Prediction</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #1D4ED8; margin-bottom: 6px;">
                    {res['tabnet_prob'] * 100:.1f}%
                </div>
                <div class="med-card-body">
                    Model Confidence for ASD Traits.<br>
                    Sequential sparse attention analysis.
                </div>
            </div>
            """)

        with c2:
            render_html(f"""
            <div class="med-card">
                <div class="med-card-header">
                    <div class="med-card-icon">⚡</div>
                    <span class="pill-badge {'pill-amber' if res['mlp_pred'] == 1 else 'pill-green'}">
                        {'ASD Positive' if res['mlp_pred'] == 1 else 'ASD Negative'}
                    </span>
                </div>
                <div class="med-card-title">MLP Neural Net Prediction</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #7C3AED; margin-bottom: 6px;">
                    {res['mlp_prob'] * 100:.1f}%
                </div>
                <div class="med-card-body">
                    Calibrated Probability.<br>
                    Threshold cutoff applied at 0.60.
                </div>
            </div>
            """)

        with c3:
            render_html(f"""
            <div class="med-card">
                <div class="med-card-header">
                    <div class="med-card-icon">📋</div>
                    <span class="pill-badge pill-blue">Q-CHAT Score</span>
                </div>
                <div class="med-card-title">Behavioral Domain Scores</div>
                <div style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin-bottom: 6px;">
                    {res['aq10_score']} / 10
                </div>
                <div class="med-card-body">
                    <strong>Domain A (Social):</strong> {res['a_domain']} / 9<br>
                    <strong>Domain B (Repetitive):</strong> {res['b_domain']} / 1
                </div>
            </div>
            """)

        # Actions: Open and Print Clinical Report OR Start New Screening
        st.markdown("<br>", unsafe_allow_html=True)
        r_btn_col1, r_btn_col2, r_btn_col3, r_spacer = st.columns([2.5, 1.8, 1.8, 1.9])
        with r_btn_col1:
            if st.button("📄 View & Print Official Patient Report", type="primary", use_container_width=True):
                st.session_state["nav_target"] = "Clinical Test Report"
                st.rerun()
        with r_btn_col2:
            if st.button("🔄 Start New Screening", use_container_width=True):
                st.session_state["wiz_step"] = 1
                st.session_state["wiz_results"] = None
                st.rerun()
        with r_btn_col3:
            if st.button("🏠 Return to Home", use_container_width=True, key="step6_home_btn"):
                st.session_state["nav_target"] = "Home"
                st.rerun()

        # Guidance Recommendation
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Clinical Recommendation & Next Steps")
        if is_elevated:
            st.markdown("""1. **Pediatric Consultation:** Present these screening findings to your child's pediatrician or family physician.
2. **Multidisciplinary Assessment:** Request a formal evaluation with a developmental pediatrician, child psychologist, or pediatric neurologist.
3. **Early Intervention Services:** Initiate county/state early intervention programs immediately; referral does not require a finalized formal diagnosis.""")
        else:
            st.markdown("""1. **Maintain Routine Checkups:** Continue standard 18- and 24-month well-child pediatric checkups.
2. **Monitor Emerging Milestones:** Keep tracking speech, social smiling, and motor milestone progressions.
3. **Re-Screen if Concerns Arise:** Re-evaluate if you observe any regression in acquired social or communicative abilities.""")

    render_disclaimer()
