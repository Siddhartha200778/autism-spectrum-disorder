import streamlit as st
import os

from modules.theme import inject_custom_css, render_footer, render_html
try:
    from modules.ml_pipeline import (
        load_default_dataset,
        preprocess_and_prepare,
        train_models_pipeline,
        get_benchmark_models_and_data
    )
except Exception as e:
    import traceback
    st.error(f"Module Import Error: {e}")
    st.code(traceback.format_exc())
    st.stop()

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

# Navigation Configuration matching Enterprise Clinical Research Platform
PAGES = [
    "Overview",
    "Early ASD Detection",
    "Clinical Test Report",
    "Dataset Management",
    "Model Evaluation",
    "Prediction Analysis",
    "Explainable AI",
    "Methodology",
    "About Research",
    "Clinical Contact"
]

NAV_ALIASES = {
    "Home": "Overview",
    "About Autism": "About Research",
    "Dataset Analysis": "Dataset Management",
    "AI Models": "Model Evaluation",
    "Model Comparison": "Prediction Analysis",
    "Results & Visualization": "Explainable AI",
    "Research Methodology": "Methodology",
    "About Us": "About Research",
    "Contact": "Clinical Contact"
}

PAGE_ICONS = {
    "Overview": "🏠",
    "Early ASD Detection": "🩺",
    "Clinical Test Report": "📄",
    "Dataset Management": "📊",
    "Model Evaluation": "🧠",
    "Prediction Analysis": "⚖️",
    "Explainable AI": "📈",
    "Methodology": "🔬",
    "About Research": "📘",
    "Clinical Contact": "📬"
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
    <div style="padding: 10px 0 16px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 18px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: #16324F; border: 1.5px solid rgba(255, 255, 255, 0.25); width: 38px; height: 38px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.05rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; box-shadow: 0 2px 8px rgba(0,0,0,0.25);">
                AS
            </div>
            <div>
                <div style="font-weight: 800; font-size: 0.88rem; color: #FFFFFF; letter-spacing: 0.03em; text-transform: uppercase;">
                    ASD TODDLER SCREENING
                </div>
                <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">
                    TabNet vs MLP &bull; v2.4 CLIN
                </div>
            </div>
        </div>
    </div>
    """)

    # Synchronize programmatic navigation (buttons) with sidebar radio
    if "nav_target" in st.session_state:
        target = st.session_state.pop("nav_target")
        target = NAV_ALIASES.get(target, target)
        if target in PAGES:
            st.session_state["nav_radio"] = target
    elif "nav_selection" in st.session_state:
        target = st.session_state.pop("nav_selection")
        target = NAV_ALIASES.get(target, target)
        if target in PAGES:
            st.session_state["nav_radio"] = target

    if "nav_radio" not in st.session_state or st.session_state["nav_radio"] not in PAGES:
        st.session_state["nav_radio"] = "Overview"

    selected_page = st.radio(
        "Platform Navigation",
        options=PAGES,
        key="nav_radio",
        format_func=lambda x: f"{PAGE_ICONS.get(x, '•')}  {x}"
    )
    st.session_state["active_page"] = selected_page

    # Sidebar Compute Environment Telemetry (Swiss Spec)
    st.markdown("<br>", unsafe_allow_html=True)
    if "models_result" in st.session_state:
        tab_acc = st.session_state["models_result"]["tabnet"]["accuracy"] * 100
        mlp_acc = st.session_state["models_result"]["mlp"]["accuracy"] * 100
        perf_extra = f"""
        <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #CBD5E1; margin-bottom: 6px;">
            <span style="color: #94A3B8;">TabNet Acc:</span>
            <span style="font-family: monospace; font-weight: 600; color: #38BDF8;">{tab_acc:.1f}%</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #CBD5E1; margin-bottom: 8px;">
            <span style="color: #94A3B8;">MLP Baseline:</span>
            <span style="font-family: monospace; font-weight: 600; color: #F1F5F9;">{mlp_acc:.1f}%</span>
        </div>
        """
    else:
        perf_extra = ""

    render_html(f"""
    <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 14px 16px; margin-top: 10px;">
        <div style="font-size: 0.7rem; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px;">
            COMPUTE ENVIRONMENT
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #CBD5E1; margin-bottom: 6px;">
            <span style="color: #94A3B8;">Torch Runtime:</span>
            <span style="font-family: monospace; font-weight: 600; color: #F1F5F9;">2.2.1+cpu</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #CBD5E1; margin-bottom: 6px;">
            <span style="color: #94A3B8;">TabNet Engine:</span>
            <span style="font-family: monospace; font-weight: 600; color: #F1F5F9;">py-tabnet 4.1</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #CBD5E1; margin-bottom: 8px;">
            <span style="color: #94A3B8;">Validation Split:</span>
            <span style="font-family: monospace; font-weight: 600; color: #F1F5F9;">5-Fold Strat</span>
        </div>
        {perf_extra}
        <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 8px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #10B981; box-shadow: 0 0 6px rgba(16,185,129,0.5);"></span>
                <span style="font-size: 0.74rem; color: #10B981; font-weight: 700;">Validated Pipeline</span>
            </div>
            <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">N=1,054</span>
        </div>
    </div>
    """)

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
    st.session_state["current_page_tracked"] = "Overview"

if selected_page != st.session_state["current_page_tracked"]:
    old_p = st.session_state["current_page_tracked"]
    if not st.session_state["nav_history"] or st.session_state["nav_history"][-1] != old_p:
        st.session_state["nav_history"].append(old_p)
    st.session_state["current_page_tracked"] = selected_page

# Universal Top Navigation Bar (on every page except Overview/Home)
if selected_page not in ("Overview", "Home"):
    prev_target = st.session_state["nav_history"][-1] if st.session_state["nav_history"] else "Overview"
    top_c1, top_c2, top_c3, top_spacer = st.columns([1.6, 1.6, 1.8, 5.0])
    with top_c1:
        if st.button(f"⬅️ Back ({prev_target})", key="global_top_back", help=f"Return to {prev_target}"):
            dest = st.session_state["nav_history"].pop() if st.session_state["nav_history"] else "Overview"
            st.session_state["nav_target"] = dest
            st.rerun()
    with top_c2:
        if st.button("🏠 Overview", key="global_top_home", help="Navigate to Overview page"):
            st.session_state["nav_target"] = "Overview"
            st.rerun()
    with top_c3:
        if selected_page != "Early ASD Detection":
            if st.button("🩺 Early Detection", key="global_top_screener", help="Open ASD Screener"):
                st.session_state["nav_target"] = "Early ASD Detection"
                st.rerun()
        else:
            if st.button("📄 Test Report", key="global_top_report", help="Open Clinical Test Report"):
                st.session_state["nav_target"] = "Clinical Test Report"
                st.rerun()
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

# Page Router
PAGE_ROUTERS = {
    "Overview": home.render,
    "Home": home.render,
    "Early ASD Detection": detection.render,
    "Clinical Test Report": test_report.render,
    "Dataset Management": dataset_analysis.render,
    "Dataset Analysis": dataset_analysis.render,
    "Model Evaluation": models.render,
    "AI Models": models.render,
    "Prediction Analysis": comparison.render,
    "Model Comparison": comparison.render,
    "Explainable AI": results.render,
    "Results & Visualization": results.render,
    "Methodology": methodology.render,
    "Research Methodology": methodology.render,
    "About Research": about_asd.render,
    "About Autism": about_asd.render,
    "About Us": about_us.render,
    "Clinical Contact": contact.render,
    "Contact": contact.render
}

render_fn = PAGE_ROUTERS.get(selected_page, home.render)
render_fn()

# Universal Bottom Navigation Bar (on every page except Overview/Home)
if selected_page not in ("Overview", "Home"):
    st.markdown("<br><hr style='border: none; border-top: 1px solid #E2E8F0; margin: 25px 0 15px 0;'>", unsafe_allow_html=True)
    prev_target = st.session_state["nav_history"][-1] if st.session_state["nav_history"] else "Overview"
    b_c1, b_c2, b_c3, b_spacer = st.columns([1.6, 1.6, 2.0, 4.8])
    with b_c1:
        if st.button(f"⬅️ Go Back ({prev_target})", key="global_bot_back"):
            dest = st.session_state["nav_history"].pop() if st.session_state["nav_history"] else "Overview"
            st.session_state["nav_target"] = dest
            st.rerun()
    with b_c2:
        if st.button("🏠 Return to Overview", key="global_bot_home"):
            st.session_state["nav_target"] = "Overview"
            st.rerun()
    with b_c3:
        if selected_page != "Early ASD Detection":
            if st.button("🩺 Early ASD Detection", key="global_bot_screener"):
                st.session_state["nav_target"] = "Early ASD Detection"
                st.rerun()
        else:
            if st.button("📄 Clinical Test Report", key="global_bot_report"):
                st.session_state["nav_target"] = "Clinical Test Report"
                st.rerun()

# Global Footer
render_footer()
