---
name: training-rollout-builder
description: Plan training deployment and measurement for ANY project or change program — turning a curriculum blueprint (curriculum.json) and needs matrix into a rollout plan: delivery waves by business unit/location/go-live, the schedule and logistics, super-user/champion enablement, learner comms touchpoints, readiness criteria, a Kirkpatrick L1–L4 measurement plan tied to the CIA's value levers, and a spaced reinforcement/sustainment plan. Step 4 of the training suite (Implement & Evaluate). Use when the user asks to plan a training rollout, build a deployment/delivery schedule, set up training measurement or evaluation, plan reinforcement/sustainment, or organize super-users/champions. Note: this is the training-delivery layer — broad change comms/stakeholder engagement live in the CIA/SHA work.
---

# Training Rollout & Measurement Builder

Turn the curriculum into a **deployment + measurement plan** — who gets trained when, how you'll know it landed, and how it sticks. Step 4 (Implement & Evaluate) of the training suite.

## Read first
- `../_training-shared/project-context.example.json` — copy it per project, swap the values, and read the project's copy (locations, audiences, measurement config, modalities). **If no per-project copy exists, create one** from the example, filling it from the conversation and any upstream artifacts. Note: this is a different file from `project.json` (the renderer config in step 10, whose brand slots are literally named `navy`/`magenta` = primary/accent).
- `../_training-shared/references/LEARNING-METHODOLOGY.md` — §2 (70-20-10, esp. social/experiential), §7 (Kirkpatrick), §8 (anti-patterns).
- `references/ROLLOUT_MEASUREMENT.md` — plan structure + measurement design.

## Inputs
- **`curriculum.json`** (modules, paths, hours, assessments) and **`training_needs.json`** (audiences, populations, constraints, priorities). If absent, ask for the module list, audiences, and go-live date(s).
- **Go-live date(s) / waves** — ask the user; this drives the whole schedule (work backward from go-live).

## Workflow
1. **Confirm the timeline.** Get go-live date(s) and any wave structure (by BU, location, or phase). Everything schedules backward from go-live. **Multi-go-live programs:** give each `go_lives` entry an `offset_weeks` (weeks after the first go-live, e.g. GL-2 = GL-1 + 8 weeks) when the spacing is known — the renderer then plots all waves on one absolute axis; without offsets it renders one timeline section per go-live.
2. **Define delivery waves.** Group audiences × locations into waves. Sequence super-users/champions *first* (train-the-trainer), then the broader population — **per go-live**: each go-live gets its own super-user/TTT wave ahead of its population waves. Each wave lists `modules`, `audiences`, `dates`, `delivery_mode`, `headcount`. Modules the curriculum marks `gated — do not build` go in `deferred_modules` with the reason, never in a wave.
3. **Schedule + logistics.** Map modules to dates/sessions respecting `access_constraints` (shift work, peak business season, no-email frontline). Note environment/sandbox readiness, devices, facilitators, room/VILT needs.
4. **Enable super-users/champions.** The 20% social band: who they are, their deeper track, their role at go-live and after.
5. **Learner comms touchpoints.** Training-specific only (invites, pre-work, reminders, "you're go-live ready"). Defer broad change/stakeholder comms to the CIA/SHA engagement work — don't duplicate it; reference it.
6. **Readiness criteria + carry the gates.** Define "trained and ready" per audience (assessment passed, practice completed, access granted). This is the go/no-go training gate. Then **carry every curriculum `non_training_gates` entry into the plan**: program-level preconditions → `program_gates`, site-specific ones → `site_gates`, audience-specific ones → that audience's `readiness_criteria`. Machine-check (or at minimum list side by side) that every flagged gate from the curriculum landed somewhere — none may silently drop.
7. **Measurement plan (Kirkpatrick).** L1 reaction, L2 learning (from curriculum assessments), L3 behavior (on-the-job adoption), L4 results — tie L4 to the CIA `value_levers` / `benefit_at_risk`. Name the metric, method, owner, timing for each.
8. **Reinforcement / sustainment.** Spaced microlearning, refreshers, job-aid upkeep, new-hire onboarding (critical for high-turnover audiences), and how new CIA impacts re-enter the loop.
9. **Write `rollout_plan.md`** (structure in `references/ROLLOUT_MEASUREMENT.md`) **and `rollout_plan.json`** (schema in `references/ROLLOUT_SCHEMA.md`) — wave windows are week offsets backward from go-live; only include real dates the user confirmed. Plus a one-screen summary (waves table, readiness gates, measurement scorecard).
10. **Render** (run it yourself; `python3`, or `python` on Windows). Write a small `project.json` first if one doesn't exist (use `examples/project.example.json` as the shape):
   ```
   python3 scripts/rollout_render.py --records rollout_plan.json --config project.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> Training Rollout.xlsx` (Waves & Sessions + Readiness + Measurement sheets) and `<Project> Rollout Dashboard.html` (self-contained: wave timeline anchored backward from go-live in weeks — no fabricated dates — readiness gates, Kirkpatrick L1–L4 panel with linked value levers, super-user enablement, reinforcement schedule, learner comms).
11. **QA.** Every wave `modules` id exists in `curriculum.json` (or sits in `deferred_modules` with a reason); super-user waves precede their population **per go-live**; every curriculum `non_training_gates` entry appears in `program_gates` / `site_gates` / `readiness_criteria`; L4 rows carry a `value_lever`; no invented dates/headcounts (PLACEHOLDER + flag instead). Open the HTML (or headless-render it) and confirm the timeline bars land in the right GL-week windows (multi-go-live: waves plot against their own go-live, not `go_lives[0]`) and all panels render. Report where the files were written.

## Output
- `rollout_plan.md` + `rollout_plan.json` — waves, schedule, super-user plan, comms touchpoints, readiness criteria, measurement plan, reinforcement plan.
- `<Project> Training Rollout.xlsx` + `<Project> Rollout Dashboard.html` — rendered deliverables.

## Notes
- **Won't overwrite:** re-running the renderer refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate. Requires `openpyxl`.
- Scope boundary: this is **training delivery + evaluation**. Enterprise change comms, stakeholder engagement, and sponsorship live in the CIA/SHA deliverables — reference them, don't rebuild them.
- Don't invent dates or headcount — ask, or placeholder + flag.
- Composable: standalone (give it modules + go-live) or chained (curriculum + needs in → rollout out).
