from flask import Flask, render_template, session, jsonify, request
from words import get_random_word
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

MAX_WRONG = 6


def get_game_state():
    word = session.get("word", "")
    guessed = set(session.get("guessed", []))
    wrong = session.get("wrong", 0)

    display = [letter if letter in guessed else "_" for letter in word]
    won = "_" not in display
    lost = wrong >= MAX_WRONG

    return {
        "display": display,
        "guessed": sorted(list(guessed)),
        "wrong": wrong,
        "max_wrong": MAX_WRONG,
        "won": won,
        "lost": lost,
        "word": word if (won or lost) else None,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/new", methods=["POST"])
def new_game():
    session["word"] = get_random_word()
    session["guessed"] = []
    session["wrong"] = 0
    return jsonify(get_game_state())


@app.route("/api/state")
def state():
    if "word" not in session:
        session["word"] = get_random_word()
        session["guessed"] = []
        session["wrong"] = 0
    return jsonify(get_game_state())


@app.route("/api/guess", methods=["POST"])
def guess():
    data = request.get_json()
    letter = data.get("letter", "").upper()

    if not letter or len(letter) != 1 or not letter.isalpha():
        return jsonify({"error": "Invalid letter"}), 400

    if "word" not in session:
        return jsonify({"error": "No active game"}), 400

    guessed = set(session.get("guessed", []))
    word = session["word"]
    wrong = session.get("wrong", 0)

    state = get_game_state()
    if state["won"] or state["lost"]:
        return jsonify({"error": "Game already over"}), 400

    if letter not in guessed:
        guessed.add(letter)
        if letter not in word:
            wrong += 1
        session["guessed"] = list(guessed)
        session["wrong"] = wrong

    return jsonify(get_game_state())


if __name__ == "__main__":
    app.run(debug=True)
