from flask import session, redirect, url_for


def require_student():
    """Ensure student details are present in session; otherwise redirect to setup.

    Returns a redirect response when student context is missing, else None.
    """
    if not session.get("student"):
        return redirect(url_for("wmc.setup"))
    return None


def add_module_result(slug: str, result: dict) -> None:
    """Store a module's result under the orchestrator sequence state in session."""
    seq = session.get("sequence") or {}
    results = seq.get("results") or {}
    results[slug] = result
    seq["results"] = results
    session["sequence"] = seq

