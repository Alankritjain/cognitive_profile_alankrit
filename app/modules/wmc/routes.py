from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.core.session import require_student, add_module_result
from .models import DigitSpanTest
import random


bp = Blueprint(
    "wmc",
    __name__,
    url_prefix="/wmc",
    template_folder="templates",
    static_folder="static",
)

MODULE_META = {
    "slug": "wmc",
    "name": "WMC",
}


@bp.route("/setup", methods=["GET", "POST"], endpoint="setup")
def setup():
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

    return render_template("wmc/setup.html")


@bp.route("/instructions", methods=["GET"])
def instructions():
    guard = require_student()
    if guard:
        return guard
    return render_template("wmc/instructions.html", student=session["student"])


@bp.route("/start/<mode>", methods=["GET", "POST"], endpoint="start")
def start(mode):
    guard = require_student()
    if guard:
        return guard

    if mode not in ["forward", "backward"]:
        mode = "forward"

    # Always record current mode
    prev_mode = session.get("mode")
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
    if "lives" not in session:
        session["lives"] = 2

    # If user navigated to a different mode manually, reset counters for new phase
    if prev_mode and prev_mode != mode:
        session["fails"] = 0
        session["lives"] = 2

    span_length = session["span_length"]
    sequence = [random.randint(0, 9) for _ in range(span_length)]
    session["digit_sequence"] = sequence

    # Show overlay when entering backward phase after forward
    show_backward_overlay = False
    if mode == "backward":
        show_backward_overlay = bool(session.pop("show_backward_overlay", False))

    return render_template(
        "wmc/test.html",
        sequence=sequence,
        span_length=span_length,
        mode=session["mode"],
        show_backward_overlay=show_backward_overlay,
    )


@bp.route("/check", methods=["POST"], endpoint="check")
def check():
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
        # Correct: increase span, reset fails, update max span
        if mode == "forward":
            session["max_span_forward"] = max(
                session["max_span_forward"], session["span_length"]
            )
        else:
            session["max_span_backward"] = max(
                session["max_span_backward"], session["span_length"]
            )
        session["span_length"] += 1
        session["fails"] = 0
        session["lives"] = 2
    else:
        # Incorrect
        session["fails"] += 1
        # Decrease lives but not below 0
        session["lives"] = max(int(session.get("lives", 2)) - 1, 0)
        if session["fails"] >= 2:
            if mode == "forward":
                # Switch to backward test
                session["mode"] = "backward"
                session["span_length"] = 2
                session["fails"] = 0
                session["lives"] = 2
                session["show_backward_overlay"] = True
                return redirect(url_for("wmc.start", mode="backward"))
            else:
                # After backward phase ends, start N-2 Span test
                return redirect(url_for("wmc.n2"))

    return redirect(url_for("wmc.start", mode=mode))


@bp.route("/result")
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
        backward_raw=backward_raw,
    )

    # Include N-2 Span results if available
    n2_attempts = int(session.get("n2_attempts", 0))
    n2_correct = int(session.get("n2_correct", 0))
    n2_percentage = float(session.get("n2_percentage", 0.0))

    # Store in orchestrator session results (if present)
    try:
        d = student.to_dict()
        d.update({
            "n2_attempts": n2_attempts,
            "n2_correct": n2_correct,
            "n2_percentage": n2_percentage,
        })
        add_module_result("wmc", d)
    except Exception:
        pass

    if request.args.get("format") == "json":
        out = student.to_dict()
        out.update({
            "n2_attempts": n2_attempts,
            "n2_correct": n2_correct,
            "n2_percentage": n2_percentage,
        })
        return jsonify(out)

    return render_template(
        "wmc/result.html",
        result=student.to_dict(),
        student=student_info,
        n2_attempts=n2_attempts,
        n2_correct=n2_correct,
        n2_percentage=n2_percentage,
    )


# ---------- N-2 SPAN TEST ----------
@bp.route("/n2")
def n2():
    guard = require_student()
    if guard:
        return guard

    attempts = 20
    offset = 2
    total_nodes = attempts + offset

    # Generate random sequence for nodes
    digits = [random.randint(0, 9) for _ in range(total_nodes)]

    # Persist basic params for result calculation
    session["n2_attempts"] = attempts
    session["n2_digits"] = digits
    session["n2_offset"] = offset

    # Build labels A.. for each node
    labels = [chr(ord('A') + i) for i in range(total_nodes)]

    return render_template(
        "wmc/n2.html",
        labels=labels,
        digits=digits,
        attempts=attempts,
        offset=offset,
    )


@bp.route("/n2/submit", methods=["POST"])
def n2_submit():
    guard = require_student()
    if guard:
        return guard

    # Accept form-encoded values
    try:
        correct = int(request.form.get("correct", 0))
        attempts = int(request.form.get("attempts", 20))
    except Exception:
        correct = 0
        attempts = int(session.get("n2_attempts", 20))

    percentage = round((correct / attempts) * 100.0 if attempts else 0.0, 2)
    session["n2_correct"] = correct
    session["n2_percentage"] = percentage

    return redirect(url_for("wmc.result"))
