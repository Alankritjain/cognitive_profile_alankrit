from flask import Flask
import os


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Secret key required for session
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(24)

    # Register main routes blueprint (home/tiles/change-student)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Register runner/orchestrator blueprint (handles multi-test flow)
    try:
        from app.orchestrator.routes import run_bp
        app.register_blueprint(run_bp)
    except Exception:
        # Allow app to run even if runner not ready during development
        pass

    # Register all test modules via registry
    try:
        from app.orchestrator.registry import MODULES
        for mod in MODULES:
            app.register_blueprint(mod["bp"])  # each module exposes a Blueprint as `bp`
    except Exception:
        # Allow app to run even if modules aren't fully wired yet
        pass

    return app

