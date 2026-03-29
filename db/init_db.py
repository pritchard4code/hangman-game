"""
init_db.py — Run this script once to initialise the hangman PostgreSQL database.

It will:
  1. Create all tables (words, games, guesses) via SQLAlchemy
  2. Seed the words table from words.py if it is empty

Usage:
    python db/init_db.py

The script reads the database URL from the DB_URL environment variable,
or falls back to the default local connection string.
"""

import sys
import os

# Allow importing from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app, db
from models import Word
from words import WORDS


def init():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables ready.")

        existing = Word.query.count()
        if existing == 0:
            print(f"Seeding {len(WORDS)} words...")
            for w in WORDS:
                db.session.add(Word(word=w.upper()))
            db.session.commit()
            print(f"Done. {len(WORDS)} words inserted.")
        else:
            print(f"Words table already contains {existing} rows — skipping seed.")


if __name__ == "__main__":
    init()
