import os
from google import genai
from config.settings import GEMINI_MODEL

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", GEMINI_MODEL)
        self.demo_mode = not bool(api_key)
        self.client = genai.Client(api_key=api_key) if api_key else None

    def generate(self, prompt: str, response_schema=None):
        if self.demo_mode:
            return None
        config = {}
        if response_schema:
            config["response_mime_type"] = "application/json"
            config["response_schema"] = response_schema
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config or None,
        )
        return response.text
