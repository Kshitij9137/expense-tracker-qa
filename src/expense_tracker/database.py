"""Database layer: owns the SQLite connection and schema."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    category     TEXT    NOT NULL,
    description  TEXT    NOT NULL DEFAULT '',
    spent_on     TEXT    NOT NULL
);
CREATE TABLE IF NOT EXISTS budgets (
    category     TEXT PRIMARY KEY,
    limit_cents  INTEGER NOT NULL CHECK (limit_cents > 0)
);
CREATE INDEX IF NOT EXISTS idx_expenses_date     ON expenses (spent_on);
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses (category);
"""


def connect(path: str = "expenses.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
