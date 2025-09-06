# tests/digit_span_test/controller.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from .models import DigitSpanTest
import random

digit_span_bp = Blueprint(
    "digit_span",
    __name__,
    url_prefix="/digit-span",
    template_folder="templates",
    static_folder="static"
)

def require_student():
    """Guard to ensure setup is completed before accessing tests."""
    if not session.get("student"):
        return redirect(url_for("digit_span.setup"))
    return None

# ---------- SETUP (single route, unique function name, endpoint kept as 'setup') ----------
@digit_span_bp.route("/setup", methods=["GET", "POST"], endpoint="setup")
def student_setup():
    if request.method == "POST":
        # Save student details
        student = {
            "name": (request.form.get("name") or "").strip(),
            "age": int(request.form.get("age", 0) or 0),
            "class": (request.form.get("class") or "").strip(),
        }

        # Reset session for a clean run
        session.clear()
        session["student"] = student

        # Initialize test state (safe defaults)
        session["mode"] = "forward"
        session["span_length"] = 2
        session["fails"] = 0
        session["max_span_forward"] = 0
        session["max_span_backward"] = 0

        # After setup, go to tiles page
        return redirect(url_for("main.tests"))

    return render_template("digit_span/setup.html")

# ---------- INSTRUCTIONS ----------
@digit_span_bp.route("/instructions", methods=["GET"])
def instructions():
    guard = require_student()
    if guard:
        return guard
    return render_template("digit_span/instructions.html", student=session["student"])

# ---------- START TEST ----------
@digit_span_bp.route("/start/<mode>", methods=["GET", "POST"])
def start_test(mode):
    guard = require_student()
    if guard:
        return guard

    if mode not in ["forward", "backward"]:
        mode = "forward"

    # Always record current mode
    session["mode"] = mode

    # Initialize defaults if missing
    if "span_length" not in session:
        session["span_length"] = 2
    if "fails" not in session:
        session["fails"] = 0
    if "max_span_forward" not in session:
        session["max_span_forward"] = 0
    if "max_span_backward" not in session:
        session["max_span_backward"] = 0

    span_length = session["span_length"]
    sequence = [random.randint(0, 9) for _ in range(span_length)]
    session["digit_sequence"] = sequence

    return render_template(
        "digit_span/test.html",
        sequence=sequence,
        span_length=span_length,
        mode=session["mode"]
    )

# ---------- CHECK ANSWER ----------
@digit_span_bp.route("/check", methods=["POST"])
def check_sequence():
    guard = require_student()
    if guard:
        return guard

    correct_sequence = session.get("digit_sequence", [])
    mode = session.get("mode", "forward")

    user_sequence_str = request.form.get("user_sequence", "")
    user_sequence = [int(d) for d in user_sequence_str if d.isdigit()]

    if mode == "backward":
        correct_sequence = list(reversed(correct_sequence))

    if user_sequence == correct_sequence:
        # Correct → increase span, reset fails, update max span
        if mode == "forward":
            session["max_span_forward"] = max(session["max_span_forward"], session["span_length"])
        else:
            session["max_span_backward"] = max(session["max_span_backward"], session["span_length"])
        session["span_length"] += 1
        session["fails"] = 0
    else:
        # Incorrect
        session["fails"] += 1
        if session["fails"] >= 2:
            if mode == "forward":
                # Switch to backward test (NOTE: if you want a transition screen, we can redirect there instead)
                session["mode"] = "backward"
                session["span_length"] = 2
                session["fails"] = 0
                return redirect(url_for("digit_span.start_test", mode="backward"))
            else:
                return redirect(url_for("digit_span.result"))

    return redirect(url_for("digit_span.start_test", mode=mode))

# ---------- RESULT ----------
@digit_span_bp.route("/result")
def result():
    guard = require_student()
    if guard:
        return guard

    forward_raw = session.get("max_span_forward", 0)
    backward_raw = session.get("max_span_backward", 0)
    student_info = session.get("student", {})  # dict: name, age, class

    # Build the model using dict values
    student = DigitSpanTest(
        name=student_info.get("name", "Anonymous"),
        age=student_info.get("age", 0),
        student_class=student_info.get("class", "NA"),
        forward_raw=forward_raw,
        backward_raw=backward_raw
    )

    if request.args.get("format") == "json":
        return jsonify(student.to_dict())

    return render_template("digit_span/result.html", result=student.to_dict(), student=student_info)
