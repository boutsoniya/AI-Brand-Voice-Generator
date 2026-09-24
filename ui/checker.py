import streamlit as st
from core.consistency_checker import check_consistency

def render_checker(client):
    st.title("Consistency Checker")
    st.caption("Evaluate existing copy against the active Brand Voice Profile.")
    profile = st.session_state.get("brand_profile")
    if not profile:
        st.info("Create a Brand Voice Profile first in Brand Voice Studio.")
        return
    content = st.text_area("Content to check", height=260, placeholder="Paste existing marketing copy here...")
    if st.button("Check Brand Consistency", type="primary", use_container_width=True):
        if not content.strip():
            st.error("Add some content to evaluate.")
            return
        with st.spinner("Checking voice consistency..."):
            result = check_consistency(client, profile, content)
        st.metric("Overall consistency", f"{result.overall_score}%")
        cols = st.columns(4)
        for col, (label, value) in zip(cols, [("Tone",result.tone_score),("Vocabulary",result.vocabulary_score),("Structure",result.structure_score),("Audience fit",result.audience_fit)]):
            col.metric(label, f"{value}%")
        left,right = st.columns(2)
        with left:
            st.markdown("#### Issues")
            for item in result.issues: st.warning(item)
        with right:
            st.markdown("#### Suggestions")
            for item in result.suggestions: st.success(item)
