"""
Resume Fit - Flask application.

Two routes:
  /           serves the page
  /api/analyse  takes a resume file + job text, returns the analysis as JSON

The front end calls /api/analyse with fetch, so results appear without a
page reload. That is what lets the score animate in.
"""

import json
import os

from flask import Flask, jsonify, render_template, request

import analyzer

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload cap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_jobs():
    with open(os.path.join(BASE_DIR, "data", "jobs.json"), encoding="utf-8") as f:
        return json.load(f)


JOBS = load_jobs()


@app.route("/")
def index():
    return render_template("index.html", jobs=JOBS)


@app.route("/api/analyse", methods=["POST"])
def api_analyse():
    # --- validate the upload ---
    if "resume" not in request.files:
        return jsonify({"error": "No resume was uploaded."}), 400

    uploaded = request.files["resume"]
    if not uploaded.filename:
        return jsonify({"error": "No file selected."}), 400

    allowed = (".pdf", ".docx", ".txt")
    if not uploaded.filename.lower().endswith(allowed):
        return jsonify({"error": "Upload a PDF, DOCX or TXT file."}), 400

    # --- validate the job side ---
    mode = request.form.get("mode", "library")

    if mode == "custom":
        job_text = request.form.get("job_text", "").strip()
        if len(job_text) < 60:
            return jsonify({
                "error": "That job description is too short to analyse. "
                         "Paste the full posting, including the requirements."
            }), 400
        job_label = request.form.get("job_title", "").strip() or "Your pasted role"
    else:
        try:
            index_value = int(request.form.get("job_index", 0))
            job = JOBS[index_value]
        except (ValueError, IndexError):
            return jsonify({"error": "That role could not be found."}), 400
        job_text = f"{job['title']} {job['description']}"
        job_label = f"{job['title']} at {job['company']}"

    # --- read the resume ---
    resume_text, error = analyzer.extract_text(uploaded, uploaded.filename)
    if error:
        return jsonify({"error": error}), 400

    if len(resume_text.split()) < 40:
        return jsonify({
            "error": "Very little text was found in that file. If it is a "
                     "scanned PDF, export a text-based version instead."
        }), 400

    # --- analyse ---
    fit = analyzer.analyse_fit(resume_text, job_text)
    verdict_label, verdict_note = fit["verdict"]

    checks = analyzer.health_checks(resume_text, uploaded.filename)

    return jsonify({
        "job_label": job_label,
        "score": fit["score"],
        "coverage": fit["coverage"],
        "wording": fit["wording"],
        "verdict": verdict_label,
        "verdict_note": verdict_note,
        "matched": fit["matched"],
        "missing": fit["missing"],
        "extra": fit["extra"][:12],
        "plan": analyzer.learning_plan(fit["missing"], limit=6),
        "checks": [
            {"name": n, "state": ("pass" if p is True
                                  else "warn" if p is None else "fail"),
             "message": m}
            for n, p, m in checks
        ],
        "health_score": analyzer.health_score(checks),
        "recommendations": [
            {"title": j["title"], "company": j["company"], "level": j["level"],
             "location": j["location"], "score": j["score"]}
            for j in analyzer.recommend_jobs(resume_text, JOBS, top_n=5)
        ],
    })


@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": "That file is larger than 5 MB."}), 413


if __name__ == "__main__":
    app.run(debug=True, port=8000)
