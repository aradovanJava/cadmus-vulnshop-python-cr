"""Product search API."""
from flask import Blueprint, request, jsonify, g
from ..db import get_db

bp = Blueprint("api_search", __name__, url_prefix="/api")


@bp.get("/search")
def search():
    """-- T1 [A05] SQL injection: two sinks in one statement --------------
    The search term is concatenated into the WHERE clause, and the sort
    column is concatenated into ORDER BY. The first is fixable by binding;
    the second cannot be bound at all and needs an allow-list.
    Bandit B608. Payload:  ?q=' OR '1'='1
    """
    q = request.args.get("q", "")
    sort = request.args.get("sort", "name")
    sql = ("SELECT id, name, price FROM products "
           "WHERE name LIKE '%" + q + "%' ORDER BY " + sort)
    rows = get_db().execute(sql).fetchall()
    return jsonify(query=sql, results=[dict(r) for r in rows])
