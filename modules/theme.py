import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from textwrap import dedent

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

    /* Universal High-Contrast Main Content Text Rules */
    .stApp,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        color: #0F172A !important;
    }

    /* Force all text elements in the main body to be deep navy/slate */
    .main p,
    .main span,
    .main div,
    .main label,
    .main li,
    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] label,
    [data-testid="stMain"] li {
        color: #0F172A !important;
    }

    /* All form widget labels, titles, and text in MAIN container */
    .main [data-testid="stWidgetLabel"],
    .main [data-testid="stWidgetLabel"] *,
    .main [data-testid="stWidgetLabel"] p,
    .main [data-testid="stWidgetLabel"] span,
    .main label[data-testid="stWidgetLabel"],
    [data-testid="stMain"] [data-testid="stWidgetLabel"],
    [data-testid="stMain"] [data-testid="stWidgetLabel"] * {
        color: #0A192F !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    /* Radio button option cards & question text (MAIN CONTAINER ONLY) */
    .main div[data-testid="stRadio"] div[role="radiogroup"] > label,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"],
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        margin: 4px 10px 6px 0 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        cursor: pointer !important;
    }

    .main div[data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"]:hover,
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        border-color: #1D4ED8 !important;
        background-color: #EFF6FF !important;
        transform: translateY(-1px) !important;
    }

    .main div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    .main div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"] p,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"] span,
    .main div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
    .main .stRadio label p,
    .main .stRadio label span,
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"] p,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"] span,
    [data-testid="stMain"] div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        color: #0A192F !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
        line-height: 1.4 !important;
    }

    /* Slider labels and values */
    .main .stSlider,
    .main .stSlider label,
    .main .stSlider label p,
    .main .stSlider div[data-baseweb="slider"],
    .main .stSlider span,
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] p {
        color: #0A192F !important;
        font-weight: 700 !important;
    }

    /* Dropdown/Selectbox labels and text */
    .main .stSelectbox,
    .main .stSelectbox label,
    .main .stSelectbox label p,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #0A192F !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] ul li {
        background-color: #FFFFFF !important;
        color: #0A192F !important;
    }
    div[data-baseweb="popover"] ul li:hover {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
    }

    /* Headings in main body */
    h1, h2, h3, h4, h5, h6,
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #0A192F !important;
        font-weight: 800 !important;
    }

    /* Overall Background */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F0F7FF 50%, #F8FAFC 100%);
    }

    /* ========================================================
       SIDEBAR & LEFT NAVIGATION HIGH-CONTRAST STYLING
       ======================================================== */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071326 0%, #0B192C 60%, #151A30 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    }

    /* "Platform Navigation" Header Label in Sidebar */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {
        color: #60A5FA !important;
        font-size: 0.78rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 8px !important;
        opacity: 1 !important;
    }

    /* Sidebar Navigation Menu Container */
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div,
    [data-testid="stSidebar"] div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
        padding: 8px 6px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        gap: 3px !important;
    }

    /* Sidebar Radio Item Button Base */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label,
    [data-testid="stSidebar"] div[role="radiogroup"] > label,
    [data-testid="stSidebar"] label[data-baseweb="radio"] {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 9px 14px !important;
        margin: 2px 0 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        box-shadow: none !important;
    }

    /* Sidebar Navigation Item Text - Luminous Pure White for maximum legibility */
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stRadio label *,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label *,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label span,
    [data-testid="stSidebar"] div[role="radiogroup"] label,
    [data-testid="stSidebar"] div[role="radiogroup"] label *,
    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label span,
    [data-testid="stSidebar"] div[role="radiogroup"] > label p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label span,
    [data-testid="stSidebar"] label[data-baseweb="radio"] p,
    [data-testid="stSidebar"] label[data-baseweb="radio"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        opacity: 1 !important;
    }

    /* Active / Selected Sidebar Item */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked),
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(29, 78, 216, 0.45) 0%, rgba(37, 99, 235, 0.35) 100%) !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) span {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Hover effect on sidebar items: royal blue glow with pure white bold text */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover,
    [data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
        background: rgba(37, 99, 235, 0.28) !important;
        border-color: rgba(96, 165, 250, 0.45) !important;
        transform: translateX(4px) !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover span {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Radio dot icon in sidebar */
    [data-testid="stSidebar"] div[role="radiogroup"] svg {
        fill: #60A5FA !important;
    }

    /* Sidebar general text headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #FFFFFF !important;
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
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 9px 18px !important;
        transition: all 0.18s ease !important;
        border: 1px solid #CBD5E1 !important;
    }

    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background-color: #16324F !important;
        border-color: #16324F !important;
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background-color: #1E3A5F !important;
        border-color: #1E3A5F !important;
        box-shadow: 0 4px 12px rgba(22, 50, 79, 0.25) !important;
        transform: translateY(-1px) !important;
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

    /* ========================================================
       SWISS CLINICAL RESEARCH PLATFORM DESIGN SYSTEM (SPEC 2.4)
       ======================================================== */
    .clinical-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0 16px 0;
        margin-bottom: 12px;
        border-bottom: 1px solid #E2E8F0;
        flex-wrap: wrap;
        gap: 12px;
    }

    .clinical-breadcrumbs {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.82rem;
    }

    .crumb-root {
        font-weight: 800;
        color: #1E293B;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .crumb-sep {
        color: #94A3B8;
        font-weight: 400;
    }

    .crumb-current {
        color: #64748B;
        font-weight: 600;
    }

    .protocol-pills-group {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .protocol-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .protocol-pill-teal {
        background: #F0FDFA;
        border: 1px solid #CCFBF1;
        color: #0F766E;
    }

    .protocol-pill-teal .pill-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #0D9488;
        display: inline-block;
    }

    .protocol-pill-slate {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #475569;
    }

    /* Decision Support Amber Banner */
    .decision-support-banner {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 8px;
        padding: 12px 18px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 22px;
    }

    .decision-banner-icon {
        font-size: 1.15rem;
        line-height: 1.2;
    }

    .decision-banner-content {
        font-size: 0.81rem;
        color: #92400E;
        line-height: 1.5;
    }

    .decision-banner-title {
        font-weight: 800;
        letter-spacing: 0.02em;
        margin-right: 4px;
        text-transform: uppercase;
    }

    /* Enterprise Clinical Hero Card */
    .clinical-hero-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px 28px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        margin-bottom: 22px;
    }

    .clinical-hero-title {
        font-size: 1.68rem;
        font-weight: 800;
        color: #16324F !important;
        letter-spacing: -0.02em;
        line-height: 1.25;
        margin: 0 0 8px 0;
    }

    .clinical-hero-desc {
        font-size: 0.92rem;
        color: #475569 !important;
        line-height: 1.55;
        margin: 0;
        max-width: 860px;
    }

    /* Swiss Metric Cards */
    .metric-card-swiss {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .metric-label-swiss {
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748B;
        text-transform: capitalize;
        margin-bottom: 6px;
    }

    .metric-value-swiss {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 8px;
    }

    .metric-meta-swiss {
        font-size: 0.74rem;
        color: #64748B;
    }

    /* Architecture Benchmark Cards */
    .arch-card-swiss {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px 22px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .arch-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .arch-title {
        font-size: 0.82rem;
        font-weight: 800;
        color: #0F172A;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .arch-badge-teal {
        background: #CCFBF1;
        border: 1px solid #99F6E4;
        color: #0F766E;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .arch-badge-blue {
        background: #E0F2FE;
        border: 1px solid #BAE6FD;
        color: #0369A1;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .arch-desc {
        font-size: 0.83rem;
        color: #475569 !important;
        line-height: 1.5;
        margin: 0 0 16px 0;
        flex-grow: 1;
    }

    .arch-stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        padding-top: 14px;
        border-top: 1px solid #F1F5F9;
    }

    .arch-stat-box {
        display: flex;
        flex-direction: column;
    }

    .arch-stat-lbl {
        font-size: 0.68rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 2px;
    }

    .arch-stat-val {
        font-size: 0.96rem;
        font-weight: 800;
        color: #0F172A;
    }

    /* Section Bar */
    .section-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 12px 0;
        margin: 28px 0 16px 0;
        border-bottom: 1px solid #E2E8F0;
        flex-wrap: wrap;
        gap: 8px;
    }

    .section-bar-title {
        font-size: 0.86rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .section-bar-badge {
        display: inline-flex;
        align-items: center;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #475569;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 9999px;
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

def render_html(content):
    """Safely renders HTML using st.html (or fallback to st.markdown) without treating indentation as code."""
    if not content:
        return
    if hasattr(st, "html"):
        st.html(content)
    else:
        cleaned_lines = [line.strip() for line in str(content).splitlines() if line.strip()]
        cleaned_html = " ".join(cleaned_lines)
        st.markdown(cleaned_html, unsafe_allow_html=True)

def render_section_header(title, subtitle=None, badge=None):
    """Renders a consistent, high-impact clinical section header."""
    badge_html = f'<div class="clinical-brand-badge">{badge}</div>' if badge else ""
    subtitle_html = f'<p style="color: #475569 !important; font-size: 1.05rem; margin-top: 4px; margin-bottom: 24px; line-height: 1.5;">{subtitle}</p>' if subtitle else ""
    html = f"""<div style="margin-bottom: 16px;">
{badge_html}
<h2 style="font-size: 1.9rem; font-weight: 800; color: #0A192F !important; letter-spacing: -0.02em; margin: 0;">{title}</h2>
{subtitle_html}
</div>"""
    render_html(html)

def render_disclaimer():
    """Renders the standard healthcare AI clinical disclaimer banner."""
    html = """<div class="disclaimer-banner">
<div class="disclaimer-title"><span>⚠️</span> RESEARCH & CLINICAL DECISION SUPPORT NOTICE</div>
<p class="disclaimer-text">
This system is an academic research platform designed for developmental risk stratification using machine learning and deep tabular networks. 
It is <strong>not</strong> a certified diagnostic medical device and does <strong>not</strong> substitute for comprehensive multidisciplinary evaluation by pediatricians, child psychiatrists, or developmental specialists.
</p>
</div>"""
    render_html(html)

def render_footer():
    """Renders the modern platform footer."""
    html = """<div class="clinical-footer">
<p style="font-weight: 600; color: #0F172A; margin-bottom: 4px;">
Interpretable Deep Learning for Early ASD Detection
</p>
<p style="margin: 0; color: #64748B; font-size: 0.82rem;">
Academic Clinical AI Research Initiative &bull; Powered by PyTorch TabNet & Multi-Layer Perceptrons &bull; Streamlit Cloud
</p>
</div>"""
    render_html(html)

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
