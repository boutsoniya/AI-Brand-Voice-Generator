import streamlit as st
from core.content_generator import generate_content
from core.consistency_checker import check_consistency
from database.repository import save_generation

def render_generator(client):
    st.title("Content Generator")
    profile = st.session_state.get("brand_profile")
    if not profile:
        st.info("Create a Brand Voice Profile first in Brand Voice Studio.")
        return
    st.caption("Using voice: " + profile.summary)
    c1,c2 = st.columns(2)
    with c1:
        content_type = st.selectbox("Content type", ["Instagram Post","LinkedIn Post","Marketing Email","Ad Headline","Tagline","Blog Intro"])
        objective = st.text_input("Objective", "Launch a new product")
        audience = st.text_input("Target audience", "Young professionals")
        key_message = st.text_area("Key message", "Launching our new product today.")
    with c2:
        cta = st.text_input("Call to action", "Try it today.")
        length = st.select_slider("Length", ["Short","Medium","Long"], value="Medium")
        creativity = st.slider("Creativity", 1, 10, 6)
    if st.button("Generate Content", type="primary", use_container_width=True):
        with st.spinner("Writing in your brand voice..."):
            content = generate_content(client, profile, content_type, objective, audience, key_message, cta, length, creativity)
            result = check_consistency(client, profile, content)
        st.session_state.generated_content = content
        st.session_state.generated_result = result
    if st.session_state.get("generated_content"):
        st.divider()
        st.subheader("Generated Content")
        st.text_area("Copy", st.session_state.generated_content, height=240)
        result = st.session_state.generated_result
        cols = st.columns(5)
        for col, (label, value) in zip(cols, [("Overall",result.overall_score),("Tone",result.tone_score),("Vocabulary",result.vocabulary_score),("Structure",result.structure_score),("Audience",result.audience_fit)]):
            col.metric(label, f"{value}%")
        if st.button("Save generation"):
            save_generation(None, content_type, st.session_state.generated_content, result.overall_score)
            st.success("Saved.")
