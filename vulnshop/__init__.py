"""
cadmus-vulnshop-cr · CADMUS-CR-15 Secure Coding Python
=======================================================
DELIBERATELY VULNERABLE TRAINING APPLICATION — Cyber Range nodes CR1-CR4.

Binds to 127.0.0.1 only. Contains at least one unauthenticated remote code
execution path. Sandbox use only; never expose, never use real data.
Every seed address is .invalid and the version qualifier is -TRAINING.
"""
import os
from flask import Flask, g, session, request

VERSION = "2.4.0-TRAINING"


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),
    )

    # -- T12 [A04·A02] hardcoded secret key, committed to the repository ---------
    #    Session cookies are forgeable by anyone with read access to this file.
    app.secret_key = "vulnshop-dev-secret-do-not-change-2024"

    # -- T13 [A02] CSRF protection is never installed -----------------------
    #    Flask-WTF is in requirements.txt but CSRFProtect is never applied,
    #    so every state-changing POST accepts a cross-site request.
    app.config["WTF_CSRF_ENABLED"] = False

    from .db import init_db, close_db
    from .services import audit

    app.teardown_appcontext(close_db)

    # -- M1 [A01·A02] the base rule for the whole application ---------------
    #    There is no default-deny. An endpoint added next week is public
    #    unless its author remembers to decorate it. This is one line and it
    #    is the highest-leverage weakness in the application.
    @app.before_request
    def default_access_rule():
        g.user = None
        uid = session.get("user_id")
        if uid:
            from .db import query_one
            g.user = query_one("SELECT * FROM users WHERE id = ?", (uid,))
        # -- M12 [A07·A01] the remember-me cookie is also a role claim ------
        #    Format is "username:role", not signed, not HttpOnly, 30 days.
        #    The client can edit it and become an administrator.
        if g.user is None:
            raw = request.cookies.get("vs_remember")
            if raw and ":" in raw:
                username, role = raw.split(":", 1)
                from .db import query_one
                row = query_one("SELECT * FROM users WHERE username = ?", (username,))
                if row:
                    g.user = dict(row)
                    g.user["role"] = role      # role taken from the cookie
        return None                            # permit everything by default

    # -- M16 [A10] the error handler renders the traceback to the client ----
    @app.errorhandler(Exception)
    def show_error(exc):
        import traceback
        from flask import render_template
        return render_template("error.html",
                               trace=traceback.format_exc(),
                               message=str(exc)), 500

    from .mvc import shop, account, cart, admin_mvc, support
    from .api import products, orders, users, importer, reset, reports, search, auth

    for bp in (shop.bp, account.bp, cart.bp, admin_mvc.bp, support.bp,
               products.bp, orders.bp, users.bp, importer.bp,
               reset.bp, reports.bp, search.bp, auth.bp):
        app.register_blueprint(bp)

    with app.app_context():
        init_db()

    @app.context_processor
    def inject_globals():
        return {"current_user": getattr(g, "user", None), "version": VERSION}

    return app
