import streamlit as st
from modules.theme import render_html

def render():
    # 1. Top Clinical Breadcrumb & Protocol Metadata Bar
    render_html("""
    <div class="clinical-top-bar">
        <div class="clinical-breadcrumbs">
            <span class="crumb-root">CLINICAL RESEARCH PLATFORM</span>
            <span class="crumb-sep">/</span>
            <span class="crumb-current">Overview</span>
        </div>
        <div class="protocol-pills-group">
            <div class="protocol-pill protocol-pill-teal">
                <span class="pill-dot"></span>
                <span>Cohort: Q-CHAT-10 Toddler (12-36 Months)</span>
            </div>
            <div class="protocol-pill protocol-pill-slate">
                <span>IRB Protocol: #PR-2024-884A</span>
            </div>
        </div>
    </div>
    """)

    # 2. Decision Support Amber Disclaimer Banner
    render_html("""
    <div class="decision-support-banner">
        <div class="decision-banner-icon">⚠️</div>
        <div class="decision-banner-content">
            <span class="decision-banner-title">RESEARCH SCREENING DECISION SUPPORT FRAMEWORK:</span>
            <span class="decision-banner-text">This system evaluates deep neural representation models for early behavioral marker detection. It is designed solely for academic and clinical research triage validation and does not constitute a definitive psychiatric or neurodevelopmental diagnosis.</span>
        </div>
    </div>
    """)

    # 3. Enterprise Clinical Hero Card with Integrated CTA Button
    hero_col_left, hero_col_right = st.columns([3.8, 1.2])
    with hero_col_left:
        render_html("""
        <div style="padding-top: 4px;">
            <h1 class="clinical-hero-title">Interpretable Deep Learning for Early ASD Detection in Toddlers</h1>
            <p class="clinical-hero-desc">
                Comparative clinical benchmark investigating attention-based sparse mask tabular transformers (TabNet) versus baseline feedforward multilayer perceptrons (MLP) on 1,054 toddler Q-CHAT-10 screening records.
            </p>
        </div>
        """)
    with hero_col_right:
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        if st.button("Inference Screening Tool ➔", type="primary", use_container_width=True, key="hero_cta_screener"):
            st.session_state["nav_target"] = "Early ASD Detection"
            st.rerun()

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # 4. 4 Swiss Metric Highlight Cards (Row of 4)
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        render_html("""
        <div class="metric-card-swiss">
            <div class="metric-label-swiss">Total Cohort Records</div>
            <div class="metric-value-swiss">1,054</div>
            <div class="metric-meta-swiss">Ages 12-36 Months &bull; Median 27.5m</div>
        </div>
        """)
    with mc2:
        render_html("""
        <div class="metric-card-swiss">
            <div class="metric-label-swiss">Positive ASD Screening Cases</div>
            <div class="metric-value-swiss">728</div>
            <div class="metric-meta-swiss"><span style="color: #B45309; font-weight: 600;">69.07% Clinical Prevalence in Cohort</span></div>
        </div>
        """)
    with mc3:
        render_html("""
        <div class="metric-card-swiss">
            <div class="metric-label-swiss">TabNet AUROC (5-Fold CV)</div>
            <div class="metric-value-swiss">0.9924</div>
            <div class="metric-meta-swiss"><span style="color: #0D7A75; font-weight: 700;">+0.0246 vs Baseline MLP</span></div>
        </div>
        """)
    with mc4:
        render_html("""
        <div class="metric-card-swiss">
            <div class="metric-label-swiss">Sparse Attention Sparsity</div>
            <div class="metric-value-swiss">84.2%</div>
            <div class="metric-meta-swiss">Entmax / Sparsemax Masking</div>
        </div>
        """)

    st.markdown("<div style='margin-bottom: 22px;'></div>", unsafe_allow_html=True)

    # 5. Side-by-Side Model Architecture Cards
    arch1, arch2 = st.columns(2)
    with arch1:
        render_html("""
        <div class="arch-card-swiss">
            <div class="arch-header-row">
                <div class="arch-title">PROPOSED MODEL: TABNET ARCHITECTURE</div>
                <span class="arch-badge-teal">SOTA Tabular</span>
            </div>
            <p class="arch-desc">
                Uses sequential multi-step decision steps with attentive transformers to perform instance-wise feature selection, enabling direct white-box interpretability without external surrogate models.
            </p>
            <div class="arch-stats-grid">
                <div class="arch-stat-box">
                    <span class="arch-stat-lbl">Test Acc</span>
                    <span class="arch-stat-val">98.10%</span>
                </div>
                <div class="arch-stat-box">
                    <span class="arch-stat-lbl">Precision</span>
                    <span class="arch-stat-val">98.67%</span>
                </div>
                <div class="arch-stat-box">
                    <span class="arch-stat-lbl">F1-Score</span>
                    <span class="arch-stat-val">0.9862</span>
                </div>
            </div>
        </div>
        """)

    with arch2:
        render_html("""
        <div class="arch-card-swiss">
            <div class="arch-header-row">
                <div class="arch-title">BENCHMARK BASELINE: MULTILAYER PERCEPTRON</div>
                <span class="arch-badge-blue">Feedforward DNN</span>
            </div>
            <p class="arch-desc">
                Standard dense 4-layer fully connected network (18-128-64-32-1) with Batch Normalization, ReLU activations, and Dropout (p=0.25). High baseline accuracy but lacks intrinsic feature selection.
            </p>
            <div class="arch-stats-grid">
                <div class="arch-stat-box">
                    <span class="arch-stat-lbl">Test Acc</span>
                    <span class="arch-stat-val">94.31%</span>
                </div>
                <div class="arch-stat-box">
                    <span class="arch-stat-lbl">Precision</span>
                    <span class="arch-stat-val">95.21%</span>
                </div>
                <div class="arch-stat-box">
                    <span class="arch-stat-lbl">F1-Score</span>
                    <span class="arch-stat-val">0.9588</span>
                </div>
            </div>
        </div>
        """)

    # 6. Cohort Demographic & Trait Distribution Section
    render_html("""
    <div class="section-header-bar">
        <div class="section-bar-title">COHORT DEMOGRAPHIC & TRAIT DISTRIBUTION (N=1,054)</div>
        <div class="section-bar-badge">
            <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10B981; margin-right:6px;"></span>
            Verified Clean Cohort
        </div>
    </div>
    """)

    # 4 Clinical Distribution Mini-Cards
    cd1, cd2, cd3, cd4 = st.columns(4)
    with cd1:
        render_html("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Sex Ratio</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #16324F; margin: 4px 0;">69.7% : 30.3%</div>
            <div style="font-size: 0.72rem; color: #64748B;">735 Male &bull; 319 Female</div>
        </div>
        """)
    with cd2:
        render_html("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Neonatal Jaundice</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #16324F; margin: 4px 0;">25.9%</div>
            <div style="font-size: 0.72rem; color: #64748B;">273 Positive History</div>
        </div>
        """)
    with cd3:
        render_html("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Family ASD History</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #16324F; margin: 4px 0;">16.1%</div>
            <div style="font-size: 0.72rem; color: #64748B;">170 Hereditary Cases</div>
        </div>
        """)
    with cd4:
        render_html("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; text-align: center;">
            <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">A-Domain Salience</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #0D7A75; margin: 4px 0;">Q6 (Joint Attn)</div>
            <div style="font-size: 0.72rem; color: #64748B;">Highest Sparse Mask Wt</div>
        </div>
        """)

    # Quick Clinical Navigation Action Bar
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    q1, q2, q3, q_spacer = st.columns([1.5, 1.5, 1.7, 2.5])
    with q1:
        if st.button("📊 Dataset Management", use_container_width=True, key="home_btn_data"):
            st.session_state["nav_target"] = "Dataset Management"
            st.rerun()
    with q2:
        if st.button("🔬 Model Evaluation", use_container_width=True, key="home_btn_eval"):
            st.session_state["nav_target"] = "Model Evaluation"
            st.rerun()
    with q3:
        if st.button("📄 Clinical Test Report", use_container_width=True, key="home_btn_rep"):
            st.session_state["nav_target"] = "Clinical Test Report"
            st.rerun()
