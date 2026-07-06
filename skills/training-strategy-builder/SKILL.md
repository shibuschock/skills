---
name: training-strategy-builder
description: Build a Training Strategy for ANY change program — the upstream strategic layer that comes BEFORE the training needs analysis. Produces an Excel strategy-on-a-page register plus a self-contained interactive HTML strategy document (principles, modality-by-workforce matrix, governance, resourcing, build-vs-buy, measurement, phasing relative to go-live, risks/assumptions/open questions). Bakes in a portable OCM/L&D method - guiding principles, modality strategy by workforce type (frontline vs office vs field), governance and ownership model, super-user multiplier resourcing, Kirkpatrick measurement framing, and a strict no-fabrication discipline (unknowns become open questions, not invented answers). Use when the user asks for a training strategy, learning strategy, training approach, enablement strategy, training governance, or training principles for a program.
---

# Training Strategy Builder

Turn program context (and optionally CIA/SHA data) into a **Training Strategy** — an **Excel register + interactive HTML strategy document** — for any change program. This is the *strategic* layer: it sets the principles, modality philosophy, governance, resourcing, measurement, and phasing that a later **training needs analysis** and curriculum must obey. It does **not** list modules or estimate hours — that is TNA/curriculum work downstream.

This skill is **conversational**: gather what you need in plain language, write the JSON files yourself, and run the script yourself. The user should never hand-edit JSON or touch a terminal.

## Workflow

1. **Gather the program basics** (ask only for what's missing):
   - Program name and shape (ERP, PLM, CRM, policy change, etc.) and rough scale.
   - **Workforce types** in scope — e.g., Frontline, Office/Professional, Field — and roughly where they sit (BUs/locations).
   - **Go-live horizon**: single cutover or phased waves, and roughly when.
   - **Constraints**: budget posture, trainer availability, release-from-work limits, union/seasonal factors, languages.
   - **LMS / tooling landscape**: existing LMS, in-app guidance tools (e.g., a digital adoption platform), sandbox availability, authoring tools.
   - Brand preferences if any (colors/font/footer).
   Then **write `project.json`** yourself (shape: `examples/project.example.json`). Note: `project.json` is the *renderer config* — its brand slots are literally named `navy`/`magenta` but mean primary/accent, so put the program's actual colors in them. It is a different file from the suite's per-project context file (copied from `../_training-shared/project-context.example.json`), which carries audiences/tone/platform for the downstream training skills — **if that context file doesn't exist yet, create it** from the example while you have the program facts in hand. If an upstream skill (e.g. cia-builder) already produced a `project.json`, reuse it — extra fields are ignored by this renderer.

2. **Read the references before drafting**:
   - `references/METHODOLOGY.md` — what a training strategy decides vs. what it doesn't; principles, modality defaults by workforce type, governance, resourcing, build-vs-buy, measurement, phasing, risk discipline.
   - `references/SCHEMA.md` — every field of `training_strategy.json`.

3. **Optionally ingest CIA/SHA context.** If the engagement has `cia_records.json` / `sha_records.json` (from cia-builder / sha-builder), read them for evidence: which dimensions dominate (a Skills/Capability-heavy CIA strengthens the training case), which areas carry volume, which stakeholder groups are large or resistant. Use this to ground principles and phasing — cite it in `rationale` fields. Never invent counts if the files aren't there.

4. **Draft the strategy.** Write `training_strategy.json` per the schema. Rules:
   - Every principle carries an implication ("so we will…"), not just a slogan.
   - One `modality_strategy` entry per workforce type, with rationale. Defaults in METHODOLOGY.md are **tunable starting points** — confirm them against the program's constraints.
   - Governance rows name a *role*, not a person, unless the user supplies names.
   - **Do not fabricate.** Anything unknown (LMS decision, trainer commitment, budget) goes in `open_questions`, not as an invented answer. A short open-questions list is a sign of a healthy strategy, not a gap.

5. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/strategy_render.py --plan training_strategy.json --config project.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> Training Strategy.xlsx` and `<Project> Training Strategy.html`.

6. **QA.** Open or headless-render the HTML; confirm the principle tiles, modality matrix, governance panel, phasing timeline, and risk/assumption/open-question panels render with the real content. Spot-check the xlsx sheets. Report where the files were written.

## Downstream handoff

The strategy's decisions are **constraints on the TNA**: workforce types and modality defaults scope the needs analysis; governance names who validates it; phasing sets when training must land. Hand `training_strategy.json` to the training-needs / curriculum work (e.g., a training-needs-builder skill) so the TNA inherits — not re-litigates — these decisions.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate.
- Requires `openpyxl` (`pip install openpyxl`). The HTML is a single self-contained file, zero runtime dependencies.
- Reuse for any program by swapping `project.json` + `training_strategy.json`. Examples use "Acme ERP".
