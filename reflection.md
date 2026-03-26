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

During Phase 2 implementation, I made the following refinements to the initial design:

1. **Added `completed` field to Task** - Tasks now track whether they've been completed using a boolean flag. This enables progress tracking and helps users see what's been done vs. what's pending.

2. **Added `mark_complete()` method** - Instead of just storing completion status, I added a dedicated method to change the task's state, making the API clearer.

3. **Added `get_all_tasks()` to Owner** - To simplify scheduling across multiple pets, I added a helper method that collects all tasks from all of the owner's pets. This makes it easier for the Scheduler to work with aggregate data.

4. **Enhanced priority scoring algorithm** - The initial design had a simple `get_priority_score()`, but during implementation I realized that certain task categories (medication, feeding) should always be urgent regardless of assigned priority. I added category-based bonuses to the score calculation.

5. **Added `__str__` methods** - For better debugging and demo output, I added readable string representations to all classes.

6. **Fixed type hints** - Changed `any` to `Any` (from typing module) to follow Python conventions.

**Why these changes made sense:**
- Task completion tracking is essential for the UI to show progress
- The priority scoring refinement reflects real-world pet care (meds and food can't be skipped)
- Helper methods like `get_all_tasks()` reduce coupling between Scheduler and Owner
- The `__str__` methods make debugging and testing much easier

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers multiple constraints in this order of importance:

1. **Time constraint (hard limit)** - Never schedule tasks beyond available time per day
2. **Task priority (1-5 scale)** - Higher priority tasks are scheduled first
3. **Task category urgency** - Medication and feeding tasks get automatic priority boost
4. **Task duration** - Shorter-duration tasks can fit in small time gaps
5. **Owner preferences** (future) - Reserved for owner-specific preferences (start time, order, etc.)

**Decision-making process:**
- Started with simple priority (1-5 scale)
- Observed that all feeding and medication tasks are inherently urgent → added category-based scoring
- Time constraint is non-negotiable since the problem states "available time"
- Sorted tasks by calculated priority score in descending order

**b. Tradeoffs**

**Tradeoff: Greedy scheduling vs. optimal scheduling**

My implementation uses a **greedy algorithm** - it sorts tasks by priority and fits them into available time in order, without trying to rearrange or remove lower-priority tasks to fit more tasks overall.

*Example:* If a low-priority task (grooming, 15 min) fits in the schedule and there's remaining time, it stays. A higher-priority task that's 20 min isn't added if only 10 min remains, even though removing grooming would make room.

*Why this tradeoff is reasonable:*
- **Simplicity**: Easy to understand and explain to users
- **Predictability**: The schedule doesn't change unexpectedly when tasks are added/removed
- **Real-world applicability**: Pet owners likely follow a routine order; rearranging too much feels chaotic
- **Extensibility**: If better scheduling is needed later, algorithms can be swapped in

*Downside:* Might not maximize task count fits in some edge cases.

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
