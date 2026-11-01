import streamlit as st
import os

from modules.theme import inject_custom_css, render_footer
from modules.ml_pipeline import load_default_dataset, preprocess_and_prepare, train_models_pipeline

# Page Configuration
st.set_page_config(
    page_title="Interpretable Deep Learning for Early ASD Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Healthcare AI Design System
inject_custom_css()

# Import Page Modules
from modules.pages import (
    home,
    about_asd,
    detection,
    test_report,
    dataset_analysis,
    models,
    comparison,
    results,
    methodology,
    about_us,
    contact
)

# Navigation Configuration
PAGES = [
    "Home",
    "About Autism",
    "Early ASD Detection",
    "Clinical Test Report",
    "Dataset Analysis",
    "AI Models",
    "Model Comparison",
    "Results & Visualization",
    "Research Methodology",
    "About Us",
    "Contact"
]

PAGE_ICONS = {
    "Home": "🏠",
    "About Autism": "📘",
    "Early ASD Detection": "🩺",
    "Clinical Test Report": "📄",
    "Dataset Analysis": "📊",
    "AI Models": "🧠",
    "Model Comparison": "⚖️",
    "Results & Visualization": "📈",
    "Research Methodology": "🔬",
    "About Us": "👥",
    "Contact": "📬"
}

# Auto-initialize Session State and Benchmark Dataset
if "raw_dataset" not in st.session_state or st.session_state["raw_dataset"] is None:
    raw_df = load_default_dataset()
    if raw_df is not None:
        st.session_state["raw_dataset"] = raw_df
        st.session_state["dataset_source"] = "Benchmark Research Dataset (dl dataset.xls)"
        st.session_state["dataset_size"] = "71.2 KB"

if "models_result" not in st.session_state and "raw_dataset" in st.session_state and st.session_state["raw_dataset"] is not None:
    with st.spinner("Initializing TabNet & MLP models on benchmark dataset..."):
        try:
            prep = preprocess_and_prepare(st.session_state["raw_dataset"])
            models_trained = train_models_pipeline(prep)
            st.session_state["prepared_data"] = prep
            st.session_state["models_result"] = models_trained
            st.session_state["data_preprocessed"] = True
        except Exception as e:
            st.warning(f"Note: Model training ready on user request ({e})")

# Sidebar Branding & Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 18px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%); width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; box-shadow: 0 4px 12px rgba(37,99,235,0.4);">
                🧠
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.05rem; color: #FFFFFF; letter-spacing: -0.01em;">
                    ASD DeepScreen
                </div>
                <div style="font-size: 0.75rem; color: #93C5FD; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                    Clinical Healthcare AI
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sync selection between buttons and radio
    if "nav_radio" not in st.session_state:
        st.session_state["nav_radio"] = "Home"

    if "nav_selection" in st.session_state and st.session_state["nav_selection"] != st.session_state["nav_radio"]:
        st.session_state["nav_radio"] = st.session_state["nav_selection"]

    selected_page = st.radio(
        "Platform Navigation",
        options=PAGES,
        index=PAGES.index(st.session_state["nav_radio"]) if st.session_state["nav_radio"] in PAGES else 0,
        format_func=lambda x: f"{PAGE_ICONS.get(x, '•')}  {x}",
        key="nav_radio"
    )
    st.session_state["nav_selection"] = selected_page

    # Model & Data Status Badge in Sidebar
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px; margin-top: 10px;">
        <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">
            SYSTEM STATUS
        </div>
    """, unsafe_allow_html=True)

    if "models_result" in st.session_state:
        tab_acc = st.session_state["models_result"]["tabnet"]["accuracy"] * 100
        mlp_acc = st.session_state["models_result"]["mlp"]["accuracy"] * 100
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981;"></span>
            <span style="font-size: 0.8rem; color: #E2E8F0; font-weight: 600;">Models Active & Calibrated</span>
        </div>
        <div style="font-size: 0.74rem; color: #94A3B8; margin-left: 14px;">
            TabNet Acc: {tab_acc:.1f}% &bull; MLP Acc: {mlp_acc:.1f}%
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #F59E0B;"></span>
            <span style="font-size: 0.8rem; color: #E2E8F0; font-weight: 600;">Awaiting Data Training</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Research Attribution
    st.markdown("""
    <div style="padding: 16px 4px 4px 4px; font-size: 0.74rem; color: #64748B; text-align: center; margin-top: 15px;">
        Interpretable Deep Learning for Early ASD Detection<br>
        Research Platform &bull; Streamlit Cloud
    </div>
    """, unsafe_allow_html=True)

# Page Router
PAGE_ROUTERS = {
    "Home": home.render,
    "About Autism": about_asd.render,
    "Early ASD Detection": detection.render,
    "Clinical Test Report": test_report.render,
    "Dataset Analysis": dataset_analysis.render,
    "AI Models": models.render,
    "Model Comparison": comparison.render,
    "Results & Visualization": results.render,
    "Research Methodology": methodology.render,
    "About Us": about_us.render,
    "Contact": contact.render
}

render_fn = PAGE_ROUTERS.get(selected_page, home.render)
render_fn()

# Global Footer
render_footer()
