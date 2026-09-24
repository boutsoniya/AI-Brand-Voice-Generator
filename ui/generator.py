import streamlit as st
from core.content_generator import generate_content
from core.consistency_checker import check_consistency
from core.tts import synthesize_speech
from database.repository import save_generation, update_generation_audio
from ui.styles import hero

CONTENT_TYPES = ["Instagram Post", "LinkedIn Post", "Marketing Email", "Ad Headline", "Tagline", "Blog Intro"]


def _save_current_generation():
    return save_generation(
        st.session_state.get("brand_id"),
        st.session_state.generated_type,
        st.session_state.generated_content,
        st.session_state.generated_result.overall_score,
    )


def render_generator(client):
    hero("Content Generator", "Create, listen to, edit, and check marketing copy before publishing.")
    profile = st.session_state.get("brand_profile")
    if not profile:
        st.info("Start in Brand Voice Studio. Analyze 3–5 writing samples to create your Voice DNA.")
        if st.button("Go to Brand Voice Studio", type="primary"):
            st.session_state.page = "Brand Voice Studio"
            st.rerun()
        return

    brand = st.session_state.get("brand_name", "Active brand")
    st.markdown("**How it works:** 1. Set the brief → 2. Generate → 3. Listen & edit → 4. Check → 5. Save")
    st.caption(f"Active voice · {brand}")

    c1, c2 = st.columns(2)
    with c1:
        content_type = st.selectbox("Content type", CONTENT_TYPES)
        objective = st.text_input("Objective", "Launch a new product")
        audience = st.text_input("Target audience", "Young professionals")
        key_message = st.text_area("Key message", "Launching our new product today.", height=110)
    with c2:
        cta = st.text_input("Call to action", "Try it today.")
        length = st.select_slider("Length", ["Short", "Medium", "Long"], value="Medium")
        creativity = st.slider("Creativity", 1, 10, 6)
        st.caption("Higher creativity allows more variation while still passing the voice profile to the model.")

    if st.button("Generate & check", type="primary", use_container_width=True):
        with st.spinner("Writing and evaluating against Voice DNA..."):
            content = generate_content(client, profile, content_type, objective, audience, key_message, cta, length, creativity)
            result = check_consistency(client, profile, content)
        st.session_state.generated_content = content
        st.session_state.generated_result = result
        st.session_state.generated_type = content_type
        st.session_state.voice_audio = None
        st.session_state.generation_id = _save_current_generation()
        st.success("Draft generated and saved to History.")

    if not st.session_state.get("generated_content"):
        return

    content = st.session_state.generated_content
    result = st.session_state.generated_result
    st.divider()
    st.subheader("Generated draft")
    st.caption("Your draft is saved automatically. Edit it, create a voice preview, or refine it below.")

    edited = st.text_area(
        "Edit before publishing",
        content,
        height=240,
        key=f"generated_editor_{hash(content)}",
    )
    if edited != content:
        st.session_state.generated_content = edited

    st.markdown("**Voice preview**")
    st.caption("Generate an MP3 from the current draft. The preview is stored with this generation.")
    if st.button("🔊 Generate voice preview", use_container_width=True):
        try:
            with st.spinner("Creating voice preview..."):
                audio = synthesize_speech(edited)
            st.session_state.voice_audio = audio
            generation_id = st.session_state.get("generation_id")
            if generation_id:
                update_generation_audio(generation_id, audio)
            else:
                st.session_state.generation_id = save_generation(
                    st.session_state.get("brand_id"),
                    st.session_state.generated_type,
                    edited,
                    result.overall_score,
                    audio,
                )
            st.success("Voice preview created and saved.")
        except Exception as exc:
            st.error(f"Voice preview could not be created: {exc}")

    if st.session_state.get("voice_audio"):
        st.audio(st.session_state.voice_audio, format="audio/mp3")
        st.download_button(
            "Download voice preview",
            data=st.session_state.voice_audio,
            file_name=f"generation_{st.session_state.get('generation_id', 'preview')}.mp3",
            mime="audio/mpeg",
            use_container_width=True,
        )

    cols = st.columns(5)
    for col, (label, value) in zip(cols, [
        ("Overall", result.overall_score),
        ("Tone", result.tone_score),
        ("Vocabulary", result.vocabulary_score),
        ("Structure", result.structure_score),
        ("Audience", result.audience_fit),
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
                st.session_state.generated_type = content_type
                st.session_state.voice_audio = None
                st.session_state.generation_id = save_generation(
                    st.session_state.get("brand_id"),
                    content_type,
                    refined,
                    refined_result.overall_score,
                )
                st.success("Refined version saved as a new generation.")
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
            file_name=f"{st.session_state.generated_type.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with d2:
        if st.button("Open History", use_container_width=True):
            st.session_state.page = "History"
            st.rerun()
