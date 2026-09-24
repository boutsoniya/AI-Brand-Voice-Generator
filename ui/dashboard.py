import streamlit as st
from database.repository import counts, recent_generations
from ui.styles import hero

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
