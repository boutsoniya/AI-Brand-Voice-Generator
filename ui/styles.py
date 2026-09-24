import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    .block-container { max-width: 1280px; padding: 2.2rem 2rem 4rem; }
    [data-testid="stSidebar"] { border-right: 1px solid #e8ebef; }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }
    [data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e5e7eb; padding: 16px 18px;
        border-radius: 14px; box-shadow: 0 1px 2px rgba(0,0,0,.03);
    }
    .hero {
        padding: 26px 28px; border: 1px solid #e5e7eb; border-radius: 18px;
        background: linear-gradient(135deg,#ffffff 0%,#f8fafc 100%);
        margin-bottom: 22px;
    }
    .eyebrow { font-size: .76rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color:#64748b; }
    .hero h1 { margin: 6px 0 8px; font-size: 2.25rem; letter-spacing: -.04em; }
    .hero p { color:#64748b; margin:0; max-width:760px; font-size:1rem; }
    .card {
        border:1px solid #e5e7eb; border-radius:16px; padding:20px;
        background:#fff; height:100%;
    }
    .muted { color:#64748b; }
    .score-good { font-size:2.4rem; font-weight:750; letter-spacing:-.04em; }
    .small-label { font-size:.78rem; color:#64748b; text-transform:uppercase; letter-spacing:.08em; font-weight:700; }
    div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button { border-radius:10px; font-weight:650; min-height:44px; }
    input, textarea, select { font-size:16px !important; }
    button:focus-visible, input:focus-visible, textarea:focus-visible, select:focus-visible { outline:3px solid #94a3b8 !important; outline-offset:2px !important; }
    @media (max-width: 768px) { .block-container { padding:1.2rem 1rem 3rem; } .hero { padding:20px; } .hero h1 { font-size:1.8rem; } }
    </style>
    """, unsafe_allow_html=True)

def hero(title, subtitle, eyebrow="BRAND VOICE WORKSPACE"):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{eyebrow}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )
