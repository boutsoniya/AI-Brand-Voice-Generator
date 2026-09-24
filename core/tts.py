from io import BytesIO
from gtts import gTTS


def synthesize_speech(text: str, language: str = "en", slow: bool = False) -> bytes:
    """Create MP3 speech audio from generated copy."""
    if not text or not text.strip():
        raise ValueError("Text is required for speech generation.")
    audio = BytesIO()
    gTTS(text=text.strip(), lang=language, slow=slow).write_to_fp(audio)
    return audio.getvalue()
