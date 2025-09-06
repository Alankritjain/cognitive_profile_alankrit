# app/routes.py
from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def root():
    # Always collect student details first
    return redirect(url_for("wmc.setup"))


@main_bp.route("/tests")
def tests():
    # Tiles page should be accessible only after setup
    if not session.get("student"):
        return redirect(url_for("wmc.setup"))
    return render_template("home.html", student=session["student"])


@main_bp.route("/change-student")
def change_student():
    # Clear current student context and go back to setup
    session.clear()
    return redirect(url_for("wmc.setup"))
