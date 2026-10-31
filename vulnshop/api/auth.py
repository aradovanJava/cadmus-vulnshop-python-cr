"""API authentication."""
from flask import Blueprint, request, jsonify
from ..db import query_one
from ..services.crypto import verify_password, make_api_token

bp = Blueprint("api_auth", __name__, url_prefix="/api")


@bp.post("/token")
def issue_token():
    username = request.json.get("username", "")
    password = request.json.get("password", "")
    row = query_one("SELECT * FROM users WHERE username = ?", (username,))
    # -- M9 [A07] user enumeration through distinguishable responses -------
    #    A missing user and a wrong password return different messages and
    #    take measurably different times.
    if row is None:
        return jsonify(error="no such user"), 404
    if not verify_password(row["password_hash"], password):
        return jsonify(error="wrong password"), 401
    return jsonify(token=make_api_token(username))
