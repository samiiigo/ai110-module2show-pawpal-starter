# PawPal+ Project Reflection

## 1. System Design

### Core Actions (from scenario analysis)

1. **Add/manage pets** - Owner creates a pet profile with basic info (name, species, age, special needs)
2. **Create and manage care tasks** - Owner adds tasks (walk, feeding, meds, enrichment, grooming) with duration and priority level
3. **Generate daily schedule** - App produces a daily plan that selects and orders tasks based on time available, priorities, and owner preferences

---

**a. Initial design**

I designed PawPal+ with four main classes following a clean separation of concerns:

1. **Owner** - Represents the pet owner with their name, email, available time per day, and preferences. Manages the collection of pets they own. Responsibilities: tracking owner constraints and preferences.

2. **Pet** - Represents a pet with attributes like name, species, age, and special needs. Holds a collection of care tasks assigned to that pet. Responsibilities: storing pet information and managing tasks specific to the pet.

3. **Task** - Represents a discrete care activity (walk, feeding, medication, etc.) using dataclass for clean data storage. Each task has a name, description, duration in minutes, priority level (1-5), category, and frequency. Methods include `get_priority_score()` to calculate urgency and `is_urgent()` to flag time-sensitive tasks.

4. **Scheduler** - The core logic engine that generates daily schedules. Takes an owner and pet, considers available time, and produces an ordered list of tasks that fit within constraints. Key methods: `prioritize_tasks()` to rank by importance, `assign_times()` to slot tasks into time slots, and `explain_plan()` to justify scheduling decisions.

**Design rationale:**
- Used dataclasses for Task, Pet, and Owner to keep data structures clean and maintainable
- Created a separate Scheduler class so scheduling logic is decoupled from data representation
- Relationships: Owner has many Pets, each Pet has many Tasks, and Scheduler orchestrates the planning

**b. Design changes**

- This section will be completed during Phase 2 (implementation).
- As we build the scheduling logic, we may discover missing relationships or refactor responsibilities between classes.
- Any significant changes to the UML structure or class behavior will be documented here.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
