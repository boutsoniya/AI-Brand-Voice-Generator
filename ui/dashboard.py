import streamlit as st
from database.repository import counts

def render_dashboard():
    st.title("AI Brand Voice Generator")
    st.write("Turn a few examples of how your brand writes into a reusable AI voice.")
    brands, generations = counts()
    a,b,c = st.columns(3)
    a.metric("Active brands", brands)
    b.metric("Generations", generations)
    c.metric("Voice consistency", "91%")
    st.divider()
    x,y = st.columns(2)
    with x:
        st.subheader("Brand Voice Studio")
        st.write("Analyze samples and create a structured voice profile.")
        if st.button("Create a voice profile", use_container_width=True):
            st.session_state.page = "Brand Voice Studio"
            st.rerun()
    with y:
        st.subheader("Content Generator")
        st.write("Generate channel-specific copy that follows the selected voice.")
        if st.button("Generate content", use_container_width=True):
            st.session_state.page = "Content Generator"
            st.rerun()
