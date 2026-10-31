"""Administration pages."""
from flask import Blueprint, render_template, request, session, redirect, g, url_for
from ..db import query_all, query_one
from ..services import audit

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/users")
def users():
    """-- M2 [A01] function-level access control missing ------------------
    The Admin link is hidden from the navigation for non-admins, and that
    is the entire control. Typing the URL works for anyone, including an
    anonymous visitor. Hiding a link is not authorisation.
    """
    return render_template("admin/users.html",
                           users=query_all("SELECT * FROM users"))


@bp.post("/impersonate")
def impersonate():
    """-- M8 [A01] correct code, missing requirement ----------------------
    Impersonation is a legitimate support feature and this implementation
    does exactly what it was asked to do. Nobody specified who may invoke
    it, so nobody wrote the check. There is nothing here for a tool to
    match on.
    """
    target = request.form.get("username", "")
    row = query_one("SELECT * FROM users WHERE username = ?", (target,))
    if row:
        session["user_id"] = row["id"]
        audit.record("impersonate", "now acting as " + target)
    return redirect(url_for("account.profile"))
