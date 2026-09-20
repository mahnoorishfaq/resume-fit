# Resume Fit

A web app that reads your resume against a job ad and tells you what a
screening system would see: which skills landed, which are missing, what to
learn next, and whether the resume itself is well built.

Built with Flask, scikit-learn and vanilla JavaScript. No framework, no
build step.

---

## Running it

**1. Open the folder in VS Code**

File -> Open Folder -> select `resumefit`

**2. Create and activate a virtual environment**

Terminal -> New Terminal, then:

```
python -m venv venv
venv\Scripts\activate
```

`(venv)` should appear at the start of your prompt. On Mac or Linux use
`source venv/bin/activate`.

If Windows blocks the activate script, run this once first:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**3. Install the packages**

```
pip install -r requirements.txt
```

On a slow connection, add `--timeout 120 --retries 10`.

**4. Start the server**

```
python app.py
```

**5. Open http://localhost:8000 in your browser**

To stop it, press Ctrl+C in the terminal.

---

## Using it

**Step 1 — upload your resume.** Drag a file onto the panel or click to
browse. PDF, DOCX or TXT, up to 5 MB. Export from Word or Google Docs as
PDF for the best results; a scanned or photographed resume has no readable
text in it.

**Step 2 — give it a job.** Two ways:

- **Paste a job ad** (the default). Copy a real posting from LinkedIn,
  Indeed, Rozee.pk or a company careers page and paste the whole thing.
  Include the requirements section — that is where the skills are. The
  counter tells you when there is enough text.
- **Try a sample role.** Twelve realistic job descriptions bundled with the
  app, for testing it without hunting for a posting first.

**Step 3 — press Check the match.**

There is a test resume at `data/sample_resume.txt` if you want to see the
output before using your own.

---

## What you get back

**Fit score.** Skill coverage weighted at 75%, wording similarity at 25%.
Matching the skills a job asks for matters more than echoing its vocabulary.

**Skills that landed / skills missing.** Split by what your resume actually
shows against what the job asks for.

**What to learn next.** Each missing skill comes with a specific action, not
a link dump. Skills that appear in many job ads and rarely in student
resumes are flagged as high leverage and sorted first.

**Resume health.** Eight checks that run on your document alone: contact
details, portfolio links, length, section headings, quantified results,
action verbs, filler phrases, file format.

**Roles that fit you better.** Your resume scored against all twelve sample
roles and ranked, so you can spot the direction you already suit.

---

## Project structure

```
resumefit/
├── app.py                 Flask routes
├── analyzer.py            text extraction, matching, scoring, checks
├── skills_db.py           skill taxonomy with aliases and learning notes
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/app.js
└── data/
    ├── jobs.json          the sample role library
    └── sample_resume.txt  a test resume
```

---

## Adding your own jobs

`data/jobs.json` is a plain list. Add entries in the same shape:

```json
{
  "title": "Job title",
  "company": "Company name",
  "level": "Internship",
  "location": "Remote",
  "description": "The full job description text."
}
```

Save and restart the app. New roles appear in the sample list and in the
recommendations.

## Adding skills

`skills_db.py` holds the skill dictionary. Each entry has aliases (so
"sklearn" and "scikit-learn" resolve to the same skill), a category, and a
learning note. Adding entries here is the fastest way to make the tool more
accurate.

---

## How the matching works

Skills are found by matching against a dictionary of aliases with word
boundaries enforced, so "R" does not match every word containing the letter
r. Wording similarity uses TF-IDF cosine similarity from scikit-learn.

TF-IDF was chosen over sentence embeddings deliberately: it runs in
milliseconds with no model download, which keeps the app deployable on a
free tier.

## Known limitations

- The matcher cannot tell a skill you **used** from one you merely
  **listed**. A keyword-stuffed skills section scores well.
- Skill detection is dictionary-based. A skill missing from `skills_db.py`
  is invisible to the tool.
- The health checks are heuristics, not rules. A short resume is not always
  a weak one.
- The sample jobs are representative examples, not live postings.

## Deploying

The app includes `gunicorn` in requirements. On Render, Railway or similar:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

No API keys or environment variables are needed.

## Privacy

Uploaded files are read into memory, analysed, and discarded. Nothing is
written to disk and nothing is stored.
