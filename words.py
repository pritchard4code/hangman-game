import random

WORDS = [
    "python", "javascript", "programming", "computer", "software",
    "algorithm", "database", "network", "interface", "keyboard",
    "elephant", "giraffe", "penguin", "dolphin", "butterfly",
    "adventure", "mystery", "treasure", "journey", "courage",
    "mountains", "waterfall", "volcano", "glacier", "canyon",
    "chocolate", "sandwich", "broccoli", "strawberry", "pineapple",
    "guitar", "trumpet", "violin", "saxophone", "percussion",
    "hospital", "library", "cathedral", "stadium", "museum",
    "telescope", "microscope", "thermometer", "calculator", "compass",
    "philosophy", "democracy", "revolution", "civilization", "knowledge",
]


def get_random_word():
    return random.choice(WORDS).upper()
