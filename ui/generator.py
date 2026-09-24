import streamlit as st
from core.content_generator import generate_content
from core.consistency_checker import check_consistency
from database.repository import save_generation
from ui.styles import hero

CONTENT_TYPES = ["Instagram Post","LinkedIn Post","Marketing Email","Ad Headline","Tagline","Blog Intro"]

def render_generator(client):
    hero("Content Generator", "Turn a campaign brief into ready-to-edit copy without losing the brand's learned voice.")
    profile = st.session_state.get("brand_profile")
    if not profile:
        st.info("Create a Brand Voice Profile first in Brand Voice Studio.")
        return

    brand = st.session_state.get("brand_name", "Active brand")
    st.caption(f"Active voice · {brand}")
    c1, c2 = st.columns(2)
    with c1:
        content_type = st.selectbox("Content type", CONTENT_TYPES)
        objective = st.text_input("Objective", "Launch a new product")
        audience = st.text_input("Target audience", "Young professionals")
        key_message = st.text_area("Key message", "Launching our new product today.", height=110)
    with c2:
        cta = st.text_input("Call to action", "Try it today.")
        length = st.select_slider("Length", ["Short","Medium","Long"], value="Medium")
        creativity = st.slider("Creativity", 1, 10, 6)
        st.caption("Higher creativity allows more variation while still passing the voice profile to the model.")

    if st.button("Generate & check", type="primary", use_container_width=True):
        with st.spinner("Writing and evaluating against Voice DNA..."):
            content = generate_content(client, profile, content_type, objective, audience, key_message, cta, length, creativity)
            result = check_consistency(client, profile, content)
        st.session_state.generated_content = content
        st.session_state.generated_result = result
        st.session_state.generated_type = content_type

    if st.session_state.get("generated_content"):
        content = st.session_state.generated_content
        result = st.session_state.generated_result
        st.divider()
        st.subheader("Generated draft")
        edited = st.text_area("Edit before publishing", content, height=240, key="generated_editor")
        st.session_state.generated_content = edited

        cols = st.columns(5)
        for col, (label, value) in zip(cols, [
            ("Overall", result.overall_score), ("Tone", result.tone_score),
            ("Vocabulary", result.vocabulary_score), ("Structure", result.structure_score),
            ("Audience", result.audience_fit)
        ]):
            col.metric(label, f"{value}%")

        with st.expander("Refine this draft", expanded=False):
            refinement = st.text_input(
                "What should change?",
                placeholder="e.g. Make it warmer, shorten the opening, and make the CTA softer.",
            )
            if st.button("Regenerate with this direction", use_container_width=True):
                if not refinement.strip():
                    st.warning("Describe the change you want first.")
                else:
                    with st.spinner("Refining the draft while preserving Voice DNA..."):
                        refined = generate_content(
                            client, profile, content_type, objective, audience,
                            key_message, cta, length, creativity, refinement.strip()
                        )
                        refined_result = check_consistency(client, profile, refined)
                    st.session_state.generated_content = refined
                    st.session_state.generated_result = refined_result
                    st.rerun()

        left, right = st.columns(2)
        with left:
            st.markdown("#### What to improve")
            for item in result.issues:
                st.warning(item)
        with right:
            st.markdown("#### Keep in mind")
            for item in result.suggestions:
                st.success(item)

        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "Download as .txt",
                data=edited,
                file_name=f"{st.session_state.generated_type.lower().replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with d2:
            if st.button("Save to history", use_container_width=True):
                save_generation(st.session_state.get("brand_id"), st.session_state.generated_type, edited, result.overall_score)
                st.success("Saved to generation history.")
