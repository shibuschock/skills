# Training artifacts — the handoff contract

The suite's skills are **composable**: each runs standalone, but their inputs/outputs chain. This file is the contract so any skill can pick up where another left off (or where the CIA left off). Keep these artifacts in one working folder per engagement.

```
   [0] training-strategy-builder ──► training_strategy.json   (optional strategic layer)
                                          │
cia_records.json  ─┐                      │ (optional input: modality defaults,
                   ▼                      ▼  governance, phasing constraints)
   [1] training-needs-builder  ──► training_needs.json
                                      │
                                      ▼
   [2] curriculum-architect  ──► curriculum.json
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
   [3] training-content-builder ──► modules/<id>.md   [4] training-rollout-builder ──► rollout_plan.md
       (one set per module; interactive-learning-         (deploy + measurement, reads curriculum + needs)
        builder renders the interactive twin)
```

All skills read the project's copy of **`_training-shared/project-context.example.json`** for project specifics and **`LEARNING-METHODOLOGY.md`** for the method.

**If no per-project context file exists, CREATE one**: copy `_training-shared/project-context.example.json` into the engagement's working folder (e.g. `project-context.<project>.json`), fill it from the conversation and any upstream artifacts (`project.json`, the CIA), and leave `PLACEHOLDER` where nothing is confirmed. Do not point skills at the Acme example itself.

**Two different files, two different jobs:**
- **`project.json`** — the *renderer config* each render script takes via `--config`. Its brand slots are literally named `navy`/`magenta` but mean *primary*/*accent* — put the program's actual colors in them regardless of hue.
- **The per-project context file** (copied from `project-context.example.json`) — the *content context*: audiences, tone, platform, modalities, measurement. Skills read it while authoring; renderers don't (except `interactive-learning-builder`, whose `--context` flag takes this file, not `project.json`).

## Artifact summary

| Artifact | Produced by | Consumed by | Schema |
|---|---|---|---|
| `cia_records.json` | cia-builder | [1], [3] (change_considerations) | `cia-builder/references/CIA_SCHEMA.md` |
| `training_strategy.json` | [0] strategy (optional) | [1] — modality defaults per workforce type, governance, phasing | `training-strategy-builder/references/SCHEMA.md` |
| `training_needs.json` | [1] needs | [2], [4] | `training-needs-builder/references/NEEDS_SCHEMA.md` |
| `curriculum.json` | [2] curriculum | [3], [4] | `curriculum-architect/references/CURRICULUM_SCHEMA.md` |
| `modules/<id>.md` (+ assets) | [3] content | delivery | `training-content-builder/references/CONTENT_TEMPLATES.md` |
| `<id>.html` / `<id>_scorm.zip` | interactive-learning-builder | delivery / LMS | `interactive-learning-builder/references/OBJECT_SCHEMA.md` |
| `rollout_plan.md` | [4] rollout | program team | `training-rollout-builder/references/ROLLOUT_MEASUREMENT.md` |
| `rollout_plan.json` | [4] rollout | `rollout_render.py` (xlsx + HTML dashboard) | `training-rollout-builder/references/ROLLOUT_SCHEMA.md` |

## Standalone use (no upstream artifact)

Each skill degrades gracefully:
- **needs** with no strategy → derive modalities from the CIA + methodology alone (the strategy is optional).
- **needs** with no CIA → runs its own intake (asks for roles, impacts, scope).
- **curriculum** with no `training_needs.json` → builds the needs matrix inline first (or asks).
- **content** with no `curriculum.json` → asks for the single module's objectives + audience.
- **rollout** with no curriculum → asks for the module list + go-live dates.

## Linkage keys (so artifacts cross-reference)

- A needs row carries `source_impacts` = the CIA `id`/`title` it derives from.
- A curriculum module carries `maps_to_needs` (capability refs) and `maps_to_impacts` (CIA ids).
- A rollout wave carries `modules` (curriculum module ids) and `audiences`.

This keeps an unbroken thread: **change impact → training need → module → rollout wave → measurement**, so any deliverable can be traced back to the business change that justified it.
