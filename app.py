import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])


def get_or_create_pet(owner: Owner, name: str, pet_species: str) -> Pet:
    """Return an existing pet by name, or create one if it doesn't exist yet."""
    normalized_name = name.strip().lower()
    for pet in owner.get_pets():
        if pet.name.strip().lower() == normalized_name:
            pet.species = pet_species
            return pet

    new_pet = Pet(name=name.strip(), species=pet_species, age=1)
    owner.add_pet(new_pet)
    return new_pet


if "owner" not in st.session_state:
    default_email = f"{owner_name.strip().lower() or 'owner'}@example.com"
    st.session_state.owner = Owner(
        name=owner_name.strip() or "Owner",
        email=default_email,
        available_time_per_day=120,
    )

owner: Owner = st.session_state.owner
owner.name = owner_name.strip() or owner.name

current_pet = get_or_create_pet(owner, pet_name or "Pet", species)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    priority_map = {"low": 1, "medium": 3, "high": 5}
    task_name = task_title.strip()
    if task_name:
        current_pet.add_task(
            Task(
                name=task_name,
                description=f"{task_name} for {current_pet.name}",
                duration_minutes=int(duration),
                priority=priority_map[priority],
                category="general",
            )
        )
        st.success(f"Added task '{task_name}' for {current_pet.name}.")
    else:
        st.warning("Please enter a task title before adding a task.")

pet_tasks = current_pet.get_tasks()
if pet_tasks:
    task_rows = [
        {
            "title": task.name,
            "duration_minutes": task.duration_minutes,
            "priority": task.priority,
            "category": task.category,
            "completed": task.completed,
        }
        for task in pet_tasks
    ]
    st.write("Current tasks:")
    st.table(task_rows)
else:
    st.info(f"No tasks yet for {current_pet.name}. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

available_time = st.number_input(
    "Available time today (minutes)",
    min_value=15,
    max_value=600,
    value=owner.available_time_per_day,
    step=15,
)
owner.available_time_per_day = int(available_time)

if st.button("Generate schedule"):
    if not pet_tasks:
        st.warning(f"Add at least one task for {current_pet.name} before generating a schedule.")
    else:
        scheduler = Scheduler(owner, current_pet, owner.available_time_per_day)
        generated_schedule = scheduler.generate_schedule()

        if not generated_schedule:
            st.warning("No schedule could be generated with the current constraints.")
        else:
            st.success(f"Schedule generated for {current_pet.name}!")
            schedule_rows = [
                {
                    "task": task.name,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "category": task.category,
                }
                for task in generated_schedule
            ]
            st.table(schedule_rows)
            st.markdown("### Plan Explanation")
            st.text(scheduler.explain_plan(generated_schedule))
