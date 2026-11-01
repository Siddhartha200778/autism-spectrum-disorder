import streamlit as st
from modules.theme import render_section_header, render_disclaimer, render_html

def render():
    render_section_header(
        "About the Project & Research Initiative",
        "Interpretable Deep Learning for Early ASD Detection — Advancing Pediatric Healthcare AI.",
        badge="PROJECT PROFILE"
    )

    # Core Research Overview
    render_html("""
    <div class="med-card" style="border-left: 5px solid #1D4ED8; margin-bottom: 25px;">
        <div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">
            Interpretable Deep Learning for Early ASD Detection
        </div>
        <div class="med-card-body" style="font-size: 1.02rem; line-height: 1.7; color: #334155;">
            This project represents an academic deep learning research initiative dedicated to developing accurate, interpretable, and computationally efficient machine learning models for early behavioral screening of Autism Spectrum Disorder (ASD). 
            By systematically benchmarking attentive tabular neural networks (<strong>TabNet</strong>) against multi-layer perceptron (<strong>MLP</strong>) baselines on standardized pediatric screening cohorts, the framework demonstrates how deep learning can assist healthcare providers in identifying developmental risk markers during early childhood.
        </div>
    </div>
    """)

    # Pillars
    c1, c2, c3 = st.columns(3)
    with c1:
        render_html("""
        <div class="med-card">
            <div class="med-card-icon">🎯</div>
            <div class="med-card-title" style="margin-top: 10px;">Our Mission</div>
            <div class="med-card-body">
                To shorten the diagnostic latency between initial parental concern and clinical developmental intervention through reliable, non-invasive digital screening technology.
            </div>
        </div>
        """)

    with c2:
        render_html("""
        <div class="med-card">
            <div class="med-card-icon">🔍</div>
            <div class="med-card-title" style="margin-top: 10px;">Algorithmic Transparency</div>
            <div class="med-card-body">
                To eliminate the opacity of conventional "black-box" medical neural networks by leveraging sequential attention masks that directly reveal feature salience.
            </div>
        </div>
        """)

    with c3:
        render_html("""
        <div class="med-card">
            <div class="med-card-icon">🌐</div>
            <div class="med-card-title" style="margin-top: 10px;">Global Accessibility</div>
            <div class="med-card-body">
                To engineer an ultra-lightweight, browser-deployable healthcare architecture capable of running reliably on mobile devices and low-resource healthcare networks.
            </div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Technology Stack
    st.subheader("Technology Stack & Deep Learning Frameworks")
    
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        render_html("""
        <div class="med-card">
            <div style="font-weight: 700; color: #1D4ED8; font-size: 1.1rem; margin-bottom: 6px;">Deep Learning</div>
            <div class="med-card-body">
                &bull; PyTorch 2.x<br>
                &bull; PyTorch-TabNet<br>
                &bull; Scikit-Learn MLP
            </div>
        </div>
        """)

    with t2:
        render_html("""
        <div class="med-card">
            <div style="font-weight: 700; color: #7C3AED; font-size: 1.1rem; margin-bottom: 6px;">Data Processing</div>
            <div class="med-card-body">
                &bull; Imbalanced-Learn (SMOTE)<br>
                &bull; Pandas & NumPy<br>
                &bull; Openpyxl & XLRD
            </div>
        </div>
        """)

    with t3:
        render_html("""
        <div class="med-card">
            <div style="font-weight: 700; color: #059669; font-size: 1.1rem; margin-bottom: 6px;">Visualization</div>
            <div class="med-card-body">
                &bull; Matplotlib<br>
                &bull; Seaborn<br>
                &bull; Altair & CSS3
            </div>
        </div>
        """)

    with t4:
        render_html("""
        <div class="med-card">
            <div style="font-weight: 700; color: #D97706; font-size: 1.1rem; margin-bottom: 6px;">Deployment</div>
            <div class="med-card-body">
                &bull; Streamlit Cloud<br>
                &bull; GitHub Integration<br>
                &bull; Zero GPU Serverless
            </div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Attribution & Team Details
    st.subheader("Research Attribution & Governance")
    render_html("""
    <div class="med-card">
        <div class="med-card-title">Project Affiliation & Academic Context</div>
        <div class="med-card-body">
            This system was engineered as a university deep learning research project focusing on applied healthcare informatics, medical decision support, and explainable artificial intelligence.
            <br><br>
            <strong>Project Title:</strong> Interpretable Deep Learning for Early ASD Detection<br>
            <strong>Research Repository:</strong> <code>autism-spectrum-disorder</code> (Connected to Streamlit Cloud)<br>
            <strong>Clinical Dataset:</strong> Toddler Autism Screening Dataset (1,054 records, Q-CHAT-10 Protocol)
        </div>
    </div>
    """)

    render_disclaimer()
