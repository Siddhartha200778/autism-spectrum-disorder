import streamlit as st
from modules.theme import render_section_header, render_disclaimer, render_html

def render():
    render_section_header(
        "Research Methodology & Experimental Workflow",
        "Step-by-step overview of data ingestion, clinical feature engineering, synthetic oversampling, and deep neural model training.",
        badge="SCIENTIFIC METHODOLOGY"
    )

    # Visual Workflow Diagram (High-Fidelity Clinical Architecture)
    render_html("""
    <div style="background: #FFFFFF; border: 1px solid #E3E8EE; border-radius: 10px; padding: 24px 20px; box-shadow: 0 1px 3px rgba(32,43,54,0.03); margin-bottom: 24px;">
        <h4 style="color: #202B36; font-size: 15px; font-weight: 700; margin-bottom: 18px; text-align: center; text-transform: uppercase; letter-spacing: 0.04em;">
            End-to-End Clinical Deep Learning Pipeline
        </h4>
        <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 8px;">
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 1</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">Dataset Ingestion</div>
            </div>
            <div style="color: #667085; font-weight: bold; font-size: 12px;">→</div>
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 2</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">Preprocessing</div>
            </div>
            <div style="color: #667085; font-weight: bold; font-size: 12px;">→</div>
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 3</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">Feature Eng.</div>
            </div>
            <div style="color: #667085; font-weight: bold; font-size: 12px;">→</div>
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 4</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">Stratified Split</div>
            </div>
            <div style="color: #667085; font-weight: bold; font-size: 12px;">→</div>
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 5</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">SMOTE (Train)</div>
            </div>
            <div style="color: #667085; font-weight: bold; font-size: 12px;">→</div>
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 6</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">TabNet & MLP</div>
            </div>
            <div style="color: #667085; font-weight: bold; font-size: 12px;">→</div>
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 7</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">Evaluation</div>
            </div>
            <div style="color: #667085; font-weight: bold; font-size: 12px;">→</div>
            <div style="background: #EDF4F4; border: 1px solid #D0E3E3; border-radius: 6px; padding: 10px 14px; text-align: center; min-width: 110px;">
                <div style="font-size: 11px; font-weight: 700; color: #167C80;">STAGE 8</div>
                <div style="font-size: 12px; font-weight: 600; color: #202B36; margin-top: 3px;">Visualization</div>
            </div>
        </div>
    </div>
    """)

    # Detailed Step Explanations
    st.subheader("Detailed Pipeline Stages")

    col1, col2 = st.columns(2)

    with col1:
        render_html("""
        <div class="med-card">
            <div class="med-card-title">1. Dataset Collection</div>
            <div class="med-card-body">
                Comprises 1,054 toddler screening records collected using standardized Q-CHAT-10 screening protocols. 
                Features encompass 10 core behavioral indicators, child age (months), biological sex, ethnicity, neonatal jaundice history, immediate family ASD history, and who completed the questionnaire.
            </div>
        </div>
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">2. Data Cleaning & Preprocessing</div>
            <div class="med-card-body">
                Redundant record identifiers (e.g., <code>Case_No</code>) are discarded. 
                Forward-fill imputation mitigates sparse recording gaps. 
                Categorical demographic attributes (<code>Sex</code>, <code>Ethnicity</code>, <code>Jaundice</code>, <code>Family_ASD</code>, <code>Screener</code>) are encoded via deterministic Label Encoding.
            </div>
        </div>
        """)

        render_html(r"""
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
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">4. Stratified Train-Test Splitting</div>
            <div class="med-card-body">
                An 80/20 stratified split isolates an untouched hold-out test set to ensure rigorous zero-leakage generalizability assessment. 
                Continuous covariates such as <code>Age</code> are normalized via <code>StandardScaler</code> fitted strictly on training data.
            </div>
        </div>
        """)

    with col2:
        render_html("""
        <div class="med-card">
            <div class="med-card-title">5. SMOTE Resampling (Training Fold Only)</div>
            <div class="med-card-body">
                Synthetic Minority Over-sampling Technique (SMOTE) balances class distributions strictly within the training fold. 
                Synthesizing plausible borderline cases in feature space enhances sensitivity and safeguards against diagnostic bias without contaminating the test set.
            </div>
        </div>
        """)

        render_html("""
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
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">7. Model Evaluation & Discrimination</div>
            <div class="med-card-body">
                Models are evaluated on the untouched holdout test partition across Accuracy, Precision, Recall, F1-Score, and ROC-AUC. 
                Decision thresholds are calibrated (e.g. 0.60 for MLP) to optimize clinical specificity.
            </div>
        </div>
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">8. Result Visualization & Interpretability</div>
            <div class="med-card-body">
                TabNet feature importances are extracted and visualized alongside confusion matrices and receiver operating characteristic curves, delivering transparent clinical audit trails.
            </div>
        </div>
        """)

    render_disclaimer()
