"""
Tests for PawPal+ System

Tests verify key behaviors of the system:
- Task completion tracking
- Pet task management
- Owner pet management
- Scheduling logic
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTask:
    """Test the Task class."""
    
    def test_task_creation(self):
        """Verify that a task can be created with all attributes."""
        task = Task(
            name="Walk",
            description="Morning walk",
            duration_minutes=30,
            priority=5,
            category="exercise"
        )
        assert task.name == "Walk"
        assert task.duration_minutes == 30
        assert task.priority == 5
        assert task.completed is False
    
    def test_mark_complete(self):
        """Verify that mark_complete() changes the task's status."""
        task = Task(
            name="Feeding",
            description="Feed the pet",
            duration_minutes=10,
            priority=5,
            category="feeding"
        )
        assert task.completed is False
        task.mark_complete()
        assert task.completed is True
    
    def test_is_urgent_high_priority(self):
        """Verify that high priority tasks are marked as urgent."""
        urgent_task = Task(
            name="Medication",
            description="Give medication",
            duration_minutes=5,
            priority=5,
            category="medication"
        )
        assert urgent_task.is_urgent() is True
    
    def test_is_urgent_low_priority(self):
        """Verify that low priority tasks are not marked as urgent."""
        normal_task = Task(
            name="Grooming",
            description="Brush coat",
            duration_minutes=15,
            priority=2,
            category="grooming"
        )
        assert normal_task.is_urgent() is False
    
    def test_get_priority_score(self):
        """Verify that priority score is calculated correctly."""
        feeding_task = Task(
            name="Feeding",
            description="Feed the pet",
            duration_minutes=10,
            priority=5,
            category="feeding"
        )
        score = feeding_task.get_priority_score()
        # 5 * 100 + 50 (feeding bonus) = 550
        assert score == 550
    
    def test_get_priority_score_medication(self):
        """Verify that medication tasks get priority boost."""
        med_task = Task(
            name="Medication",
            description="Give meds",
            duration_minutes=5,
            priority=3,
            category="medication"
        )
        score = med_task.get_priority_score()
        # 3 * 100 + 50 (medication bonus) = 350
        assert score == 350


class TestPet:
    """Test the Pet class."""
    
    def test_pet_creation(self):
        """Verify that a pet can be created with attributes."""
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=["needs exercise"]
        )
        assert pet.name == "Mochi"
        assert pet.species == "dog"
        assert pet.age == 3
        assert len(pet.special_needs) == 1
    
    def test_add_task_to_pet(self):
        """Verify that adding a task to a pet increases the task count."""
        pet = Pet(name="Mochi", species="dog", age=3)
        
        assert len(pet.tasks) == 0
        
        task = Task(
            name="Walk",
            description="Morning walk",
            duration_minutes=30,
            priority=5,
            category="exercise"
        )
        pet.add_task(task)
        
        assert len(pet.tasks) == 1
        assert pet.tasks[0].name == "Walk"
    
    def test_add_multiple_tasks_to_pet(self):
        """Verify that multiple tasks can be added to a pet."""
        pet = Pet(name="Luna", species="cat", age=5)
        
        task1 = Task("Feeding", "Feed Luna", 5, 5, "feeding")
        task2 = Task("Playtime", "Play with Luna", 15, 3, "enrichment")
        task3 = Task("Grooming", "Brush Luna", 10, 2, "grooming")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        assert len(pet.tasks) == 3
    
    def test_get_tasks_from_pet(self):
        """Verify that get_tasks() returns all tasks for a pet."""
        pet = Pet(name="Mochi", species="dog", age=3)
        
        task1 = Task("Walk", "Morning walk", 30, 5, "exercise")
        task2 = Task("Feeding", "Breakfast", 10, 5, "feeding")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        tasks = pet.get_tasks()
        assert len(tasks) == 2
        assert tasks[0].name == "Walk"
        assert tasks[1].name == "Feeding"
    
    def test_get_pet_info(self):
        """Verify that get_info() returns pet information correctly."""
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=["needs exercise"]
        )
        task = Task("Walk", "Morning walk", 30, 5, "exercise")
        pet.add_task(task)
        
        info = pet.get_info()
        assert info["name"] == "Mochi"
        assert info["species"] == "dog"
        assert info["age"] == 3
        assert info["task_count"] == 1


class TestOwner:
    """Test the Owner class."""
    
    def test_owner_creation(self):
        """Verify that an owner can be created."""
        owner = Owner(
            name="Jordan",
            email="jordan@example.com",
            available_time_per_day=120
        )
        assert owner.name == "Jordan"
        assert owner.email == "jordan@example.com"
        assert owner.available_time_per_day == 120
    
    def test_add_pet_to_owner(self):
        """Verify that a pet can be added to an owner."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet = Pet("Mochi", "dog", 3)
        
        assert len(owner.pets) == 0
        owner.add_pet(pet)
        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Mochi"
    
    def test_add_multiple_pets_to_owner(self):
        """Verify that an owner can have multiple pets."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet1 = Pet("Mochi", "dog", 3)
        pet2 = Pet("Luna", "cat", 5)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        assert len(owner.pets) == 2
    
    def test_get_pets_from_owner(self):
        """Verify that get_pets() returns all pets for an owner."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet1 = Pet("Mochi", "dog", 3)
        pet2 = Pet("Luna", "cat", 5)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        pets = owner.get_pets()
        assert len(pets) == 2
        assert pets[0].name == "Mochi"
        assert pets[1].name == "Luna"
    
    def test_get_all_tasks_across_pets(self):
        """Verify that get_all_tasks() returns tasks from all pets."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        
        mochi = Pet("Mochi", "dog", 3)
        mochi.add_task(Task("Walk", "Morning walk", 30, 5, "exercise"))
        mochi.add_task(Task("Feeding", "Breakfast", 10, 5, "feeding"))
        
        luna = Pet("Luna", "cat", 5)
        luna.add_task(Task("Feeding", "Breakfast", 5, 5, "feeding"))
        
        owner.add_pet(mochi)
        owner.add_pet(luna)
        
        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 3
    
    def test_set_owner_preferences(self):
        """Verify that owner preferences can be set."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        
        assert len(owner.preferences) == 0
        
        owner.set_preferences({"start_time": "8:00 AM", "priority": "exercise"})
        
        assert owner.preferences["start_time"] == "8:00 AM"
        assert owner.preferences["priority"] == "exercise"


class TestScheduler:
    """Test the Scheduler class."""
    
    def test_scheduler_creation(self):
        """Verify that a scheduler can be created."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet = Pet("Mochi", "dog", 3)
        scheduler = Scheduler(owner, pet, 120)
        
        assert scheduler.pet.name == "Mochi"
        assert scheduler.available_time == 120
    
    def test_prioritize_tasks(self):
        """Verify that tasks are prioritized correctly."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet = Pet("Mochi", "dog", 3)
        scheduler = Scheduler(owner, pet, 120)
        
        task1 = Task("Grooming", "Brush", 15, 2, "grooming")
        task2 = Task("Feeding", "Breakfast", 10, 5, "feeding")
        task3 = Task("Playtime", "Play", 20, 3, "enrichment")
        
        tasks = [task1, task2, task3]
        prioritized = scheduler.prioritize_tasks(tasks)
        
        # Feeding should be first (priority 5), then Playtime (priority 3), then Grooming (priority 2)
        assert prioritized[0].name == "Feeding"
        assert prioritized[1].name == "Playtime"
        assert prioritized[2].name == "Grooming"
    
    def test_generate_schedule_with_limited_time(self):
        """Verify that scheduler respects available time constraints."""
        owner = Owner("Jordan", "jordan@example.com", 50)  # Only 50 minutes
        pet = Pet("Mochi", "dog", 3)
        
        # Add tasks totaling 85 minutes
        pet.add_task(Task("Walk", "Morning walk", 30, 5, "exercise"))
        pet.add_task(Task("Feeding", "Breakfast", 10, 5, "feeding"))
        pet.add_task(Task("Dinner", "Dinner", 10, 5, "feeding"))
        pet.add_task(Task("Playtime", "Play", 20, 3, "enrichment"))
        pet.add_task(Task("Grooming", "Brush", 15, 2, "grooming"))
        
        scheduler = Scheduler(owner, pet, owner.available_time_per_day)
        schedule = scheduler.generate_schedule()
        
        # Calculate total time in schedule
        total_time = sum(task.duration_minutes for task in schedule)
        assert total_time <= 50  # Should not exceed available time
    
    def test_assign_times_to_tasks(self):
        """Verify that tasks are assigned time slots correctly."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet = Pet("Mochi", "dog", 3)
        scheduler = Scheduler(owner, pet, 120)
        
        task1 = Task("Feeding", "Breakfast", 10, 5, "feeding")
        task2 = Task("Walk", "Morning walk", 30, 5, "exercise")
        
        time_schedule = scheduler.assign_times([task1, task2])
        
        assert "Feeding" in time_schedule
        assert "Walk" in time_schedule
        assert time_schedule["Feeding"] == ("08:00", "08:10")
        assert time_schedule["Walk"] == ("08:10", "08:40")
    
    def test_explain_plan(self):
        """Verify that explain_plan() generates a readable explanation."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet = Pet("Mochi", "dog", 3)
        pet.add_task(Task("Feeding", "Breakfast", 10, 5, "feeding"))
        pet.add_task(Task("Walk", "Morning walk", 30, 5, "exercise"))
        
        scheduler = Scheduler(owner, pet, 120)
        schedule = scheduler.generate_schedule()
        
        explanation = scheduler.explain_plan(schedule)
        
        assert "Mochi" in explanation
        assert "Feeding" in explanation
        assert "Walk" in explanation
        assert "08:00" in explanation  # Start time should be in explanation
        assert "120" in explanation  # Available time should be mentioned
    
    def test_generate_schedule_with_no_tasks(self):
        """Verify that scheduler handles pets with no tasks."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet = Pet("Mochi", "dog", 3)  # No tasks added
        
        scheduler = Scheduler(owner, pet, 120)
        schedule = scheduler.generate_schedule()
        
        assert schedule == []


# Integration Tests
class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_full_workflow(self):
        """Verify the complete workflow from owner creation to schedule generation."""
        # Create owner
        owner = Owner("Jordan", "jordan@example.com", 120)
        
        # Create pets
        mochi = Pet("Mochi", "dog", 3, special_needs=["needs exercise"])
        luna = Pet("Luna", "cat", 5)
        
        owner.add_pet(mochi)
        owner.add_pet(luna)
        
        # Add tasks
        mochi.add_task(Task("Walk", "30-min walk", 30, 5, "exercise"))
        mochi.add_task(Task("Feeding", "Meals", 20, 5, "feeding"))
        
        luna.add_task(Task("Feeding", "Meals", 10, 5, "feeding"))
        luna.add_task(Task("Playtime", "Interactive play", 15, 3, "enrichment"))
        
        # Generate schedules
        scheduler_mochi = Scheduler(owner, mochi, owner.available_time_per_day)
        schedule_mochi = scheduler_mochi.generate_schedule()
        
        scheduler_luna = Scheduler(owner, luna, owner.available_time_per_day)
        schedule_luna = scheduler_luna.generate_schedule()
        
        # Verify results
        assert len(owner.get_pets()) == 2
        assert len(owner.get_all_tasks()) == 4
        assert len(schedule_mochi) > 0
        assert len(schedule_luna) > 0
    
    def test_task_completion_tracking(self):
        """Verify that multiple tasks can be completed and tracked."""
        owner = Owner("Jordan", "jordan@example.com", 120)
        pet = Pet("Mochi", "dog", 3)
        
        owner.add_pet(pet)
        
        task1 = Task("Walk", "Morning walk", 30, 5, "exercise")
        task2 = Task("Feeding", "Breakfast", 10, 5, "feeding")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Complete tasks
        task1.mark_complete()
        task2.mark_complete()
        
        # Verify completion
        assert task1.completed is True
        assert task2.completed is True
        assert all(task.completed for task in pet.get_tasks())
