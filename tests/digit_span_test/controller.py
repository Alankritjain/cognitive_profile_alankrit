from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .models import DigitSpanTest
import random

# Blueprint
digit_span_bp = Blueprint(
    "digit_span",
    __name__,
    url_prefix="/digit-span",
    template_folder="templates",
    static_folder="static"   # 👈 add this
)




@digit_span_bp.route("/instructions")
def instructions():
    session.clear()
    return render_template("digit_span/instructions.html")

@digit_span_bp.route("/setup", methods=["GET", "POST"])
def setup():
    """
    Collects student details (name, age, class) before starting the test.
    Always starts with FORWARD mode first.
    """
    if request.method == "POST":
        session["student_name"] = request.form.get("name")
        session["student_age"] = int(request.form.get("age"))
        session["student_class"] = request.form.get("class")

        # Always begin with forward mode
        return redirect(url_for("digit_span.start_test", mode="forward"))

    return render_template("digit_span/setup.html")


@digit_span_bp.route("/start/<mode>")
def start_test(mode):
    if mode not in ["forward", "backward"]:
        mode = "forward"

    if "span_length" not in session:
        session["span_length"] = 2
        session["fails"] = 0
        session["max_span_forward"] = 0
        session["max_span_backward"] = 0
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
    correct_sequence = session.get("digit_sequence", [])
    mode = session.get("mode", "forward")

    user_sequence_str = request.form.get("user_sequence", "")
    user_sequence = [int(d) for d in user_sequence_str if d.isdigit()]

    if mode == "backward":
        correct_sequence = list(reversed(correct_sequence))

    if user_sequence == correct_sequence:
        if mode == "forward":
            session["max_span_forward"] = max(session["max_span_forward"], session["span_length"])
        else:
            session["max_span_backward"] = max(session["max_span_backward"], session["span_length"])
        session["span_length"] += 1
        session["fails"] = 0
    else:
        session["fails"] += 1
        if session["fails"] >= 2:
            if mode == "forward":
                # Switch to backward test
                session["mode"] = "backward"
                session["span_length"] = 2
                session["fails"] = 0
                return redirect(url_for("digit_span.start_test", mode="backward"))
            else:
                return redirect(url_for("digit_span.result"))

    return redirect(url_for("digit_span.start_test", mode=mode))


@digit_span_bp.route("/result")
def result():
    forward_raw = session.get("max_span_forward", 0)
    backward_raw = session.get("max_span_backward", 0)

    student = DigitSpanTest(
        name=session.get("student_name", "Anonymous"),
        age=session.get("student_age", 0),
        student_class=session.get("student_class", "NA"),
        forward_raw=forward_raw,
        backward_raw=backward_raw
    )

    if request.args.get("format") == "json":
        return jsonify(student.to_dict())

    return render_template("digit_span/result.html", result=student.to_dict())
