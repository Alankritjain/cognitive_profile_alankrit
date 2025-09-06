from flask import Blueprint, render_template
from app.core.session import require_student, add_module_result


bp = Blueprint("als", __name__, url_prefix="/als", template_folder="templates", static_folder="static")

MODULE_META = {"slug": "als", "name": "ALS"}


@bp.route("/instructions")
def instructions():
    guard = require_student()
    if guard:
        return guard
    return render_template("als/instructions.html")


@bp.route("/result")
def result():
    guard = require_student()
    if guard:
        return guard
    add_module_result("als", {"slug": "als", "summary": "Placeholder result"})
    return render_template("als/result.html")

