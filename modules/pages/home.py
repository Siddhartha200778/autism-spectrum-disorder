import streamlit as st
from modules.theme import render_disclaimer, render_section_header

def render():
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="clinical-brand-badge" style="background: rgba(255,255,255,0.15); color: #93C5FD; border-color: rgba(255,255,255,0.25);">
            CLINICAL AI &bull; DEEP LEARNING FRAMEWORK
        </div>
        <h1 class="hero-title">
            Early Autism Spectrum Disorder Detection Using Artificial Intelligence
        </h1>
        <p class="hero-subtitle">
            An interpretable deep tabular research architecture benchmarking Attentive TabNet and Multi-Layer Perceptrons (MLP) for reliable, explainable pediatric autism risk stratification.
        </p>
        <div class="hero-stats-bar">
            <div class="hero-stat-item">
                <span class="hero-stat-value">1,054</span>
                <span class="hero-stat-label">Clinical Records</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-value">100.0%</span>
                <span class="hero-stat-label">MLP Peak Accuracy</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-value">91.0%</span>
                <span class="hero-stat-label">TabNet Accuracy</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-value">10 Items</span>
                <span class="hero-stat-label">Q-Chat Protocol</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-value">SMOTE</span>
                <span class="hero-stat-label">Class Balanced</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Action Buttons
    c_btn1, c_btn2, c_spacer = st.columns([1.5, 1.5, 4])
    with c_btn1:
        if st.button("🚀 Start Detection", use_container_width=True, type="primary"):
            st.session_state["nav_selection"] = "Early ASD Detection"
            st.rerun()
    with c_btn2:
        if st.button("🔬 Explore Project", use_container_width=True):
            st.session_state["nav_selection"] = "Research Methodology"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Medical Disclaimer Banner
    render_disclaimer()

    # Project Overview Cards
    render_section_header("About The Research Project", "Bridging the gap between early childhood developmental screening and interpretable deep learning.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">🧠</div>
                <span class="pill-badge pill-blue">Interpretability</span>
            </div>
            <div class="med-card-title">Attentive TabNet Architecture</div>
            <div class="med-card-body">
                Leverages sequential sparse attention masks to dynamically identify which behavioral markers (Q1–Q10) contribute most to risk classification at each decision step.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">⚡</div>
                <span class="pill-badge pill-purple">Deep Learning</span>
            </div>
            <div class="med-card-title">Optimized MLP Network</div>
            <div class="med-card-body">
                Employs regularized multi-layer perceptrons with non-linear activations and early stopping, providing robust baseline discrimination across pediatric cohorts.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">⚖️</div>
                <span class="pill-badge pill-green">Imbalance Handling</span>
            </div>
            <div class="med-card-title">SMOTE Resampling</div>
            <div class="med-card-body">
                Synthetic Minority Over-sampling Technique is rigorously restricted to training folds to prevent diagnostic bias and data leakage while optimizing recall.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Key Features Grid
    render_section_header("Key Platform Capabilities", "Comprehensive toolkit designed for researchers, clinicians, and developmental screening.")
    
    kf1, kf2 = st.columns(2)
    with kf1:
        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">🎯 Instant Behavioral Risk Assessment</div>
            <div class="med-card-body">
                Interactive Q-Chat-10 questionnaire allowing parents and clinicians to screen toddlers across A-domain (Social Communication) and B-domain (Repetitive Behaviors) with real-time confidence scores.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">📊 Multi-Format Dataset Processing</div>
            <div class="med-card-body">
                Seamless drag-and-drop ingestion of CSV, XLS, and XLSX files with automatic schema validation, automated categorical encoding, and zero-configuration preprocessing.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with kf2:
        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">🔬 Comparative Analytics Dashboard</div>
            <div class="med-card-body">
                Side-by-side performance benchmarking across Accuracy, Precision, Recall, and F1-score with interactive ROC-AUC curves and dynamic confusion matrices.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="med-card">
            <div class="med-card-title">📈 Feature Salience Attribution</div>
            <div class="med-card-body">
                Direct extraction of TabNet feature importances, unveiling which questions and demographic indicators drive predictive variance without black-box opacity.
            </div>
        </div>
        """, unsafe_allow_html=True)
