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
            frequency="daily"
        ),
        Task(
            name="Breakfast",
            description="Feed Mochi breakfast",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily"
        ),
        Task(
            name="Dinner",
            description="Feed Mochi dinner",
            duration_minutes=10,
            priority=5,
            category="feeding",
            frequency="daily"
        ),
        Task(
            name="Playtime",
            description="Interactive play and training",
            duration_minutes=20,
            priority=3,
            category="enrichment",
            frequency="daily"
        ),
        Task(
            name="Grooming",
            description="Brush coat and check nails",
            duration_minutes=15,
            priority=2,
            category="grooming",
            frequency="weekly"
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
            frequency="daily"
        ),
        Task(
            name="Dinner",
            description="Feed Luna dinner",
            duration_minutes=5,
            priority=5,
            category="feeding",
            frequency="daily"
        ),
        Task(
            name="Litter Box",
            description="Clean litter box",
            duration_minutes=10,
            priority=4,
            category="maintenance",
            frequency="daily"
        ),
        Task(
            name="Playtime",
            description="Interactive play with toys",
            duration_minutes=15,
            priority=3,
            category="enrichment",
            frequency="daily"
        ),
    ]
    
    for task in luna_tasks:
        luna.add_task(task)
    
    print(f"✓ Added {len(luna_tasks)} tasks for {luna.name}:\n")
    for task in luna_tasks:
        print(f"  - {task}")
    print()
    
    # Step 5: Generate schedules
    print("=" * 60)
    print("GENERATING DAILY SCHEDULES")
    print("=" * 60)
    print()
    
    # Schedule for Mochi
    scheduler_mochi = Scheduler(
        owner=owner,
        pet=mochi,
        available_time=owner.available_time_per_day
    )
    
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
    
    # Step 6: Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Owner: {owner.name}")
    print(f"Pets: {len(owner.get_pets())}")
    print(f"Total tasks: {len(owner.get_all_tasks())}")
    print(f"Mochi's scheduled tasks: {len(mochi_schedule)}/{len(mochi_tasks)}")
    print(f"Luna's scheduled tasks: {len(luna_schedule)}/{len(luna_tasks)}")
    print()
    
    # Step 7: Test task completion
    print("=" * 60)
    print("TESTING TASK COMPLETION")
    print("=" * 60)
    print()
    
    if mochi_schedule:
        task_to_complete = mochi_schedule[0]
        print(f"Before completion: {task_to_complete}")
        task_to_complete.mark_complete()
        print(f"After completion:  {task_to_complete}")
        print()


if __name__ == "__main__":
    main()
