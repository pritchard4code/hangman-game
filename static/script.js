const BODY_PARTS = ["head", "body", "left-arm", "right-arm", "left-leg", "right-leg"];

async function fetchJSON(url, options = {}) {
    const res = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    return res.json();
}

function buildKeyboard() {
    const keyboard = document.getElementById("keyboard");
    keyboard.innerHTML = "";
    for (let i = 65; i <= 90; i++) {
        const letter = String.fromCharCode(i);
        const btn = document.createElement("button");
        btn.className = "key-btn";
        btn.id = `key-${letter}`;
        btn.textContent = letter;
        btn.addEventListener("click", () => guessLetter(letter));
        keyboard.appendChild(btn);
    }
}

function updateUI(state) {
    // Word display
    const wordDisplay = document.getElementById("word-display");
    wordDisplay.innerHTML = state.display
        .map(ch => `<div class="letter-slot ${ch !== "_" ? "revealed" : "blank"}">${ch}</div>`)
        .join("");

    // Hangman drawing
    BODY_PARTS.forEach((part, i) => {
        const el = document.getElementById(part);
        if (i < state.wrong) {
            el.classList.remove("hidden");
        } else {
            el.classList.add("hidden");
        }
    });

    // Wrong count
    document.getElementById("wrong-count").textContent =
        `${state.wrong} / ${state.max_wrong} wrong`;

    // Keyboard states
    const guessedSet = new Set(state.guessed);
    const wordLetters = new Set(state.display.filter(ch => ch !== "_"));

    for (let i = 65; i <= 90; i++) {
        const letter = String.fromCharCode(i);
        const btn = document.getElementById(`key-${letter}`);
        if (!btn) continue;
        btn.disabled = guessedSet.has(letter) || state.won || state.lost;
        btn.classList.remove("correct", "wrong");
        if (guessedSet.has(letter)) {
            if (state.won) {
                btn.classList.add("correct");
            } else {
                // Check if the letter is in the word (revealed or full word shown)
                const inWord = state.word
                    ? state.word.includes(letter)
                    : state.display.includes(letter);
                btn.classList.add(inWord ? "correct" : "wrong");
            }
        }
    }

    // Guessed letters
    document.getElementById("guessed-letters").textContent = state.guessed.join("  ");

    // Message
    const msg = document.getElementById("message");
    if (state.won) {
        msg.textContent = "You won!";
        msg.className = "message win";
    } else if (state.lost) {
        msg.textContent = `Game over! The word was: ${state.word}`;
        msg.className = "message lose";
    } else {
        msg.className = "message hidden";
    }
}

async function guessLetter(letter) {
    const state = await fetchJSON("/api/guess", {
        method: "POST",
        body: JSON.stringify({ letter }),
    });
    if (!state.error) updateUI(state);
}

async function newGame() {
    const state = await fetchJSON("/api/new", { method: "POST" });
    updateUI(state);
}

async function init() {
    buildKeyboard();
    const state = await fetchJSON("/api/state");
    updateUI(state);
    document.getElementById("new-game-btn").addEventListener("click", newGame);

    // Keyboard support
    document.addEventListener("keydown", (e) => {
        const letter = e.key.toUpperCase();
        if (letter.length === 1 && letter >= "A" && letter <= "Z") {
            const btn = document.getElementById(`key-${letter}`);
            if (btn && !btn.disabled) guessLetter(letter);
        }
    });
}

init();
