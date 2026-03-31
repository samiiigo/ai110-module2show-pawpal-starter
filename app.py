from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet-care planning with sorting, recurrence, filtering, and conflict warnings.")


def get_or_create_pet(owner: Owner, name: str, pet_species: str) -> Pet:
    """Return an existing pet by name, or create one if needed."""
    normalized_name = name.strip().lower()
    for pet in owner.get_pets():
        if pet.name.strip().lower() == normalized_name:
            pet.species = pet_species
            return pet

    new_pet = Pet(name=name.strip() or "Pet", species=pet_species, age=1)
    owner.add_pet(new_pet)
    return new_pet


if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        email="jordan@example.com",
        available_time_per_day=120,
    )

owner: Owner = st.session_state.owner

st.subheader("Owner & Pet")
col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value=owner.name)
with col2:
    pet_name = st.text_input("Active pet", value="Mochi")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])

owner.name = owner_name.strip() or owner.name
current_pet = get_or_create_pet(owner, pet_name, species)

owner.available_time_per_day = int(
    st.number_input(
        "Available time today (minutes)",
        min_value=15,
        max_value=600,
        value=owner.available_time_per_day,
        step=15,
    )
)

scheduler = Scheduler(owner, current_pet, owner.available_time_per_day)

st.divider()
st.subheader("Add Task")

with st.form("add_task_form", clear_on_submit=True):
    t1, t2, t3 = st.columns(3)
    with t1:
        task_name = st.text_input("Task name", value="Morning walk")
        category = st.selectbox(
            "Category",
            ["exercise", "feeding", "medication", "grooming", "enrichment", "general"],
        )
    with t2:
        duration_minutes = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.slider("Priority", min_value=1, max_value=5, value=4)
    with t3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        scheduled_time = st.time_input("Scheduled time", value=time(8, 0))

    due_date = st.date_input("Due date", value=date.today())
    submitted = st.form_submit_button("Add task")

if submitted:
    clean_name = task_name.strip()
    if not clean_name:
        st.warning("Please provide a task name.")
    else:
        current_pet.add_task(
            Task(
                name=clean_name,
                description=f"{clean_name} for {current_pet.name}",
                duration_minutes=int(duration_minutes),
                priority=int(priority),
                category=category,
                frequency=frequency,
                scheduled_time=scheduled_time.strftime("%H:%M"),
                due_date=due_date,
            )
        )
        st.success(f"Added '{clean_name}' for {current_pet.name}.")

st.divider()
st.subheader("Task Intelligence")

view1, view2 = st.columns(2)
with view1:
    completion_view = st.selectbox("Completion filter", ["all", "pending", "completed"])
with view2:
    sort_by_time_enabled = st.toggle("Sort chronologically", value=True)

completed_filter = None
if completion_view == "pending":
    completed_filter = False
elif completion_view == "completed":
    completed_filter = True

visible_tasks = scheduler.filter_tasks(pet_name=current_pet.name, completed=completed_filter)
if sort_by_time_enabled:
    visible_tasks = scheduler.sort_by_time(visible_tasks)

if visible_tasks:
    st.table(
        [
            {
                "task": task.name,
                "due_date": task.due_date.isoformat(),
                "time": task.scheduled_time,
                "duration_min": task.duration_minutes,
                "priority": task.priority,
                "category": task.category,
                "frequency": task.frequency,
                "completed": task.completed,
            }
            for task in visible_tasks
        ]
    )
else:
    st.info("No tasks match the selected view for this pet.")

conflicts = scheduler.detect_conflicts()
if conflicts:
    st.warning("Potential scheduling conflicts detected. Adjust one task time in each pair to avoid overlap confusion.")
    for item in conflicts:
        st.warning(item)
else:
    st.success("No date/time conflicts detected across your pets.")

pending_names = [task.name for task in current_pet.get_tasks() if not task.completed]
if pending_names:
    complete_col1, complete_col2 = st.columns([2, 1])
    with complete_col1:
        task_to_complete = st.selectbox("Mark task complete", pending_names)
    with complete_col2:
        if st.button("Complete task"):
            finished = scheduler.mark_task_complete(task_to_complete, pet_name=current_pet.name)
            if finished is None:
                st.warning("Could not find a pending task with that name.")
            else:
                st.success(
                    f"Completed '{finished.name}'. If recurring, the next occurrence was added automatically."
                )
                st.rerun()

st.divider()
st.subheader("Generate Daily Schedule")

if st.button("Generate schedule"):
    generated_schedule = scheduler.generate_schedule()
    if not generated_schedule:
        st.warning("No schedule could be generated with the current constraints.")
    else:
        st.success(f"Schedule generated for {current_pet.name}.")
        time_slots = scheduler.assign_times(generated_schedule)
        st.table(
            [
                {
                    "task": task.name,
                    "time_window": f"{time_slots[task.name][0]} - {time_slots[task.name][1]}",
                    "duration_min": task.duration_minutes,
                    "priority": task.priority,
                    "category": task.category,
                }
                for task in generated_schedule
            ]
        )
        st.text(scheduler.explain_plan(generated_schedule))
