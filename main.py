"""
PawPal+ Demo Script

This is a temporary "testing ground" to verify the system logic works
in the terminal before integrating with Streamlit.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Create a demo scenario with an owner, pets, tasks, and schedule."""
    
    print("=" * 60)
    print("PawPal+ System Demo")
    print("=" * 60)
    print()
    
    # Step 1: Create an owner
    owner = Owner(
        name="Jordan",
        email="jordan@example.com",
        available_time_per_day=120  # 2 hours per day
    )
    print(f"✓ Created owner: {owner.name} ({owner.available_time_per_day} min/day available)\n")
    
    # Step 2: Create pets
    mochi = Pet(
        name="Mochi",
        species="dog",
        age=3,
        special_needs=["needs regular exercise", "allergic to wheat"]
    )
    
    luna = Pet(
        name="Luna",
        species="cat",
        age=5,
        special_needs=["sensitive stomach"]
    )
    
    owner.add_pet(mochi)
    owner.add_pet(luna)
    
    print(f"✓ Created pets:")
    print(f"  - {mochi}")
    print(f"  - {luna}\n")
    
    # Step 3: Add tasks for Mochi (dog)
    mochi_tasks = [
        Task(
            name="Morning Walk",
            description="Take Mochi for a 30-minute walk",
            duration_minutes=30,
            priority=5,
            category="exercise",
            frequency="daily",
            scheduled_time="09:30",
        ),
        Task(
            name="Breakfast",
            description="Feed Mochi breakfast",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily",
            scheduled_time="08:00",
        ),
        Task(
            name="Dinner",
            description="Feed Mochi dinner",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily",
            scheduled_time="18:00",
        ),
        Task(
            name="Playtime",
            description="Interactive play and training",
            duration_minutes=20,
            priority=3,
            category="enrichment",
            frequency="daily",
            scheduled_time="17:00",
        ),
        Task(
            name="Grooming",
            description="Brush coat and check nails",
            duration_minutes=15,
            priority=2,
            category="grooming",
            frequency="weekly",
            scheduled_time="12:00",
        ),
    ]
    
    for task in mochi_tasks:
        mochi.add_task(task)
    
    print(f"✓ Added {len(mochi_tasks)} tasks for {mochi.name}:\n")
    for task in mochi_tasks:
        print(f"  - {task}")
    print()
    
    # Step 4: Add tasks for Luna (cat)
    luna_tasks = [
        Task(
            name="Breakfast",
            description="Feed Luna breakfast",
            duration_minutes=5,
            priority=5,
            category="feeding",
            frequency="daily",
            scheduled_time="08:00",
        ),
        Task(
            name="Dinner",
            description="Feed Luna dinner",
            duration_minutes=5,
            priority=5,
            category="feeding",
            frequency="daily",
            scheduled_time="18:00",
        ),
        Task(
            name="Litter Box",
            description="Clean litter box",
            duration_minutes=10,
            priority=4,
            category="maintenance",
            frequency="daily",
            scheduled_time="08:00",
        ),
        Task(
            name="Playtime",
            description="Interactive play with toys",
            duration_minutes=15,
            priority=3,
            category="enrichment",
            frequency="daily",
            scheduled_time="16:30",
        ),
    ]
    
    for task in luna_tasks:
        luna.add_task(task)
    
    print(f"✓ Added {len(luna_tasks)} tasks for {luna.name}:\n")
    for task in luna_tasks:
        print(f"  - {task}")
    print()
    
    # Step 5: Demonstrate sorting and filtering
    print("=" * 60)
    print("SORTING AND FILTERING")
    print("=" * 60)
    print("Mochi tasks before sorting:")
    for task in mochi.get_tasks():
        print(f"  - {task.name} at {task.scheduled_time}")
    print()

    scheduler_mochi = Scheduler(
        owner=owner,
        pet=mochi,
        available_time=owner.available_time_per_day
    )
    sorted_by_time = scheduler_mochi.sort_by_time(mochi.get_tasks())

    print("Mochi tasks sorted by time:")
    for task in sorted_by_time:
        print(f"  - {task.name} at {task.scheduled_time}")
    print()

    pending_mochi = scheduler_mochi.filter_tasks(pet_name="Mochi", completed=False)
    print(f"Pending tasks for Mochi: {len(pending_mochi)}")
    for task in pending_mochi:
        print(f"  - {task.name} ({task.frequency})")
    print()

    # Step 6: Generate schedules
    print("=" * 60)
    print("GENERATING DAILY SCHEDULES")
    print("=" * 60)
    print()
    
    # Schedule for Mochi
    mochi_schedule = scheduler_mochi.generate_schedule()
    print(scheduler_mochi.explain_plan(mochi_schedule))
    print()
    
    # Schedule for Luna
    scheduler_luna = Scheduler(
        owner=owner,
        pet=luna,
        available_time=owner.available_time_per_day
    )
    
    luna_schedule = scheduler_luna.generate_schedule()
    print(scheduler_luna.explain_plan(luna_schedule))
    print()
    
    # Step 7: Conflict detection
    print("=" * 60)
    print("CONFLICT DETECTION")
    print("=" * 60)
    conflict_warnings = scheduler_mochi.detect_conflicts()
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"WARNING: {warning}")
    else:
        print("No conflicts found.")
    print()

    # Step 8: Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Owner: {owner.name}")
    print(f"Pets: {len(owner.get_pets())}")
    print(f"Total tasks: {len(owner.get_all_tasks())}")
    print(f"Mochi's scheduled tasks: {len(mochi_schedule)}/{len(mochi_tasks)}")
    print(f"Luna's scheduled tasks: {len(luna_schedule)}/{len(luna_tasks)}")
    print()
    
    # Step 9: Test task completion and recurring automation
    print("=" * 60)
    print("TESTING TASK COMPLETION + RECURRING")
    print("=" * 60)
    print()
    
    if mochi_schedule:
        task_to_complete = mochi_schedule[0]
        before_count = len(mochi.get_tasks())
        print(f"Before completion: {task_to_complete}")
        scheduler_mochi.mark_task_complete(task_to_complete.name, pet_name="Mochi")
        print(f"After completion:  {task_to_complete}")
        after_count = len(mochi.get_tasks())
        print(f"Task count before: {before_count}, after: {after_count}")

        if after_count > before_count:
            recurring_task = mochi.get_tasks()[-1]
            print(
                f"New recurring task created: {recurring_task.name} due {recurring_task.due_date} at {recurring_task.scheduled_time}"
            )

        completed_tasks = scheduler_mochi.filter_tasks(pet_name="Mochi", completed=True)
        print(f"Completed tasks for Mochi: {len(completed_tasks)}")
        print()


if __name__ == "__main__":
    main()
