# Reflection — CareerPrep Job-Hunting Agent

## What I built
I built a file-driven Job-Hunting Agent in Python following the GAME
framework. It reads job posters, my resume, and course knowledge-base notes
from three separate folders, performs keyword-based skill matching, and
produces a complete set of career-preparation outputs together with an
application tracker and reminders.

## What works well
- The agent runs end-to-end with a single command (`python app.py --auto`)
  and also offers an interactive menu for adding applications.
- Inputs are **fully folder-driven**, so no job description is hard-coded.
- Outputs include not only the required reports but also a cover letter,
  a LinkedIn outreach template, a project-to-JD mapping, a 7-day plan, and
  a status dashboard.
- The reminder system understands urgency (`OVERDUE`, `TODAY`, `TOMORROW`,
  this week) by comparing against today's date.
- A JSON memory file stores the last run's summary for future comparison.

## What I tested
- Running with the included sample files in all three input folders.
- Running with an empty input folder (the agent prints a clear instruction
  instead of crashing).
- Adding a new application via the menu and re-generating reminders.
- Verifying that all expected files appear under `outputs/` and `tracker/`.

## What I would improve next
- Replace keyword matching with embeddings or an LLM call for richer
  skill extraction and resume tailoring.
- Build a small Streamlit dashboard on top of the same `app.py` functions.
- Export the final report as a styled PDF using `reportlab`.
- Add per-company preparation checklists driven by KB tags.

## What I learned
- How to translate a real-world workflow into clearly separated agent
  actions (read → analyse → match → generate → track → remind).
- Why structuring inputs as folders makes the agent reusable across many
  different jobs without changing code.
- The importance of memory (CSV + JSON) for an agent to feel useful across
  multiple runs, not just one.
