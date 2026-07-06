# Training Strategy Methodology

A portable OCM/L&D method for the *strategic* training layer of a change program. Everything here is a **tunable default** — confirm against the engagement's real constraints before asserting it.

## 1. What a training strategy decides — and what it doesn't

**Decides (this skill):**
- Guiding principles the whole training effort must obey.
- Delivery philosophy and the modality mix per workforce type.
- Governance: who owns curriculum, content accuracy, delivery, and quality.
- Resourcing model: core team, multipliers (super-users/champions), vendor stance.
- Build-vs-buy posture for content and tooling.
- Measurement approach and how readiness feeds go/no-go.
- Phasing relative to go-live (waves, readiness gates, hypercare reinforcement).
- Risks, assumptions, and open questions.

**Does NOT decide (downstream — TNA and curriculum stage):**
- Module lists, course catalogs, or learning paths.
- Training hours, effort, or FTE sizing. *Never put hours in a strategy.*
- Role-to-course mapping or learner rosters.
- Content itself (guides, e-learning, job aids).

If the user asks for those, point to the TNA/curriculum stage (training-needs-builder and successors) — the strategy is its input, not its substitute.

## 2. Guiding principles (defaults)

Each principle must carry an implication. Common defaults:
- **Role-based** — built around what each role does, not generic system tours.
- **Just-in-time** — delivered close to go-live, when it will be used and remembered.
- **Minimal but sufficient** — teach the critical path; reinforce the rest in the flow of work.
- **Reinforced in the flow of work** — in-app guidance and job aids at the moment of need.
- **Build once, reuse** — modular content reused across BUs, locations, and waves.
- **Powered by the network** — local trainers and champions carry and sustain delivery.

Tune, drop, or add per program — a good strategy has 4–7 principles, each defensible from evidence (CIA volume, workforce shape, constraints).

## 3. Delivery philosophy & modality strategy by workforce type

Match method to audience and change depth. Stated as **tunable defaults**, not rules:

| Workforce type | Primary modalities (default) | Why |
|---|---|---|
| **Frontline** (store, venue, warehouse, plant floor) | In-app guidance, job aids/quick refs, microlearning, short huddle-based ILT | Hard to release from work; high turnover; needs task-level help at the moment of need |
| **Office / Professional** (back office, planners, analysts, finance) | Deeper ILT/VILT mix, hands-on sandbox labs, e-learning for concepts/policy | Higher process complexity and judgment; can be scheduled; benefits from practice |
| **Field** (technicians, reps, distributed crews) | Mobile-friendly microlearning, VILT, job aids, peer coaching | Dispersed; limited connectivity/time windows |

General modality logic: **ILT/hands-on labs** for high-severity, high-complexity transactional change; **VILT** for dispersed audiences; **e-learning** for awareness/policy at scale; **in-app guidance + job aids** to reduce formal training load and sustain proficiency.

## 4. Governance & roles

Name who owns what — role-level, with named people only if the client supplies them:
- **Training/OCM workstream** — owns the strategy, TNA, curriculum design, reusable core content, delivery coordination, readiness gates.
- **Business process owners** — own content *accuracy* for their processes; validate role-to-curriculum mapping; approve readiness.
- **Business / divisions** — provide trainers and SMEs, release learners, back-fill champions.
- **Change network / champions** — deliver and reinforce locally, surface adoption friction, sustain proficiency post-go-live.

The pattern: the workstream designs and coordinates; **the business owns accuracy, trainers, and the decision to go live**.

## 5. Resourcing model

Three layers:
- **Core team** — instructional designers/developers + a training lead; sized in the TNA stage, stance set here (e.g., "small core team, network-scaled delivery").
- **Multipliers** — train-the-trainer with super-users/champions as the scale mechanism; ties into change-network-builder if that skill is in play.
- **Vendor stance** — where external capacity is acceptable (content development, LMS admin, delivery surge) vs. what stays in-house (process knowledge, ownership).

## 6. Build-vs-buy (content & tooling)

Take a stance per category, e.g.: LMS (use existing vs. procure), in-app guidance / digital adoption platform, authoring tools, off-the-shelf generic content (e.g., basic system navigation) vs. custom role/process content. Unknown tooling decisions are **open questions**, not assumed purchases.

## 7. Measurement

Frame with **Kirkpatrick**: L1 reaction → L2 learning (competency checks) → L3 behavior (adoption, in-app usage, error rates) → L4 results (process outcomes returning to baseline). The strategy sets the *approach* and the decision links:
- Completion/competency thresholds feed the **go/no-go readiness gate** per wave.
- Low-readiness groups trigger targeted intervention before cutover.
- Hypercare metrics decide when reinforcement tapers.

The detailed L1–L4 plan lives in the rollout skill; link to it in `measurement.links`. Adoption metrics tie into adoption-metrics-builder where used. **Never invent targets or baselines** — thresholds without a source are open questions.

## 8. Phasing relative to go-live

Anchor everything to go-live offsets, not calendar dates (which the program owns):
- Train-the-trainer first; then role-based delivery per wave, close to that wave's go-live.
- Readiness gates (e.g., T-60 / T-30) confirming content, trainers, and learners are ready — offsets are tunable.
- Hypercare reinforcement and refreshers in the weeks after each go-live.
- For phased programs with system co-existence: a "which system for which process" transition curriculum for roles running old and new in parallel, retired as each phase cuts over.

## 9. Risks, assumptions, open questions — no fabrication

- Every risk gets a mitigation and an owner (role-level is fine).
- Assumptions are stated so they can be tested, not buried.
- **Anything unknown is an open question, not an invented answer.** An LMS not yet chosen, a trainer commitment not yet secured, an unconfirmed budget — record them as open questions with who must answer. A blank or a question is correct; a fabricated fact is a defect.
