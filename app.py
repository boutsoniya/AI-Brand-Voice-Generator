import streamlit as st
from dotenv import load_dotenv
from config.settings import APP_NAME
from core.gemini_client import GeminiClient
from database.db import init_db
from database.repository import latest_brand
from models.voice_profile import VoiceProfile
from ui.styles import inject_styles
from ui.dashboard import render_dashboard
from ui.brand_studio import render_brand_studio
from ui.generator import render_generator
from ui.checker import render_checker
from ui.history import render_history

load_dotenv()
init_db()
st.set_page_config(page_title=APP_NAME, page_icon="✦", layout="wide")
inject_styles()

for key, default in {
    "page": "Dashboard",
    "brand_profile": None,
    "brand_id": None,
    "brand_name": "Demo workspace",
    "generated_content": None,
    "generated_result": None,
    "generated_type": "Instagram Post",
    "check_result": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Restore the latest saved brand after a refresh or new Streamlit session.
if st.session_state.brand_profile is None:
    saved_brand = latest_brand()
    if saved_brand:
        saved_id, saved_name, _description, saved_profile = saved_brand
        st.session_state.brand_id = saved_id
        st.session_state.brand_name = saved_name
        st.session_state.brand_profile = VoiceProfile.model_validate(saved_profile)

with st.sidebar:
    st.markdown('<div class="brand-mark"><span class="brand-dot"></span>BrandVoice</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.68rem;color:#9E9C94;letter-spacing:.13em;text-transform:uppercase;margin-top:8px;">Creative voice studio</div>', unsafe_allow_html=True)
    st.divider()
    pages = ["Dashboard", "Brand Voice Studio", "Content Generator", "Consistency Checker", "History"]
    page = st.radio("Workspace", pages, index=pages.index(st.session_state.page))
    st.session_state.page = page
    st.divider()
    if st.session_state.brand_profile:
        st.markdown("**Active voice**")
        st.caption(st.session_state.brand_name)
        st.markdown('<div style="color:#9AC28F;font-size:.78rem;font-weight:750;">● Voice DNA ready</div>', unsafe_allow_html=True)
    else:
        st.caption("No voice profile loaded")
    st.divider()
    st.caption("Gemini · Streamlit · Pydantic · SQLite")

client = GeminiClient()

if page == "Dashboard":
    render_dashboard()
elif page == "Brand Voice Studio":
    render_brand_studio(client)
elif page == "Content Generator":
    render_generator(client)
elif page == "Consistency Checker":
    render_checker(client)
else:
    render_history()
