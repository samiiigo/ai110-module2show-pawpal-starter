"""
PawPal+ System Logic

This module contains the core classes for the PawPal+ pet care scheduling system.
It handles representing owners, pets, tasks, and the scheduling logic that creates
daily plans based on constraints and priorities.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, time


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
    """
    name: str
    description: str
    duration_minutes: int
    priority: int  # 1-5, 5 is highest
    category: str
    frequency: str = "daily"
    
    def get_priority_score(self) -> int:
        """Calculate the priority score for scheduling.
        
        Returns:
            An integer representing the task's importance for scheduling.
        """
        pass
    
    def is_urgent(self) -> bool:
        """Determine if this task is urgent.
        
        Returns:
            True if the task should be prioritized, False otherwise.
        """
        pass


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
        """Return pet information as a dictionary.
        
        Returns:
            A dictionary containing pet details and special needs.
        """
        pass
    
    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list.
        
        Args:
            task: The Task object to add.
        """
        pass
    
    def get_tasks(self) -> List[Task]:
        """Retrieve all tasks for this pet.
        
        Returns:
            A list of Task objects assigned to this pet.
        """
        pass


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
        """Add a pet to the owner's collection.
        
        Args:
            pet: The Pet object to add.
        """
        pass
    
    def get_pets(self) -> List[Pet]:
        """Retrieve all pets owned by this owner.
        
        Returns:
            A list of Pet objects.
        """
        pass
    
    def set_preferences(self, prefs: Dict[str, any]) -> None:
        """Update the owner's preferences and constraints.
        
        Args:
            prefs: Dictionary of preferences to set.
        """
        pass


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
        pass
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority and importance.
        
        Args:
            tasks: List of Task objects to prioritize.
            
        Returns:
            A sorted list of tasks, highest priority first.
        """
        pass
    
    def assign_times(self, tasks: List[Task]) -> Dict[str, any]:
        """Assign start times to each task in the schedule.
        
        Args:
            tasks: Ordered list of tasks to schedule.
            
        Returns:
            A dictionary mapping task names to start times and end times.
        """
        pass
    
    def explain_plan(self, schedule: List[Task]) -> str:
        """Generate a human-readable explanation of why this schedule was chosen.
        
        Args:
            schedule: The list of scheduled tasks.
            
        Returns:
            A string explaining the scheduling decisions and reasoning.
        """
        pass
