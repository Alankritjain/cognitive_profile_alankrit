from flask import Blueprint, render_template
from app.core.session import require_student, add_module_result


bp = Blueprint("att", __name__, url_prefix="/att", template_folder="templates", static_folder="static")

MODULE_META = {"slug": "att", "name": "ATT"}


@bp.route("/instructions")
def instructions():
    guard = require_student()
    if guard:
        return guard
    return render_template("att/instructions.html")


@bp.route("/result")
def result():
    guard = require_student()
    if guard:
        return guard
    add_module_result("att", {"slug": "att", "summary": "Placeholder result"})
    return render_template("att/result.html")

