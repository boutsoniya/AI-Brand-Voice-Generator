import streamlit as st


def inject_styles():
    st.markdown("""
    <style>
    :root {
        --canvas:#F3EFE7; --surface:#FBF8F1; --surface-2:#E8E1D5;
        --ink:#20211D; --muted:#756F66; --line:#D8D0C3;
        --tomato:#D45D45; --tomato-dark:#B84935; --moss:#657257;
        --mustard:#D6A746; --sidebar:#20231F;
    }
    html,body,[data-testid="stAppViewContainer"]{background:var(--canvas);color:var(--ink);}
    [data-testid="stHeader"]{background:rgba(243,239,231,.92);}
    .block-container{max-width:1280px;padding:1.5rem 2.2rem 5rem;}
    [data-testid="stSidebar"]{background:var(--sidebar);border-right:0;}
    [data-testid="stSidebar"] .block-container{padding:1.5rem 1rem 2rem;}
    [data-testid="stSidebar"] hr{border-color:#3B3E38;}
    [data-testid="stSidebar"] [role="radiogroup"]{gap:3px;}
    [data-testid="stSidebar"] [role="radio"]{padding:9px 11px;border-radius:6px;color:#D8D5CD;transition:.15s ease;}
    [data-testid="stSidebar"] [role="radio"]:hover{background:#30342E;}
    [data-testid="stSidebar"] [role="radio"][aria-checked="true"]{background:#F1ECE2;color:#20211D;font-weight:750;}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#9E9C94;}
    .brand-mark{display:flex;align-items:center;gap:10px;color:#F7F3EA;font-size:1.2rem;font-weight:800;letter-spacing:-.04em;}
    .brand-dot{width:11px;height:11px;background:var(--tomato);display:inline-block;border-radius:50%;box-shadow:7px 0 0 var(--mustard);}
    .hero{position:relative;overflow:hidden;min-height:185px;padding:31px 34px 29px;border:1px solid var(--line);border-radius:8px;background:var(--surface);margin-bottom:22px;box-shadow:0 7px 22px rgba(42,37,30,.045);}
    .hero:before{content:"";position:absolute;right:26px;bottom:-72px;width:190px;height:190px;border:1px solid #CFC5B6;border-radius:50%;box-shadow:0 0 0 24px #F6F1E8,0 0 0 25px #D8D0C3;opacity:.65;}
    .hero:after{content:"";position:absolute;right:65px;bottom:15px;width:38px;height:38px;background:var(--tomato);border-radius:3px;transform:rotate(12deg);opacity:.9;}
    .eyebrow{font-size:.69rem;font-weight:850;letter-spacing:.17em;text-transform:uppercase;color:var(--tomato);}
    .hero h1{position:relative;z-index:1;margin:7px 0 9px;max-width:850px;font-size:2.5rem;line-height:1.03;letter-spacing:-.052em;color:var(--ink);}
    .hero p{position:relative;z-index:1;color:var(--muted);margin:0;max-width:760px;font-size:1rem;line-height:1.6;}
    .card{position:relative;border:1px solid var(--line);border-radius:7px;padding:22px;background:var(--surface);height:100%;box-shadow:0 4px 13px rgba(42,37,30,.035);transition:.16s ease;}
    .card:hover{transform:translateY(-2px);border-color:#BFB4A4;box-shadow:0 10px 25px rgba(42,37,30,.08);}
    .card h3{color:var(--ink);margin:8px 0 7px;letter-spacing:-.025em;}
    .card p{line-height:1.55;}
    .card-accent{position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--tomato);}
    .card-accent.moss{background:var(--moss);}
    .small-label{font-size:.68rem;color:var(--tomato);text-transform:uppercase;letter-spacing:.13em;font-weight:850;}
    .muted{color:var(--muted);}
    .section-kicker{display:inline-block;color:var(--ink);background:var(--surface-2);border-left:3px solid var(--tomato);padding:5px 9px;font-size:.68rem;font-weight:850;letter-spacing:.07em;text-transform:uppercase;margin-bottom:8px;}
    [data-testid="stMetric"]{background:var(--surface);border:1px solid var(--line);border-radius:7px;padding:14px 16px;box-shadow:0 3px 10px rgba(42,37,30,.035);}
    [data-testid="stMetricLabel"]{color:var(--muted);}
    [data-testid="stMetricValue"]{color:var(--ink);letter-spacing:-.04em;}
    div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div,div[data-baseweb="select"]>div{background:var(--surface)!important;border-color:#CEC5B7!important;border-radius:6px!important;}
    div[data-baseweb="input"]>div:focus-within,div[data-baseweb="textarea"]>div:focus-within,div[data-baseweb="select"]>div:focus-within{border-color:var(--tomato)!important;box-shadow:0 0 0 1px var(--tomato)!important;}
    input,textarea,select{font-size:16px!important;}
    div[data-testid="stButton"]>button,div[data-testid="stDownloadButton"]>button{border-radius:6px;font-weight:750;min-height:44px;border:1px solid #C8BFB1;background:var(--surface);color:var(--ink);transition:.15s ease;}
    div[data-testid="stButton"]>button[kind="primary"]{background:var(--tomato);border-color:var(--tomato);color:white;}
    div[data-testid="stButton"]>button:hover,div[data-testid="stDownloadButton"]>button:hover{border-color:var(--tomato);color:var(--tomato-dark);transform:translateY(-1px);}
    div[data-testid="stButton"]>button[kind="primary"]:hover{background:var(--tomato-dark);color:white;}
    [data-testid="stAlert"]{border-radius:6px;border:1px solid var(--line);}
    [data-testid="stExpander"]{border:1px solid var(--line);border-radius:7px;background:var(--surface);}
    .workflow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:6px 0 18px;}
    .workflow span{padding:6px 10px;background:var(--surface);border:1px solid var(--line);font-size:.75rem;font-weight:750;}
    .workflow b{color:var(--tomato);font-size:.8rem;}
    button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid var(--mustard)!important;outline-offset:2px!important;}
    @media(max-width:768px){.block-container{padding:1rem 1rem 3rem}.hero{min-height:160px;padding:24px 21px}.hero h1{font-size:1.9rem}.hero:before,.hero:after{display:none}}
    </style>
    """, unsafe_allow_html=True)


def hero(title, subtitle, eyebrow="BRAND VOICE WORKSPACE"):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def section_kicker(text):
    st.markdown(f'<div class="section-kicker">{text}</div>', unsafe_allow_html=True)


def workflow(items):
    parts=[]
    for i,item in enumerate(items):
        parts.append(f"<span>{i+1:02d} &nbsp; {item}</span>")
        if i < len(items)-1:
            parts.append("<b>→</b>")
    st.markdown('<div class="workflow">'+''.join(parts)+'</div>', unsafe_allow_html=True)
