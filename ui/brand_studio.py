import streamlit as st
from core.voice_analyzer import analyze_voice
from database.repository import save_brand
from ui.styles import hero, section_kicker

def render_brand_studio(client):
    hero(
        "Brand Voice Studio",
        "Teach the system how your brand already writes. Use 3–5 representative samples for a more reliable profile.",
    )
    section_kicker("Step 1 · Tell us about the brand")
    name = st.text_input("Brand name", placeholder="e.g. Acme Coffee")
    description = st.text_area("Brand context", placeholder="What does the brand do, who is it for, and what should it feel like?", height=90)
    section_kicker("Step 2 · Show us how it writes")
    samples = st.text_area(
        "Writing samples",
        height=250,
        placeholder="Paste posts, emails, landing-page copy, taglines or campaign text. Separate different examples with a blank line.",
    )
    st.caption("Tip: mix social posts, emails, website copy and campaign lines for a stronger signal.")
    if st.button("Analyze & build Voice DNA", type="primary", use_container_width=True):
        if len(samples.strip()) < 80:
            st.error("Add a little more sample text (at least ~80 characters) so the analysis has enough signal.")
            return
        with st.spinner("Extracting the brand's writing patterns..."):
            profile = analyze_voice(client, samples)
        st.session_state.brand_profile = profile
        brand_name = name.strip() or "Untitled brand"
        st.session_state.brand_id = save_brand(brand_name, description.strip(), profile)
        st.session_state.brand_name = brand_name
        st.success("Voice DNA created. You can now generate or audit content.")
        render_profile(profile)
    elif st.session_state.get("brand_profile"):
        render_profile(st.session_state.brand_profile)

def render_profile(profile):
    st.divider()
    section_kicker("Your brand, distilled")
    st.subheader("Voice DNA")
    st.caption("A compact representation of how this brand should sound across channels.")
    cols = st.columns(5)
    labels = [("Formality","formality"),("Warmth","warmth"),("Confidence","confidence"),("Playfulness","playfulness"),("Technicality","technicality")]
    for col, (label, key) in zip(cols, labels):
        col.metric(label, f"{getattr(profile.tone, key)}/10")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Personality")
        st.write(" · ".join(profile.personality))
        st.markdown("#### Preferred vocabulary")
        st.write(" · ".join(profile.preferred_vocabulary))
        st.markdown("#### Patterns to repeat")
        for item in profile.preferred_patterns:
            st.write("• " + item)
    with right:
        st.markdown("#### Guardrails")
        for item in profile.avoid:
            st.write("• " + item)
        st.markdown("#### Sentence style")
        style = profile.sentence_style
        st.write(f"**Length:** {style.average_length}  ·  **Rhythm:** {style.rhythm}  ·  **Complexity:** {style.complexity}")
        st.markdown("#### Voice summary")
        st.info(profile.summary)
