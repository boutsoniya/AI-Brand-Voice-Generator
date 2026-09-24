def build_prompt(profile, content_type, objective, audience, key_message, cta, length, creativity, refinement=None):
    refinement_block = f"\nREFINEMENT REQUEST\n{refinement}\n" if refinement else ""
    return f"""
You are the dedicated copywriter for this brand.

BRAND VOICE
Personality: {profile.personality}
Tone: {profile.tone.model_dump()}
Sentence style: {profile.sentence_style.model_dump()}
Preferred vocabulary: {profile.preferred_vocabulary}
Preferred patterns: {profile.preferred_patterns}
Avoid: {profile.avoid}
Audience relationship: {profile.audience_relationship}
Summary: {profile.summary}

REQUEST
Content type: {content_type}
Objective: {objective}
Audience: {audience}
Key message: {key_message}
CTA: {cta}
Length: {length}
Creativity: {creativity}/10
{refinement_block}
Write original marketing copy. Preserve the brand voice without copying sample text.
Do not mention AI. Return only the final copy.
"""

def generate_content(client, profile, content_type, objective, audience, key_message, cta, length, creativity, refinement=None):
    if client.demo_mode:
        base = f"Something new just landed.\n\n{key_message}. Built to make your everyday experience simpler, clearer, and more useful.\n\n{cta or 'Discover it today.'}"
        if refinement:
            return base + f"\n\nRefined direction: {refinement}"
        return base
    prompt = build_prompt(profile, content_type, objective, audience, key_message, cta, length, creativity, refinement)
    return client.generate(prompt).strip()
