# Training Suite (shared layer)

Composable Claude Code skills that take a transformation from **change impact → training need → curriculum → materials → rollout & measurement** — project-agnostic, configured per engagement by copying `project-context.example.json`.

They deliberately interlock with the existing **`cia-builder`** skill: a CIA's change impacts are the input that justifies every training need.

## The skills

| # | Skill | ADDIE | In → Out |
|---|-------|-------|----------|
| 1 | `training-needs-builder` | Analyze | CIA (`cia_records.json`) → `training_needs.json` |
| 2 | `curriculum-architect` | Design | `training_needs.json` → `curriculum.json` |
| 3 | `training-content-builder` | Develop | one module → `modules/<id>/*.md` |
| 3b | `interactive-learning-builder` | Develop | one module → interactive HTML (+ optional SCORM) |
| 4 | `training-rollout-builder` | Implement/Evaluate | `curriculum.json` + needs → `rollout_plan.md` |

Each runs **standalone** (it will ask for, or build, what it needs) **or chained** (artifacts flow skill-to-skill). See `references/ARTIFACTS.md` for the handoff contract and `references/LEARNING-METHODOLOGY.md` for the method (70-20-10, Bloom's, proficiency model, modalities, Kirkpatrick).

## Shared layer (`_training-shared/`)
Not a skill (no SKILL.md) — just assets the suite reads:
- `project-context.example.json` — **the per-project config.** Copy this file for each engagement, swap the values, and point the skills at the copy. Fields marked `PLACEHOLDER` must be confirmed/replaced — nothing in it is fact until confirmed.
- `references/LEARNING-METHODOLOGY.md` — the methodology.
- `references/ARTIFACTS.md` — the artifact chain.

## Typical use
1. Build/refresh the CIA with `cia-builder`.
2. Copy `project-context.example.json` to the engagement folder, fill in the real values (replace placeholders).
3. Run skills 1→2→3→4, reviewing each artifact, or jump to whichever step you need.
4. Keep the JSON artifacts in one engagement folder so re-runs are incremental.

## Reuse for another project
Copy the context file, change the values, and run the same skills against that project's CIA. The methodology is portable; only the context file is project-specific.

## Design principles
- **Traceability** — impact → need → module → wave stays linked, so any deliverable defends itself.
- **Don't fabricate** — blanks/placeholders over invented system screens, hours, or headcount.
- **Right response to the right change** — flags mindset/role shifts where a course is the wrong tool.
- **70-20-10** — every plan names experiential + social + formal, not just the course.
