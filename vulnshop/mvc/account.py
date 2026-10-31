"""Account area — login, profile and order history."""
from flask import (Blueprint, render_template, request, redirect, session,
                   make_response, g, url_for)
from ..db import query_one, query_all
from ..services.crypto import verify_password
from ..services.authorization import can_access
from ..services import audit

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        row = query_one("SELECT * FROM users WHERE username = ?", (username,))
        # -- M9 [A07] username enumeration --------------------------------
        #    Two ordinary return statements that say different things.
        if row is None:
            error = "No account called %s" % username
        elif not verify_password(row["password_hash"], password):
            error = "Wrong password for %s" % username
            # -- M10 [A07] no lockout, no rate limit, no alert -------------
            audit.record_login_failure(username)
        else:
            # -- M11 [A07] the session id is not rotated on privilege change
            #    A cookie planted before login stays valid afterwards.
            session["user_id"] = row["id"]
            resp = make_response(redirect(url_for("account.profile")))
            # -- M12 [A07·A01] role carried in an unsigned client cookie ---
            resp.set_cookie("vs_remember", "%s:%s" % (row["username"], row["role"]),
                            max_age=60 * 60 * 24 * 30, httponly=False, secure=False)
            return resp
    return render_template("account/login.html", error=error)


@bp.get("/logout")
def logout():
    session.clear()
    resp = make_response(redirect(url_for("shop.index")))
    resp.delete_cookie("vs_remember")
    return resp


@bp.get("/profile")
def profile():
    if g.user is None:
        return redirect(url_for("account.login"))
    return render_template("account/profile.html", user=g.user)


@bp.get("/orders")
def my_orders():
    """Correctly scoped to the caller. Compare with order_detail below."""
    if g.user is None:
        return redirect(url_for("account.login"))
    rows = query_all("SELECT * FROM orders WHERE user_id = ?", (g.user["id"],))
    return render_template("account/orders.html", orders=rows)


@bp.get("/orders/<int:order_id>")
def order_detail(order_id):
    """-- M3 [A01] object-level access control missing (MVC tier) ---------
    The listing above is scoped to the caller with a WHERE user_id clause;
    this lookup is not. The two methods sit next to each other, which is
    the point: the predicate is present in the first and absent in the
    second. findById(id) is idiomatic, so no rule fires.

    Combined with M5 (sequential ids from 1000) this is a full export.
    """
    row = query_one("SELECT * FROM orders WHERE id = ?", (order_id,))
    lines = query_all("SELECT * FROM order_lines WHERE order_id = ?", (order_id,))
    return render_template("account/order_detail.html", order=row, lines=lines)
