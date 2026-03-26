"""
PawPal+ System Logic

This module contains the core classes for the PawPal+ pet care scheduling system.
It handles representing owners, pets, tasks, and the scheduling logic that creates
daily plans based on constraints and priorities.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, time, timedelta


@dataclass
class Task:
    """Represents a pet care task.
    
    Attributes:
        name: The name of the task (e.g., 'Walk', 'Feeding')
        description: Detailed description of the task
        duration_minutes: How long the task takes to complete
        priority: Priority level (1-5, where 5 is highest)
        category: Category of task (e.g., 'exercise', 'nutrition', 'medication')
        frequency: How often this task occurs (e.g., 'daily', 'twice-daily', 'weekly')
        completed: Whether the task has been completed today
    """
    name: str
    description: str
    duration_minutes: int
    priority: int  # 1-5, 5 is highest
    category: str
    frequency: str = "daily"
    completed: bool = False
    
    def get_priority_score(self) -> int:
        """Calculate the priority score for scheduling."""
        # Higher priority value = higher score, and urgent categories get bonus
        score = self.priority * 100
        
        # Add urgency bonus for medication and feeding tasks
        if self.category in ("medication", "feeding"):
            score += 50
        
        return score
    
    def is_urgent(self) -> bool:
        """Determine if this task is urgent."""
        return self.priority >= 4 or self.category in ("medication", "feeding")
    
    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
    
    def __str__(self) -> str:
        """Return a readable string representation of the task."""
        status = "✓" if self.completed else "○"
        return f"{status} {self.name} ({self.duration_minutes}min, P{self.priority})"


@dataclass
class Pet:
    """Represents a pet.
    
    Attributes:
        name: The pet's name
        species: Type of pet (e.g., 'dog', 'cat', 'rabbit')
        age: The pet's age (in years)
        special_needs: List of special needs or considerations (e.g., 'allergic to chicken')
        tasks: List of care tasks associated with this pet
    """
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    
    def get_info(self) -> Dict[str, any]:
        """Return pet information as a dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "special_needs": self.special_needs,
            "task_count": len(self.tasks)
        }
    
    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        """Retrieve all tasks for this pet."""
        return self.tasks
    
    def __str__(self) -> str:
        """Return a readable string representation of the pet."""
        return f"{self.name} ({self.species}, {self.age} years old)"


@dataclass
class Owner:
    """Represents a pet owner.
    
    Attributes:
        name: The owner's name
        email: The owner's email address
        available_time_per_day: Minutes available per day for pet care
        preferences: Dictionary of owner preferences and constraints
        pets: List of pets owned by this owner
    """
    name: str
    email: str
    available_time_per_day: int  # in minutes
    preferences: Dict[str, any] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
    
    def get_pets(self) -> List[Pet]:
        """Retrieve all pets owned by this owner."""
        return self.pets
    
    def set_preferences(self, prefs: Dict[str, any]) -> None:
        """Update the owner's preferences and constraints."""
        self.preferences.update(prefs)
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def __str__(self) -> str:
        """Return a readable string representation of the owner."""
        return f"{self.name} ({len(self.pets)} pet{'s' if len(self.pets) != 1 else ''})"


@dataclass
class Scheduler:
    """Generates daily schedules for pet care tasks.
    
    Attributes:
        owner: The Owner object
        pet: The Pet object
        available_time: Minutes available for scheduling today
        daily_schedule: List of tasks scheduled for today
    """
    owner: Owner
    pet: Pet
    available_time: int
    daily_schedule: List[Task] = field(default_factory=list)
    
    def generate_schedule(self) -> List[Task]:
        """Create an optimal daily schedule for pet care tasks.
        
        Takes into account:
        - Available time
        - Task priorities
        - Task duration
        - Owner preferences
        
        Returns:
            A list of Task objects ordered for the day, or empty if not enough time.
        """
        # Get all tasks for this pet
        tasks = self.pet.get_tasks()
        
        if not tasks:
            return []
        
        # Sort tasks by priority
        prioritized = self.prioritize_tasks(tasks)
        
        # Fit tasks into available time
        scheduled = []
        total_time = 0
        
        for task in prioritized:
            if total_time + task.duration_minutes <= self.available_time:
                scheduled.append(task)
                total_time += task.duration_minutes
        
        self.daily_schedule = scheduled
        return scheduled
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority and importance."""
        # Sort by priority score in descending order (highest first)
        return sorted(tasks, key=lambda t: t.get_priority_score(), reverse=True)
    
    def assign_times(self, tasks: List[Task]) -> Dict[str, Tuple[str, str]]:
        """Assign start times to each task in the schedule.
        
        Returns:
            A dictionary mapping task names to (start_time, end_time) tuples.
        """
        schedule_dict = {}
        current_time = 8 * 60  # Start at 8:00 AM (480 minutes from midnight)
        
        for task in tasks:
            start_hour = current_time // 60
            start_min = current_time % 60
            start_time = f"{start_hour:02d}:{start_min:02d}"
            
            end_time_minutes = current_time + task.duration_minutes
            end_hour = end_time_minutes // 60
            end_min = end_time_minutes % 60
            end_time = f"{end_hour:02d}:{end_min:02d}"
            
            schedule_dict[task.name] = (start_time, end_time)
            current_time = end_time_minutes
        
        return schedule_dict
    
    def explain_plan(self, schedule: List[Task]) -> str:
        """Generate a human-readable explanation of why this schedule was chosen."""
        if not schedule:
            return f"Cannot schedule tasks for {self.pet.name} - not enough time available."
        
        explanation = f"Daily Schedule for {self.pet.name}:\n"
        explanation += f"Available time: {self.available_time} minutes\n\n"
        
        time_dict = self.assign_times(schedule)
        total_scheduled = 0
        
        for task in schedule:
            start_time, end_time = time_dict[task.name]
            explanation += f"  {start_time} - {end_time}: {task.name} ({task.duration_minutes}min)\n"
            explanation += f"    Priority: {task.priority}/5 | Category: {task.category}\n"
            total_scheduled += task.duration_minutes
        
        explanation += f"\nTotal scheduled: {total_scheduled}/{self.available_time} minutes\n"
        explanation += f"Scheduling strategy: Prioritized by importance and urgency.\n"
        
        if total_scheduled < self.available_time:
            remaining = self.available_time - total_scheduled
            explanation += f"Recommended: Use remaining {remaining} minutes for free play or relaxation."
        
        return explanation
    
    def __str__(self) -> str:
        """Return a readable string representation of the scheduler."""
        return f"Scheduler for {self.pet.name} ({len(self.daily_schedule)} tasks scheduled)"
