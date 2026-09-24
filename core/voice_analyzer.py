import json
from models.voice_profile import VoiceProfile

PROMPT = """
You are a professional brand voice analyst.
Analyze the supplied brand samples and infer reusable writing rules.
Return ONLY JSON matching the requested schema.
Evaluate personality, formality, warmth, confidence, playfulness,
technicality, sentence rhythm, punctuation, vocabulary, preferred
patterns, things to avoid, and audience relationship.

BRAND SAMPLES:
{samples}
"""

def demo_profile():
    return VoiceProfile(
        personality=["confident", "approachable", "modern"],
        tone={"formality":4,"warmth":7,"confidence":8,"playfulness":5,"technicality":3},
        sentence_style={"average_length":"short","rhythm":"punchy and conversational","complexity":"simple","punctuation_style":"clean and restrained"},
        preferred_vocabulary=["simple","fresh","bold","useful"],
        preferred_patterns=["benefit-led openings","active voice","short calls to action"],
        avoid=["corporate jargon","long explanations","overly formal language"],
        audience_relationship="friendly expert",
        summary="A modern, confident and approachable voice that communicates benefits simply."
    )

def analyze_voice(client, samples):
    if client.demo_mode:
        return demo_profile()
    raw = client.generate(PROMPT.format(samples=samples), response_schema=VoiceProfile)
    return VoiceProfile.model_validate(json.loads(raw))
