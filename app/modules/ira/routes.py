from flask import Blueprint, render_template
from app.core.session import require_student, add_module_result


bp = Blueprint("ira", __name__, url_prefix="/ira", template_folder="templates", static_folder="static")

MODULE_META = {"slug": "ira", "name": "IRA"}


@bp.route("/instructions")
def instructions():
    guard = require_student()
    if guard:
        return guard
    return render_template("ira/instructions.html")


@bp.route("/result")
def result():
    guard = require_student()
    if guard:
        return guard
    # Placeholder result; replace with real computation
    add_module_result("ira", {"slug": "ira", "summary": "Placeholder result"})
    return render_template("ira/result.html")

