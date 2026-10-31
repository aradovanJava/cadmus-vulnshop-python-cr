"""Order API."""
from flask import Blueprint, jsonify, g
from ..db import query_one, query_all

bp = Blueprint("api_orders", __name__, url_prefix="/api")


@bp.get("/orders/<int:order_id>")
def get_order(order_id):
    """-- M4 [A01] object-level access control missing (API tier) ---------
    Authentication is not even required. findById(id) is idiomatic in every
    ORM, which is why no rule flags it: the query is correct, the predicate
    that should constrain it was never written. Combined with M5's
    sequential ids this exports every order in the database.
    """
    row = query_one("SELECT * FROM orders WHERE id = ?", (order_id,))
    if row is None:
        return jsonify(error="not found"), 404
    lines = query_all("SELECT * FROM order_lines WHERE order_id = ?", (order_id,))
    return jsonify(order=dict(row), lines=[dict(l) for l in lines])


@bp.get("/orders")
def my_orders():
    if g.user is None:
        return jsonify(error="login required"), 401
    rows = query_all("SELECT * FROM orders WHERE user_id = ?", (g.user["id"],))
    return jsonify([dict(r) for r in rows])
