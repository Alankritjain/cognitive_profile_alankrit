# Cognitive Profiling Test (Flask)

A modular Flask application for running cognitive assessments. The current focus is the WMC (Working Memory Capacity) module, which contains three tests: Forward Digit Span, Backward Digit Span, and an N‑2 Span test. The app is organized so additional modules (IRA, ATT, META, IPS, ALS) can be built independently and orchestrated in sequence.

## Features

- Student setup with modern UI
  - Name, DOB with auto‑calculated age (10–18), class selection chips (VI–XII)
  - “Start Test” enables only when inputs are valid
- Dashboard with tiles and “Start All Tests” button
- WMC module
  - Forward Digit Span with lives and span growth
  - Backward Digit Span with transition overlay and lives
  - N‑2 Span test (20 attempts) on a labeled grid; digits flash for 500ms; recall digit from two nodes earlier; per‑attempt green/red feedback
  - Results page with forward/backward raw + z‑scores, percentiles, categories, and N‑2 percentage
- Orchestrator to sequence tests and show a consolidated summary

## Quick Start

```bash
cd cognitive_profile_alankrit
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt

# Create a local .env (optional; see .env.example)
copy .env.example .env   # Windows
# cp .env.example .env    # macOS/Linux

python run.py
# http://127.0.0.1:5000/
```

## Environment

Create a `.env` file (not committed) using `.env.example` as a template.

- `SECRET_KEY`: Flask session key (random string)
- `OPENAI_API_KEY`: optional; for future ChatGPT integration

## Folder Structure (high‑level)

```
cognitive_profile_alankrit/
  run.py
  requirements.txt
  .gitignore
  .env.example
  app/
    __init__.py           # App factory; registers blueprints
    routes.py             # Root, tiles, change-student
    templates/
      base.html
      home.html           # Tiles & Start All Tests
      summary.html        # Orchestrator summary
    static/
      css/style.css
    core/
      session.py          # require_student, add_module_result
    orchestrator/
      registry.py         # Module registry and order
      routes.py           # /run/start, /run/next, /run/summary
    modules/
      wmc/
        __init__.py
        routes.py         # Forward/Backward + N‑2 routes
        models.py         # Scoring for digit span
        templates/wmc/
          setup.html      # Modern setup (name, DOB→age, class chips)
          instructions.html
          test.html       # Forward/Backward UI
          n2.html         # N‑2 Span UI
          result.html
        static/css/style.css
      ira/, att/, meta/, ips/, als/  # Skeletons for future modules
```

## WMC Scoring

Digit Span scoring uses age‑band norms (10–13, 14–16, 17–18) with z‑scores, percentiles, and categories (Impaired → Superior). N‑2 reports percentage correct out of 20 attempts.

## Contributing — Module Contract

- Each module exposes a Flask blueprint named by its slug (`wmc`, `ira`, etc.) and a `MODULE_META` dict.
- Endpoints: `setup` (if needed), `instructions`, `start`, `check`, `result`.
- Results are added to session via `add_module_result(slug, dict)` for orchestration.

## License

For internal development use. Add a license if you plan to open source.

