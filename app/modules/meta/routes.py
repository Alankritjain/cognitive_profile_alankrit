from flask import Blueprint, render_template
from app.core.session import require_student, add_module_result


bp = Blueprint("meta", __name__, url_prefix="/meta", template_folder="templates", static_folder="static")

MODULE_META = {"slug": "meta", "name": "META"}


@bp.route("/instructions")
def instructions():
    guard = require_student()
    if guard:
        return guard
    return render_template("meta/instructions.html")


@bp.route("/result")
def result():
    guard = require_student()
    if guard:
        return guard
    add_module_result("meta", {"slug": "meta", "summary": "Placeholder result"})
    return render_template("meta/result.html")

