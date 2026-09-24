import streamlit as st
from core.voice_analyzer import analyze_voice
from database.repository import save_brand

def render_brand_studio(client):
    st.title("Brand Voice Studio")
    st.caption("Give the system examples of how your brand already communicates.")
    name = st.text_input("Brand name", placeholder="e.g. Acme Coffee")
    description = st.text_area("Describe the brand", placeholder="What does the brand do and who is it for?")
    samples = st.text_area("Brand samples", height=260, placeholder="Paste 3-5 examples of posts, emails, taglines or website copy...")
    if st.button("Analyze Brand Voice", type="primary", use_container_width=True):
        if not samples.strip():
            st.error("Add at least one brand sample.")
            return
        with st.spinner("Analyzing writing patterns..."):
            profile = analyze_voice(client, samples)
        st.session_state.brand_profile = profile
        if name.strip():
            save_brand(name.strip(), description.strip(), profile)
        st.success("Brand Voice Profile created.")
        render_profile(profile)
    elif st.session_state.get("brand_profile"):
        st.divider()
        st.subheader("Current Voice Profile")
        render_profile(st.session_state.brand_profile)

def render_profile(profile):
    st.subheader("Voice DNA")
    cols = st.columns(5)
    for col, (label, value) in zip(cols, profile.tone.model_dump().items()):
        col.metric(label.title(), f"{value}/10")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Personality")
        st.write(", ".join(profile.personality))
        st.markdown("#### Preferred vocabulary")
        st.write(", ".join(profile.preferred_vocabulary))
        st.markdown("#### Writing patterns")
        for item in profile.preferred_patterns:
            st.write("• " + item)
    with right:
        st.markdown("#### Avoid")
        for item in profile.avoid:
            st.write("• " + item)
        st.markdown("#### Style")
        st.write(profile.sentence_style.model_dump())
        st.markdown("#### Voice summary")
        st.info(profile.summary)
