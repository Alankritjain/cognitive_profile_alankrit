from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .models import DigitSpanTest
import random

# Blueprint specific to Digit Span Test
digit_span_bp = Blueprint(
    "digit_span",
    __name__,
    url_prefix="/digit-span",
    template_folder="templates"
)




@digit_span_bp.route("/instructions")
def instructions():
    """
    Instructions page for the Digit Span Test.
    Clears session so every test starts fresh.
    """
    session.clear()
    return render_template("digit_span/instructions.html")


@digit_span_bp.route("/setup", methods=["GET", "POST"])
def setup():
    """
    Collects student details (name, age, class) and chosen mode before starting the test.
    """
    if request.method == "POST":
        session["student_name"] = request.form.get("name")
        session["student_age"] = int(request.form.get("age"))
        session["student_class"] = request.form.get("class")
        mode = request.form.get("mode")

        return redirect(url_for("digit_span.start_test", mode=mode))

    return render_template("digit_span/setup.html")


@digit_span_bp.route("/start/<mode>")
def start_test(mode):
    """
    Starts or continues the Digit Span Test.
    Mode = 'forward' or 'backward'.
    Generates a random sequence of digits based on current span length.
    """
    if mode not in ["forward", "backward"]:
        mode = "forward"

    # Initialize session variables on first run
    if "span_length" not in session:
        session["span_length"] = 3  # starting length
        session["fails"] = 0
        session["max_span"] = 0
        session["mode"] = mode

    span_length = session["span_length"]
    sequence = [random.randint(0, 9) for _ in range(span_length)]
    session["digit_sequence"] = sequence

    return render_template(
        "digit_span/test.html",
        sequence=sequence,
        span_length=span_length,
        mode=session["mode"]
    )


@digit_span_bp.route("/check", methods=["POST"])
def check_sequence():
    """
    Checks user input against the stored sequence.
    Supports both forward and backward modes.
    Applies stop rule: two consecutive fails end the test.
    """
    correct_sequence = session.get("digit_sequence", [])
    mode = session.get("mode", "forward")

    user_sequence_str = request.form.get("user_sequence", "")
    user_sequence = [int(d) for d in user_sequence_str if d.isdigit()]

    # Adjust for backward mode
    if mode == "backward":
        correct_sequence = list(reversed(correct_sequence))

    if user_sequence == correct_sequence:
        # Correct → update max span and increase span length
        session["max_span"] = max(session["max_span"], session["span_length"])
        session["span_length"] += 1
        session["fails"] = 0
    else:
        # Incorrect → increase fail count
        session["fails"] += 1
        if session["fails"] >= 2:
            return redirect(url_for("digit_span.result"))

    # Continue test
    return redirect(url_for("digit_span.start_test", mode=mode))


@digit_span_bp.route("/result")
def result():
    """
    Final results page after stop rule.
    Uses DigitSpanTest class to calculate z-scores, percentiles, and categories.
    """
    max_span = session.get("max_span", 0)
    mode = session.get("mode", "forward")

    # Assign forward/backward raw score based on mode
    forward_raw = max_span if mode == "forward" else 0
    backward_raw = max_span if mode == "backward" else 0

    # Get student details from session
    student = DigitSpanTest(
        name=session.get("student_name", "Anonymous"),
        age=session.get("student_age", 0),
        student_class=session.get("student_class", "NA"),
        forward_raw=forward_raw,
        backward_raw=backward_raw
    )

    # JSON output option
    if request.args.get("format") == "json":
        return jsonify(student.to_dict())

    return render_template("digit_span/result.html", result=student.to_dict())
