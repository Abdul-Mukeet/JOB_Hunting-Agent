"""
CareerPrep Job-Hunting Agent — tailored for Abdul Mukeet
========================================================
A file-driven AI agent that helps Abdul Mukeet (BS Artificial Intelligence,
FAST National University) manage the full job-hunting workflow:
- Reads job posters, resume, and knowledge-base notes from folders.
- Performs JD/resume keyword matching and skill-gap analysis tuned for an
  AI / ML / Computer Vision / NLP / MLOps profile.
- Generates resume tailoring suggestions, interview questions, cover letters,
  and LinkedIn outreach messages signed for Mukeet.
- Maintains an application tracker (CSV) and prioritised reminders.

Designed using the GAME framework (Goal, Actions, Memory, Environment).

Run:
    python app.py            # interactive menu
    python app.py --auto     # run the full pipeline once and exit
"""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import datetime, date, timedelta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

JOB_DIR = "input_jobs"
RESUME_DIR = "input_resumes"
KB_DIR = "input_kb"
OUTPUT_DIR = "outputs"
TRACKER_DIR = "tracker"

MEMORY_FILE = os.path.join(OUTPUT_DIR, "agent_memory.json")
TRACKER_CSV = os.path.join(TRACKER_DIR, "applications.csv")
REMINDERS_TXT = os.path.join(TRACKER_DIR, "reminders.txt")

# Keywords are tuned for Abdul Mukeet's profile: BS Artificial Intelligence
# student with focus on ML, Computer Vision, NLP, MLOps and Agentic AI.
KEYWORDS = [
    "python", "c++", "sql", "machine learning", "deep learning",
    "computer vision", "nlp", "natural language processing",
    "mlops", "agentic ai", "llm", "prompt engineering", "rag",
    "recommender systems", "artificial neural networks", "neural networks",
    "data preprocessing", "feature engineering", "model evaluation",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib",
    "jupyter", "opencv", "hugging face", "transformers",
    "docker", "ci/cd", "github actions", "github", "git",
    "api", "rest", "flask", "fastapi", "streamlit", "linux",
    "oop", "data structures", "database",
    "communication", "adaptability", "teamwork", "problem solving",
    "critical thinking",
]

TRACKER_FIELDS = [
    "application_id", "company", "role", "source", "status",
    "applied_date", "interview_date", "follow_up_date", "next_action", "notes",
]

VALID_STATUSES = [
    "Not Applied", "Applied", "Shortlisted",
    "Interview Scheduled", "Rejected", "Offered",
]


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def ensure_folders() -> None:
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR]:
        os.makedirs(folder, exist_ok=True)


def _read_pdf(path: str) -> str:
    """Optional PDF reader. Returns empty string if PyPDF2 is not installed."""
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception:
        return ""
    try:
        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception:
        return ""


def _read_docx(path: str) -> str:
    """Optional DOCX reader. Returns empty string if python-docx is missing."""
    try:
        import docx  # type: ignore
    except Exception:
        return ""
    try:
        document = docx.Document(path)
        return "\n".join(p.text for p in document.paragraphs)
    except Exception:
        return ""


def read_files(folder: str) -> tuple[str, int, list[str]]:
    """Read all supported files (.txt, .pdf, .docx) from a folder."""
    combined = ""
    count = 0
    names: list[str] = []
    if not os.path.isdir(folder):
        return combined, 0, names
    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)
        if not os.path.isfile(path):
            continue
        lower = filename.lower()
        text = ""
        if lower.endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        elif lower.endswith(".pdf"):
            text = _read_pdf(path)
        elif lower.endswith(".docx"):
            text = _read_docx(path)
        else:
            continue
        if not text.strip():
            continue
        combined += f"\n\n--- FILE: {filename} ---\n{text}"
        names.append(filename)
        count += 1
    return combined, count, names


def save_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def extract_keywords(text: str) -> list[str]:
    text_lower = text.lower()
    return [kw for kw in KEYWORDS if kw in text_lower]


def compare_skills(job_skills: list[str], resume_skills: list[str]):
    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]
    score = 0.0 if not job_skills else round(len(matched) / len(job_skills) * 100, 2)
    return matched, missing, score


def resume_quality_score(resume_text: str, resume_skills: list[str]) -> tuple[int, list[str]]:
    """Heuristic 0-100 score with improvement tips."""
    tips: list[str] = []
    score = 0
    lower = resume_text.lower()

    if len(resume_text.split()) >= 150:
        score += 20
    else:
        tips.append("Resume looks short. Aim for at least 150 meaningful words.")

    if any(k in lower for k in ["project", "projects"]):
        score += 20
    else:
        tips.append("Add a Projects section with 2-3 concrete examples.")

    if "github" in lower or "git" in lower:
        score += 15
    else:
        tips.append("Add a GitHub link to showcase your code.")

    if any(k in lower for k in ["education", "university", "b.s", "bachelor"]):
        score += 10
    else:
        tips.append("Add an Education section.")

    if len(resume_skills) >= 5:
        score += 20
    else:
        tips.append("List at least 5 concrete technical skills.")

    if any(k in lower for k in ["communication", "teamwork", "problem solving"]):
        score += 15
    else:
        tips.append("Mention soft skills such as communication and teamwork.")

    return min(score, 100), tips


# ---------------------------------------------------------------------------
# Report generators
# ---------------------------------------------------------------------------

def generate_job_analysis(job_files: list[str], job_skills: list[str]) -> str:
    out = "Job Analysis Report\n===================\n\n"
    out += f"Job files analysed: {len(job_files)}\n"
    for name in job_files:
        out += f"  - {name}\n"
    out += "\nSkills/keywords detected across job posters:\n"
    for skill in job_skills:
        out += f"  - {skill}\n"
    if not job_skills:
        out += "  (no known keywords detected)\n"
    return out


def generate_skill_gap_report(job_skills, resume_skills, matched, missing, score) -> str:
    out = "Skill Gap Report\n================\n\n"
    out += f"Match Score: {score}%\n\n"
    out += "Matched Skills:\n"
    out += "".join(f"  - {s}\n" for s in matched) or "  (none)\n"
    out += "\nMissing Skills (focus areas):\n"
    out += "".join(f"  - {s}\n" for s in missing) or "  (none — great alignment!)\n"
    out += "\nResume Skills Detected:\n"
    out += "".join(f"  - {s}\n" for s in resume_skills) or "  (none)\n"
    return out


def generate_resume_suggestions(job_skills, missing, quality_score, quality_tips) -> str:
    out = "Tailored Resume Suggestions\n===========================\n\n"
    out += f"Resume Quality Score: {quality_score}/100\n\n"
    if quality_tips:
        out += "Quick wins to raise the quality score:\n"
        out += "".join(f"  - {t}\n" for t in quality_tips) + "\n"

    out += "Tailor your resume around these job keywords:\n"
    for skill in job_skills:
        out += f"  - Add or strengthen evidence of '{skill}'.\n"

    out += "\nSuggested resume bullets you can adapt (tuned for Mukeet's AI profile):\n"
    out += "  - Trained and evaluated ML models in Python using Scikit-learn and TensorFlow.\n"
    out += "  - Built data preprocessing and feature-engineering pipelines with Pandas / NumPy.\n"
    out += "  - Applied Computer Vision and NLP techniques on coursework and FYP datasets.\n"
    out += "  - Containerised ML workflows with Docker and automated them via GitHub Actions (CI/CD).\n"
    out += "  - Designed reusable C++ / Python modules using OOP and clean Git workflows.\n"

    if missing:
        out += "\nSkills to learn or highlight before interviewing:\n"
        for skill in missing:
            out += f"  - {skill}\n"
    return out


def generate_interview_questions(job_skills: list[str], kb_text: str) -> str:
    out = "Interview Questions\n===================\n\n"
    out += "Technical questions based on job posters:\n"
    for skill in job_skills:
        out += f"  - Explain your understanding of {skill}.\n"
        out += f"  - Describe a project where you used {skill}.\n"

    out += "\nHR and behavioural questions:\n"
    for q in [
        "Tell me about yourself.",
        "Why are you interested in this role?",
        "Describe your best academic or project work.",
        "What are your strengths and weaknesses?",
        "Why should we select you?",
        "Tell me about a time you handled a difficult teammate.",
    ]:
        out += f"  - {q}\n"

    out += "\nQuestions inspired by your knowledge-base notes:\n"
    kb_lines = [ln.strip("-• ").strip() for ln in kb_text.splitlines() if ln.strip()]
    seen = set()
    picked = 0
    for line in kb_lines:
        if len(line) < 25 or line.lower() in seen:
            continue
        seen.add(line.lower())
        out += f"  - How would you discuss this in an interview: \"{line}\"?\n"
        picked += 1
        if picked >= 12:
            break
    if picked == 0:
        out += "  (Add longer notes in input_kb/ to generate richer questions.)\n"
    return out


def generate_preparation_plan(missing: list[str], job_skills: list[str]) -> str:
    out = "7-Day Preparation Plan\n======================\n\n"
    focus = missing or job_skills or ["general revision"]
    today = date.today()
    for i in range(7):
        day = today + timedelta(days=i)
        topic = focus[i % len(focus)]
        out += (
            f"Day {i + 1} ({day.isoformat()}): Deep dive into '{topic}'. "
            f"Build a tiny demo and add it to GitHub. "
            f"Write 3 interview answers about it.\n"
        )
    return out


# Candidate profile (sourced from input_resumes/my_resume.txt)
CANDIDATE_NAME = "Abdul Mukeet"
CANDIDATE_DEGREE = "BS Artificial Intelligence"
CANDIDATE_UNIVERSITY = "FAST National University"
CANDIDATE_EMAIL = "mukeet0123@gmail.com"
CANDIDATE_PHONE = "+92 307 7447779"
CANDIDATE_LOCATION = "Faisalabad, Pakistan"
CANDIDATE_SIGNATURE = (
    f"{CANDIDATE_NAME}\n"
    f"{CANDIDATE_EMAIL} | {CANDIDATE_PHONE}\n"
    f"{CANDIDATE_LOCATION}"
)


def generate_cover_letter(company: str, role: str, matched: list[str]) -> str:
    skills_line = (
        ", ".join(matched[:5])
        if matched
        else "Python, Machine Learning, Computer Vision, MLOps, problem solving"
    )
    return (
        f"Dear {company} Hiring Team,\n\n"
        f"I am writing to apply for the {role} position. I am {CANDIDATE_NAME}, a final-year\n"
        f"{CANDIDATE_DEGREE} student at {CANDIDATE_UNIVERSITY} with hands-on experience in\n"
        f"{skills_line}. I am excited by the opportunity to contribute to {company} while\n"
        f"continuing to grow alongside senior AI engineers.\n\n"
        f"Through coursework in Machine Learning, Computer Vision, NLP and MLOps, an AI\n"
        f"internship at Tech Solutions Pvt. Ltd., and projects such as YAAP (real-time\n"
        f"voice/text app with translation and emotion-aware interaction) and an Applied\n"
        f"Recommendation System, I have practised the full ML workflow: data preprocessing,\n"
        f"model training and evaluation, and deployment with Docker and CI/CD pipelines.\n\n"
        f"I would welcome the chance to discuss how my AI background fits the {role} role\n"
        f"at {company}. Thank you for considering my application.\n\n"
        f"Sincerely,\n"
        f"{CANDIDATE_SIGNATURE}\n"
    )


def generate_linkedin_message(company: str, role: str) -> str:
    return (
        f"Hi [Recruiter Name],\n\n"
        f"I hope you're doing well. I recently came across the {role} opening at "
        f"{company} and I'm genuinely excited about it. I'm {CANDIDATE_NAME}, a final-year "
        f"{CANDIDATE_DEGREE} student at {CANDIDATE_UNIVERSITY}, with hands-on experience in "
        f"Python, Machine Learning, Computer Vision, NLP and MLOps (Docker + CI/CD), plus "
        f"projects on GitHub including my FYP 'YAAP'.\n\n"
        f"Would it be possible to learn a little more about the role or the team? "
        f"I'd really appreciate any guidance.\n\n"
        f"Thank you for your time!\n"
        f"{CANDIDATE_NAME}\n"
        f"{CANDIDATE_EMAIL}\n"
    )


def generate_project_mapping(resume_text: str, job_skills: list[str]) -> str:
    """Map resume project lines to job skills they likely support."""
    out = "Project-to-JD Mapping\n=====================\n\n"
    projects: list[str] = []
    capture = False
    for line in resume_text.splitlines():
        stripped = line.strip()
        if stripped.upper().startswith("PROJECT"):
            capture = True
            continue
        if capture:
            if stripped and stripped.isupper() and len(stripped) > 3:
                break
            if stripped:
                projects.append(stripped)

    if not projects:
        return out + "(No 'PROJECTS' section detected in resume.)\n"

    for proj in projects:
        proj_lower = proj.lower()
        supports = [s for s in job_skills if s in proj_lower]
        if supports:
            out += f"- {proj}\n    Supports JD skills: {', '.join(supports)}\n"
        else:
            out += f"- {proj}\n    (Consider rewriting to highlight JD keywords.)\n"
    return out


# ---------------------------------------------------------------------------
# Tracker and reminders
# ---------------------------------------------------------------------------

def init_tracker_if_missing() -> None:
    if os.path.exists(TRACKER_CSV):
        return
    os.makedirs(TRACKER_DIR, exist_ok=True)
    with open(TRACKER_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(TRACKER_FIELDS)
        writer.writerow([
            "APP-001", "ABC Tech Solutions", "Junior AI / Machine Learning Engineer",
            "Job Poster", "Interview Scheduled",
            date.today().isoformat(),
            (date.today() + timedelta(days=3)).isoformat(),
            (date.today() + timedelta(days=6)).isoformat(),
            "Revise ML fundamentals; rehearse YAAP FYP and Recommender System projects",
            "Resume tailored from job_poster_01 (Mukeet — BS AI, FAST)",
        ])
        writer.writerow([
            "APP-002", "NextGen AI Studio", "Computer Vision / MLOps Intern",
            "LinkedIn", "Applied",
            date.today().isoformat(), "",
            (date.today() + timedelta(days=5)).isoformat(),
            "Polish GitHub portfolio (Docker + CI/CD demo) and send follow-up email",
            "Applied via company portal",
        ])


def read_tracker() -> list[dict]:
    if not os.path.exists(TRACKER_CSV):
        return []
    with open(TRACKER_CSV, "r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_tracker(rows: list[dict]) -> None:
    with open(TRACKER_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=TRACKER_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in TRACKER_FIELDS})


def add_application_interactive() -> None:
    init_tracker_if_missing()
    rows = read_tracker()
    next_id = f"APP-{len(rows) + 1:03d}"
    print(f"\nAdding new application ({next_id}). Press Enter to skip optional fields.")
    company = input("Company: ").strip()
    role = input("Role: ").strip()
    source = input("Source (LinkedIn / Poster / WhatsApp / Other): ").strip()
    print("Status options:", " | ".join(VALID_STATUSES))
    status = input("Status [Not Applied]: ").strip() or "Not Applied"
    applied_date = input("Applied date (YYYY-MM-DD): ").strip()
    interview_date = input("Interview date (YYYY-MM-DD): ").strip()
    follow_up_date = input("Follow-up date (YYYY-MM-DD): ").strip()
    next_action = input("Next action: ").strip()
    notes = input("Notes: ").strip()

    rows.append({
        "application_id": next_id, "company": company, "role": role,
        "source": source, "status": status, "applied_date": applied_date,
        "interview_date": interview_date, "follow_up_date": follow_up_date,
        "next_action": next_action, "notes": notes,
    })
    write_tracker(rows)
    print(f"Saved {next_id}.")


def _parse_date(value: str):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def _urgency_label(target) -> str:
    if target is None:
        return ""
    today = date.today()
    delta = (target - today).days
    if delta < 0:
        return f"OVERDUE by {-delta} day(s)"
    if delta == 0:
        return "TODAY"
    if delta == 1:
        return "TOMORROW"
    if delta <= 7:
        return f"in {delta} days (this week)"
    return f"in {delta} days"


def generate_reminders() -> str:
    rows = read_tracker()
    out = "Application Reminders\n=====================\n"
    out += f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n"
    if not rows:
        return out + "No applications in tracker yet.\n"

    urgent: list[str] = []
    upcoming: list[str] = []
    other: list[str] = []

    for row in rows:
        app_id = row.get("application_id", "")
        company = row.get("company", "")
        role = row.get("role", "")
        status = (row.get("status") or "").strip()
        next_action = row.get("next_action", "")
        idate = _parse_date(row.get("interview_date", ""))
        fdate = _parse_date(row.get("follow_up_date", ""))

        if status.lower() == "interview scheduled" and idate:
            line = (f"- [{app_id}] INTERVIEW with {company} ({role}) "
                    f"on {idate.isoformat()} — {_urgency_label(idate)}.\n"
                    f"    Next action: {next_action or 'Prepare and rehearse.'}")
            (urgent if (idate - date.today()).days <= 2 else upcoming).append(line)
        elif status.lower() == "applied" and fdate:
            line = (f"- [{app_id}] Follow up with {company} ({role}) "
                    f"on {fdate.isoformat()} — {_urgency_label(fdate)}.\n"
                    f"    Next action: {next_action or 'Send a polite follow-up email.'}")
            (urgent if (fdate - date.today()).days <= 0 else upcoming).append(line)
        elif status.lower() == "not applied":
            other.append(f"- [{app_id}] Not applied yet for {role} at {company}. "
                         f"Tailor resume and apply.")
        elif status.lower() == "shortlisted":
            other.append(f"- [{app_id}] Shortlisted at {company}. "
                         f"Watch your email for the interview invite.")
        elif status.lower() == "offered":
            other.append(f"- [{app_id}] Offer received from {company}! "
                         f"Review terms and respond on time.")
        elif status.lower() == "rejected":
            other.append(f"- [{app_id}] Rejected at {company}. "
                         f"Ask for feedback and keep applying.")

    if urgent:
        out += "URGENT (today / overdue / within 2 days)\n" + "\n".join(urgent) + "\n\n"
    if upcoming:
        out += "Upcoming\n" + "\n".join(upcoming) + "\n\n"
    if other:
        out += "Other\n" + "\n".join(other) + "\n"
    return out


def generate_dashboard() -> str:
    rows = read_tracker()
    out = "Application Dashboard\n=====================\n\n"
    if not rows:
        return out + "No applications yet.\n"
    counts: dict[str, int] = {}
    for row in rows:
        s = (row.get("status") or "Unknown").strip() or "Unknown"
        counts[s] = counts.get(s, 0) + 1
    out += f"Total applications: {len(rows)}\n\n"
    for status in VALID_STATUSES:
        if status in counts:
            out += f"  {status:<22} {counts[status]}\n"
    extras = {k: v for k, v in counts.items() if k not in VALID_STATUSES}
    for status, n in extras.items():
        out += f"  {status:<22} {n}\n"
    return out


# ---------------------------------------------------------------------------
# Memory (JSON)
# ---------------------------------------------------------------------------

def save_memory(payload: dict) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(verbose: bool = True) -> dict:
    ensure_folders()
    job_text, job_count, job_files = read_files(JOB_DIR)
    resume_text, resume_count, _ = read_files(RESUME_DIR)
    kb_text, kb_count, _ = read_files(KB_DIR)

    if job_count == 0 or resume_count == 0 or kb_count == 0:
        print("Please add files in input_jobs/, input_resumes/, and input_kb/ first.")
        return {}

    job_skills = extract_keywords(job_text)
    resume_skills = extract_keywords(resume_text)
    matched, missing, score = compare_skills(job_skills, resume_skills)
    quality_score, quality_tips = resume_quality_score(resume_text, resume_skills)

    init_tracker_if_missing()
    tracker_rows = read_tracker()

    job_report = generate_job_analysis(job_files, job_skills)
    gap_report = generate_skill_gap_report(job_skills, resume_skills, matched, missing, score)
    suggestions = generate_resume_suggestions(job_skills, missing, quality_score, quality_tips)
    questions = generate_interview_questions(job_skills, kb_text)
    plan = generate_preparation_plan(missing, job_skills)
    mapping = generate_project_mapping(resume_text, job_skills)
    reminders = generate_reminders()
    dashboard = generate_dashboard()

    primary_app = tracker_rows[0] if tracker_rows else {
        "company": "Target Company", "role": "Target Role",
    }
    cover_letter = generate_cover_letter(
        primary_app.get("company", "Target Company"),
        primary_app.get("role", "Target Role"),
        matched,
    )
    linkedin_msg = generate_linkedin_message(
        primary_app.get("company", "Target Company"),
        primary_app.get("role", "Target Role"),
    )

    final_report = (
        "CareerPrep Job-Hunting Agent — Final Report\n"
        f"Generated: {datetime.now().isoformat(timespec='seconds')}\n"
        "===========================================\n\n"
        f"{dashboard}\n{job_report}\n{gap_report}\n{mapping}\n"
        f"{suggestions}\n{questions}\n{plan}\n{reminders}\n"
    )

    save_text(os.path.join(OUTPUT_DIR, "job_analysis_report.txt"), job_report)
    save_text(os.path.join(OUTPUT_DIR, "skill_gap_report.txt"), gap_report)
    save_text(os.path.join(OUTPUT_DIR, "tailored_resume_suggestions.txt"), suggestions)
    save_text(os.path.join(OUTPUT_DIR, "interview_questions.txt"), questions)
    save_text(os.path.join(OUTPUT_DIR, "preparation_plan.txt"), plan)
    save_text(os.path.join(OUTPUT_DIR, "project_to_jd_mapping.txt"), mapping)
    save_text(os.path.join(OUTPUT_DIR, "cover_letter.txt"), cover_letter)
    save_text(os.path.join(OUTPUT_DIR, "linkedin_outreach.txt"), linkedin_msg)
    save_text(os.path.join(OUTPUT_DIR, "dashboard.txt"), dashboard)
    save_text(os.path.join(OUTPUT_DIR, "final_agent_report.txt"), final_report)
    save_text(REMINDERS_TXT, reminders)

    save_memory({
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "counts": {"jobs": job_count, "resumes": resume_count, "kb": kb_count},
        "job_skills": job_skills,
        "resume_skills": resume_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": score,
        "resume_quality_score": quality_score,
        "tracker_rows": len(tracker_rows),
    })

    if verbose:
        print("\nAgent run complete.")
        print(f"  Job files       : {job_count}")
        print(f"  Resume files    : {resume_count}")
        print(f"  KB files        : {kb_count}")
        print(f"  Match score     : {score}%")
        print(f"  Resume quality  : {quality_score}/100")
        print(f"  Tracker rows    : {len(tracker_rows)}")
        print(f"  Outputs saved in '{OUTPUT_DIR}/' and '{TRACKER_DIR}/'.")
    return {"score": score, "quality": quality_score}


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU = """
=== CareerPrep Job-Hunting Agent (Abdul Mukeet — BS AI, FAST) ===
 1. Run full pipeline (analyse + generate all reports)
 2. Add a new application to the tracker
 3. Show application dashboard
 4. Show reminders (with urgency)
 5. Re-generate cover letter for first tracker entry
 6. Exit
Choose [1-6]: """


def menu_loop() -> None:
    ensure_folders()
    while True:
        choice = input(MENU).strip()
        if choice == "1":
            run_pipeline()
        elif choice == "2":
            add_application_interactive()
        elif choice == "3":
            print("\n" + generate_dashboard())
        elif choice == "4":
            print("\n" + generate_reminders())
        elif choice == "5":
            rows = read_tracker()
            if not rows:
                print("Tracker is empty. Add an application first.")
                continue
            row = rows[0]
            letter = generate_cover_letter(
                row.get("company", "Target Company"),
                row.get("role", "Target Role"),
                extract_keywords(read_files(RESUME_DIR)[0]),
            )
            save_text(os.path.join(OUTPUT_DIR, "cover_letter.txt"), letter)
            print("\nCover letter saved to outputs/cover_letter.txt\n")
            print(letter)
        elif choice == "6":
            print("Goodbye. Best of luck with your applications!")
            return
        else:
            print("Please choose a number from 1 to 6.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--auto" in sys.argv:
        run_pipeline()
    else:
        try:
            menu_loop()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
