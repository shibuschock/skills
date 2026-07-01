---
name: cia-builder
description: Build a Change Impact Assessment (CIA) for ANY project from current/future-state transcripts, interviews, or workshop notes — producing an Excel workbook plus a self-contained interactive HTML dashboard (filter, sort, drill to full detail). Bakes in a portable OCM method: the 6 MECE Change Dimensions (each impact tagged multi-label with one Primary), severity/complexity scoring, scope disposition, and optional analytical layers (TOM Shifts, Value Realization, Training Needs, Workshop/Future-State status). Supports an incremental update loop to re-run on new transcripts. Use when the user asks to create, build, update, refresh, or analyze a CIA, change impact assessment, or change-impact analysis from transcripts, interviews, or current-vs-future-state notes — for any new or existing project.
---

# CIA Builder

Turn raw transcripts (current state + future state) into a **Change Impact Assessment** — an **Excel workbook + interactive HTML dashboard** — for any project. Claude does the extraction; a bundled Python script does the rendering. Nothing is hardcoded to a client; everything drives off a small `project.json` that Claude fills in.

This skill is **conversational**: gather what you need in plain language, write the config and records files yourself, and run the scripts yourself. The user should never have to hand-edit JSON or run a terminal.

## Workflow

1. **Gather the project basics** (ask only for what's missing): project name, business units, locations, and — if the user has brand preferences — colors/font/footer. Ask where their transcripts live and where they want the outputs. Then **write `project.json`** yourself (use `examples/project.example.json` as the shape). Include the optional `tom_shifts` / `benefits` / `training` blocks only if the engagement actually uses those layers.

2. **Read the references before extracting** (they define every field and rule):
   - `references/CIA_SCHEMA.md` — record fields (core + optional).
   - `references/METHODOLOGY.md` — the 6 Change Dimensions (MECE), scoring, scope, optional layers.

3. **Extract the impacts.** Read the current/future-state transcripts and write `cia_records.json` — one object per distinct **change impact** (a current→future change to how people work). Apply the rules: tag every dimension that materially applies and pick exactly one **Primary**; Skills ≠ tool training; score severity/complexity 1–5 only where the session supports it; populate optional fields only where the transcript backs them. **Do not fabricate — a blank is correct, an invented value is a defect.** For large transcript sets, split across subagents (Agent tool), each returning a JSON chunk against the schema; then merge and validate (every record has the required fields; the Primary is within `dimensions`).

4. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/cia_render.py cia    --records cia_records.json --config project.json --outdir OUT
   python3 scripts/cia_render.py readme --config project.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> CIA.xlsx`, `<Project> CIA Dashboard.html`, `README.md`. The dashboard grows extra tabs — **TOM Shifts**, **Value Realization**, **Training Needs**, **Workshop Status** — only when the records carry the fields that feed them.

5. **Update later (incremental).** When new transcripts arrive, don't rebuild — follow `references/UPDATE_LOOP.md`: extract just the new records, merge them into the existing `cia_records.json` with `scripts/cia_merge.py`, then re-render. Keep `cia_records.json` as the canonical dataset between runs.

6. **QA.** Open the HTML (or headless-render it) and confirm the tabs/filters work, rows expand to detail, and the tiles drill into the register. Spot-check a few records against the transcript. Report where the files were written.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate (e.g. after an incremental update).
- Requires `openpyxl` (`pip install openpyxl`). The HTML output is a single self-contained file with zero runtime dependencies.
- Derived fields — `severity_label`, `impact_score` (= complexity × severity), Primary-first dimension ordering, `future_state_status` defaults, staleness — are computed by the renderer. Don't hand-compute them.
- Reuse for any project by swapping the transcripts + `project.json`.
- **Stakeholder analysis is a separate skill** (`sha-builder`). Keep CIA `roles_impacted` names consistent with the SHA stakeholder-group names so the two stay reconciled.
