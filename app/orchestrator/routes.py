from flask import Blueprint, session, redirect, url_for, render_template
from .registry import MODULES


run_bp = Blueprint("run", __name__, url_prefix="/run")


def _order():
    return [m["meta"]["slug"] for m in MODULES]


@run_bp.route("/start")
def start():
    # Ensure student exists; otherwise go to WMC setup (first module)
    if not session.get("student"):
        return redirect(url_for("wmc.setup"))

    session["sequence"] = {"index": 0, "order": _order(), "results": {}}
    first = session["sequence"]["order"][0]
    return redirect(url_for(f"{first}.instructions"))


@run_bp.route("/next")
def next():
    seq = session.get("sequence") or {}
    order = seq.get("order") or _order()
    idx = int(seq.get("index", 0)) + 1

    seq["index"] = idx
    session["sequence"] = seq

    if idx >= len(order):
        return redirect(url_for("run.summary"))

    slug = order[idx]
    return redirect(url_for(f"{slug}.instructions"))


@run_bp.route("/summary")
def summary():
    seq = session.get("sequence") or {}
    results = seq.get("results") or {}
    student = session.get("student") or {}
    return render_template("summary.html", results=results, student=student)

