import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    .block-container { max-width: 1200px; padding-top: 2rem; }
    [data-testid="stMetric"] { background:#fff; border:1px solid #e7e7e7; padding:18px; border-radius:14px; }
    </style>
    """, unsafe_allow_html=True)
