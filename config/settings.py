import os

APP_NAME = "AI Brand Voice Generator"
DB_PATH = os.getenv("BRANDVOICE_DB", "data/brandvoice.db")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
