# CareerPrep Job-Hunting Agent — Tailored for Abdul Mukeet

A beginner-friendly, **file-driven AI agent** that helps **Abdul Mukeet**
(BS Artificial Intelligence, FAST National University) manage the full
job-hunting workflow: reading job posters, analysing his resume,
generating tailored suggestions, building interview questions from course
knowledge, tracking applications, and producing prioritised reminders.

Built around the **GAME framework** (Goal, Actions, Memory, Environment)
and tuned around an **AI / ML / Computer Vision / NLP / MLOps** profile.

---

## Candidate Profile

| Field | Value |
| --- | --- |
| Name | **Abdul Mukeet** |
| Degree | BS Artificial Intelligence (2022 – Expected 2026) |
| University | FAST National University, Faisalabad |
| Email | mukeet0123@gmail.com |
| Phone | +92 307 7447779 |
| Focus areas | Machine Learning, Computer Vision, NLP, MLOps, Agentic AI |
| Tools | Python, C++, SQL, TensorFlow, Scikit-learn, Pandas, NumPy, Docker, CI/CD, GitHub |
| Highlight projects | YAAP (FYP — voice/text app with translation & emotion-aware interaction), Applied Recommendation System, Game Store DB, GitHub Simulation in C++ |
| Experience | AI Intern, Tech Solutions Pvt. Ltd. (Jun – Aug 2025) |

The full resume lives in [input_resumes/my_resume.txt](input_resumes/my_resume.txt)
and is what the agent reads on every run.

---

## Folder Structure

```
job-hunting-agent/
├── app.py                  # main agent (menu + auto modes), tuned for Mukeet
├── requirements.txt        # optional PDF/DOCX dependencies
├── README.md
├── reflection.md
├── input_jobs/             # paste job posters here (.txt / .pdf)
├── input_resumes/          # Mukeet's resume (.txt / .pdf / .docx)
├── input_kb/               # course slides / notes (.txt / .pdf)
├── outputs/                # generated reports (auto-created)
├── tracker/                # applications.csv + reminders.txt
└── samples/                # tiny example files
```

---

## Quick Start

1. Install Python 3.10+.
2. (Optional) Install PDF / DOCX support:
   ```powershell
   pip install -r requirements.txt
   ```
3. Drop your real files into the three `input_*` folders. Mukeet's resume is
   already in `input_resumes/my_resume.txt` — add new job posters into
   `input_jobs/` and any course/interview notes into `input_kb/`.
4. Run the agent:
   ```powershell
   python app.py            # interactive menu
   python app.py --auto     # one-shot pipeline
   ```

---

## What the Agent Produces

Inside `outputs/`:

| File | Purpose |
| --- | --- |
| `job_analysis_report.txt` | AI/ML keywords detected across job posters |
| `skill_gap_report.txt` | Match score, matched skills, missing skills vs. Mukeet's resume |
| `tailored_resume_suggestions.txt` | AI-focused resume bullets + quality score & tips |
| `interview_questions.txt` | Technical (ML/CV/NLP/MLOps), HR, and KB-inspired questions |
| `preparation_plan.txt` | 7-day study plan focused on Mukeet's missing skills |
| `project_to_jd_mapping.txt` | Which of Mukeet's projects (YAAP, Recommender, etc.) support which JD skills |
| `cover_letter.txt` | Cover letter signed by **Abdul Mukeet** for the first tracker entry |
| `linkedin_outreach.txt` | Recruiter outreach message signed by Mukeet |
| `dashboard.txt` | Counts of applications by status |
| `final_agent_report.txt` | All sections combined |
| `agent_memory.json` | JSON snapshot of the last run |

Inside `tracker/`:

| File | Purpose |
| --- | --- |
| `applications.csv` | Application status, dates, next actions, notes (seeded with AI roles) |
| `reminders.txt` | Reminders grouped as **URGENT / Upcoming / Other** |

---

## Menu Options

```
=== CareerPrep Job-Hunting Agent (Abdul Mukeet — BS AI, FAST) ===
 1. Run full pipeline (analyse + generate all reports)
 2. Add a new application to the tracker
 3. Show application dashboard
 4. Show reminders (with urgency)
 5. Re-generate cover letter for first tracker entry
 6. Exit
```

---

## How It's Tailored for Mukeet

- **Keyword vocabulary** in `app.py` is tuned around Mukeet's stack:
  Python, C++, SQL, Machine Learning, Deep Learning, Computer Vision, NLP,
  MLOps, Agentic AI, LLMs / Prompt Engineering, Recommender Systems,
  TensorFlow, Scikit-learn, Pandas, NumPy, OpenCV, Hugging Face,
  Docker, CI/CD, GitHub Actions, Flask / FastAPI / Streamlit, OOP, etc.
- **Resume-bullet suggestions** are framed around AI workflows
  (model training, feature engineering, CV/NLP, Docker + CI/CD).
- **Cover letter** is automatically signed with Mukeet's name, email and
  phone, and references his FYP (**YAAP**), the Applied Recommendation
  System, and his AI internship at Tech Solutions Pvt. Ltd.
- **LinkedIn outreach** introduces him as a final-year BS AI student at
  FAST and links to his GitHub portfolio.
- **Seeded tracker rows** are AI-focused (Junior AI / ML Engineer,
  Computer Vision / MLOps Intern) instead of generic web roles.

All personalisation lives in clearly named constants (`CANDIDATE_NAME`,
`CANDIDATE_EMAIL`, …) at the top of `app.py`, so it can be re-tuned
later without touching the pipeline logic.

---

## Unique Features (beyond minimum spec)

- **Interactive CLI menu** plus `--auto` non-interactive mode.
- **PDF and DOCX reading** (optional, gracefully degrades if libs missing).
- **Resume Quality Score (0-100)** with concrete improvement tips.
- **Reminder urgency** labels: `OVERDUE`, `TODAY`, `TOMORROW`, `this week`.
- **Application dashboard** with counts per status.
- **Cover-letter generator** personalised from the tracker + matched skills,
  signed by Abdul Mukeet.
- **LinkedIn outreach message** template generator.
- **Project-to-JD mapping** (which of Mukeet's projects supports which job skill).
- **7-day preparation plan** focused on missing skills.
- **JSON memory file** (`outputs/agent_memory.json`) so the next run can
  compare progress.

---

## GAME Framework Mapping

- **Goal** — Help Abdul Mukeet go from scattered job material to a structured,
  AI-focused job-hunt workflow.
- **Actions** — read files, extract AI/ML keywords, match skills against
  Mukeet's resume, tailor resume bullets, generate interview questions,
  update tracker, produce reminders.
- **Memory** — `tracker/applications.csv`, `tracker/reminders.txt`, and
  `outputs/agent_memory.json`.
- **Environment** — local folders (`input_jobs/`, `input_resumes/`,
  `input_kb/`, `outputs/`, `tracker/`) and a GitHub repository.

---

## Notes

- The agent works on **`.txt` files only** by default — install the optional
  packages in `requirements.txt` to also support `.pdf` and `.docx`.
- Remove private contact information from any real job posters you paste.
- Edit `tracker/applications.csv` directly, or use **menu option 2** to add
  new applications interactively.
- To re-tailor the agent for a different candidate, update the
  `CANDIDATE_*` constants near the top of `app.py` and tweak the
  `KEYWORDS` list to match their stack.
