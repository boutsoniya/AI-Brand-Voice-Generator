import streamlit as st
from core.consistency_checker import check_consistency
from ui.styles import hero, section_kicker

def render_checker(client):
    hero("Consistency Checker", "Review existing copy before publishing. The checker compares it against the active Voice DNA.")
    profile = st.session_state.get("brand_profile")
    if not profile:
        st.info("Create a Brand Voice Profile first in Brand Voice Studio.")
        return

    section_kicker("Paste what you want to review")
    content = st.text_area("Content to check", height=260, placeholder="Paste a LinkedIn post, email, ad, landing page section or other copy...")
    if st.button("Check brand consistency", type="primary", use_container_width=True):
        if not content.strip():
            st.error("Add some content to evaluate.")
            return
        with st.spinner("Comparing tone, vocabulary, structure and audience fit..."):
            result = check_consistency(client, profile, content)
        st.session_state.check_result = result

    result = st.session_state.get("check_result")
    if result:
        st.divider()
        section_kicker("Voice audit")
        st.subheader("Consistency report")
        st.metric("Overall consistency", f"{result.overall_score}%")
        cols = st.columns(4)
        for col, (label, value) in zip(cols, [
            ("Tone", result.tone_score), ("Vocabulary", result.vocabulary_score),
            ("Structure", result.structure_score), ("Audience fit", result.audience_fit)
        ]):
            col.metric(label, f"{value}%")
        left, right = st.columns(2)
        with left:
            st.markdown("#### Issues")
            if result.issues:
                for item in result.issues: st.warning(item)
            else:
                st.success("No major issues detected.")
        with right:
            st.markdown("#### Suggestions")
            for item in result.suggestions: st.success(item)
