"""Report generation and download."""
import os
import subprocess
from flask import Blueprint, request, jsonify, send_file, Response

bp = Blueprint("api_reports", __name__, url_prefix="/api")

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "reports")


@bp.post("/reports/generate")
def generate():
    """-- T2 [A05] OS command injection through a shell ------------------
    fmt reaches a shell, so a semicolon runs a second command with the
    privileges of the application process. Bandit B602/B605.
    Payload:  {"format": "csv; id"}
    """
    fmt = request.json.get("format", "csv")
    name = request.json.get("name", "orders")
    os.makedirs(REPORT_DIR, exist_ok=True)
    cmd = "echo generating %s report > %s/%s.%s" % (fmt, REPORT_DIR, name, fmt)
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
    return jsonify(command=cmd, stdout=out.stdout, stderr=out.stderr)


@bp.get("/reports/download")
def download():
    """-- T3 [A01] path traversal on the download parameter --------------
    The filename is joined to the report directory with no containment
    check, so ../ escapes it. os.path.join is not a security control.
    Payload:  ?file=../vulnshop/services/crypto.py
    """
    filename = request.args.get("file", "orders.csv")
    path = os.path.join(REPORT_DIR, filename)
    if not os.path.exists(path):
        return jsonify(error="no such report", looked_at=path), 404
    with open(path, "rb") as fh:
        return Response(fh.read(), mimetype="text/plain")
