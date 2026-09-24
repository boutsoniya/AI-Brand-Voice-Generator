def build_prompt(profile, content_type, objective, audience, key_message, cta, length, creativity):
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

Write original marketing copy. Preserve the brand voice without copying
sample text. Do not mention AI. Return only the final copy.
"""

def generate_content(client, profile, content_type, objective, audience, key_message, cta, length, creativity):
    if client.demo_mode:
        return f"Something new just landed.\n\n{key_message}. Built to make your everyday experience simpler, clearer, and more useful.\n\n{cta or 'Discover it today.'}"
    return client.generate(build_prompt(profile, content_type, objective, audience, key_message, cta, length, creativity)).strip()
