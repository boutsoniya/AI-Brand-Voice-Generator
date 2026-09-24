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
    st.markdown("## ✦ BrandVoice")
    st.caption("A practical brand intelligence workspace")
    st.divider()
    pages = ["Dashboard", "Brand Voice Studio", "Content Generator", "Consistency Checker"]
    page = st.radio("Workspace", pages, index=pages.index(st.session_state.page))
    st.session_state.page = page
    st.divider()
    if st.session_state.brand_profile:
        st.markdown("**Active voice**")
        st.caption(st.session_state.brand_name)
        st.success("Voice DNA ready")
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
else:
    render_checker(client)
