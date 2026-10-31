"""Cart and checkout."""
from flask import Blueprint, render_template, request, redirect, g, url_for
from ..db import query_one, execute, get_db

bp = Blueprint("cart", __name__, url_prefix="/cart")


@bp.get("/")
def view():
    return render_template("shop/cart.html",
                           products=get_db().execute("SELECT * FROM products").fetchall())


@bp.post("/checkout")
def checkout():
    """-- M13 [A06] the server trusts values it already knows -------------
    unit_price arrives from a hidden field in cart.html and quantity has no
    bound. Any price a genuine client may send, an attacker may also send,
    so no validation rule separates them. A negative quantity credits the
    account.

    Neither file is wrong on its own: the template renders a hidden input,
    the controller reads a form field. The weakness appears only when the
    two are read together.
    """
    product_id = int(request.form.get("product_id", 1))
    quantity = int(request.form.get("quantity", 1))
    unit_price = int(request.form.get("unit_price", 0))
    total = quantity * unit_price
    if g.user is None:
        return redirect(url_for("account.login"))
    cur = execute("INSERT INTO orders (user_id, total, status, placed) "
                  "VALUES (?,?,?,?)", (g.user["id"], total, "NEW", "2026-08-24"))
    execute("INSERT INTO order_lines (order_id, product_id, quantity, unit_price) "
            "VALUES (?,?,?,?)", (cur.lastrowid, product_id, quantity, unit_price))
    return redirect(url_for("account.my_orders"))
