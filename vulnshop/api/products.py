"""Product API."""
from flask import Blueprint, request, jsonify
from ..db import query_all, query_one, execute
from ..services.authorization import is_admin

bp = Blueprint("api_products", __name__, url_prefix="/api")


@bp.get("/products")
def list_products():
    return jsonify([dict(r) for r in query_all("SELECT * FROM products")])


@bp.post("/products/<int:pid>/description")
def update_description(pid):
    """-- M18 [A01] no role check on a content-authoring endpoint ----------
    The navigation only shows this to staff, which is not a control. Any
    caller can write the description that T5 later renders unescaped, so
    this is the injection point for the stored cross-site scripting.
    """
    execute("UPDATE products SET description = ? WHERE id = ?",
            (request.json.get("description", ""), pid))
    return jsonify(ok=True)
