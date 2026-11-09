import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from textwrap import dedent

# ── Colour Tokens (Professional Clinical Palette) ────────────────────────
COLOR_BG         = "#F4F6F8"
COLOR_CARD       = "#FFFFFF"
COLOR_SIDEBAR    = "#14243A"
COLOR_ACCENT     = "#167C80"
COLOR_ACCENT_LT  = "#1A9599"
COLOR_TEXT_MAIN   = "#202B36"
COLOR_TEXT_MUTED  = "#667085"
COLOR_BORDER     = "#E3E8EE"
COLOR_HIGHLIGHT  = "#EDF4F4"
COLOR_SUCCESS    = "#059669"
COLOR_WARNING    = "#D97706"
COLOR_DANGER     = "#DC2626"


def inject_custom_css() -> None:
    """Injects the professional clinical design system CSS into Streamlit."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root, html, body, .stApp {
        --secondary-background-color: #FFFFFF !important;
        --background-color: #F4F6F8 !important;
        --text-color: #202B36 !important;
        --primary-color: #167C80 !important;
        --bg: #F4F6F8;
        --card: #FFFFFF;
        --sidebar: #14243A;
        --accent: #167C80;
        --accent-lt: #1A9599;
        --text-main: #202B36;
        --text-muted: #667085;
        --border: #E3E8EE;
        --highlight: #EDF4F4;
    }

    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
        background-color: #14243A !important;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        color: #202B36;
        font-size: 14px;
        font-weight: 400;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }

    /* ── Paragraph & Body Text (14–16px, comfortable line spacing) ───── */
    p, .main p, [data-testid="stMarkdownContainer"] p, .body-text, .med-card-body, .arch-desc {
        font-family: 'Inter', sans-serif !important;
        font-size: 14.5px !important;
        font-weight: 400 !important;
        line-height: 1.65 !important;
        color: #526071 !important;
        margin-top: 0 !important;
        margin-bottom: 12px !important;
    }

    /* Avoid excessively bold text — clean 600 weight for emphasis */
    strong, b, .main strong, .main b {
        font-weight: 600 !important;
        color: #202B36 !important;
    }

    /* ── Universal Main Content Text ──────────────────────────────────── */
    .stApp,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        color: #202B36 !important;
    }

    .main p, .main span, .main div, .main label, .main li,
    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] label,
    [data-testid="stMain"] li {
        color: #202B36 !important;
    }

    /* ── Form Widget Labels (MAIN) ────────────────────────────────────── */
    .main [data-testid="stWidgetLabel"],
    .main [data-testid="stWidgetLabel"] *,
    [data-testid="stMain"] [data-testid="stWidgetLabel"],
    [data-testid="stMain"] [data-testid="stWidgetLabel"] * {
        color: #202B36 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        opacity: 1 !important;
    }

    /* ── Radio Buttons (MAIN — detection wizard) ──────────────────────── */
    .main div[data-testid="stRadio"] div[role="radiogroup"] > label,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"],
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E3E8EE !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        margin: 4px 10px 6px 0 !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }

    .main div[data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"]:hover,
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        border-color: #167C80 !important;
        background-color: #EDF4F4 !important;
    }

    .main div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    .main div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"] p,
    .main div[data-testid="stRadio"] label[data-baseweb="radio"] span,
    .main div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
    .main .stRadio label p, .main .stRadio label span,
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    [data-testid="stMain"] div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"] p,
    [data-testid="stMain"] div[data-testid="stRadio"] label[data-baseweb="radio"] span,
    [data-testid="stMain"] div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        color: #202B36 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        opacity: 1 !important;
        line-height: 1.4 !important;
    }

    /* ── Sliders ──────────────────────────────────────────────────────── */
    .main .stSlider, .main .stSlider label, .main .stSlider label p,
    .main .stSlider div[data-baseweb="slider"], .main .stSlider span,
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] p {
        color: #202B36 !important;
        font-weight: 600 !important;
    }

    /* ── Text Inputs, Text Areas, Number & Date Inputs (Clean White & High Contrast) ── */
    div[data-testid="stTextInput"],
    div[data-testid="stTextArea"],
    div[data-testid="stNumberInput"],
    div[data-testid="stDateInput"],
    .stTextInput,
    .stTextArea,
    .stNumberInput,
    .stDateInput {
        margin-bottom: 8px !important;
        background-color: transparent !important;
    }

    div[data-testid="stTextInput"] div,
    div[data-testid="stTextInput"] div *,
    div[data-testid="stTextArea"] div,
    div[data-testid="stTextArea"] div *,
    div[data-testid="stNumberInput"] div,
    div[data-testid="stNumberInput"] div *,
    div[data-testid="stDateInput"] div,
    div[data-testid="stDateInput"] div *,
    .main div[data-baseweb="input"],
    .main div[data-baseweb="input"] *,
    .main div[data-baseweb="base-input"],
    .main div[data-baseweb="base-input"] *,
    .main div[data-baseweb="textarea"],
    .main div[data-baseweb="textarea"] * {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
    }

    div[data-testid="stTextInput"] [data-baseweb="input"],
    div[data-testid="stTextInput"] [data-baseweb="base-input"],
    div[data-testid="stTextArea"] [data-baseweb="textarea"],
    div[data-testid="stTextArea"] [data-baseweb="base-input"],
    div[data-testid="stNumberInput"] [data-baseweb="input"],
    div[data-testid="stDateInput"] [data-baseweb="input"] {
        border: 1.5px solid #C5D0DA !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        overflow: hidden !important;
    }

    div[data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
    div[data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
        border-color: #167C80 !important;
        box-shadow: 0 0 0 2px rgba(22, 124, 128, 0.2) !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    .main input,
    .main textarea,
    input[type="text"],
    input[type="number"],
    textarea {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #202B36 !important;
        -webkit-text-fill-color: #202B36 !important;
        caret-color: #202B36 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 8px 12px !important;
    }

    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder,
    .main input::placeholder,
    .main textarea::placeholder {
        color: #8899A6 !important;
        -webkit-text-fill-color: #8899A6 !important;
        font-weight: 400 !important;
    }

    /* ── Selectbox & Dropdowns (Clean White Background & Readable Text) ── */
    div[data-testid="stSelectbox"],
    div[data-testid="stSelectbox"] div,
    div[data-testid="stSelectbox"] div *,
    .main div[data-baseweb="select"],
    .main div[data-baseweb="select"] * {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #202B36 !important;
        -webkit-text-fill-color: #202B36 !important;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
        border: 1.5px solid #C5D0DA !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    div[data-testid="stSelectbox"] svg,
    div[data-baseweb="select"] svg {
        fill: #202B36 !important;
        color: #202B36 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] ul li {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #202B36 !important;
        -webkit-text-fill-color: #202B36 !important;
    }

    div[data-baseweb="popover"] ul li:hover,
    div[data-baseweb="popover"] ul li[aria-selected="true"] {
        background-color: #EDF4F4 !important;
        background: #EDF4F4 !important;
        color: #167C80 !important;
        -webkit-text-fill-color: #167C80 !important;
    }

    /* ── Dark Hero Banners & Precautions Banner Contrast Fix ──────────── */
    .main .precautions-hero-banner,
    .main .precautions-hero-banner *,
    .main div.precautions-hero-banner h1,
    .main div.precautions-hero-banner h2,
    .main div.precautions-hero-banner h3,
    .main div.precautions-hero-banner p,
    .main div.precautions-hero-banner span,
    .main div.precautions-hero-banner strong,
    div[class*="precautions-hero-banner"] h1,
    div[class*="precautions-hero-banner"] p,
    div[class*="precautions-hero-banner"] span,
    div[class*="precautions-hero-banner"] strong,
    .precautions-hero-banner,
    .precautions-hero-banner *,
    .precautions-hero-banner h1,
    .precautions-hero-banner h2,
    .precautions-hero-banner h3 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .main div.precautions-hero-banner p,
    .precautions-hero-banner p,
    .precautions-hero-banner div p {
        color: #E2E8F0 !important;
        -webkit-text-fill-color: #E2E8F0 !important;
    }
    .main div.precautions-hero-banner strong,
    .precautions-hero-banner strong {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .main div.precautions-hero-banner .hero-pill-badge,
    .precautions-hero-banner .hero-pill-badge,
    .precautions-hero-banner span.hero-pill-badge {
        color: #93C5FD !important;
        -webkit-text-fill-color: #93C5FD !important;
    }

    /* ── Headings Hierarchy (Publication-Grade Clinical Specs) ────────── */
    /* Main headings: 26–30px, semibold */
    h1, .main h1, .main-page-heading, .clinical-hero-title, .hero-title {
        font-family: 'Inter', sans-serif !important;
        font-size: 28px !important;
        font-weight: 600 !important;
        line-height: 1.25 !important;
        letter-spacing: -0.02em !important;
        color: #202B36 !important;
        margin: 0 0 12px 0 !important;
    }

    /* Section headings: 18–20px, semibold */
    h2, .main h2, h3, .main h3, .section-heading {
        font-family: 'Inter', sans-serif !important;
        font-size: 19px !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
        letter-spacing: -0.01em !important;
        color: #202B36 !important;
        margin: 0 0 10px 0 !important;
    }

    h4, .main h4 {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        color: #202B36 !important;
        margin: 0 0 6px 0 !important;
    }

    h5, .main h5, h6, .main h6 {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        color: #202B36 !important;
        margin: 0 0 4px 0 !important;
    }

    /* ── Overall Background ───────────────────────────────────────────── */
    .stApp {
        background: #F4F6F8;
    }

    /* ══════════════════════════════════════════════════════════════════════
       SIDEBAR
       ══════════════════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
        background: #14243A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Platform Navigation label */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {
        color: #5BA8AB !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 8px !important;
        opacity: 1 !important;
    }

    /* Sidebar nav container */
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div,
    [data-testid="stSidebar"] div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 10px !important;
        padding: 6px 4px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        gap: 2px !important;
    }

    /* Sidebar radio item base - perfect vertical centering of dot and label text */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label,
    [data-testid="stSidebar"] div[role="radiogroup"] > label,
    [data-testid="stSidebar"] label[data-baseweb="radio"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 6px !important;
        padding: 8px 14px !important;
        margin: 1px 0 !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        box-shadow: none !important;
    }

    /* Radio circle / dot container alignment - zero out any vertical offset */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child,
    [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child,
    [data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child,
    [data-testid="stSidebar"] div[role="radiogroup"] input + div,
    [data-testid="stSidebar"] label[data-baseweb="radio"] input + div {
        margin: 0 10px 0 0 !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
        align-self: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
        top: 0 !important;
        transform: none !important;
    }

    /* Radio label markdown container - vertically centered */
    [data-testid="stSidebar"] div[data-testid="stRadio"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label[data-baseweb="radio"] [data-testid="stMarkdownContainer"] {
        display: flex !important;
        align-items: center !important;
        align-self: center !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }

    /* Sidebar nav text — clean white, zero margin, vertically centered with dot */
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
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em !important;
        line-height: 1.25 !important;
        opacity: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        align-self: center !important;
    }

    /* Active sidebar navigation indicator — high-visibility clinical indicator */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked),
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] {
        background: rgba(22, 124, 128, 0.35) !important;
        border-left: 4px solid #167C80 !important;
        border-top: 1px solid rgba(22, 124, 128, 0.5) !important;
        border-right: 1px solid rgba(22, 124, 128, 0.5) !important;
        border-bottom: 1px solid rgba(22, 124, 128, 0.5) !important;
        border-radius: 6px !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25) !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) span,
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] p,
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
    }

    /* Inactive sidebar items */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:not(:has(input:checked)) p,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:not(:has(input:checked)) span {
        color: #B2BEC9 !important;
        font-weight: 500 !important;
    }

    /* Hover on sidebar items */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover,
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover,
    [data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        border-left: 4px solid rgba(22, 124, 128, 0.6) !important;
    }

    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* High-contrast radio dot indicator in sidebar - centered */
    [data-testid="stSidebar"] div[role="radiogroup"] input:checked + div,
    [data-testid="stSidebar"] div[role="radiogroup"] input:checked + div > div {
        background-color: #167C80 !important;
        border-color: #167C80 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        align-self: center !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] svg {
        fill: #167C80 !important;
        color: #167C80 !important;
    }

    /* Sidebar headings */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #FFFFFF !important;
    }

    /* ── Brand Badge ──────────────────────────────────────────────────── */
    .clinical-brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(22, 124, 128, 0.08);
        color: #167C80;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border: 1px solid rgba(22, 124, 128, 0.2);
        margin-bottom: 12px;
    }

    /* ── Hero Container (Solid Clinical Palette) ──────────────────────── */
    .hero-container {
        background: #14243A;
        border-radius: 8px;
        padding: 32px 36px;
        color: #FFFFFF;
        box-shadow: 0 1px 3px rgba(20, 36, 58, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 26px;
        font-weight: 700;
        line-height: 1.25;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 14px;
        font-weight: 400;
        line-height: 1.6;
        color: #C1CCD6;
        max-width: 820px;
        margin-bottom: 20px;
    }

    .hero-stats-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .hero-stat-item {
        background: rgba(255, 255, 255, 0.06);
        padding: 10px 18px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
    }

    .hero-stat-value {
        font-size: 20px;
        font-weight: 700;
        color: #5BA8AB;
    }

    .hero-stat-label {
        font-size: 12px;
        font-weight: 500;
        color: #C1CCD6;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Medical Cards ────────────────────────────────────────────────── */
    .med-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 22px;
        border: 1px solid #E3E8EE;
        box-shadow: none;
        transition: all 0.15s ease;
        margin-bottom: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .med-card:hover {
        box-shadow: 0 4px 16px rgba(32, 43, 54, 0.06);
        border-color: #C5D0DA;
    }

    .med-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }

    .med-card-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        background: #EDF4F4;
        border: 1px solid #D0E3E3;
    }

    .med-card-title {
        font-size: 17px;
        font-weight: 600;
        color: #202B36;
        margin-bottom: 6px;
    }

    .med-card-body {
        font-size: 14px;
        color: #667085;
        line-height: 1.6;
        flex-grow: 1;
    }

    /* ── Pill Badges ──────────────────────────────────────────────────── */
    .pill-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .pill-blue {
        background: #EDF4F4;
        color: #167C80;
    }

    .pill-purple {
        background: #EDF4F4;
        color: #14243A;
    }

    .pill-green {
        background: #D1FAE5;
        color: #065F46;
    }

    .pill-amber {
        background: #FEF3C7;
        color: #92400E;
    }

    /* ── Disclaimer Banner ────────────────────────────────────────────── */
    .disclaimer-banner {
        background: linear-gradient(90deg, #FEF2F2 0%, #FFFBEB 100%);
        border-left: 4px solid #EF4444;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 16px 0 24px 0;
        border-top: 1px solid #FEE2E2;
        border-right: 1px solid #FEE2E2;
        border-bottom: 1px solid #FEE2E2;
    }

    .disclaimer-title {
        font-size: 14px;
        font-weight: 700;
        color: #991B1B;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }

    .disclaimer-text {
        font-size: 13px;
        color: #7F1D1D;
        line-height: 1.5;
        margin: 0;
    }

    /* ── Streamlit Metric (Specs: 28–32px bold value, 11–12px label) ── */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 16px 20px;
        border-radius: 10px;
        border: 1px solid #E3E8EE;
        box-shadow: none;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 11.5px !important;
        font-weight: 500 !important;
        color: #667085 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        line-height: 1.35 !important;
    }

    [data-testid="stMetricValue"],
    .metric-value-swiss,
    .metric-value {
        font-family: 'Inter', sans-serif !important;
        font-size: 30px !important;
        font-weight: 700 !important;
        line-height: 1.15 !important;
        letter-spacing: -0.02em !important;
        color: #167C80 !important;
        margin-bottom: 4px !important;
    }

    /* ── Buttons (Enterprise Clinical Spec) ───────────────────────────── */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 8px 18px !important;
        transition: all 0.15s ease !important;
        border: 1px solid #E3E8EE !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Primary buttons: Dark navy #14243A background with pure white #FFFFFF text */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"],
    button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        background-color: #14243A !important;
        border: 1px solid #14243A !important;
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="stBaseButton-primary"] *,
    button[kind="primary"] *,
    button[data-testid="stBaseButton-primary"] *,
    button[kind="primary"] p,
    button[kind="primary"] span,
    button[kind="primary"] div,
    [data-testid="stBaseButton-primary"] p,
    [data-testid="stBaseButton-primary"] span,
    [data-testid="stBaseButton-primary"] div {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover,
    button[kind="primary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        background-color: #167C80 !important;
        border-color: #167C80 !important;
        box-shadow: 0 2px 8px rgba(22, 124, 128, 0.25) !important;
    }

    .stButton > button[kind="primary"]:hover *,
    .stButton > button[data-testid="stBaseButton-primary"]:hover *,
    button[kind="primary"]:hover *,
    button[data-testid="stBaseButton-primary"]:hover * {
        color: #FFFFFF !important;
    }

    /* Secondary buttons: Crisp white card background with dark text */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"],
    button[kind="secondary"],
    button[data-testid="stBaseButton-secondary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E3E8EE !important;
        color: #202B36 !important;
    }

    .stButton > button[kind="secondary"] *,
    .stButton > button[data-testid="stBaseButton-secondary"] *,
    button[kind="secondary"] *,
    button[data-testid="stBaseButton-secondary"] *,
    button[kind="secondary"] p,
    button[kind="secondary"] span,
    [data-testid="stBaseButton-secondary"] p,
    [data-testid="stBaseButton-secondary"] span {
        color: #202B36 !important;
        font-weight: 500 !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover,
    button[kind="secondary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #F4F6F8 !important;
        border-color: #167C80 !important;
    }

    .stButton > button[kind="secondary"]:hover *,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover *,
    button[kind="secondary"]:hover *,
    button[data-testid="stBaseButton-secondary"]:hover * {
        color: #167C80 !important;
    }

    /* ── Tabs ─────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #F4F6F8;
        padding: 4px;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        color: #667085;
        border: none;
        font-size: 14px;
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #167C80 !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
        font-weight: 600;
    }

    /* ── Progress Bars ────────────────────────────────────────────────── */
    .domain-meter-container {
        background: #E3E8EE;
        border-radius: 9999px;
        height: 8px;
        width: 100%;
        overflow: hidden;
        margin: 6px 0 12px 0;
    }

    .domain-meter-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.5s ease;
    }

    /* ── Wizard Stepper ───────────────────────────────────────────────── */
    .stepper-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border: 1px solid #E3E8EE;
        border-radius: 10px;
        padding: 12px 20px;
        margin-bottom: 20px;
        overflow-x: auto;
    }

    .step-node {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 600;
        color: #667085;
        white-space: nowrap;
    }

    .step-node.active {
        color: #167C80;
    }

    .step-circle {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F4F6F8;
        color: #667085;
        font-size: 12px;
        font-weight: 700;
    }

    .step-node.active .step-circle {
        background: #167C80;
        color: #FFFFFF;
        box-shadow: 0 0 0 3px rgba(22, 124, 128, 0.15);
    }

    .step-node.completed .step-circle {
        background: #059669;
        color: #FFFFFF;
    }

    /* ── Printable Report ─────────────────────────────────────────────── */
    .printable-report {
        background: #FFFFFF;
        border: 1px solid #E3E8EE;
        border-radius: 10px;
        padding: 32px 36px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        color: #202B36;
        font-family: 'Inter', -apple-system, sans-serif;
        margin-bottom: 24px;
    }

    .report-header-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 2px solid #167C80;
        padding-bottom: 16px;
        margin-bottom: 20px;
    }

    .report-table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0 18px 0;
        font-size: 14px;
    }

    .report-table th {
        background: #F4F6F8;
        color: #202B36;
        font-weight: 600;
        text-align: left;
        padding: 10px 14px;
        border-bottom: 2px solid #E3E8EE;
    }

    .report-table td {
        padding: 9px 14px;
        border-bottom: 1px solid #E3E8EE;
        color: #202B36;
    }

    .report-table tr:hover {
        background: #F4F6F8;
    }

    /* ── Print Stylesheet ─────────────────────────────────────────────── */
    @media print {
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        .stButton, .no-print,
        header, footer, .clinical-footer {
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

    /* ══════════════════════════════════════════════════════════════════════
       SWISS CLINICAL LAYOUT CLASSES
       ══════════════════════════════════════════════════════════════════════ */
    .clinical-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0 14px 0;
        margin-bottom: 12px;
        border-bottom: 1px solid #E3E8EE;
        flex-wrap: wrap;
        gap: 10px;
    }

    .clinical-breadcrumbs {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
    }

    .crumb-root {
        font-weight: 700;
        color: #202B36;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .crumb-sep { color: #C5D0DA; font-weight: 400; }

    .crumb-current { color: #667085; font-weight: 500; }

    .protocol-pills-group {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }

    .protocol-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 500;
    }

    .protocol-pill-teal {
        background: #EDF4F4;
        border: 1px solid #D0E3E3;
        color: #167C80;
    }

    .protocol-pill-teal .pill-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #167C80;
        display: inline-block;
    }

    .protocol-pill-slate {
        background: #F4F6F8;
        border: 1px solid #E3E8EE;
        color: #667085;
    }

    /* Decision Support Banner */
    .decision-support-banner {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 8px;
        padding: 12px 16px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 20px;
    }

    .decision-banner-icon { font-size: 1.1rem; line-height: 1.2; }
    .decision-banner-content { font-size: 13px; color: #92400E; line-height: 1.5; }
    .decision-banner-title { font-weight: 700; letter-spacing: 0.02em; margin-right: 4px; text-transform: uppercase; }

    /* Hero Card */
    .clinical-hero-card {
        background: #FFFFFF;
        border: 1px solid #E3E8EE;
        border-radius: 10px;
        padding: 22px 26px;
        margin-bottom: 20px;
    }

    .clinical-hero-title {
        font-size: 26px;
        font-weight: 700;
        color: #202B36 !important;
        letter-spacing: -0.02em;
        line-height: 1.25;
        margin: 0 0 8px 0;
    }

    .clinical-hero-desc {
        font-size: 14px;
        color: #667085 !important;
        line-height: 1.55;
        margin: 0;
        max-width: 860px;
    }

    /* Swiss Metric Cards */
    .metric-card-swiss {
        background: #FFFFFF;
        border: 1px solid #E3E8EE;
        border-radius: 8px;
        padding: 16px 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .metric-label-swiss {
        font-size: 12px;
        font-weight: 500;
        color: #667085;
        text-transform: capitalize;
        margin-bottom: 6px;
    }

    .metric-value-swiss {
        font-size: 30px;
        font-weight: 700;
        color: #202B36;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 6px;
    }

    .metric-meta-swiss {
        font-size: 12px;
        color: #667085;
    }

    /* Architecture Cards */
    .arch-card-swiss {
        background: #FFFFFF;
        border: 1px solid #E3E8EE;
        border-radius: 8px;
        padding: 18px 20px;
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
        font-size: 13px;
        font-weight: 700;
        color: #202B36;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .arch-badge-teal {
        background: #EDF4F4;
        border: 1px solid #D0E3E3;
        color: #167C80;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .arch-badge-blue {
        background: #EDF4F4;
        border: 1px solid #D0E3E3;
        color: #14243A;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .arch-desc {
        font-size: 13px;
        color: #667085 !important;
        line-height: 1.5;
        margin: 0 0 14px 0;
        flex-grow: 1;
    }

    .arch-stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        padding-top: 12px;
        border-top: 1px solid #E3E8EE;
    }

    .arch-stat-box { display: flex; flex-direction: column; }

    .arch-stat-lbl {
        font-size: 11px;
        color: #667085;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 2px;
    }

    .arch-stat-val {
        font-size: 15px;
        font-weight: 700;
        color: #202B36;
    }

    /* Section Bar */
    .section-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0 10px 0;
        margin: 24px 0 14px 0;
        border-bottom: 1px solid #E3E8EE;
        flex-wrap: wrap;
        gap: 8px;
    }

    .section-bar-title {
        font-size: 13px;
        font-weight: 700;
        color: #202B36;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .section-bar-badge {
        display: inline-flex;
        align-items: center;
        background: #F4F6F8;
        border: 1px solid #E3E8EE;
        color: #667085;
        font-size: 12px;
        font-weight: 500;
        padding: 2px 10px;
        border-radius: 9999px;
    }

    /* Footer */
    .clinical-footer {
        text-align: center;
        padding: 30px 20px 16px 20px;
        margin-top: 40px;
        border-top: 1px solid #E3E8EE;
        color: #667085;
        font-size: 13px;
    }

    /* ══════════════════════════════════════════════════════════════════════
       HAMBURGER SIDEBAR TOGGLE
       ══════════════════════════════════════════════════════════════════════ */

    /* Collapsed control */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    header [data-testid="collapsedControl"],
    header [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
    }

    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] button {
        background: #FFFFFF !important;
        border: 1px solid #E3E8EE !important;
        border-radius: 6px !important;
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 1px 4px rgba(32,43,54,0.08) !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        position: relative !important;
    }

    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background: #F4F6F8 !important;
        border-color: #C5D0DA !important;
    }

    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        display: none !important;
    }

    [data-testid="collapsedControl"] button::before,
    [data-testid="stSidebarCollapsedControl"] button::before {
        content: '' !important;
        display: block !important;
        width: 16px !important;
        height: 2px !important;
        background: #202B36 !important;
        border-radius: 1px !important;
        box-shadow: 0 -5px 0 0 #202B36, 0 5px 0 0 #202B36 !important;
        pointer-events: none !important;
    }

    [data-testid="collapsedControl"]::after,
    [data-testid="stSidebarCollapsedControl"]::after {
        display: none !important;
    }

    /* Sidebar close/toggle button (expanded) */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarHeader"] button,
    [data-testid="stSidebar"] button[kind="header"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 6px !important;
        width: 34px !important;
        height: 34px !important;
        min-width: 34px !important;
        min-height: 34px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        position: relative !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarHeader"] button:hover,
    [data-testid="stSidebar"] button[kind="header"]:hover {
        background: rgba(255,255,255,0.14) !important;
        border-color: rgba(255,255,255,0.25) !important;
    }

    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarHeader"] svg,
    [data-testid="stSidebar"] button[kind="header"] svg {
        display: none !important;
    }

    [data-testid="stSidebarCollapseButton"] button::before,
    [data-testid="stSidebarHeader"] button::before,
    [data-testid="stSidebar"] button[kind="header"]::before {
        content: '' !important;
        display: block !important;
        width: 14px !important;
        height: 2px !important;
        background: #FFFFFF !important;
        border-radius: 1px !important;
        box-shadow: 0 -4px 0 0 #FFFFFF, 0 4px 0 0 #FFFFFF !important;
        pointer-events: none !important;
    }

    /* ── Responsive Viewport Adjustments (Tablet & Mobile) ────────────── */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 2rem !important;
        }

        .clinical-top-bar {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 8px !important;
        }

        .protocol-pills-group {
            width: 100% !important;
        }

        .med-card {
            padding: 16px !important;
            margin-bottom: 12px !important;
        }

        .report-table {
            display: block !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
        }

        .stepper-container {
            padding: 10px 12px !important;
            gap: 10px !important;
        }

        .arch-stats-grid {
            grid-template-columns: 1fr !important;
            gap: 8px !important;
        }

        .clinical-hero-card {
            padding: 18px 20px !important;
        }

        .clinical-hero-title {
            font-size: 20px !important;
        }

        .metric-value-swiss {
            font-size: 24px !important;
        }
    }

    /* ══════════════════════════════════════════════════════════════════════
       PRECAUTIONS ROYAL BLUE HERO BANNER (PURE WHITE TEXT GUARANTEE)
       ══════════════════════════════════════════════════════════════════════ */
    .precautions-hero-banner,
    .precautions-hero-banner *,
    .precautions-hero-banner div,
    .precautions-hero-banner span,
    .precautions-hero-banner h1,
    .precautions-hero-banner h2,
    .precautions-hero-banner h3,
    .precautions-hero-banner p,
    .precautions-hero-banner strong,
    .precautions-hero-title,
    .precautions-hero-desc,
    .main .precautions-hero-banner,
    .main .precautions-hero-banner *,
    .main .precautions-hero-banner div,
    .main .precautions-hero-banner span,
    .main .precautions-hero-banner p,
    .main .precautions-hero-banner strong,
    [data-testid="stMain"] .precautions-hero-banner,
    [data-testid="stMain"] .precautions-hero-banner *,
    [data-testid="stMarkdownContainer"] .precautions-hero-banner,
    [data-testid="stMarkdownContainer"] .precautions-hero-banner * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    .precautions-hero-desc,
    .precautions-hero-banner .precautions-hero-desc,
    .precautions-hero-banner p,
    .main .precautions-hero-banner p {
        color: #E2E8F0 !important;
        -webkit-text-fill-color: #E2E8F0 !important;
    }

    .precautions-hero-banner .hero-pill-badge,
    .main .precautions-hero-banner .hero-pill-badge {
        color: #93C5FD !important;
        -webkit-text-fill-color: #93C5FD !important;
    }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_html(content: str) -> None:
    """Safely renders HTML using st.markdown or st.html."""
    if not content:
        return
    # When content contains <style> tags, always use st.markdown so DOMPurify does not strip or delay CSS
    if "<style" in str(content).lower():
        st.markdown(content, unsafe_allow_html=True)
        return
    if hasattr(st, "html"):
        st.html(content)
    else:
        cleaned_lines = [line.strip() for line in str(content).splitlines() if line.strip()]
        cleaned_html = " ".join(cleaned_lines)
        st.markdown(cleaned_html, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str | None = None, badge: str | None = None) -> None:
    """Renders a publication-grade clinical section header with the professional palette."""
    badge_html = f'<div class="clinical-brand-badge">{badge}</div>' if badge else ""
    subtitle_html = (
        f'<p style="color: #526071 !important; font-size: 14.5px; font-weight: 400; margin-top: 6px; '
        f'margin-bottom: 18px; line-height: 1.65;">{subtitle}</p>'
    ) if subtitle else ""
    html = f"""<div style="margin-bottom: 20px;">
{badge_html}
<h1 style="font-size: 28px; font-weight: 600; color: #202B36 !important; letter-spacing: -0.02em; line-height: 1.25; margin: 0 0 8px 0;">{title}</h1>
{subtitle_html}
</div>"""
    render_html(html)


def render_disclaimer() -> None:
    """Renders the standard healthcare AI clinical disclaimer banner."""
    html = """<div class="disclaimer-banner">
<div class="disclaimer-title"><span>&#9888;</span> RESEARCH & CLINICAL DECISION SUPPORT NOTICE</div>
<p class="disclaimer-text">
This system is an academic research platform designed for developmental risk stratification using machine learning and deep tabular networks.
It is <strong>not</strong> a certified diagnostic medical device and does <strong>not</strong> substitute for comprehensive multidisciplinary evaluation by pediatricians, child psychiatrists, or developmental specialists.
</p>
</div>"""
    render_html(html)


def render_footer() -> None:
    """Renders the modern platform footer."""
    html = """<div class="clinical-footer">
<p style="font-weight: 600; color: #202B36; margin-bottom: 4px;">
Interpretable Deep Learning for Early ASD Detection
</p>
<p style="margin: 0; color: #667085; font-size: 13px;">
Academic Clinical AI Research Initiative &bull; Powered by PyTorch TabNet & Multi-Layer Perceptrons &bull; Streamlit Cloud
</p>
</div>"""
    render_html(html)


def apply_chart_theme(fig, ax):
    """Applies standardized clinical styling to Matplotlib/Seaborn plots."""
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E3E8EE')
    ax.spines['bottom'].set_color('#E3E8EE')
    ax.spines['left'].set_linewidth(1.0)
    ax.spines['bottom'].set_linewidth(1.0)
    ax.tick_params(colors='#526071', labelsize=9, width=1.0)
    ax.grid(True, linestyle='--', alpha=0.35, color='#E3E8EE')
    ax.xaxis.label.set_color('#202B36')
    ax.xaxis.label.set_fontsize(10)
    ax.xaxis.label.set_weight('bold')
    ax.yaxis.label.set_color('#202B36')
    ax.yaxis.label.set_fontsize(10)
    ax.yaxis.label.set_weight('bold')
    return fig, ax
