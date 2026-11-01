import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Primary Color Constants
COLOR_NAVY = "#0A192F"
COLOR_NAVY_LIGHT = "#1E293B"
COLOR_ROYAL = "#1D4ED8"
COLOR_ROYAL_LIGHT = "#3B82F6"
COLOR_PURPLE = "#7C3AED"
COLOR_PURPLE_LIGHT = "#A855F7"
COLOR_BG_LIGHT = "#F0F7FF"
COLOR_BG_ALT = "#F8FAFC"
COLOR_CARD_BORDER = "#E2E8F0"
COLOR_TEXT_MAIN = "#0F172A"
COLOR_TEXT_MUTED = "#64748B"
COLOR_SUCCESS = "#059669"
COLOR_WARNING = "#D97706"
COLOR_DANGER = "#DC2626"

def inject_custom_css():
    """Injects modern, healthcare-grade AI design system CSS into Streamlit."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-navy: #0A192F;
        --royal-blue: #1D4ED8;
        --royal-blue-light: #2563EB;
        --soft-purple: #7C3AED;
        --light-blue-bg: #F0F7FF;
        --slate-bg: #F8FAFC;
        --border-color: #E2E8F0;
        --text-primary: #0F172A;
        --text-secondary: #475569;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }

    /* Overall Background */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F0F7FF 50%, #F8FAFC 100%);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A192F 0%, #0F172A 70%, #1E1B4B 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }

    /* Sidebar Radio Buttons */
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    [data-testid="stSidebar"] .stRadio label {
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.25s ease;
        margin-bottom: 2px;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(59, 130, 246, 0.15);
        color: #FFFFFF !important;
        transform: translateX(4px);
    }

    /* Header & Branding Containers */
    .clinical-brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(29, 78, 216, 0.1);
        color: #1D4ED8;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border: 1px solid rgba(29, 78, 216, 0.25);
        margin-bottom: 12px;
    }

    .hero-container {
        background: linear-gradient(135deg, #0A192F 0%, #1E3A8A 55%, #312E81 100%);
        border-radius: 20px;
        padding: 44px 40px;
        color: #FFFFFF;
        box-shadow: 0 20px 40px -15px rgba(10, 25, 47, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }

    .hero-container::after {
        content: "";
        position: absolute;
        top: -40%;
        right: -20%;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(124, 58, 237, 0.35) 0%, rgba(37, 99, 235, 0) 70%);
        pointer-events: none;
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        line-height: 1.25;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin-bottom: 14px;
    }

    .hero-subtitle {
        font-size: 1.12rem;
        font-weight: 400;
        line-height: 1.6;
        color: #CBD5E1;
        max-width: 820px;
        margin-bottom: 24px;
    }

    .hero-stats-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        margin-top: 24px;
        padding-top: 24px;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
    }

    .hero-stat-item {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(8px);
        padding: 12px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        display: flex;
        flex-direction: column;
    }

    .hero-stat-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: #93C5FD;
    }

    .hero-stat-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #E2E8F0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Medical Cards */
    .med-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .med-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px -6px rgba(15, 23, 42, 0.09);
        border-color: #93C5FD;
    }

    .med-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
    }

    .med-card-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.35rem;
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
    }

    .med-card-title {
        font-size: 1.18rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 8px;
    }

    .med-card-body {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.6;
        flex-grow: 1;
    }

    /* Pill Badges */
    .pill-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .pill-blue {
        background: #DBEAFE;
        color: #1E40AF;
    }

    .pill-purple {
        background: #F3E8FF;
        color: #6B21A8;
    }

    .pill-green {
        background: #D1FAE5;
        color: #065F46;
    }

    .pill-amber {
        background: #FEF3C7;
        color: #92400E;
    }

    /* Medical Disclaimer Banner */
    .disclaimer-banner {
        background: linear-gradient(90deg, #FEF2F2 0%, #FFFBEB 100%);
        border-left: 5px solid #EF4444;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 20px 0 30px 0;
        border-top: 1px solid #FEE2E2;
        border-right: 1px solid #FEE2E2;
        border-bottom: 1px solid #FEE2E2;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.05);
    }

    .disclaimer-title {
        font-size: 0.98rem;
        font-weight: 700;
        color: #991B1B;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    .disclaimer-text {
        font-size: 0.88rem;
        color: #7F1D1D;
        line-height: 1.5;
        margin: 0;
    }

    /* Streamlit Metric Customization */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 18px 20px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #1D4ED8 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 22px;
        transition: all 0.2s ease;
        border: none;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(29, 78, 216, 0.25);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
        color: #475569;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1D4ED8 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    /* Clinical Progress & Meter Bars */
    .domain-meter-container {
        background: #E2E8F0;
        border-radius: 9999px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin: 6px 0 12px 0;
    }

    .domain-meter-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.6s ease;
    }

    /* Step-by-Step Wizard Stepper */
    .stepper-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 14px 22px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        overflow-x: auto;
    }

    .step-node {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.84rem;
        font-weight: 700;
        color: #64748B;
        white-space: nowrap;
    }

    .step-node.active {
        color: #1D4ED8;
    }

    .step-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F1F5F9;
        color: #475569;
        font-size: 0.82rem;
        font-weight: 800;
    }

    .step-node.active .step-circle {
        background: #1D4ED8;
        color: #FFFFFF;
        box-shadow: 0 0 0 4px rgba(29, 78, 216, 0.2);
    }

    .step-node.completed .step-circle {
        background: #059669;
        color: #FFFFFF;
    }

    /* Official Printable Report Styling */
    .printable-report {
        background: #FFFFFF;
        border: 2px solid #CBD5E1;
        border-radius: 16px;
        padding: 36px 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        color: #0F172A;
        font-family: 'Inter', -apple-system, sans-serif;
        margin-bottom: 30px;
    }

    .report-header-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid #1D4ED8;
        padding-bottom: 18px;
        margin-bottom: 22px;
    }

    .report-table {
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0 20px 0;
        font-size: 0.92rem;
    }

    .report-table th {
        background: #F1F5F9;
        color: #0F172A;
        font-weight: 700;
        text-align: left;
        padding: 10px 14px;
        border-bottom: 2px solid #CBD5E1;
    }

    .report-table td {
        padding: 9px 14px;
        border-bottom: 1px solid #E2E8F0;
        color: #334155;
    }

    .report-table tr:hover {
        background: #F8FAFC;
    }

    /* Print Stylesheet */
    @media print {
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        .stButton,
        .no-print,
        header,
        footer,
        .clinical-footer {
            display: none !important;
        }

        body, .stApp {
            background: #FFFFFF !important;
            color: #000000 !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .printable-report {
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
        }

        .report-header-banner {
            border-bottom: 2px solid #000000 !important;
        }

        .med-card {
            box-shadow: none !important;
            border: 1px solid #CCCCCC !important;
            page-break-inside: avoid;
        }
    }

    /* Footer */
    .clinical-footer {
        text-align: center;
        padding: 35px 20px 20px 20px;
        margin-top: 50px;
        border-top: 1px solid #E2E8F0;
        color: #64748B;
        font-size: 0.86rem;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_section_header(title, subtitle=None, badge=None):
    """Renders a consistent, high-impact clinical section header."""
    badge_html = f'<div class="clinical-brand-badge">{badge}</div>' if badge else ""
    subtitle_html = f'<p style="color: #64748B; font-size: 1.05rem; margin-top: 4px; margin-bottom: 24px; line-height: 1.5;">{subtitle}</p>' if subtitle else ""
    
    st.markdown(f"""
    <div style="margin-bottom: 16px;">
        {badge_html}
        <h2 style="font-size: 1.9rem; font-weight: 800; color: #0A192F; letter-spacing: -0.02em; margin: 0;">
            {title}
        </h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def render_disclaimer():
    """Renders the standard healthcare AI clinical disclaimer banner."""
    st.markdown("""
    <div class="disclaimer-banner">
        <div class="disclaimer-title">
            <span>⚠️</span> RESEARCH & CLINICAL DECISION SUPPORT NOTICE
        </div>
        <p class="disclaimer-text">
            This system is an academic research platform designed for developmental risk stratification using machine learning and deep tabular networks. 
            It is <strong>not</strong> a certified diagnostic medical device and does <strong>not</strong> substitute for comprehensive multidisciplinary evaluation by pediatricians, child psychiatrists, or developmental specialists.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Renders the modern platform footer."""
    st.markdown("""
    <div class="clinical-footer">
        <p style="font-weight: 600; color: #0F172A; margin-bottom: 4px;">
            Interpretable Deep Learning for Early ASD Detection
        </p>
        <p style="margin: 0; color: #64748B; font-size: 0.82rem;">
            Academic Clinical AI Research Initiative &bull; Powered by PyTorch TabNet & Multi-Layer Perceptrons &bull; Streamlit Cloud
        </p>
    </div>
    """, unsafe_allow_html=True)

def apply_chart_theme(fig, ax):
    """Applies modern styling to Matplotlib/Seaborn plots."""
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    ax.tick_params(colors='#475569', labelsize=9)
    ax.grid(True, linestyle='--', alpha=0.35, color='#CBD5E1')
    ax.xaxis.label.set_color('#0F172A')
    ax.xaxis.label.set_fontsize(10)
    ax.xaxis.label.set_weight('bold')
    ax.yaxis.label.set_color('#0F172A')
    ax.yaxis.label.set_fontsize(10)
    ax.yaxis.label.set_weight('bold')
    return fig, ax
