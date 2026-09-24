# AI Brand Voice Generator

A Gemini-powered brand intelligence workspace that learns how a brand writes, turns that style into a structured Voice DNA, generates new marketing copy, and checks the copy for consistency.

## Why this project exists

Generic AI copy can be grammatically correct while still sounding unlike the company that publishes it. This project treats brand voice as reusable structured context rather than a one-off prompt.

**Samples → Voice DNA → Content Brief → Generation → Consistency Check → Refine → Save**

## Product capabilities

### 1. Brand Voice Studio
Paste representative posts, emails, landing-page copy or campaign text. The analyzer extracts:

- Personality traits
- Formality, warmth, confidence, playfulness and technicality
- Sentence length, rhythm, complexity and punctuation style
- Preferred vocabulary
- Reusable writing patterns
- Words/styles to avoid
- Audience relationship
- Human-readable voice summary

### 2. Content Generator
Generate channel-specific drafts for:

- Instagram
- LinkedIn
- Marketing email
- Ad headline
- Tagline
- Blog introduction

The brief includes objective, audience, key message, CTA, length and creativity.

### 3. Consistency Checker
Every generated draft can be evaluated across:

- Overall consistency
- Tone
- Vocabulary
- Structure
- Audience fit

The checker also returns concrete issues and suggestions.

### 4. Refinement loop
A generated draft can be regenerated with a natural-language direction such as:

> Make it warmer, shorten the opening, and soften the CTA.

The original Voice DNA remains in context during refinement.

### 5. Demo mode
The application works without a Gemini API key using deterministic demo data. The dashboard includes a one-click **Load demo brand** flow for mentor reviews and UI walkthroughs.

### 6. Persistence
SQLite stores brand profiles and generation history locally.

## Architecture

```
┌───────────────────────────────┐
│        Streamlit UI           │
│ Dashboard / Studio / Generate │
│ Checker / History             │
└──────────────┬────────────────┘
               │
┌──────────────▼────────────────┐
│       Application Core        │
│ Voice Analyzer                │
│ Content Generator             │
│ Consistency Checker           │
└──────────────┬────────────────┘
               │
       ┌───────▼────────┐
       │  Gemini API    │
       │ structured     │
       │ JSON outputs   │
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │ Pydantic Models│
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │ SQLite         │
       │ brands         │
       │ generations    │
       └────────────────┘
```

## Tech stack

- Python 3.8+
- Streamlit
- Google Gemini via `google-genai`
- Pydantic
- SQLite
- python-dotenv
- pytest
- GitHub Actions

LangChain/FastAPI can be added later as service/API layers; the current implementation keeps the core application intentionally small and testable.

## Project structure

```
AI-Brand-Voice-Generator/
├── app.py
├── config/
├── core/
│   ├── gemini_client.py
│   ├── voice_analyzer.py
│   ├── content_generator.py
│   └── consistency_checker.py
├── database/
├── models/
├── ui/
├── tests/
├── .github/workflows/
├── .streamlit/
├── render.yaml
├── requirements.txt
└── README.md
```

## Run locally

```bash
git clone https://github.com/boutsoniya/AI-Brand-Voice-Generator.git
cd AI-Brand-Voice-Generator

python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Create `.env` from `.env.example` and add:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=your_supported_gemini_model
```

Then:

```bash
streamlit run app.py
```

If no Gemini key is configured, the UI automatically falls back to demo mode.

## Testing

```bash
pytest -q
```

GitHub Actions runs the test suite on pushes and pull requests.

## Deployment

A `render.yaml` blueprint is included for Render. Configure `GEMINI_API_KEY` as a secret environment variable and deploy the Streamlit service.

The repository does not hard-code API credentials.

## Mentor demo flow

1. Open Dashboard.
2. Click **Load demo brand**.
3. Review Voice DNA in Brand Voice Studio.
4. Open Content Generator.
5. Create a LinkedIn/Instagram/email draft.
6. Review the five consistency dimensions.
7. Open **Refine this draft** and change the direction.
8. Save the final version to history.
9. Open Consistency Checker and paste any independent copy for comparison.

## Engineering notes

- Pydantic models keep LLM output structured and validated.
- Demo mode makes the interface reviewable without external API access.
- SQLite keeps the prototype self-contained.
- Gemini model selection is configurable through an environment variable.
- Human review remains part of the publishing workflow; generated copy should be reviewed before external publication.

## Repository

https://github.com/boutsoniya/AI-Brand-Voice-Generator
