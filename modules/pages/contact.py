import streamlit as st
from modules.theme import render_section_header, render_disclaimer, render_html

def render():
    render_section_header(
        "Contact & Research Collaborations",
        "Connect with our research team, submit feedback, or explore collaborative pediatric screening initiatives.",
        badge="GET IN TOUCH"
    )

    c_form, c_info = st.columns([1.8, 1.2])

    with c_form:
        st.subheader("Send a Message / Research Inquiry")
        with st.form("contact_form"):
            name = st.text_input("Full Name", placeholder="e.g. Dr. Jane Smith")
            email = st.text_input("Email Address", placeholder="e.g. j.smith@university.edu")
            affiliation = st.text_input("Institution / Organization", placeholder="e.g. Dept of Pediatrics / University Medical Center")
            inquiry_type = st.selectbox(
                "Inquiry Category",
                options=[
                    "Academic Research Collaboration",
                    "Clinical Trial Integration",
                    "Dataset Sharing & Validation",
                    "Technical / Model Architecture Question",
                    "General Feedback"
                ]
            )
            message = st.text_area("Message / Research Note", placeholder="Detail your research question, dataset inquiries, or clinical collaboration proposals...")
            submitted = st.form_submit_button("Send Inquiry", type="primary", use_container_width=True)

        if submitted:
            if not name or not email or not message:
                st.error("Please fill in your name, email, and message.")
            else:
                st.success(f"Thank you, {name}! Your inquiry regarding '{inquiry_type}' has been recorded. Our research team will review your message.")

    with c_info:
        st.subheader("Research Hub Details")
        render_html("""
        <div class="med-card">
            <div class="med-card-title">Research Inquiries</div>
            <div class="med-card-body">
                <strong>Project:</strong> Interpretable Deep Learning for Early ASD Detection<br>
                <strong>Platform:</strong> Streamlit Cloud & GitHub<br>
                <strong>Field:</strong> Biomedical Informatics & Deep Learning
            </div>
        </div>
        """)

        st.subheader("Frequently Asked Questions")
        with st.expander("Can this tool replace a pediatric diagnostic evaluation?"):
            st.write("No. This platform is an academic screening and risk stratification decision support aid. Formal autism diagnosis requires comprehensive clinical evaluation by qualified developmental specialists using gold-standard tools (ADOS-2, ADI-R).")

        with st.expander("How does TabNet provide interpretability?"):
            st.write("TabNet employs sequential decision steps with sparse attention masks, providing explicit quantitative importance weights for each behavioral question and demographic attribute.")

        with st.expander("Is my uploaded patient data stored?"):
            st.write("No. When deploying on Streamlit Cloud, uploaded files are processed in-memory during the active browser session and are not permanently logged or persisted on external databases.")

    render_disclaimer()
