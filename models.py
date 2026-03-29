from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False)
    times_used = db.Column(db.Integer, default=0, nullable=False)

    games = db.relationship("Game", back_populates="word_ref", lazy=True)

    def __repr__(self):
        return f"<Word {self.word}>"


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), nullable=False)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    outcome = db.Column(db.String(10), nullable=True)   # 'win', 'loss', or None if in progress
    wrong_count = db.Column(db.Integer, default=0, nullable=False)

    word_ref = db.relationship("Word", back_populates="games")
    guesses = db.relationship("Guess", back_populates="game", lazy=True, order_by="Guess.guessed_at")

    def __repr__(self):
        return f"<Game {self.id} word={self.word_ref.word} outcome={self.outcome}>"


class Guess(db.Model):
    __tablename__ = "guesses"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    letter = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    guessed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    game = db.relationship("Game", back_populates="guesses")

    def __repr__(self):
        return f"<Guess {self.letter} correct={self.is_correct}>"
