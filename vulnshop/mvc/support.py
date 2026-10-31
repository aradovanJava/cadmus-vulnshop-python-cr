"""Support desk."""
import os
from flask import Blueprint, render_template, request, redirect, g, url_for, Response
from ..db import query_all, query_one, execute
from ..services.authorization import can_access

bp = Blueprint("support", __name__, url_prefix="/support")

ATTACH_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "attachments")


@bp.route("/", methods=["GET", "POST"])
def tickets():
    if request.method == "POST":
        execute("INSERT INTO tickets (user_id, subject, body, attachment) "
                "VALUES (?,?,?,?)",
                (g.user["id"] if g.user else 0,
                 request.form.get("subject", ""),
                 request.form.get("body", ""),
                 request.form.get("attachment", "")))
        return redirect(url_for("support.tickets"))
    return render_template("support/tickets.html",
                           tickets=query_all("SELECT * FROM tickets"))


@bp.get("/ticket/<int:tid>")
def ticket(tid):
    """The ownership gate here delegates to AuthorizationService.can_access.

    That call is what makes T18 exploitable rather than merely untidy: for a
    ticket id that does not exist the owner is None, int(None) raises, and
    the except branch returns True. Read can_access before deciding whether
    this route is guarded.
    """
    row = query_one("SELECT * FROM tickets WHERE id = ?", (tid,))
    if not can_access(g.user, row["user_id"] if row else None):
        return "forbidden", 403
    return render_template("support/ticket.html", ticket=row)


@bp.get("/attachment")
def attachment():
    """-- T4 [A01] path traversal, second location ------------------------
    The same shape as T3 in a different tier. Participants who fix one
    location and not the other have treated a design flaw as a local bug.
    """
    name = request.args.get("name", "receipt.txt")
    path = os.path.join(ATTACH_DIR, name)
    if not os.path.exists(path):
        return Response("no such attachment: " + path, status=404, mimetype="text/plain")
    with open(path, "rb") as fh:
        return Response(fh.read(), mimetype="text/plain")
