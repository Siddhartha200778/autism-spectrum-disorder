import streamlit as st
import os

from modules.theme import inject_custom_css, render_footer, render_html
try:
    from modules.ml_pipeline import (
        load_default_dataset,
        preprocess_and_prepare,
        train_models_pipeline,
        get_benchmark_models_and_data,
    )
    _ML_PIPELINE_OK = True
except Exception as _ml_import_err:
    import logging as _logging
    _logging.warning("ml_pipeline import failed: %s", _ml_import_err)
    _ML_PIPELINE_OK = False

    # Stub fallbacks so the rest of app.py runs without crashing
    def load_default_dataset():  # type: ignore[override]
        return None

    def preprocess_and_prepare(df):  # type: ignore[override]
        return None

    def train_models_pipeline(prep):  # type: ignore[override]
        return None

    def get_benchmark_models_and_data():  # type: ignore[override]
        return None, None

# Page Configuration
st.set_page_config(
    page_title="Interpretable Deep Learning for Early ASD Detection",
    page_icon="AS",
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
    "Test Report",
    "Dataset Analysis",
    "AI Models",
    "Model Comparison",
    "Results & Visualization",
    "Research Methodology",
    "About Us",
    "Contact"
]

PAGE_ICONS = {
    "Home":                   "01.",
    "About Autism":           "02.",
    "Early ASD Detection":    "03.",
    "Clinical Test Report":   "04.",
    "Dataset Analysis":       "05.",
    "AI Models":              "06.",
    "Model Comparison":       "07.",
    "Results & Visualization":"08.",
    "Research Methodology":   "09.",
    "About Us":               "10.",
    "Contact":                "11.",
}

# Auto-initialize Pre-trained Models and Benchmark Dataset (Cached across all sessions)
cached_prep, cached_models = get_benchmark_models_and_data()

if "raw_dataset" not in st.session_state or st.session_state["raw_dataset"] is None:
    if cached_prep is not None and "raw_df" in cached_prep:
        st.session_state["raw_dataset"] = cached_prep["raw_df"]
    else:
        st.session_state["raw_dataset"] = load_default_dataset()
    st.session_state["dataset_source"] = "Toddler ASD Dataset (toddler_asd_dataset.csv)"
    st.session_state["dataset_size"] = "1,054 records &bull; 71.2 KB"

if "prepared_data" not in st.session_state and cached_prep is not None:
    st.session_state["prepared_data"] = cached_prep

if "models_result" not in st.session_state and cached_models is not None:
    st.session_state["models_result"] = cached_models
    st.session_state["data_preprocessed"] = True

# Sidebar Branding & Navigation
with st.sidebar:
    render_html("""
    <div style="padding: 10px 0 18px 0; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: #1D4ED8; width: 44px; height: 44px; border-radius: 10px;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 1.1rem; font-weight: 900; color: #FFFFFF;
                        flex-shrink: 0; box-shadow: 0 4px 14px rgba(29,78,216,0.5);">
                AS
            </div>
            <div>
                <div style="font-weight: 800; font-size: 0.95rem; color: #FFFFFF; line-height: 1.2;">
                    ASD TODDLER SCREENING
                </div>
                <div style="font-size: 0.68rem; color: #94A3B8; font-weight: 600; margin-top: 2px;">
                    TabNet v1.9EF &#183; py-tabnet 4.1
                </div>
            </div>
        </div>
    </div>
    """)

    # Synchronize programmatic navigation (buttons) with sidebar radio
    if "nav_target" in st.session_state:
        target = st.session_state.pop("nav_target")
        if target in PAGES:
            st.session_state["nav_radio"] = target
    elif "nav_selection" in st.session_state:
        target = st.session_state.pop("nav_selection")
        if target in PAGES:
            st.session_state["nav_radio"] = target

    if "nav_radio" not in st.session_state or st.session_state["nav_radio"] not in PAGES:
        st.session_state["nav_radio"] = "Home"

    selected_page = st.radio(
        "Platform Navigation",
        options=PAGES,
        key="nav_radio",
        format_func=lambda x: f"{PAGE_ICONS.get(x, '•')}  {x}"
    )
    st.session_state["active_page"] = selected_page

    # Live System Status Badge in Sidebar
    st.markdown("<br>", unsafe_allow_html=True)
    if "models_result" in st.session_state:
        tab_acc = st.session_state["models_result"]["tabnet"]["accuracy"] * 100
        mlp_acc = st.session_state["models_result"]["mlp"]["accuracy"] * 100
        status_html = f"""
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px; margin-top: 10px;">
            <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">SYSTEM STATUS</div>
            <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981; box-shadow: 0 0 8px rgba(16,185,129,0.6);"></span>
                <span style="font-size: 0.82rem; color: #E2E8F0; font-weight: 700;">Models Active & Calibrated</span>
            </div>
            <div style="font-size: 0.74rem; color: #94A3B8; margin-left: 14px;">TabNet: {tab_acc:.1f}% &bull; MLP: {mlp_acc:.1f}%</div>
        </div>
        """
    else:
        status_html = """
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px; margin-top: 10px;">
            <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">SYSTEM STATUS</div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #F59E0B;"></span>
                <span style="font-size: 0.82rem; color: #E2E8F0; font-weight: 700;">Awaiting Data Training</span>
            </div>
        </div>
        """
    render_html(status_html)

    # Sidebar Research Attribution
    render_html("""
    <div style="padding: 16px 4px 4px 4px; font-size: 0.74rem; color: #64748B; text-align: center; margin-top: 15px;">
        Interpretable Deep Learning for Early ASD Detection<br>
        Research Platform &bull; Streamlit Cloud
    </div>
    """)

# Navigation History Tracking
if "nav_history" not in st.session_state:
    st.session_state["nav_history"] = []

if "current_page_tracked" not in st.session_state:
    st.session_state["current_page_tracked"] = "Home"

if selected_page != st.session_state["current_page_tracked"]:
    old_p = st.session_state["current_page_tracked"]
    if not st.session_state["nav_history"] or st.session_state["nav_history"][-1] != old_p:
        st.session_state["nav_history"].append(old_p)
    st.session_state["current_page_tracked"] = selected_page

# Universal Top Navigation Bar (on every page except Home)
if selected_page != "Home":
    prev_target = st.session_state["nav_history"][-1] if st.session_state["nav_history"] else "Home"
    top_c1, top_c2, top_c3, top_spacer = st.columns([1.6, 1.6, 1.8, 5.0])
    with top_c1:
        if st.button(f"← Back ({prev_target})", key="global_top_back", help=f"Return to {prev_target}"):
            dest = st.session_state["nav_history"].pop() if st.session_state["nav_history"] else "Home"
            st.session_state["nav_target"] = dest
            st.rerun()
    with top_c2:
        if st.button("Home", key="global_top_home", help="Navigate to Home page"):
            st.session_state["nav_target"] = "Home"
            st.rerun()
    with top_c3:
        if selected_page != "Early ASD Detection":
            if st.button("Early Detection", key="global_top_screener", help="Open ASD Screener"):
                st.session_state["nav_target"] = "Early ASD Detection"
                st.rerun()
        else:
            if st.button("Test Report", key="global_top_report", help="Clinical Test Report"):
                st.session_state["nav_target"] = "Test Report"
                st.rerun()
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

# Page Router
PAGE_ROUTERS = {
    "Home": home.render,
    "About Autism": about_asd.render,
    "Early ASD Detection": detection.render,
    "Test Report": test_report.render,
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

# Universal Bottom Navigation Bar (on every page except Home)
if selected_page != "Home":
    st.markdown("<br><hr style='border: none; border-top: 1px solid #E2E8F0; margin: 25px 0 15px 0;'>", unsafe_allow_html=True)
    prev_target = st.session_state["nav_history"][-1] if st.session_state["nav_history"] else "Home"
    b_c1, b_c2, b_c3, b_spacer = st.columns([1.6, 1.6, 2.0, 4.8])
    with b_c1:
        if st.button(f"← Back ({prev_target})", key="global_bot_back"):
            dest = st.session_state["nav_history"].pop() if st.session_state["nav_history"] else "Home"
            st.session_state["nav_target"] = dest
            st.rerun()
    with b_c2:
        if st.button("Home", key="global_bot_home"):
            st.session_state["nav_target"] = "Home"
            st.rerun()
    with b_c3:
        if selected_page != "Early ASD Detection":
            if st.button("Early ASD Detection", key="global_bot_screener"):
                st.session_state["nav_target"] = "Early ASD Detection"
                st.rerun()
        else:
            if st.button("Clinical Test Report", key="global_bot_report"):
                st.session_state["nav_target"] = "Test Report"
                st.rerun()

# Global Footer
render_footer()
