"""Database access and seed data."""
import os
import sqlite3
from flask import g

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "vulnshop.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_all(sql, args=()):
    return get_db().execute(sql, args).fetchall()


def query_one(sql, args=()):
    return get_db().execute(sql, args).fetchone()


def execute(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    return cur


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY,
    username      TEXT UNIQUE,
    password_hash TEXT,
    role          TEXT,
    email         TEXT,
    full_name     TEXT,
    balance       INTEGER DEFAULT 0,
    risk_score    INTEGER DEFAULT 0,
    api_token     TEXT,
    locked        INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY,
    name        TEXT,
    description TEXT,
    price       INTEGER,
    stock       INTEGER
);
CREATE TABLE IF NOT EXISTS orders (
    id       INTEGER PRIMARY KEY,
    user_id  INTEGER,
    total    INTEGER,
    status   TEXT,
    placed   TEXT
);
CREATE TABLE IF NOT EXISTS order_lines (
    id         INTEGER PRIMARY KEY,
    order_id   INTEGER,
    product_id INTEGER,
    quantity   INTEGER,
    unit_price INTEGER
);
CREATE TABLE IF NOT EXISTS tickets (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER,
    subject TEXT,
    body    TEXT,
    attachment TEXT
);
CREATE TABLE IF NOT EXISTS reset_codes (
    id       INTEGER PRIMARY KEY,
    username TEXT,
    code     TEXT
);
"""

# -- T17 [A07] hardcoded credentials in seed data -------------------------
#    All four training accounts share one weak password. Whether this is a
#    finding depends on a fact the scanner cannot see: does this seed run
#    outside a test profile? (It does — init_db is called unconditionally.)
SEED_PASSWORD = "Password123"


def init_db():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for d in ("attachments", "reports"):
        os.makedirs(os.path.join(base, d), exist_ok=True)
    fresh = not os.path.exists(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    if fresh:
        from .services.crypto import hash_password
        users = [
            (1, "alice",    "user",  "alice@example.invalid",   "Alice Nowak",     820,  12),
            (2, "bob",      "user",  "bob@example.invalid",     "Bob Marek",       410,  47),
            (3, "carol",    "user",  "carol@example.invalid",   "Carol Fischer",  1290,   3),
            (4, "adminjoe", "admin", "adminjoe@example.invalid", "Joe Kovac",      5000,   0),
        ]
        for uid, un, role, email, name, bal, risk in users:
            db.execute(
                "INSERT INTO users (id, username, password_hash, role, email, "
                "full_name, balance, risk_score, api_token) VALUES (?,?,?,?,?,?,?,?,?)",
                (uid, un, hash_password(SEED_PASSWORD), role, email, name, bal, risk,
                 "vs_tok_%s_static" % un))
        db.executemany(
            "INSERT INTO products (name, description, price, stock) VALUES (?,?,?,?)",
            [("Mechanical Keyboard", "<b>Tactile</b> switches, PBT keycaps.", 89, 40),
             ("27in Monitor", "1440p, 165Hz, height adjustable.", 249, 12),
             ("USB-C Dock", "Dual display, 100W passthrough.", 130, 25),
             ("Webcam Pro", "1080p60 with a physical shutter.", 72, 33),
             ("Desk Lamp", "Adjustable colour temperature.", 45, 60)])
        # -- M5 [A01] order ids are sequential from 1000 ---------------------
        #    On its own this is unremarkable. Combined with M3/M4 it converts
        #    a single IDOR into a complete export of every order.
        oid = 1000
        for uid, total in ((1, 338), (1, 72), (2, 130), (3, 249), (3, 45), (4, 89)):
            db.execute("INSERT INTO orders (id, user_id, total, status, placed) "
                       "VALUES (?,?,?,?,?)",
                       (oid, uid, total, "SHIPPED", "2026-08-0%d" % (oid % 7 + 1)))
            db.execute("INSERT INTO order_lines (order_id, product_id, quantity, unit_price) "
                       "VALUES (?,?,?,?)", (oid, (oid % 5) + 1, 1, total))
            oid += 1
        db.execute("INSERT INTO tickets (user_id, subject, body, attachment) "
                   "VALUES (?,?,?,?)",
                   (2, "Where is my dock?", "Ordered a week ago, no update.", "receipt.txt"))
    db.commit()
    db.close()
