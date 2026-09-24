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

def list_brands():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT id, name, description, profile_json FROM brands ORDER BY id DESC"
        ).fetchall()

def save_generation(brand_id, content_type, content, score=None):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO generations(brand_id, content_type, content, score) VALUES (?, ?, ?, ?)",
            (brand_id, content_type, content, score)
        )
        return cur.lastrowid

def counts():
    with sqlite3.connect(DB_PATH) as conn:
        return (
            conn.execute("SELECT COUNT(*) FROM brands").fetchone()[0],
            conn.execute("SELECT COUNT(*) FROM generations").fetchone()[0]
        )

def recent_generations(limit=6):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            """SELECT g.id, COALESCE(b.name, 'Demo workspace'), g.content_type,
                      g.content, g.score, g.created_at
               FROM generations g LEFT JOIN brands b ON b.id = g.brand_id
               ORDER BY g.id DESC LIMIT ?""",
            (limit,)
        ).fetchall()

def latest_brand():
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT id, name, description, profile_json FROM brands ORDER BY id DESC LIMIT 1"
        ).fetchone()
    if not row:
        return None
    return row[0], row[1], row[2], json.loads(row[3])
