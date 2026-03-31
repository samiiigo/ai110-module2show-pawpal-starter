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

**Tradeoff: Exact-match conflict detection instead of overlap detection**

The conflict checker currently flags warnings when two tasks have the exact same date and start time (for example, both at 08:00). It does not yet compute full duration overlap windows (for example, 08:00-08:30 overlapping with 08:15-08:45).

*Why this tradeoff is reasonable:*
- **Lightweight implementation**: Fast and easy to reason about while building core features
- **Clear user feedback**: Exact clashes are the most obvious schedule mistakes
- **Low complexity**: Avoids introducing time-range logic before basic planning is stable

*Downside:* Some partial overlaps can be missed until a later, more advanced conflict algorithm is added.

---

## 3. AI Collaboration

**a. How you used AI**

I used VS Code Copilot in distinct ways across phases:

1. **Design brainstorming** - I asked Copilot to pressure-test my class responsibilities before coding (for example, where recurrence and conflict logic should live). This helped me keep behavior in `Scheduler` and avoid scattering logic across the UI.
2. **Implementation acceleration** - I used suggestions for method scaffolding and repetitive test patterns, then edited details manually.
3. **Debugging support** - When tests failed during development, I asked Copilot to explain failure causes and whether the issue was likely in assertion logic or scheduling behavior.
4. **Documentation drafting** - I used Copilot to draft concise README and reflection language, then rewrote sections to match what I actually implemented.

Most helpful prompts were specific and grounded in my files, such as:
- "Given this `Scheduler` implementation, what edge cases are most likely to break recurrence?"
- "Explain why this conflict test might pass even when overlap logic is incomplete."
- "Suggest tests for exact time collisions vs. no-collision control cases."

**b. Judgment and verification**

One AI suggestion I rejected was to implement complex overlap-based conflict detection immediately (full interval intersection) while I was still stabilizing exact-slot conflict behavior.

I modified that suggestion to keep a simpler exact date/time collision detector first, because:
1. It matched current requirements and test scope.
2. It reduced risk of introducing subtle time math bugs.
3. It kept the code easier to explain during demos.

I verified this decision by writing/keeping tests for duplicate-time warnings and ensuring they passed consistently, while documenting overlap detection as a future enhancement.

---

## 4. Testing and Verification

**a. What you tested**

I tested:

1. **Sorting correctness** - tasks are returned in chronological order.
2. **Recurrence behavior** - completing a daily task creates a new task for the next day.
3. **Conflict detection** - duplicate date/time slots produce warnings.
4. **Schedule generation constraints** - generated plans stay within available time.
5. **Edge paths** - pets with no tasks, completion filtering behavior, and end-to-end workflow.

These tests are important because they validate both expected user experience (happy path) and failure-prone boundaries (time conflicts, empty task lists, recurring state changes).

**b. Confidence**

My confidence is **4/5**. The existing suite gives strong coverage for the implemented logic and common edge cases.

Next edge cases I would test:
1. Weekly recurrence date rollovers across month/year boundaries.
2. Multiple tasks with the same name on one pet when marking completion.
3. Robust handling of malformed time strings if external input bypasses the UI.
4. Future overlap-based conflicts (08:00-08:30 vs. 08:15-08:45), not just exact-time clashes.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the separation of concerns: data classes model the domain cleanly, while `Scheduler` owns scheduling intelligence. That structure made it much easier to test and to connect logic to the Streamlit UI without duplicating business rules.

**b. What you would improve**

In another iteration, I would add:

1. True interval-based conflict detection.
2. Better identity for tasks (IDs) so completion actions are unambiguous when names repeat.
3. Multi-pet daily optimization that allocates shared owner time globally across all pets.
4. Persistent storage so tasks and completions survive app restarts.

**c. Key takeaway**

My biggest takeaway is that AI can accelerate implementation, but architectural quality still depends on deliberate human decisions. The strongest results came when I treated Copilot as a collaborator for options and speed, while I stayed responsible for boundaries, tradeoffs, and verification.

Using separate chat sessions by phase helped me stay organized: design conversations stayed conceptual, test conversations stayed evidence-based, and polish conversations focused on UX/docs. That separation reduced context drift and made decisions easier to audit.
