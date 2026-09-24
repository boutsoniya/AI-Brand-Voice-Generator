# AI Brand Voice Generator

AI Brand Voice Generator is a Gemini-powered Streamlit application that converts existing marketing examples into a reusable Brand Voice Profile and uses that profile to generate and evaluate new content.

## Core workflow

Brand samples -> Voice analysis -> Structured Voice Profile -> Content generation -> Consistency check -> Refine

## Features

- Brand Voice Studio
- Voice DNA and tone dimensions
- Gemini-powered content generation
- Instagram, LinkedIn, email, ad, tagline and blog formats
- Consistency scoring
- Actionable improvement suggestions
- SQLite persistence
- Demo mode for UI review without an API key
- Modular architecture for future FastAPI and multi-brand support

## Tech stack

Python, Streamlit, Google Gemini, Pydantic, SQLite

## Local setup

1. Create a virtual environment.
2. Install dependencies with pip install -r requirements.txt.
3. Copy .env.example to .env.
4. Add GEMINI_API_KEY for live Gemini generation.
5. Run: streamlit run app.py

Without a Gemini key, the app runs in demo mode so the complete interface can be reviewed.

## Architecture

Streamlit UI
  -> Application services
  -> Voice Analyzer / Content Generator / Consistency Checker
  -> Gemini API
  -> Pydantic structured models
  -> SQLite repository

## Project structure

app.py
config/
core/
database/
models/
ui/
tests/

## Demo

Add the deployed Streamlit URL here after deployment.

## GitHub

https://github.com/boutsoniya/AI-Brand-Voice-Generator

## Notes

Generated marketing copy is AI-assisted and should be reviewed by a human before publication.
