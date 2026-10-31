"""Password reset."""
from flask import Blueprint, request, jsonify
from ..db import query_one, execute
from ..services.crypto import make_reset_code, hash_password

bp = Blueprint("api_reset", __name__, url_prefix="/api")


@bp.post("/reset/request")
def request_reset():
    username = request.json.get("username", "")
    code = make_reset_code()
    execute("INSERT INTO reset_codes (username, code) VALUES (?,?)", (username, code))
    # the code is returned in the response purely so the lab needs no mail server
    return jsonify(sent=True, debug_code=code)


@bp.post("/reset/confirm")
def confirm_reset():
    """-- M14 [A06] the reset design has no bound of any kind -------------
    Four digits is ten thousand possibilities. There is no expiry, no
    attempt limit, no single-use invalidation and no binding to a session.
    Every line of arithmetic here is correct; the contract is what is
    missing, which is why no tool reports it.
    """
    username = request.json.get("username", "")
    code = request.json.get("code", "")
    new_password = request.json.get("password", "")
    row = query_one("SELECT * FROM reset_codes WHERE username = ? AND code = ?",
                    (username, code))
    if row is None:
        return jsonify(error="bad code"), 400
    execute("UPDATE users SET password_hash = ? WHERE username = ?",
            (hash_password(new_password), username))
    return jsonify(ok=True)
