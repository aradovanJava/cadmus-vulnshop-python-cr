"""Bulk import — the remote code execution chain."""
import base64
import pickle
import yaml
from flask import Blueprint, request, jsonify

bp = Blueprint("api_import", __name__, url_prefix="/api")


@bp.post("/import/session")
def import_session():
    """-- T14 [A08] unauthenticated deserialisation of attacker bytes ------
    pickle is an instruction set, not a data format: __reduce__ lets a
    crafted payload call anything. There is no authentication on this
    route. This is a genuine remote code execution chain, not a simulated
    one — which is why the application must stay bound to 127.0.0.1.
    Bandit B301/B403.
    """
    blob = base64.b64decode(request.data or b"")
    state = pickle.loads(blob)
    return jsonify(restored=str(state))


@bp.post("/import/catalogue")
def import_catalogue():
    """-- T15 [A08·A03] yaml.full_load on an uploaded document -------------
    FullLoader still constructs Python objects through the !!python tags.
    This is the reachable sink that makes the pinned PyYAML advisory a
    genuine finding rather than a theoretical one — the dependency alone
    is harmless, and the sink alone would be harmless with safe_load.
    A tool sees one or the other; a human joins them.
    """
    doc = yaml.load(request.data or b"{}", Loader=yaml.FullLoader)
    return jsonify(parsed=str(doc))
