# Hangman

A browser-based Hangman game built with Python (Flask) and vanilla JavaScript.

## Features

- SVG hangman drawing that progressively reveals body parts on wrong guesses
- On-screen A–Z keyboard with visual feedback (green = correct, red = wrong)
- Physical keyboard input support
- 50-word vocabulary spanning multiple categories
- Session-based game state (each browser tab has its own game)
- New Game button to reset at any time

## Requirements

- Python 3.8+
- Flask 3.0+

## Installation

```bash
# Clone the repository
git clone https://github.com/pritchard4code/hangman-game.git
cd hangman-game

# Create and activate a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

Then open your browser at **http://localhost:5000**.

## Project Structure

```
hangman-game/
├── app.py              # Flask application and API routes
├── words.py            # Word list and random word selector
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Main game page (SVG + layout)
└── static/
    ├── style.css       # Dark-themed styles
    └── script.js       # Game logic and API calls
```

## API Endpoints

| Method | Endpoint     | Description                        |
|--------|--------------|------------------------------------|
| GET    | `/`          | Serve the game page                |
| GET    | `/api/state` | Get current game state             |
| POST   | `/api/new`   | Start a new game                   |
| POST   | `/api/guess` | Submit a letter guess `{"letter": "A"}` |

### Game State Response

```json
{
  "display":  ["_", "Y", "_", "_", "_", "_"],
  "guessed":  ["A", "E", "Y"],
  "wrong":    2,
  "max_wrong": 6,
  "won":      false,
  "lost":     false,
  "word":     null
}
```

`word` is only revealed when the game is over (won or lost).

## How to Play

1. The app picks a random word and shows it as blank slots.
2. Click a letter on the on-screen keyboard (or press a key) to guess.
3. Correct guesses reveal the letter in its position(s).
4. Wrong guesses draw a body part on the gallows — 6 wrong guesses and it's game over.
5. Guess all letters before the hangman is complete to win.

## License

MIT
