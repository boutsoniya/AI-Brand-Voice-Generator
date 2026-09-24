from models.voice_profile import VoiceProfile

def test_voice_profile_validation():
    profile = VoiceProfile(
        personality=["friendly"],
        tone={"formality":4,"warmth":7,"confidence":8,"playfulness":5,"technicality":3},
        sentence_style={"average_length":"short","rhythm":"punchy","complexity":"simple","punctuation_style":"clean"},
        preferred_vocabulary=["simple"],
        preferred_patterns=["active voice"],
        avoid=["jargon"],
        audience_relationship="friendly expert",
        summary="Clear and friendly."
    )
    assert profile.tone.warmth == 7
