import streamlit as st
from database.repository import list_generations, get_brand
from models.voice_profile import VoiceProfile
from ui.styles import hero, section_kicker


def render_history():
    hero(
        "Generation History",
        "Every saved draft and voice preview stays available here so you can revisit, compare, and reuse previous work.",
    )
    rows = list_generations(100)
    if not rows:
        st.info("No saved generations yet. Create your first draft in Content Generator.")
        if st.button("Open Content Generator", type="primary"):
            st.session_state.page = "Content Generator"
            st.rerun()
        return

    section_kicker("Find past work")
    search = st.text_input("Search history", placeholder="Search by brand, content type, or copy...")
    brand_names = ["All brands"] + sorted({str(row[2]) for row in rows})
    brand_filter = st.selectbox("Brand", brand_names, label_visibility="collapsed")
    filtered = rows

    if search.strip():
        q = search.lower()
        filtered = [
            row for row in filtered
            if q in str(row[2]).lower()
            or q in str(row[3]).lower()
            or q in str(row[4]).lower()
        ]
    if brand_filter != "All brands":
        filtered = [row for row in filtered if str(row[2]) == brand_filter]

    st.caption(f"{len(filtered)} saved generation(s)")

    for row_id, brand_id, brand, kind, content, score, audio_blob, created in filtered:
        with st.container(border=True):
            top = st.columns([4, 1])
            with top[0]:
                st.markdown(f"**{kind}** · {brand}")
                st.caption(str(created))
            with top[1]:
                st.metric("Score", f"{score or '—'}%")

            st.write(content)

            actions = st.columns([1, 1, 1, 2])
            with actions[0]:
                if st.button("Use this", key=f"use_{row_id}", use_container_width=True):
                    brand_row = get_brand(brand_id) if brand_id else None
                    if brand_row:
                        st.session_state.brand_id = brand_row[0]
                        st.session_state.brand_name = brand_row[1]
                        st.session_state.brand_profile = VoiceProfile.model_validate(brand_row[3])
                    st.session_state.generated_content = content
                    st.session_state.generated_type = kind
                    st.session_state.generated_result = None
                    st.session_state.voice_audio = audio_blob
                    st.session_state.generation_id = row_id
                    st.session_state.page = "Content Generator"
                    st.rerun()

            with actions[1]:
                st.download_button(
                    "Download text",
                    data=content,
                    file_name=f"generation_{row_id}.txt",
                    mime="text/plain",
                    key=f"download_text_{row_id}",
                    use_container_width=True,
                )

            with actions[2]:
                if audio_blob:
                    st.download_button(
                        "Download MP3",
                        data=audio_blob,
                        file_name=f"generation_{row_id}.mp3",
                        mime="audio/mpeg",
                        key=f"download_audio_{row_id}",
                        use_container_width=True,
                    )
                else:
                    st.caption("No audio")

            with actions[3]:
                if audio_blob:
                    st.audio(audio_blob, format="audio/mp3")
                else:
                    st.caption("No voice preview saved for this generation.")
