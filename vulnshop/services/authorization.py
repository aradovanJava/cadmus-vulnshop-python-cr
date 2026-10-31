"""Authorisation decisions."""
from flask import g


def can_access(user, resource_owner_id) -> bool:
    """-- T18 [A10 -> A01] the finding that carries the CR1 debrief -------

    Bandit reports the bare except as B110 at LOW severity, because as a
    rule that is correct: try/except/pass is usually a code-quality issue.

    Here it sits inside an authorisation gate whose except branch returns
    True. Anyone who can induce a TypeError — by supplying a resource whose
    owner id is None, for instance — is authorised. Nothing in the syntax
    marks this method as a security decision, so only a human can re-rate
    it from Minor to Blocker.

    Participants met this shape in N1 (excerpt 3) and refactored it in N2.
    """
    try:
        if user is None:
            return False
        if user["role"] == "admin":
            return True
        return int(user["id"]) == int(resource_owner_id)
    except Exception:
        return True          # fail OPEN


def is_admin() -> bool:
    user = getattr(g, "user", None)
    return bool(user) and user["role"] == "admin"
