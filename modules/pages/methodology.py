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
            <div class="med-card-title">3. Leakage Mitigation & Predictive Feature Selection</div>
            <div class="med-card-body">
                In the published benchmark dataset, the ground-truth target was defined deterministically by the rule $\text{Q-CHAT-10} \ge 4$. 
                Including <code>Qchat-10-Score</code> or engineered proxy sums ($\sum Q_i$) directly as inputs causes circular target leakage. 
                To ensure authentic machine learning, all aggregate score columns are <strong>strictly excluded</strong> from the input space. 
                Models learn exclusively from:
                <ul>
                    <li>10 item-level behavioral indicators (<code>Q1</code>–<code>Q10</code>)</li>
                    <li>Demographic & clinical covariates (<code>Age</code>, <code>Sex</code>, <code>Ethnicity</code>, <code>Jaundice</code>, <code>Family_ASD</code>, <code>Screener</code>)</li>
                </ul>
            </div>
        </div>
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">4. Stratified Train-Validation-Test Splitting</div>
            <div class="med-card-body">
                An 80/20 stratified split isolates an untouched hold-out test set ($N=211$) to ensure rigorous zero-leakage generalizability assessment. 
                Within the training partition ($N=843$), an internal validation split ($N=169$) is carved exclusively to guide TabNet early stopping. 
                Continuous covariates such as <code>Age</code> are normalized via <code>StandardScaler</code> fitted strictly on training data.
            </div>
        </div>
        """)

    with col2:
        render_html("""
        <div class="med-card">
            <div class="med-card-title">5. SMOTE Resampling (Training Partition Only)</div>
            <div class="med-card-body">
                Synthetic Minority Over-sampling Technique (SMOTE) balances class distributions strictly within the training partition ($N=674 \\rightarrow 930$). 
                Neither the internal validation fold ($N=169$) nor the holdout test cohort ($N=211$) is ever touched by SMOTE, preserving authentic patient data distributions.
            </div>
        </div>
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">6. Deep Neural Architecture Training</div>
            <div class="med-card-body">
                Two complementary architectures are trained on the 16 clinical predictors:
                <ul>
                    <li><strong>TabNet:</strong> Sequential attentive decision steps, sparsemax masks, Adam optimizer ($lr=0.02$), validation-partition early stopping (patience 15).</li>
                    <li><strong>MLP:</strong> Dense feedforward topology $(16 \\rightarrow 8)$, ReLU activation, L2 penalty ($\\alpha=0.1$), early stopping on training validation split.</li>
                </ul>
            </div>
        </div>
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">7. Model Evaluation & Discrimination</div>
            <div class="med-card-body">
                Models are evaluated on the untouched holdout test partition ($N=211$) across Accuracy, Precision, Recall, Specificity, F1-Score, and ROC-AUC. 
                TabNet achieves 91.94% Accuracy, 94.52% Recall, and 0.9688 AUC, while the MLP baseline achieves 85.78% Accuracy, 86.30% Recall, and 0.9468 AUC.
            </div>
        </div>
        """)

        render_html("""
        <div class="med-card">
            <div class="med-card-title">8. Result Visualization & Interpretability</div>
            <div class="med-card-body">
                TabNet instance-wise feature importances are extracted and visualized alongside confusion matrices and receiver operating characteristic curves, delivering transparent clinical audit trails.
            </div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Scientific Limitations and Disclosures Section
    st.subheader("Scientific Disclosures & Methodological Limitations")
    render_html("""
    <div style="background: #FFFFFF; border: 1px solid #E3E8EE; border-radius: 10px; padding: 22px 24px; box-shadow: 0 1px 3px rgba(32,43,54,0.03);">
        <div style="font-size: 13px; font-weight: 700; color: #B45309; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
            Methodological Transparency & Limitations Notice
        </div>
        <ul style="font-size: 13px; color: #526071; line-height: 1.7; margin: 0; padding-left: 18px;">
            <li><strong>Label-Definition Bias:</strong> Ground-truth diagnosis in the benchmark toddler dataset was assigned using the clinical screening cutoff rule (Q-CHAT-10 &ge; 4). When score sums are excluded, models learn directly from individual behavioral items and demographic traits.</li>
            <li><strong>Cohort Prevalence Skew:</strong> The dataset exhibits a 69.07% ASD positive prevalence (728 positive vs 326 negative cases), which is substantially higher than general population toddler prevalence (~2–3%). SMOTE is used strictly on training data to mitigate training bias.</li>
            <li><strong>Demographic Representation:</strong> Male toddlers comprise 69.73% of the dataset cohort (735 male vs 319 female), reflecting documented clinical referral patterns but requiring caution regarding cross-gender generalizability.</li>
            <li><strong>Non-Diagnostic Research Scope:</strong> This platform is designed solely for academic risk stratification and developmental decision support research. It does not constitute a certified in vitro diagnostic medical device (SaMD) and must never substitute for direct multidisciplinary clinical evaluation.</li>
        </ul>
    </div>
    """)

    render_disclaimer()
