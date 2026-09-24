import json
import sqlite3
from config.settings import DB_PATH

def save_brand(name, description, profile):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO brands(name, description, profile_json) VALUES (?, ?, ?)",
            (name, description, json.dumps(profile.model_dump()))
        )
        return cur.lastrowid

def save_generation(brand_id, content_type, content, score=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO generations(brand_id, content_type, content, score) VALUES (?, ?, ?, ?)",
            (brand_id, content_type, content, score)
        )

def counts():
    with sqlite3.connect(DB_PATH) as conn:
        return (
            conn.execute("SELECT COUNT(*) FROM brands").fetchone()[0],
            conn.execute("SELECT COUNT(*) FROM generations").fetchone()[0]
        )
