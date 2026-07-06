---
name: curriculum-architect
description: Design a training curriculum from a needs matrix for ANY project or change program — turning training_needs.json (from training-needs-builder) into a curriculum blueprint: role-based learning paths, sequenced modules with measurable Bloom's-aligned learning objectives, a 70-20-10 modality blend (experiential/social/formal), prerequisites, and an assessment plan. Uses backward design (objectives → assessment → content) and keeps a traceable link from each module back to the training need and the originating change impact. Step 2 of the training suite; output (curriculum.json) feeds training-content-builder and training-rollout-builder. Use when the user asks to design a curriculum, build learning paths, structure training into modules, sequence courses, or write learning objectives.
---

# Curriculum Architect

Turn a training needs matrix into a **curriculum blueprint** — what gets learned, in what order, how, and how you'll know it worked. Step 2 (Design) of the training suite. Uses **backward design**: objectives first, then how you'll assess them, then content.

## Read first
- `../_training-shared/project-context.example.json` — copy it per project, swap the values, and read the project's copy (audiences, modalities, blend, tone). **If no per-project copy exists, create one** from the example, filling it from the conversation and any upstream artifacts. Note: this is a different file from `project.json` (the renderer config in step 9, whose brand slots are literally named `navy`/`magenta` = primary/accent).
- `../_training-shared/references/LEARNING-METHODOLOGY.md` — §2 (70-20-10), §3 (proficiency), §4 (Bloom's), §5 (modalities), §6 (andragogy).
- `references/CURRICULUM_SCHEMA.md` — the output schema.
- If chaining: `../_training-shared/references/ARTIFACTS.md`.

## Input
- **`training_needs.json`** from `training-needs-builder` (preferred). If absent, build the needs matrix inline first (invoke the needs method) or ask the user for audiences + capabilities + proficiency targets.

## Workflow
1. **Load needs + context.** Group needs by `audience` → these become **learning paths**. **Clustering target: paths ≈ distinct learner experiences, not one path per audience string.** A path may include modules owned by another audience; prefer shared modules over per-audience clones; treat compound audience strings ("Warehouse Associates & Supervisors") as membership in multiple paths, not a new path; fold thin audiences (one need) into the nearest experience.
2. **Cluster capabilities into modules.** Within a path, group related capabilities into modules sized for the audience (frontline: short, point-of-need; leads/support: longer). Respect progressive disclosure — foundational before advanced. Dedup capabilities shared across audiences into a common module where sensible.
3. **Sequence.** Order modules within each path; set `prerequisites`. Net-new capability (large gap) gets more runway and practice.
4. **Write learning objectives (backward design).** For each module, write observable, measurable objectives at the right `bloom_level` (§4). Each objective references the `capability` it satisfies. "By the end, the learner can [verb] …".
5. **Design the assessment** for each objective set *before* content: type (task check / scenario / quiz), mastery threshold, and which Kirkpatrick level it hits (usually L2). This is the backward-design gate.
6. **Set the 70-20-10 blend.** For each module, name what happens in all three bands — not just the formal 10%. Pull modalities from the needs' `recommended_modalities` and the catalog (§5). For mindset/role-flagged needs, weight social/experiential (set per-module `blend_weights` when the ratio genuinely shifts — the renderer draws the actual proportions).
   **Carry the gates.** Any need flagged `training_alone_insufficient` MUST carry its `non_training_response` into the module's `non_training_gates` (or into a gated placeholder module with `status: "gated — do not build"` when the content can't be defined yet, e.g. an undefined role). Training must never be presented as the fix for a non-training problem — the gates travel with the module into content and rollout.
   **Hours convention:** `duration_minutes` covers the **formal band only** (scheduled facilitated time, incl. hands-on labs). Experiential/social bands are estimated separately or left unsized — ongoing on-the-job practice is described, not clocked.
7. **Build content outlines.** A high-level section list per module (the detailed build is training-content-builder's job — don't write the materials here).
8. **Write `curriculum.json`** per the schema, plus a **markdown blueprint** (paths → modules table with hours, modality blend, objectives count, assessment type) for the user.
9. **Render** (run it yourself; `python3`, or `python` on Windows). Write a small `project.json` first if one doesn't exist (use `examples/project.example.json` as the shape):
   ```
   python3 scripts/curriculum_render.py --records curriculum.json --config project.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> Curriculum.xlsx` (Modules Register + Learning Paths sheets) and `<Project> Curriculum Blueprint.html` (self-contained: path-per-role view with module sequence + prerequisites, module cards with Bloom-tagged objectives, 70-20-10 blend bars, assessment, and traceability back to needs + impacts).
10. **QA.** Every module `maps_to_needs` (need ids that exist in `training_needs.json`) and transitively `maps_to_impacts`. Every objective has a Bloom verb + an assessment. No path targets "Expert" for a frontline audience without justification. Total hours per path are realistic against `access_constraints` (shared modules count once per learner — the program-total tile sums per-path and therefore double-counts them; the unique-module tile is the build/delivery volume). Every `training_alone_insufficient` need's gate appears in some module's `non_training_gates` (or a gated placeholder). Open the HTML (or headless-render it) and confirm every path renders its sequence, module cards show objectives/blend/assessment, gate chips show on gated modules, and no module shows as MISSING. Report where the files were written.

## Output
- `curriculum.json` — paths + modules + objectives + assessment plan (feeds content + rollout).
- `<Project> Curriculum.xlsx` + `<Project> Curriculum Blueprint.html` — rendered deliverables.
- A markdown curriculum blueprint for review.

## Notes
- **Won't overwrite:** re-running the renderer refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate. Requires `openpyxl`.
- Backward design is the rule: objective → assessment → content, never content-first.
- Don't write the actual slides/guides here — that's `training-content-builder`. This skill defines the *blueprint*.
- Composable: standalone or chained (needs in → curriculum out).
