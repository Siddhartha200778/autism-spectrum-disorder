import streamlit as st
from modules.theme import render_section_header, render_disclaimer

def render():
    render_section_header(
        "Research Methodology & Experimental Workflow",
        "Step-by-step overview of data ingestion, clinical feature engineering, synthetic oversampling, and deep neural model training.",
        badge="SCIENTIFIC METHODOLOGY"
    )

    # Visual Workflow Diagram (High-Fidelity CSS & SVG Architecture)
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 28px 20px; box-shadow: 0 4px 16px rgba(15,23,42,0.04); margin-bottom: 30px;">
        <h4 style="color: #0A192F; font-size: 1.15rem; font-weight: 700; margin-bottom: 20px; text-align: center;">
            End-to-End Clinical Deep Learning Pipeline
        </h4>
        <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 8px;">
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">📁</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #1D4ED8; margin-top: 4px;">1. Dataset Collection</div>
            </div>
            <div style="color: #94A3B8; font-weight: bold; font-size: 1.1rem;">➔</div>
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">🧹</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #1D4ED8; margin-top: 4px;">2. Preprocessing</div>
            </div>
            <div style="color: #94A3B8; font-weight: bold; font-size: 1.1rem;">➔</div>
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">⚙️</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #1D4ED8; margin-top: 4px;">3. Feature Eng.</div>
            </div>
            <div style="color: #94A3B8; font-weight: bold; font-size: 1.1rem;">➔</div>
            <div style="background: #F3E8FF; border: 1px solid #DDD6FE; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">✂️</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #7C3AED; margin-top: 4px;">4. Train-Test Split</div>
            </div>
            <div style="color: #94A3B8; font-weight: bold; font-size: 1.1rem;">➔</div>
            <div style="background: #F3E8FF; border: 1px solid #DDD6FE; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">⚖️</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #7C3AED; margin-top: 4px;">5. SMOTE Resampling</div>
            </div>
            <div style="color: #94A3B8; font-weight: bold; font-size: 1.1rem;">➔</div>
            <div style="background: #FDF2F8; border: 1px solid #FBCFE8; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">🤖</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #BE185D; margin-top: 4px;">6. TabNet & MLP Training</div>
            </div>
            <div style="color: #94A3B8; font-weight: bold; font-size: 1.1rem;">➔</div>
            <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">📊</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #047857; margin-top: 4px;">7. Model Evaluation</div>
            </div>
            <div style="color: #94A3B8; font-weight: bold; font-size: 1.1rem;">➔</div>
            <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 10px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 1.2rem;">📈</div>
                <div style="font-size: 0.78rem; font-weight: 700; color: #047857; margin-top: 4px;">8. Result Visualization</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Step Explanations
    st.subheader("Detailed Pipeline Stages")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">1. Dataset Collection</div>
            <div class="med-card-body">
                Comprises 1,054 toddler screening records collected using standardized Q-CHAT-10 screening protocols. 
                Features encompass 10 core behavioral indicators, child age (months), biological sex, ethnicity, neonatal jaundice history, immediate family ASD history, and who completed the questionnaire.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">2. Data Cleaning & Preprocessing</div>
            <div class="med-card-body">
                Redundant record identifiers (e.g., <code>Case_No</code>) are discarded. 
                Forward-fill imputation mitigates sparse recording gaps. 
                Categorical demographic attributes (<code>Sex</code>, <code>Ethnicity</code>, <code>Jaundice</code>, <code>Family_ASD</code>, <code>Screener</code>) are encoded via deterministic Label Encoding.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">3. Feature Engineering & Clinical Domains</div>
            <div class="med-card-body">
                Domain-specific clinical knowledge is embedded into synthetic aggregates:
                <ul>
                    <li><code>AQ10</code>: Cumulative behavioral score $\sum_{i=1}^{10} Q_i$.</li>
                    <li><code>A_domain</code>: Social Communication & Reciprocal Interaction score $\sum_{i=1}^{9} Q_i$.</li>
                    <li><code>B_domain</code>: Repetitive & Stereotyped Behaviors score ($Q_{10}$).</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">4. Stratified Train-Test Splitting</div>
            <div class="med-card-body">
                An 80/20 stratified split isolates an untouched hold-out test set to ensure rigorous zero-leakage generalizability assessment. 
                Continuous covariates such as <code>Age</code> are normalized via <code>StandardScaler</code> fitted strictly on training data.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">5. SMOTE Resampling (Training Fold Only)</div>
            <div class="med-card-body">
                Synthetic Minority Over-sampling Technique (SMOTE) balances class distributions strictly within the training fold. 
                Synthesizing plausible borderline cases in feature space enhances sensitivity and safeguards against diagnostic bias without contaminating the test set.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">6. Deep Neural Architecture Training</div>
            <div class="med-card-body">
                Two complementary architectures are trained:
                <ul>
                    <li><strong>TabNet:</strong> Sequential attentive decision steps, sparsemax masks, Adam optimizer ($lr=0.02$), validation patience early stopping.</li>
                    <li><strong>MLP:</strong> Dense feedforward topology $(16 \rightarrow 8)$, ReLU activation, L2 penalty ($\alpha=0.1$), early stopping on 20% validation split.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">7. Model Evaluation & Discrimination</div>
            <div class="med-card-body">
                Models are evaluated on the untouched holdout test partition across Accuracy, Precision, Recall, F1-Score, and ROC-AUC. 
                Decision thresholds are calibrated (e.g. 0.60 for MLP) to optimize clinical specificity.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">8. Result Visualization & Interpretability</div>
            <div class="med-card-body">
                TabNet feature importances are extracted and visualized alongside confusion matrices and receiver operating characteristic curves, delivering transparent clinical audit trails.
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_disclaimer()
