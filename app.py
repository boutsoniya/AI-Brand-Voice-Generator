import streamlit as st
from dotenv import load_dotenv
from config.settings import APP_NAME
from core.gemini_client import GeminiClient
from database.db import init_db
from ui.styles import inject_styles
from ui.dashboard import render_dashboard
from ui.brand_studio import render_brand_studio
from ui.generator import render_generator
from ui.checker import render_checker

load_dotenv()
init_db()
st.set_page_config(page_title=APP_NAME, page_icon="✦", layout="wide")
inject_styles()

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "brand_profile" not in st.session_state:
    st.session_state.brand_profile = None

with st.sidebar:
    st.markdown("## ✦ BrandVoice")
    st.caption("AI brand consistency workspace")
    pages = ["Dashboard","Brand Voice Studio","Content Generator","Consistency Checker"]
    page = st.radio("Workspace", pages, index=pages.index(st.session_state.page))
    st.session_state.page = page
    st.divider()
    st.caption("Powered by Gemini • Streamlit")

client = GeminiClient()

if page == "Dashboard": render_dashboard()
elif page == "Brand Voice Studio": render_brand_studio(client)
elif page == "Content Generator": render_generator(client)
else: render_checker(client)
