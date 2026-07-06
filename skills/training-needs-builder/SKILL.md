---
name: training-needs-builder
description: Derive a training needs analysis (TNA) from change impacts for ANY project or change program — turning a CIA (Change Impact Assessment from the cia-builder skill) or raw current/future-state notes into a training needs matrix (audience × capability × current/target proficiency × priority × recommended modalities). Maps each need back to the change impact and Change Dimension that justifies it, and flags impacts where formal training is the wrong response (mindset/role shifts). Step 1 of the training suite; output (training_needs.json) feeds curriculum-architect and training-rollout-builder. Use when the user asks to analyze training needs, build a TNA, figure out "who needs to learn what", or convert a CIA into training requirements.
---

# Training Needs Builder

Turn change into **who needs to learn what, to what level, and how** — a defensible training needs matrix. Step 1 (Analyze) of the training suite. Works for any project or change program.

## Read first
- `../_training-shared/project-context.example.json` — copy it per project, swap the values, and read the project's copy (audiences, modalities, tone). Confirm/replace any `PLACEHOLDER`. **If no per-project copy exists, create one** from the example, filling it from the conversation and any upstream artifacts. Note: this is a different file from `project.json` (the renderer config in step 7, whose brand slots are literally named `navy`/`magenta` = primary/accent) — the context file carries audiences/tone/platform; `project.json` carries name + brand for the render script.
- `../_training-shared/references/LEARNING-METHODOLOGY.md` — §1 (impact→response map), §3 (proficiency), §5 (modalities).
- `references/NEEDS_SCHEMA.md` — the output schema.
- If chaining: `../_training-shared/references/ARTIFACTS.md`.

## Inputs (in priority order)
1. **A CIA** — `cia_records.json` from the `cia-builder` skill (preferred; it's the canonical change data). Each impact carries `roles_impacted`, `role_changes`, and `dimensions`; it MAY also carry `severity`, `complexity`, `priority`, `training_modality`, `estimated_training_hours`, `access_constraints`, and stable `id`s — treat those as optional and don't assume them (see the fallback rules in the workflow). If impacts have no `id`, use titles as `source_impacts` keys and note the fragility.
2. **`training_strategy.json`** from `training-strategy-builder` (optional, read it when present). It supplies modality DEFAULTS per workforce type, governance, LMS/tooling, and phasing constraints the TNA inherits. **Conflict rule:** the strategy sets modality defaults per workforce type; per-impact CIA evidence (`training_modality`) overrides the default for that specific need. Note deviations rather than re-litigating the strategy.
3. **Raw current/future-state notes** — if no CIA exists, run a light intake (ask for the roles, the changes, and scope) and derive needs directly.

## Workflow
1. **Load context + inputs.** Read the project context file and the CIA (or run intake). Reconcile audiences in the context file against the CIA's actual `roles_impacted` — the CIA is canonical for roles.
2. **Derive needs.** For each change impact, ask: *what must each affected role be able to DO that they can't today?* Produce one needs row per **audience × capability**. A single impact can yield several capabilities; multiple impacts can roll into one capability — dedup.
3. **Classify each need** using the methodology:
   - Set `target_proficiency` from the job (Competent for most operational roles, Proficient for leads/super-users — see §3).
   - Estimate `current_proficiency`; the gap sizes effort.
   - Set `bloom_level` for the capability (usually Apply for system tasks — see §4).
   - Carry `driver_dimensions` from the CIA `dimensions`; set `recommended_modalities` from the impact→response map (and the CIA's `training_modality` if present).
   - Set `priority`: inherit the impact's `priority` if present; else derive from `impact_score` = severity × complexity if those exist; **else derive from qualitative signals** (compliance exposure, go-live criticality, population size) and record the basis in `notes` so the derivation is auditable.
4. **Flag the mismatches.** Mark `training_alone_insufficient: true` and note the coaching/comms response when **either** (a) `Mindset/Culture` or `Role/Accountability` is the impact's PRIMARY dimension, **or** (b) the impact's mitigation/consideration text names a non-training response (policy decision, role redesign, sponsor action, negotiated commitment). A secondary Mindset/Culture dimension alone doesn't force the flag — note it instead. Don't silently produce a course for a non-training problem.
   **Disposition every impact.** Impacts that yield no trainable need go in a `needs_dispositions` list (see NEEDS_SCHEMA.md) with a "no-need" reason, so impact coverage is machine-checkable — nothing disappears silently.
5. **Size it.** Carry `estimated_hours` and `access_constraints` from the CIA; add `population_size` (PLACEHOLDER if unknown — flag it).
6. **Write `training_needs.json`** per `NEEDS_SCHEMA.md` (need ids `TN-01`, `TN-02`, …), plus a short **markdown summary** (needs grouped by audience, with totals and the flagged mismatches).
7. **Render** (run it yourself; `python3`, or `python` on Windows). Write a small `project.json` first if one doesn't exist (use `examples/project.example.json` as the shape):
   ```
   python3 scripts/needs_render.py --records training_needs.json --config project.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> TNA.xlsx` (Needs Matrix + By Audience sheets) and `<Project> TNA Dashboard.html` (self-contained: summary tiles, filterable needs table with priority heat, current→target proficiency, modality chips, CIA traceability, and `training_alone_insufficient` flags). The renderer **drops any hours/effort field by design** — sizing is a curriculum-stage output, never a TNA output.
8. **QA.** Every need traces to a `source_impacts` entry; no fabricated proficiencies — blanks where the source is silent; audiences match the CIA. Open the HTML (or headless-render it) and confirm the filters work, rows expand to detail, flagged needs show their non-training response, and **no hours/effort appear anywhere**. Report where the files were written.

## Output
- `training_needs.json` — the matrix (feeds curriculum + rollout).
- `needs_dispositions.json` — impacts reviewed that yielded no trainable need (coverage record; see NEEDS_SCHEMA.md).
- `<Project> TNA.xlsx` + `<Project> TNA Dashboard.html` — rendered deliverables.
- A markdown summary for the user (audiences, capability count, priority spread, flagged "not-a-training-problem" items, open placeholders).

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate. Requires `openpyxl`.
- Do not fabricate. A blank proficiency/hour is correct when the source doesn't support a value; an invented one is a defect (same rule as the CIA).
- Composable: standalone (intake) or chained (CIA in → curriculum out). Don't hand-compute anything the downstream skills derive.
