import streamlit as st
import pandas as pd
from modules.theme import render_section_header, render_disclaimer
from modules.ml_pipeline import run_single_patient_inference

def render():
    render_section_header(
        "Early ASD Clinical Screening Tool",
        "Interactive pediatric assessment powered by calibrated TabNet and Multi-Layer Perceptron neural networks.",
        badge="INTERACTIVE AI SCREENING"
    )

    if "models_result" not in st.session_state or "prepared_data" not in st.session_state:
        st.info("💡 The predictive AI models are initializing on the research benchmark dataset...")
        return

    models_dict = st.session_state["models_result"]
    prepared_data = st.session_state["prepared_data"]

    st.markdown("""
    <div class="med-card" style="margin-bottom: 25px;">
        <div class="med-card-body">
            Please complete the standardized <strong>Q-CHAT-10</strong> behavioral screening questions below based on the child's typical behaviors over recent weeks. 
            The system analyzes responses alongside demographic and developmental risk factors.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("clinical_screening_form"):
        st.subheader("1. Patient Profile & Demographics")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            age_months = st.slider("Child's Age (in Months)", min_value=12, max_value=36, value=24, step=1)
            sex = st.selectbox("Biological Sex", options=["m", "f"], format_func=lambda x: "Male" if x == "m" else "Female")
        with d_col2:
            ethnicity = st.selectbox(
                "Ethnicity",
                options=[
                    "White-European", "Asian", "Middle Eastern", "black",
                    "South Asian", "Hispanic", "Latino", "mixed", "others"
                ],
                format_func=lambda x: x.title()
            )
            screener = st.selectbox(
                "Screener / Informant",
                options=["family member", "Health Care Professional", "Others"],
                format_func=lambda x: x.title()
            )
        with d_col3:
            jaundice = st.radio("Born with neonatal jaundice?", options=["yes", "no"], index=1, horizontal=True)
            family_asd = st.radio("Immediate family member with ASD?", options=["no", "yes"], index=0, horizontal=True)

        st.markdown("<hr style='margin: 25px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        st.subheader("2. Q-CHAT-10 Behavioral Screening Questions")
        st.caption("Select whether the atypical/autistic trait is present (1) or typical response (0).")

        questions_meta = [
            ("Q1", "Does your child look at you when you call his/her name?", "Always/Usually (0)", "Rarely/Never (1)"),
            ("Q2", "How easy is it for you to establish eye contact with your child?", "Very easy/Easy (0)", "Difficult/Very difficult (1)"),
            ("Q3", "Does your child point to indicate that s/he wants something (e.g. a toy out of reach)?", "Many times a day (0)", "Rarely or never (1)"),
            ("Q4", "Does your child point to share interest with you (e.g. pointing at an airplane)?", "Many times a day (0)", "Rarely or never (1)"),
            ("Q5", "Does your child engage in pretend play (e.g. feeding a doll, talking into a toy phone)?", "Frequently (0)", "Rarely or never (1)"),
            ("Q6", "Does your child follow where you look (gaze tracking)?", "Many times a day (0)", "Rarely or never (1)"),
            ("Q7", "If someone in the family is upset, does the child show empathy or comfort them?", "Frequently (0)", "Rarely or never (1)"),
            ("Q8", "Would you describe your child's first words / vocalizations as:", "Typical & communicative (0)", "Absent or atypical echoes (1)"),
            ("Q9", "Does your child use simple communicative gestures (e.g. waving goodbye)?", "Many times a day (0)", "Rarely or never (1)"),
            ("Q10", "Does your child stare at objects with no apparent purpose or show repetitive motor mannerisms?", "Never/Rarely (0)", "Frequently/Constantly (1)")
        ]

        answers = {}
        for i in range(0, 10, 2):
            q_col1, q_col2 = st.columns(2)
            with q_col1:
                qid, qtext, opt0, opt1 = questions_meta[i]
                choice = st.radio(f"**{qid}:** {qtext}", options=[0, 1], format_func=lambda x, o0=opt0, o1=opt1: o0 if x == 0 else o1, key=qid)
                answers[qid] = choice
            with q_col2:
                qid, qtext, opt0, opt1 = questions_meta[i+1]
                choice = st.radio(f"**{qid}:** {qtext}", options=[0, 1], format_func=lambda x, o0=opt0, o1=opt1: o0 if x == 0 else o1, key=qid)
                answers[qid] = choice

        submit_btn = st.form_submit_button("🧠 Evaluate Developmental Risk with AI", type="primary", use_container_width=True)

    if submit_btn:
        patient_dict = {
            "Age": age_months,
            "Sex": sex,
            "Ethnicity": ethnicity,
            "Jaundice": jaundice,
            "Family_ASD": family_asd,
            "Screener": screener,
            **answers
        }

        with st.spinner("Executing dual-model inference across TabNet and MLP networks..."):
            res = run_single_patient_inference(patient_dict, models_dict, prepared_data)

        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("AI Screening Evaluation Report", "Integrated results from TabNet and Multi-Layer Perceptron models.")

        # Summary risk alert
        is_elevated = (res["tabnet_pred"] == 1) or (res["mlp_pred"] == 1) or (res["aq10_score"] >= 3)
        
        if is_elevated:
            st.markdown("""
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
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
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
            """, unsafe_allow_html=True)

        # Model Metric Breakdown Cards
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
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
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
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
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
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
            """, unsafe_allow_html=True)

        # Guidance Recommendation
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Clinical Recommendation & Next Steps")
        if is_elevated:
            st.markdown("""
            1. **Pediatric Consultation:** Present these screening findings to your child's pediatrician or family physician.
            2. **Multidisciplinary Assessment:** Request a formal evaluation with a developmental pediatrician, child psychologist, or pediatric neurologist.
            3. **Early Intervention Services:** Initiate county/state early intervention programs immediately; referral does not require a finalized formal diagnosis.
            """)
        else:
            st.markdown("""
            1. **Maintain Routine Checkups:** Continue standard 18- and 24-month well-child pediatric checkups.
            2. **Monitor Emerging Milestones:** Keep tracking speech, social smiling, and motor milestone progressions.
            3. **Re-Screen if Concerns Arise:** Re-evaluate if you observe any regression in acquired social or communicative abilities.
            """)

    render_disclaimer()
