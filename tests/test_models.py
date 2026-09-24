from models.voice_profile import VoiceProfile

def test_voice_profile_validation():
    profile = VoiceProfile(
        personality=["clear"],
        tone={"formality": 5, "warmth": 6, "confidence": 7, "playfulness": 4, "technicality": 3},
        sentence_style={
            "average_length": "short",
            "rhythm": "conversational",
            "complexity": "simple",
            "punctuation_style": "clean",
        },
        preferred_vocabulary=["clear"],
        preferred_patterns=["benefit-led"],
        avoid=["jargon"],
        audience_relationship="friendly expert",
        summary="Clear and friendly.",
    )
    assert profile.tone.confidence == 7
    assert profile.tone.formality <= 10
