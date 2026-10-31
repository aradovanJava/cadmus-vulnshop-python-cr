"""User API."""
from flask import Blueprint, request, jsonify, g
from ..db import query_one, get_db

bp = Blueprint("api_users", __name__, url_prefix="/api")

ALL_COLUMNS = ("username", "email", "full_name", "role", "balance",
               "risk_score", "password_hash", "api_token", "locked")


@bp.post("/users/<int:uid>/profile")
def update_profile(uid):
    """-- M7 [A01] mass assignment ----------------------------------------
    Every key in the request body is written back to the row. The interface
    exposes email and full_name; the endpoint also accepts role, balance
    and password_hash. A user promotes themselves by adding one field.
    This is the write half of M6 — the template leaks exactly the fields
    that this endpoint accepts back.
    """
    body = request.get_json(silent=True) or {}
    db = get_db()
    for key, value in body.items():
        if key in ALL_COLUMNS:
            db.execute("UPDATE users SET %s = ? WHERE id = ?" % key, (value, uid))
    db.commit()
    return jsonify(dict(query_one("SELECT * FROM users WHERE id = ?", (uid,))))
