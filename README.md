# LearnTwin

LearnTwin is an open-source learning-analytics core that turns simple classroom data
(attendance, activity, scores, small signals) into clear, teacher-friendly insights.

## Why?

Many students struggle silently until it is too late. Teachers often have the data,
but not the time or tools to turn it into something actionable. LearnTwin aims to:

- surface early-warning signs for at-risk students
- show how engagement and performance evolve over time
- give educators a quick overview without drowning them in dashboards

## Who is this for?

- Teachers / instructors who want a fast view of which students might need help
- Schools / universities exploring data-informed teaching
- Developers / researchers building or studying learning-analytics tools

## Quickstart (local demo on Windows + PowerShell)

1. Clone the project:
   git clone https://github.com/n0711/LearnTwin.git
   cd LearnTwin

2. Create and activate a virtual environment:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Install dependencies:
   pip install -r requirements.txt

4. Run the test suite to verify everything works:
   pytest

   At this stage LearnTwin behaves as a Python library with tests rather than a
   standalone server application. To explore the core logic, inspect the modules
   under src/ and learntwin/.

## Sample data

A small synthetic dataset is provided at:

- sample_data/demo_class.csv

Columns:
- student_id             – stable ID for the student
- student_name           – display name
- attendance_rate        – fraction between 0 and 1
- avg_score              – average score between 0 and 100
- last_activity_days_ago – days since last activity (0 = very recent)

Use this file to experiment locally without any real student data.

## Contributing and roadmap

LearnTwin is early-stage and open to collaborators.

- For how to set up a dev environment and send changes, see: CONTRIBUTING.md
- For the high-level direction and planned work, see: ROADMAP.md

You can also browse the GitHub Issues for tasks, ideas, and discussion.

## License and attribution

LearnTwin is free and open-source software under the MIT License (see LICENSE).

Originally initiated by Charalampos Nadiotis + colleagues 
(frontend: Andreas Lazarou, backend: Christos Paparistodimou, 
AI/analytics logic & integration: Charalampos Nadiotis).

If you use LearnTwin in a product or deployment visible to end users,
If you use LearnTwin in a product or deployment visible to end users, we kindly require that you show a small "Powered by Charalampos Nadiotis and team" note.

