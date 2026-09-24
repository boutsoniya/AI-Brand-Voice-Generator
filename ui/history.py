import streamlit as st
from database.repository import list_generations
from ui.styles import hero


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

    search = st.text_input("Search history", placeholder="Search by brand, content type, or copy...")
    filtered = rows
    if search.strip():
        q = search.lower()
        filtered = [
            row for row in rows
            if q in str(row[1]).lower() or q in str(row[2]).lower() or q in str(row[3]).lower()
        ]

    st.caption(f"{len(filtered)} saved generation(s)")
    for row_id, brand, kind, content, score, audio_blob, created in filtered:
        with st.container(border=True):
            top = st.columns([4, 1])
            with top[0]:
                st.markdown(f"**{kind}** · {brand}")
                st.caption(str(created))
            with top[1]:
                st.metric("Score", f"{score or '—'}%")
            st.write(content)
            actions = st.columns([1, 1, 2])
            with actions[0]:
                st.download_button(
                    "Download text",
                    data=content,
                    file_name=f"generation_{row_id}.txt",
                    mime="text/plain",
                    key=f"download_text_{row_id}",
                )
            with actions[1]:
                if audio_blob:
                    st.download_button(
                        "Download MP3",
                        data=audio_blob,
                        file_name=f"generation_{row_id}.mp3",
                        mime="audio/mpeg",
                        key=f"download_audio_{row_id}",
                    )
            with actions[2]:
                if audio_blob:
                    st.audio(audio_blob, format="audio/mp3")
                else:
                    st.caption("No voice preview saved for this generation.")
