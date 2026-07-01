# sha-builder

A Claude skill that turns **transcripts/interviews** into a **Stakeholder Assessment** for **any project**:

- **SHA** → `<Project> SHA.xlsx` + `<Project> SHA Dashboard.html`
- a per-project **README.md**

The HTML dashboard is a single self-contained file (no internet/dependencies): filterable, sortable table; click any row for full detail; an **Influence × Interest grid** with a dot per group.

## How it works
Claude reads the transcripts and produces structured records (guided by the bundled schema + methodology); a Python script renders the xlsx + HTML. Claude gathers inputs conversationally and runs the scripts — the user never edits JSON or runs a terminal. See `SKILL.md`.

## Methodology baked in (portable OCM)
- **Influence × Interest** (Mendelow) rating (1–5 each).
- **Engagement Strategy** quadrant derived: Manage Closely / Keep Satisfied / Keep Informed / Monitor.
- Pain points, decision authority, sentiment, comms preferences, POC, and champion per group.

## Incremental updates
Re-run on new interviews without rebuilding: extract only the new records, merge into the existing `sha_records.json` with `scripts/sha_merge.py`, then re-render. See `references/UPDATE_LOOP.md`.

## Layout
```
sha-builder/
  SKILL.md                 # instructions for Claude
  README.md                # this file
  references/
    METHODOLOGY.md         # Influence × Interest grid, scoring, engagement quadrants
    SHA_SCHEMA.md          # SHA record fields
    UPDATE_LOOP.md         # incremental refresh from new interviews
  scripts/
    sha_render.py          # xlsx + HTML + readme generator (stdlib + openpyxl)
    sha_merge.py           # dedup/merge new records into an existing dataset (stdlib only)
  examples/
    project.example.json
    sha_records.example.json
```

Requires `openpyxl`. Python 3.9+, cross-platform. Change-impact analysis is the companion **`cia-builder`** skill.
