from flask import Blueprint, render_template
from app.core.session import require_student, add_module_result


bp = Blueprint("ips", __name__, url_prefix="/ips", template_folder="templates", static_folder="static")

MODULE_META = {"slug": "ips", "name": "IPS"}


@bp.route("/instructions")
def instructions():
    guard = require_student()
    if guard:
        return guard
    return render_template("ips/instructions.html")


@bp.route("/result")
def result():
    guard = require_student()
    if guard:
        return guard
    add_module_result("ips", {"slug": "ips", "summary": "Placeholder result"})
    return render_template("ips/result.html")

