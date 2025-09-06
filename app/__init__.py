from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # ✅ Secret key required for session
    app.config["SECRET_KEY"] = os.urandom(24)

    # Import and register Digit Span blueprint
    from tests.digit_span_test.controller import digit_span_bp
    app.register_blueprint(digit_span_bp)

    # Import and register main routes blueprint
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
