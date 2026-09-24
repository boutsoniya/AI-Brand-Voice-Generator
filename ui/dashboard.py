import streamlit as st
from database.repository import counts, recent_generations, save_brand, list_brands, get_brand
from core.voice_analyzer import demo_profile
from ui.styles import hero
from models.voice_profile import VoiceProfile

def render_dashboard():
    hero(
        "Make every piece of content sound like the same brand.",
        "Analyze real writing samples once, turn them into a structured Voice DNA, then generate and audit new content against it.",
    )
    brands, generations = counts()
    a, b, c = st.columns(3)
    a.metric("Brand profiles", brands)
    b.metric("Generations", generations)
    c.metric("Voice dimensions", "5")

    st.caption("Learn the voice once. Generate consistently. Review before publishing.")
    st.write("")
    saved_brands = list_brands()
    if saved_brands:
        with st.container(border=True):
            st.markdown("**Saved brand voices**")
            options = {f"{row[1]} · {row[4]}": row[0] for row in saved_brands}
            selected = st.selectbox("Switch active Voice DNA", list(options.keys()), label_visibility="collapsed")
            if st.button("Load selected voice", use_container_width=True):
                brand = get_brand(options[selected])
                if brand:
                    st.session_state.brand_id = brand[0]
                    st.session_state.brand_name = brand[1]
                    st.session_state.brand_profile = VoiceProfile.model_validate(brand[3])
                    st.session_state.generated_content = None
                    st.session_state.generated_result = None
                    st.session_state.voice_audio = None
                    st.success(f"Loaded {brand[1]}.")
                    st.rerun()

    st.write("")
    x, y = st.columns(2)
    with x:
        st.markdown('<div class="card"><div class="small-label">01 · Learn</div><h3>Brand Voice Studio</h3><p class="muted">Paste existing posts, emails or website copy and extract tone, vocabulary, sentence style and guardrails.</p></div>', unsafe_allow_html=True)
        if st.button("Open Voice Studio →", use_container_width=True):
            st.session_state.page = "Brand Voice Studio"
            st.rerun()
    with y:
        st.markdown('<div class="card"><div class="small-label">02 · Create</div><h3>Content Generator</h3><p class="muted">Choose a channel, objective and audience. Generate copy while keeping the learned voice in context.</p></div>', unsafe_allow_html=True)
        if st.button("Open Generator →", use_container_width=True):
            st.session_state.page = "Content Generator"
            st.rerun()

    st.write("")
    with st.container(border=True):
        st.markdown("**Need a quick walkthrough?**")
        st.caption("Load a realistic demo brand in one click, then explore Voice DNA, generation and consistency checking without an API key.")
        if st.button("Load demo brand", use_container_width=True):
            profile = demo_profile()
            st.session_state.brand_profile = profile
            st.session_state.brand_name = "Northstar Coffee"
            st.session_state.brand_id = save_brand(
                "Northstar Coffee",
                "A modern coffee brand focused on simple rituals and better everyday moments.",
                profile,
            )
            st.session_state.page = "Brand Voice Studio"
            st.success("Demo brand loaded.")
            st.rerun()

    st.write("")
    st.subheader("Recent generations")
    rows = recent_generations()
    if not rows:
        st.caption("No generations yet. Create a voice profile to start.")
        return
    for _, brand, kind, content, score, created in rows:
        preview = content.replace("\n", " ")[:150]
        with st.container(border=True):
            left, right = st.columns([5,1])
            with left:
                st.markdown(f"**{kind}** · {brand}")
                st.caption(preview + ("…" if len(content) > 150 else ""))
            with right:
                st.metric("Score", f"{score or '—'}%")
