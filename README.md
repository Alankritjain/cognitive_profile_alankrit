# 🧠 Cognitive Profile Project – Digit Span Test App

A Flask-based web application to conduct **Digit Span Tests** (Forward & Backward) for assessing **Working Memory Capacity (WMC)** as part of a larger **Cognitive Profiling Platform**.

---

## 📌 Features

- **Student Setup**
  - Collects name, age, and class.
  - Student info persists in session for the test run.
- **Test Selection Dashboard**
  - Modern 6-tile UI for cognitive profiling modules:
    - WMC (Working Memory Capacity) → Digit Span Test ✅
    - IRA (Information Retrieval Ability) – Coming Soon
    - ATT (Attention) – Coming Soon
    - META (Metacognition) – Coming Soon
    - IPS (Information Processing Speed) – Coming Soon
    - ALS (Active Learning Style) – Coming Soon
- **Digit Span Test**
  - Forward Test: Repeat digits in the same order.
  - Backward Test: Repeat digits in reverse order.
  - Transition screen with instructions before switching to backward test.
  - Stop rule: two consecutive errors end a phase.
- **Results**
  - Shows raw scores, z-scores, percentiles, and performance categories.
  - Option to **download results as JSON**.
  - Student info and summary visible.
  - Buttons to choose another test or change student.
- **Modern UI**
  - Bootstrap 5 styling.
  - Responsive tile-based dashboard.
  - Clean digit display and keypad layout.

---

## 📂 Folder Structure

COGNITIVE_PROFILE_PROJECT/
│
├── run.py # Entry point to run the Flask app
├── requirements.txt # Dependencies
├── .gitignore # Ignores venv, pycache, etc.
│
├── app/
│ ├── init.py # Flask app factory
│ ├── routes.py # Root + test selection routes
│ ├── static/css/style.css # Global stylesheet
│ └── templates/
│ ├── base.html # Common base template
│ └── home.html # Tile dashboard (tests selection)
│
├── tests/
│ └── digit_span_test/ # Digit Span module
│ ├── init.py
│ ├── controller.py # Routes and test logic
│ ├── models.py # DigitSpanTest scoring model
│ ├── static/css/style.css # Test-specific CSS
│ └── templates/digit_span/
│ ├── setup.html # Student info form
│ ├── instructions.html # Test instructions
│ ├── test.html # Test interface (digit display + keypad)
│ ├── transition.html # Forward→Backward transition
│ └── result.html # Results page
│
└── venv/ # Virtual environment (ignored in Git)

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd COGNITIVE_PROFILE_PROJECT

2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows
# source venv/bin/activate  # On Mac/Linux

3. Install dependencies
pip install -r requirements.txt

🚀 Running the App
python run.py

By default, the app runs at:
👉 http://127.0.0.1:5000/

🧪 Workflow

Setup Page – Enter student details.

Test Selection (Tiles) – Choose WMC → Digit Span.

Instructions Page – Read how the test works.

Forward Test – Digits appear, student repeats them in order.

Transition Page – Short instructions before backward phase.

Backward Test – Digits appear, student repeats them in reverse.

Results Page – View/download results.

📊 Scoring Norms

Based on age norms:

Age 10–13 → mean 7.1, sd 1.5

Age 14–16 → mean 7.9, sd 1.5

Age 17–18 → mean 8.0, sd 1.5

Categories:

Impaired (<10th percentile)

Below Average (10–25th percentile)

Average (26–74th percentile)

Above Average (75–89th percentile)

Superior (≥90th percentile)

🛠️ Roadmap

 Add N-back Test (Working Memory update)

 Add Spatial Memory Test (grid-based)

 Add Attention module

 Add Firestore/SQLite backend for saving results

 Add user authentication (teacher dashboard)

 Deploy on Heroku / Render
```
