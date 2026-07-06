---
name: sha-builder
description: Build a Stakeholder Assessment (SHA) for ANY project from transcripts, interviews, or stakeholder notes — producing an Excel workbook plus a self-contained interactive HTML dashboard with an Influence × Interest (Mendelow) grid. Bakes in a portable OCM method: rate each stakeholder group on Influence and Interest (1–5) and derive the Engagement Strategy quadrant (Manage Closely / Keep Satisfied / Keep Informed / Monitor), plus pain points, decision authority, sentiment, comms preferences, POC, and champion. Use when the user asks to create, build, update, refresh, or analyze a stakeholder assessment, stakeholder analysis, stakeholder map, engagement/RACI-style plan, or Influence/Interest grid from transcripts, interviews, or stakeholder notes — for any new or existing project.
---

# SHA Builder

Turn transcripts/interviews into a **Stakeholder Assessment** — an **Excel workbook + interactive HTML dashboard** with an **Influence × Interest grid** — for any project. Claude does the extraction; a bundled Python script does the rendering. Nothing is hardcoded to a client; everything drives off a small `project.json` that Claude fills in.

This skill is **conversational**: gather what you need in plain language, write the config and records files yourself, and run the scripts yourself. The user should never have to hand-edit JSON or run a terminal.

## Workflow

1. **Gather the project basics** (ask only for what's missing): project name, business units, locations, and — if the user has brand preferences — colors/font/footer. The `brand` keys `navy` and `magenta` are **semantic slots** (`navy` = primary color, `magenta` = accent), not color requirements — put any brand's hex values there (e.g. teal in `navy`, orange in `magenta`). Ask where their transcripts/interview notes live and where they want the outputs. Then **write `project.json`** yourself (use `examples/project.example.json` as the shape).

2. **Read the references before extracting**:
   - `references/SHA_SCHEMA.md` — stakeholder record fields.
   - `references/METHODOLOGY.md` — the Influence × Interest engagement grid and scoring rules.

3. **Extract the stakeholders.** Read the transcripts/notes and write `sha_records.json` — one object per **stakeholder group/role**. Rate **Influence** (power to affect the change's success) and **Interest** (how much the change affects them) 1–5. Capture pain points, decision authority, sentiment, comms preferences, POC, and champion where supported. You may omit `engagement_strategy` — the quadrant is derived from the grid. **Do not fabricate — a blank is correct.** For a group you've identified but can't yet rate (no evidence), keep the record without scores and set `assessment_status: "Not yet assessed"` — don't drop it. For large sets, split across subagents (Agent tool), each returning a JSON chunk against the schema; merge and validate.

4. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/sha_render.py sha    --records sha_records.json --config project.json --outdir OUT
   python3 scripts/sha_render.py readme --config project.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> SHA.xlsx`, `<Project> SHA Dashboard.html`, `README.md`. The dashboard includes the **Influence / Interest** grid tab (dots plotted per group).

5. **Update later (incremental).** When new interviews arrive, follow `references/UPDATE_LOOP.md`: extract just the new records, merge them into the existing `sha_records.json` with `scripts/sha_merge.py`, then re-render. Keep `sha_records.json` as the canonical dataset between runs.

6. **Validate.** Before rendering (and after any merge), run the schema/chain validator:
   ```
   python3 scripts/validate_chain.py --sha sha_records.json [--cia cia_records.json]
   ```
   Fix every ERROR (missing required fields, influence/interest outside 1–5, duplicate or comma-containing group names). Review WARNs — group↔role mismatches mean the SHA and CIA datasets are drifting.

7. **QA.** Open the HTML (or headless-render it) and confirm the table filters, rows expand to detail, and the Influence × Interest grid shows a dot per group in the right quadrant. Spot-check a few records against the source. Report where the files were written.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate (e.g. after an incremental update).
- Requires `openpyxl` (`pip install openpyxl`). The HTML output is a single self-contained file with zero runtime dependencies.
- The **Engagement Strategy quadrant** is derived from Influence × Interest (High if ≥ 4): Manage Closely / Keep Satisfied / Keep Informed / Monitor. If you write tactics in `engagement_strategy`, the renderer fixes the leading quadrant to match the grid.
- **Change-impact analysis is a separate skill** (`cia-builder`). Keep SHA `stakeholder_group` names consistent with the CIA `roles_impacted` names so the two stay reconciled.
