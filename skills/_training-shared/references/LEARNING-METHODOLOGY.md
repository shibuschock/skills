# Learning Methodology (shared)

The portable instructional-design methodology behind the training-suite skills. Read this before producing any training deliverable. Everything here is standard, public adult-learning practice — not proprietary to any one tool. It is deliberately written to interlock with the **CIA** (Change Impact Assessment) produced by the `cia-builder` skill: change impacts are the *reason* a training need exists.

---

## 1. From change impact to learning response

A training need is never invented — it is **derived from a change impact**. The CIA's 6 Change Dimensions tell you *what kind* of learning response fits. Map them:

| CIA Change Dimension | What it means | Default learning response |
|---|---|---|
| `Skills/Capability` | People must be able to *do* something new | **Formal** training + practice (ILT/VILT/e-learning) then on-the-job |
| `Ways of Working` | Day-to-day workflow changes | **In-app guidance** + job aids + on-the-job practice |
| `Process/Policy` | New rules/steps to follow | Job aids + e-learning + reference |
| `Data/Decision Inputs` | New information drives decisions | Scenario practice + job aids |
| `Role/Accountability` | Who-does-what shifts | Coaching + manager-led conversations (not a course) |
| `Mindset/Culture` | Belief/attitude shift needed | **Coaching + comms + experiential** — training alone won't move it |

**Rule of thumb:** the higher the `Mindset/Culture` and `Role/Accountability` load, the *less* a formal course will help and the more coaching/social learning matters. Flag this — clients routinely ask for "a course" to solve an adoption problem that is really a mindset/role problem.

---

## 2. The 70-20-10 model

Design the *blend*, not just the course.

- **70% experiential** — on-the-job practice, sandbox/test environment, real tasks with a safety net, in-app guidance in the flow of work.
- **20% social** — coaching, super-users/champions, peer support, manager reinforcement, communities.
- **10% formal** — ILT, VILT, e-learning, structured content.

Most failed rollouts over-invest in the 10% and ignore the 70/20. Every curriculum this suite produces must name what happens in all three bands.

---

## 3. Proficiency model (competency levels)

Rate **current** and **target** proficiency per audience × capability. Behavioral indicators:

| Level | Looks like |
|---|---|
| **Novice** | No exposure; needs step-by-step instruction; can't yet act without help |
| **Advanced Beginner** | Can perform with a job aid / prompting; recognizes situations |
| **Competent** | Performs the standard task reliably and unaided |
| **Proficient** | Handles exceptions and edge cases; adapts to context |
| **Expert** | Optimizes, troubleshoots for others, coaches peers |

For most go-lives the realistic **target is Competent** for operational/frontline roles, **Proficient** for leads/super-users. Targeting "Expert" for everyone is a smell. The gap (current → target) sizes the effort.

---

## 4. Bloom's taxonomy — write objectives at the right level

Every learning objective is **observable + measurable**, framed as "By the end, the learner can [verb] …". Pick the verb at the cognitive level the job actually requires:

| Bloom level | Sample verbs | Use when |
|---|---|---|
| Remember | list, identify, name | Recall facts/terms |
| Understand | explain, describe, summarize | Grasp a concept |
| Apply | use, perform, execute, complete | **Most hands-on system tasks live here** |
| Analyze | compare, differentiate, troubleshoot | Decisions, exceptions |
| Evaluate | assess, prioritize, justify | Judgment roles |
| Create | design, build, plan | Configuration / design roles |

Don't write "understand the new POS" — write "complete a refund in the POS, including a manager override." Match the verb to the proficiency target.

---

## 5. Modality catalog

| Modality | Best for | Watch-outs |
|---|---|---|
| **ILT** (instructor-led, in person) | Complex/net-new capability, high-stakes, mindset shifts | Scheduling cost; hard for shift/frontline |
| **VILT** (virtual instructor-led) | Distributed audiences, demo + practice | Engagement drops past ~90 min |
| **e-learning** (self-paced) | Consistent foundational knowledge, scale, refreshers | Weak for hands-on skill; completion ≠ competence |
| **in-app guidance** (digital adoption) | Ways-of-working, in-the-flow-of-work, high turnover | Needs the system + tooling stood up |
| **job aid / quick reference** | Process/policy steps, point-of-need | Must be findable at the moment of work |
| **microlearning** | Reinforcement, spaced repetition, frontline | Not for first-time complex skills |
| **coaching** | Mindset, role shifts, exceptions | Needs capable coaches/champions |
| **on-the-job practice** | Cementing any new skill | Needs a safe place to fail (sandbox) |

**Default mix by workforce type** (a starting point to tune, not an assumption): for **high-turnover frontline** audiences (shift-based, little desk time), bias toward in-app guidance + job aids + microlearning over scheduled classroom time; for **office/professional** audiences (desk-based, judgment-heavy roles), a deeper ILT/VILT mix with scenario practice usually fits better. Confirm against the project's actual audiences and constraints.

---

## 6. Adult-learning principles (andragogy)

- **Relevance first** — adults learn what's useful *now*; tie every module to the learner's real task and the "what's in it for me."
- **Progressive disclosure** — foundational → advanced; don't dump the whole system at once.
- **Practice + feedback** — people learn by doing, not watching.
- **Spaced repetition** — reinforce over time; one big event fades fast.
- **Respect experience** — connect new ways of working to what they already do.

---

## 7. Measurement (Kirkpatrick + adoption)

Plan measurement *before* build, not after.

| Level | Question | Example |
|---|---|---|
| **L1 Reaction** | Did they find it useful? | Post-session pulse |
| **L2 Learning** | Can they do it? | In-class task check / assessment mastery |
| **L3 Behavior** | Are they doing it on the job? | System usage vs. workaround, observation |
| **L4 Results** | Did it move the business? | Adoption/benefit metrics from the CIA's value levers |

Tie L4 back to the CIA `value_levers` / `benefit_at_risk` so training measurement connects to value realization.

---

## 8. Anti-patterns to flag (don't silently comply)

- "Just build a course" for a mindset/role problem → recommend coaching + comms instead.
- Training scheduled with no sandbox/practice environment → the 70% has nowhere to happen.
- "Train everyone the same" → segment by audience and proficiency gap.
- Completion tracked, competence not → add an L2 check.
- One big bang event, no reinforcement → add spaced microlearning.
