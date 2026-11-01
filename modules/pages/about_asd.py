import streamlit as st
from modules.theme import render_section_header, render_disclaimer, render_html

def render():
    render_section_header(
        "Understanding Autism Spectrum Disorder (ASD)",
        "A clinical overview of neurodevelopmental variations, early identification, and modern AI screening.",
        badge="CLINICAL KNOWLEDGE HUB"
    )

    # Core Definition Card
    render_html("""
    <div class="med-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F7FF 100%); border-left: 5px solid #1D4ED8;">
        <div class="med-card-title" style="font-size: 1.35rem; color: #0A192F;">What is Autism Spectrum Disorder?</div>
        <div class="med-card-body" style="font-size: 1.02rem; color: #334155;">
            <strong>Autism Spectrum Disorder (ASD)</strong> is a complex, neurodevelopmental condition characterized by persistent differences in social communication, reciprocal interaction, and restricted or repetitive patterns of behaviors, interests, or activities. 
            The term <em>"spectrum"</em> reflects the wide variety in challenges, presentation, and distinct strengths that each individual experiences across cognitive, verbal, and sensory dimensions.
        </div>
    </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Early Signs & Characteristics
    st.subheader("Early Signs & Behavioral Characteristics in Toddlers (12–36 Months)")
    col1, col2 = st.columns(2)
    
    with col1:
        render_html("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">🗣️</div>
                <span class="pill-badge pill-blue">Domain A</span>
            </div>
            <div class="med-card-title">Social Communication & Interaction</div>
            <div class="med-card-body">
                <ul>
                    <li><strong>Reduced Eye Contact:</strong> Limited mutual gaze during smiling, feeding, or play.</li>
                    <li><strong>Response to Name:</strong> Inconsistent or delayed orientation when their name is called by parents.</li>
                    <li><strong>Joint Attention:</strong> Infrequent pointing to objects or following an adult's pointing gesture to share interest.</li>
                    <li><strong>Social Smiling:</strong> Diminished reciprocal smiles or facial expressions responding to others.</li>
                    <li><strong>Imitative Play:</strong> Limited mimicry of simple actions (e.g., clapping, waving bye-bye).</li>
                </ul>
            </div>
        </div>
        """)

    with col2:
        render_html("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">🔄</div>
                <span class="pill-badge pill-purple">Domain B</span>
            </div>
            <div class="med-card-title">Repetitive Behaviors & Sensory Traits</div>
            <div class="med-card-body">
                <ul>
                    <li><strong>Repetitive Movements:</strong> Rhythmic hand-flapping, spinning in circles, rocking, or toe-walking.</li>
                    <li><strong>Object Fixation:</strong> Lining up toys in rigid sequences, spinning wheels, or intensely focusing on specific parts of objects.</li>
                    <li><strong>Insistence on Sameness:</strong> Strong emotional distress over minor shifts in daily routines or environments.</li>
                    <li><strong>Sensory Hyper/Hypo-Reactivity:</strong> Unusual reactions to everyday sensory inputs such as vacuum cleaners, bright lights, or fabric textures.</li>
                </ul>
            </div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Importance of Early Screening & Neuroplasticity
    render_section_header("The Critical Window: Why Early Identification Matters", "Unlocking developmental potential during early neurological growth.")

    c1, c2, c3 = st.columns(3)
    with c1:
        render_html("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">🌱</div>
                <span class="pill-badge pill-green">Neuroplasticity</span>
            </div>
            <div class="med-card-title">Peak Neural Malleability</div>
            <div class="med-card-body">
                Between 12 and 36 months, the infant brain forms neural connections at its highest historical rate. Interventions delivered during this golden window yield the greatest improvements in language and social reciprocity.
            </div>
        </div>
        """)

    with c2:
        render_html("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">⏳</div>
                <span class="pill-badge pill-amber">Latency Reduction</span>
            </div>
            <div class="med-card-title">Closing the Diagnostic Lag</div>
            <div class="med-card-body">
                While parents frequently observe atypical signs before 18 months, clinical diagnosis often occurs at 4 to 5 years. Standardized AI screening tools empower primary healthcare providers to flag risk years earlier.
            </div>
        </div>
        """)

    with c3:
        render_html("""
        <div class="med-card">
            <div class="med-card-header">
                <div class="med-card-icon">🤝</div>
                <span class="pill-badge pill-blue">Family Empowerment</span>
            </div>
            <div class="med-card-title">Targeted Family Support</div>
            <div class="med-card-body">
                Timely risk identification connects parents with speech therapy, occupational therapy, and behavioral guidance early, significantly reducing caregiver anxiety and financial stress.
            </div>
        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Role of AI in Screening
    st.subheader("The Role of Artificial Intelligence in Modern Screening")
    render_html("""
    <div class="med-card">
        <div class="med-card-body" style="font-size: 0.98rem; line-height: 1.7;">
            Traditional screening questionnaires like the Q-CHAT (Quantitative Checklist for Autism in Toddlers) rely on manual threshold summation. 
            However, linear scoring systems can fail to detect subtle, non-linear relationships between social communication indicators and developmental milestones.
            <br><br>
            <strong>How Machine Learning & Deep Learning Elevate ASD Screening:</strong>
            <ul>
                <li><strong>Complex Feature Interaction:</strong> Deep learning models recognize multivariate correlations across behavioral questions, age normalization, and genetic family history.</li>
                <li><strong>Explainability via TabNet:</strong> Unlike conventional opaque neural networks, attentive architectures (TabNet) assign sequential attention masks to each screening item, clearly indicating <em>why</em> a toddler was categorized at elevated risk.</li>
                <li><strong>Scalability & Triage:</strong> Digital screening platforms can be deployed globally on low-resource mobile and web interfaces, serving as a frontline clinical decision support tool for pediatric clinics and community health workers.</li>
            </ul>
        </div>
    </div>
    """)

    render_disclaimer()
