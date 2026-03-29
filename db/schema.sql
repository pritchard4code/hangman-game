-- Hangman Game Database Schema
-- PostgreSQL 18+
-- Run this script as the postgres superuser to create the database and schema.

-- Create database (run connected to 'postgres' default database)
CREATE DATABASE hangman;

\connect hangman

-- Words table: stores all possible game words and usage tracking
CREATE TABLE IF NOT EXISTS words (
    id          SERIAL PRIMARY KEY,
    word        VARCHAR(50) NOT NULL UNIQUE,
    times_used  INTEGER NOT NULL DEFAULT 0
);

-- Games table: records every game session
CREATE TABLE IF NOT EXISTS games (
    id            SERIAL PRIMARY KEY,
    word_id       INTEGER NOT NULL REFERENCES words(id),
    started_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at  TIMESTAMP WITH TIME ZONE,
    outcome       VARCHAR(10) CHECK (outcome IN ('win', 'loss', 'abandoned')),
    wrong_count   INTEGER NOT NULL DEFAULT 0
);

-- Guesses table: records every letter guessed within a game
CREATE TABLE IF NOT EXISTS guesses (
    id          SERIAL PRIMARY KEY,
    game_id     INTEGER NOT NULL REFERENCES games(id),
    letter      CHAR(1) NOT NULL,
    is_correct  BOOLEAN NOT NULL,
    guessed_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_games_word_id   ON games(word_id);
CREATE INDEX IF NOT EXISTS idx_games_outcome   ON games(outcome);
CREATE INDEX IF NOT EXISTS idx_guesses_game_id ON guesses(game_id);
CREATE INDEX IF NOT EXISTS idx_words_times_used ON words(times_used);
