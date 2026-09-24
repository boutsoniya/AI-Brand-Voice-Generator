import json
from models.generation import ConsistencyResult

def demo_check(content):
    return ConsistencyResult(
        overall_score=91, tone_score=94, vocabulary_score=89,
        structure_score=90, audience_fit=92,
        issues=["The CTA could be slightly softer to better match the established voice."],
        suggestions=["Use an invitation rather than an urgent command."]
    )

def check_consistency(client, profile, content):
    if client.demo_mode:
        return demo_check(content)
    prompt = f"""
Evaluate this marketing copy against the supplied brand voice profile.

VOICE PROFILE:
{profile.model_dump_json()}

CONTENT:
{content}

Return JSON matching the requested schema. Scores must be 0-100.
Identify concrete mismatches and actionable suggestions.
"""
    raw = client.generate(prompt, response_schema=ConsistencyResult)
    return ConsistencyResult.model_validate(json.loads(raw))
