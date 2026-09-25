import streamlit as st
from core.content_generator import generate_content
from core.consistency_checker import check_consistency
from core.tts import synthesize_speech
from database.repository import save_generation, update_generation, update_generation_audio
from ui.styles import hero, section_kicker

CONTENT_TYPES = ["Instagram Post", "LinkedIn Post", "Marketing Email", "Ad Headline", "Tagline", "Blog Intro"]
QUICK_REFINES = {
    "✨ Warmer": "Make the language warmer, more human, and approachable.",
    "✂ Shorter": "Make this significantly shorter while preserving the key message.",
    "🔥 Punchier": "Make the opening stronger, punchier, and more memorable.",
    "😊 Friendlier": "Make the tone friendlier and more conversational.",
    "🎯 More persuasive": "Make the value proposition and CTA more persuasive without sounding pushy.",
    "💼 More professional": "Make the writing more polished and professional while keeping the brand personality.",
    "🧠 Clearer": "Simplify the language and make the message easier to understand.",
    "📱 Social-ready": "Make this feel native to social media with a stronger hook and easy-to-scan structure.",
}


def _save_current_generation():
    return save_generation(
        st.session_state.get("brand_id"),
        st.session_state.generated_type,
        st.session_state.generated_content,
        st.session_state.generated_result.overall_score,
    )


def _generate_and_check(client, profile, content_type, objective, audience, key_message, cta, length, creativity, refinement=None):
    content = generate_content(
        client, profile, content_type, objective, audience,
        key_message, cta, length, creativity, refinement
    )
    result = check_consistency(client, profile, content)
    return content, result


def render_generator(client):
    hero("Content Generator", "Create, compare, listen to, and refine marketing copy before publishing.")
    profile = st.session_state.get("brand_profile")
    if not profile:
        st.info("Start in Brand Voice Studio. Analyze 3–5 writing samples to create your Voice DNA.")
        if st.button("Go to Brand Voice Studio", type="primary"):
            st.session_state.page = "Brand Voice Studio"
            st.rerun()
        return

    brand = st.session_state.get("brand_name", "Active brand")
    section_kicker("Build your next piece")
    st.markdown("**Brief → Generate → Compare → Listen → Refine → Save**")
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
        st.caption("Use a higher setting when you want more variation, not a different brand voice.")

    g1, g2 = st.columns(2)
    with g1:
        generate_clicked = st.button("Create one draft", type="primary", use_container_width=True)
    with g2:
        variants_clicked = st.button("Create 3 options", use_container_width=True)

    if generate_clicked or variants_clicked:
        with st.spinner("Writing and checking against Voice DNA..."):
            if variants_clicked:
                directions = [
                    "Create a safe, highly on-brand version.",
                    "Create a fresher, more distinctive version while staying on-brand.",
                    "Create a concise, punchy version with a memorable opening.",
                ]
                variants = []
                for direction in directions:
                    text, check = _generate_and_check(
                        client, profile, content_type, objective, audience,
                        key_message, cta, length, creativity, direction
                    )
                    variants.append({"content": text, "result": check})
                st.session_state.generated_variants = variants
                chosen = variants[0]
                st.session_state.generated_content = chosen["content"]
                st.session_state.generated_result = chosen["result"]
            else:
                text, check = _generate_and_check(
                    client, profile, content_type, objective, audience,
                    key_message, cta, length, creativity
                )
                st.session_state.generated_variants = [{"content": text, "result": check}]
                st.session_state.generated_content = text
                st.session_state.generated_result = check

        st.session_state.generated_type = content_type
        st.session_state.voice_audio = None
        st.session_state.generation_id = _save_current_generation()
        st.success("Draft saved to History.")

    variants = st.session_state.get("generated_variants", [])
    if variants and len(variants) > 1:
        section_kicker("Choose a direction")
        labels = ["01 · Safe & on-brand", "02 · Fresh & distinctive", "03 · Short & punchy"]
        selected = st.radio(
            "Generated options",
            labels,
            horizontal=True,
            label_visibility="collapsed",
            key="variant_choice",
        )
        idx = labels.index(selected)
        chosen = variants[idx]
        if chosen["content"] != st.session_state.generated_content:
            st.session_state.generated_content = chosen["content"]
            st.session_state.generated_result = chosen["result"]
            st.session_state.generated_type = content_type
            st.session_state.voice_audio = None

    if not st.session_state.get("generated_content"):
        return

    content = st.session_state.generated_content
    result = st.session_state.generated_result

    st.divider()
    section_kicker("Draft workspace")
    st.subheader("Generated draft")
    st.caption("Your current draft is saved automatically. Edit it directly or use a quick refinement below.")

    edited = st.text_area(
        "Edit before publishing",
        content,
        height=240,
        key=f"generated_editor_{hash(content)}",
    )
    if edited != content:
        st.session_state.generated_content = edited
        generation_id = st.session_state.get("generation_id")
        if generation_id:
            update_generation(generation_id, edited, result.overall_score)

    actions = st.columns(4)
    with actions[0]:
        if st.button("📋 Copy-ready", use_container_width=True):
            st.info("Select the draft text above and copy it. Streamlit's browser sandbox does not expose clipboard access reliably.")
    with actions[1]:
        if st.button("✂ Shorter", use_container_width=True):
            st.session_state.quick_refine = QUICK_REFINES["✂ Shorter"]
    with actions[2]:
        if st.button("🔥 Punchier", use_container_width=True):
            st.session_state.quick_refine = QUICK_REFINES["🔥 Punchier"]
    with actions[3]:
        if st.button("😊 Friendlier", use_container_width=True):
            st.session_state.quick_refine = QUICK_REFINES["😊 Friendlier"]

    with st.expander("More quick refinements", expanded=False):
        q1, q2, q3, q4 = st.columns(4)
        for col, label in zip([q1, q2, q3, q4], ["✨ Warmer", "🎯 More persuasive", "💼 More professional", "🧠 Clearer"]):
            with col:
                if st.button(label, use_container_width=True):
                    st.session_state.quick_refine = QUICK_REFINES[label]
        q5, q6 = st.columns(2)
        with q5:
            if st.button("📱 Social-ready", use_container_width=True):
                st.session_state.quick_refine = QUICK_REFINES["📱 Social-ready"]
        with q6:
            if st.button("Custom instruction", use_container_width=True):
                st.session_state.show_custom_refine = True

    quick = st.session_state.pop("quick_refine", None)
    if quick:
        with st.spinner("Refining while preserving Voice DNA..."):
            refined, refined_result = _generate_and_check(
                client, profile, content_type, objective, audience,
                key_message, cta, length, creativity, quick
            )
        st.session_state.generated_content = refined
        st.session_state.generated_result = refined_result
        st.session_state.voice_audio = None
        st.session_state.generation_id = save_generation(
            st.session_state.get("brand_id"), content_type, refined, refined_result.overall_score
        )
        st.success("New refined version saved.")
        st.rerun()

    section_kicker("Hear it")
    st.markdown("**Voice preview**")
    st.caption("Generate an MP3 from the current draft. The audio is stored with this generation.")
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
                    st.session_state.get("brand_id"), content_type, edited, result.overall_score, audio
                )
            st.success("Voice preview ready.")
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

    with st.expander("Custom refinement", expanded=st.session_state.pop("show_custom_refine", False)):
        refinement = st.text_input(
            "What should change?",
            placeholder="e.g. Make it warmer, shorten the opening, and soften the CTA.",
        )
        if st.button("Regenerate with this direction", use_container_width=True):
            if not refinement.strip():
                st.warning("Describe the change you want first.")
            else:
                with st.spinner("Refining the draft while preserving Voice DNA..."):
                    refined, refined_result = _generate_and_check(
                        client, profile, content_type, objective, audience,
                        key_message, cta, length, creativity, refinement.strip()
                    )
                st.session_state.generated_content = refined
                st.session_state.generated_result = refined_result
                st.session_state.generated_type = content_type
                st.session_state.voice_audio = None
                st.session_state.generation_id = save_generation(
                    st.session_state.get("brand_id"), content_type, refined, refined_result.overall_score
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
