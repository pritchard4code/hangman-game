from flask import Flask, Blueprint, render_template, session, jsonify, request
from models import db, Word, Game, Guess
from datetime import datetime, timezone
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:wangu@localhost:5432/hangman"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

hangman = Blueprint("hangman", __name__, url_prefix="/hangman")

MAX_WRONG = 6


def pick_random_word():
    """Pick a random word from the DB, favouring least-used words."""
    min_used = db.session.query(db.func.min(Word.times_used)).scalar() or 0
    candidates = Word.query.filter(Word.times_used == min_used).all()
    if not candidates:
        candidates = Word.query.all()
    return random.choice(candidates)


def get_game_state():
    word_obj = session.get("word", "")
    guessed = set(session.get("guessed", []))
    wrong = session.get("wrong", 0)

    display = [letter if letter in guessed else "_" for letter in word_obj]
    won = "_" not in display
    lost = wrong >= MAX_WRONG

    return {
        "display": display,
        "guessed": sorted(list(guessed)),
        "wrong": wrong,
        "max_wrong": MAX_WRONG,
        "won": won,
        "lost": lost,
        "word": word_obj if (won or lost) else None,
    }


def finish_game(outcome):
    game_id = session.get("game_id")
    if game_id:
        game = db.session.get(Game, game_id)
        if game and game.outcome is None:
            game.outcome = outcome
            game.completed_at = datetime.now(timezone.utc)
            game.wrong_count = session.get("wrong", 0)
            db.session.commit()


@hangman.route("/")
def index():
    return render_template("index.html")


@hangman.route("/api/new", methods=["POST"])
def new_game():
    # Close any in-progress game
    state = get_game_state() if "word" in session else None
    if state and not state["won"] and not state["lost"]:
        finish_game("abandoned")

    word_obj = pick_random_word()
    word_obj.times_used += 1
    game = Game(word_ref=word_obj)
    db.session.add(game)
    db.session.commit()

    session["word"] = word_obj.word.upper()
    session["guessed"] = []
    session["wrong"] = 0
    session["game_id"] = game.id

    return jsonify(get_game_state())


@hangman.route("/api/state")
def state():
    if "word" not in session:
        word_obj = pick_random_word()
        word_obj.times_used += 1
        game = Game(word_ref=word_obj)
        db.session.add(game)
        db.session.commit()
        session["word"] = word_obj.word.upper()
        session["guessed"] = []
        session["wrong"] = 0
        session["game_id"] = game.id
    return jsonify(get_game_state())


@hangman.route("/api/guess", methods=["POST"])
def guess():
    data = request.get_json()
    letter = data.get("letter", "").upper()

    if not letter or len(letter) != 1 or not letter.isalpha():
        return jsonify({"error": "Invalid letter"}), 400

    if "word" not in session:
        return jsonify({"error": "No active game"}), 400

    current_state = get_game_state()
    if current_state["won"] or current_state["lost"]:
        return jsonify({"error": "Game already over"}), 400

    guessed = set(session.get("guessed", []))
    word = session["word"]
    wrong = session.get("wrong", 0)

    if letter not in guessed:
        is_correct = letter in word
        guessed.add(letter)
        if not is_correct:
            wrong += 1
        session["guessed"] = list(guessed)
        session["wrong"] = wrong

        # Persist guess
        game_id = session.get("game_id")
        if game_id:
            g = Guess(game_id=game_id, letter=letter, is_correct=is_correct)
            db.session.add(g)
            db.session.commit()

    new_state = get_game_state()

    # Persist game outcome if finished
    if new_state["won"]:
        finish_game("win")
    elif new_state["lost"]:
        finish_game("loss")

    return jsonify(new_state)


@hangman.route("/api/stats")
def stats():
    total = Game.query.count()
    wins = Game.query.filter_by(outcome="win").count()
    losses = Game.query.filter_by(outcome="loss").count()
    top_words = (
        db.session.query(Word.word, Word.times_used)
        .order_by(Word.times_used.desc())
        .limit(10)
        .all()
    )
    return jsonify({
        "total_games": total,
        "wins": wins,
        "losses": losses,
        "win_rate": round(wins / total * 100, 1) if total else 0,
        "top_words": [{"word": w, "times_used": t} for w, t in top_words],
    })


app.register_blueprint(hangman)


@app.route("/")
def root_redirect():
    from flask import redirect, url_for
    return redirect(url_for("hangman.index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Seed words if table is empty
        if Word.query.count() == 0:
            from words import WORDS
            for w in WORDS:
                db.session.add(Word(word=w.upper()))
            db.session.commit()
            print(f"Seeded {len(WORDS)} words into the database.")
    app.run(debug=True)
