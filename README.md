# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a pet owner plan daily care tasks with simple but practical scheduling intelligence.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- Owner and pet profile setup in a simple Streamlit workflow.
- Task creation with priority, category, frequency, date, and time.
- Sorting by time using due date + HH:MM slots.
- Filtering by completion status (all, pending, completed).
- Conflict warnings for duplicate date/time tasks across pets.
- Recurrence automation: completing daily or weekly tasks auto-creates the next occurrence.
- Time-constrained daily schedule generation with readable plan explanations.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

The scheduling layer now includes lightweight algorithms to make planning more practical:

- Sorting by time: tasks can be ordered using due date plus HH:MM scheduled time.
- Filtering views: tasks can be filtered by pet name and completion state.
- Recurring automation: completing daily or weekly tasks auto-creates the next occurrence using timedelta.
- Conflict detection: exact date/time collisions across pets are flagged as warnings.

You can see these features in action by running the CLI demo in main.py and reviewing the terminal output sections for sorting/filtering, conflicts, and recurring completion behavior.

## System Architecture

The final UML class diagram is included as [uml_final.svg](uml_final.svg).

## 📸 Demo

<a href="/course_images/ai110/pawpal_ui_final.png" target="_blank"><img src='/course_images/ai110/pawpal_ui_final.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

The tests cover core scheduler behavior, including:

- Sorting correctness for chronological task ordering.
- Recurrence logic that creates the next daily task when one is completed.
- Conflict detection for duplicate scheduled date/time slots.
- Additional happy paths and edge cases like pets with no tasks, filtering by completion, and full workflow integration.

Confidence Level: ★★★★☆ (4/5)
