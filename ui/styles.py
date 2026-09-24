import streamlit as st


def inject_styles():
    st.markdown("""
    <style>
    :root {
        --paper: #F7F3EC;
        --paper-2: #EFE8DC;
        --ink: #25211D;
        --muted: #756E65;
        --line: #DED5C8;
        --card: #FFFCF7;
        --terracotta: #B85C43;
        --olive: #6D7657;
        --mustard: #C8943D;
        --blue: #5F7890;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--paper);
        color: var(--ink);
    }
    [data-testid="stHeader"] { background: rgba(247,243,236,.88); }
    .block-container { max-width: 1240px; padding: 2rem 2.2rem 5rem; }

    [data-testid="stSidebar"] {
        background: #EEE8DE;
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] .block-container { padding: 1.8rem 1.15rem 2rem; }
    [data-testid="stSidebar"] hr { border-color: #D7CEC1; }

    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 15px 17px;
        box-shadow: 0 2px 8px rgba(52,43,34,.04);
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 34px 34px 30px;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: var(--card);
        margin-bottom: 24px;
        box-shadow: 0 4px 18px rgba(52,43,34,.045);
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 150px; height: 150px;
        right: -45px; top: -55px;
        border: 28px solid rgba(184,92,67,.10);
        border-radius: 50%;
    }
    .eyebrow {
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .16em;
        text-transform: uppercase;
        color: var(--terracotta);
    }
    .hero h1 {
        margin: 7px 0 9px;
        font-size: 2.35rem;
        line-height: 1.05;
        letter-spacing: -.045em;
        color: var(--ink);
    }
    .hero p { color: var(--muted); margin:0; max-width:780px; font-size:1rem; line-height:1.6; }

    .card {
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 21px;
        background: var(--card);
        height: 100%;
        box-shadow: 0 3px 12px rgba(52,43,34,.035);
    }
    .card:hover {
        border-color: #C9B8A4;
        box-shadow: 0 7px 22px rgba(52,43,34,.07);
        transform: translateY(-1px);
        transition: .18s ease;
    }
    .card h3 { color: var(--ink); margin-top: 7px; }
    .muted { color: var(--muted); }
    .small-label {
        font-size:.72rem;
        color:var(--terracotta);
        text-transform:uppercase;
        letter-spacing:.11em;
        font-weight:800;
    }
    .section-kicker {
        display:inline-block;
        color:var(--olive);
        background:#E7E9DD;
        border-radius:999px;
        padding:5px 10px;
        font-size:.72rem;
        font-weight:750;
        letter-spacing:.04em;
        margin-bottom:8px;
    }
    .score-good { font-size:2.4rem; font-weight:750; letter-spacing:-.04em; }

    /* Inputs */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background: #FFFCF7 !important;
        border-color: #D8CEC0 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--terracotta) !important;
        box-shadow: 0 0 0 1px var(--terracotta) !important;
    }
    input, textarea, select { font-size:16px !important; }

    /* Buttons */
    div[data-testid="stButton"] > button,
    div[data-testid="stDownloadButton"] > button {
        border-radius: 8px;
        font-weight: 700;
        min-height: 44px;
        border: 1px solid #CFC3B4;
        background: #FFFCF7;
        color: var(--ink);
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: var(--terracotta);
        border-color: var(--terracotta);
        color: white;
    }
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        border-color: var(--terracotta);
        color: var(--terracotta);
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: #9F4D38;
        color: white;
    }

    /* Radio navigation */
    [data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
    [data-testid="stSidebar"] [role="radio"] {
        padding: 7px 10px;
        border-radius: 7px;
    }
    [data-testid="stSidebar"] [role="radio"]:hover { background:#E5DDD1; }

    button:focus-visible, input:focus-visible, textarea:focus-visible, select:focus-visible {
        outline:3px solid #C8943D !important;
        outline-offset:2px !important;
    }

    /* Alerts */
    [data-testid="stAlert"] { border-radius: 9px; border: 1px solid var(--line); }

    @media (max-width: 768px) {
        .block-container { padding:1.2rem 1rem 3rem; }
        .hero { padding:24px 21px; }
        .hero h1 { font-size:1.9rem; }
    }
    </style>
    """, unsafe_allow_html=True)


def hero(title, subtitle, eyebrow="BRAND VOICE WORKSPACE"):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{eyebrow}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def section_kicker(text):
    st.markdown(f'<div class="section-kicker">{text}</div>', unsafe_allow_html=True)
