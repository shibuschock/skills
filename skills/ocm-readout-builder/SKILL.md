---
name: ocm-readout-builder
description: Build an executive readout package for ANY change program from CIA/SHA data — a Change Intensity Map (heat map of which areas change most vs least, derived from severity×complexity), per-theme who/what/how impact boards, and leader talking points in a conversational spoken register. Bakes in a portable OCM method - intensity = volume × depth derived from the CIA (never hand-scored), a Volume×Depth quadrant matrix, 4-7 executive themes clustered by story (not org chart), and theme-level "what's changing" + a spoken "so what" script per theme. Use when the user asks for an executive readout, readout deck content, change intensity map, heat map of change, impact readout, leadership briefing, or leader talking points — for any new or existing project.
---

# OCM Readout Builder

Turn a finished CIA (and optionally SHA) into an **executive readout package**: a **Change Intensity Map** (HTML heat map + Volume×Depth matrix), an **Executive Readout** (HTML with per-theme who/what/how boards + talking points), and a **Talking Points crib sheet** (Markdown, ready for docx conversion). Claude authors the themes and scripts; a bundled Python script derives the intensity math and renders. Nothing is hardcoded to a client; everything drives off `project.json`.

This skill is **conversational**: gather what you need in plain language, write the JSON files yourself, and run the script yourself. The user should never have to hand-edit JSON or run a terminal.

**Division of labor (hard rule):** the intensity map is **derived** from CIA data by the script — never hand-scored, never adjusted to look better. The talking-points prose is **Claude-authored** from the records — every theme must trace to specific impacts; no fabrication.

## Workflow

1. **Gather the basics** (ask only for what's missing): project name, the **audience** (e.g., steering committee, VP staff) and **occasion** (e.g., design readout, phase-gate), where `cia_records.json` lives (built by `cia-builder`; if none exists, build the CIA first), whether an SHA exists, brand preferences, and the output folder. Write `project.json` (shape: `examples/project.example.json` — same shape as cia-builder's, reuse the existing one if the project has it).

2. **Read the references before authoring:**
   - `references/METHODOLOGY.md` — intensity derivation, quadrant labels, theme-construction rules, talking-points register.
   - `references/SCHEMA.md` — `readout.json` fields.

3. **Ingest the records.** Read `cia_records.json` (required) and `sha_records.json` (optional — enriches the WHO panels with stakeholder positions). Note the functional areas, the high-severity impacts, the recurring roles, and the sentiment patterns — the themes come from here.

4. **Author `readout.json`.** Cluster the impacts into **4–7 executive themes** (by story, not org chart — see METHODOLOGY). Each theme: a `title`, a `whats_changing` summary (theme level, what leaders need to know), a `so_what_script` (the spoken so-what — what a leader would actually SAY, one breath per sentence, no jargon), the supporting `impact_ids` (or exact `impact_titles`), and optional `asks`. Add `exec_summary` and any framing the user wants. **Every theme must trace to real impacts in the records; every claim in a script must be supportable by a record. A thin theme is correct; an invented one is a defect.**

5. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/readout_render.py --cia cia_records.json --readout readout.json --config project.json [--sha sha_records.json] --outdir OUT
   ```
   Output in `OUT/`: `<Project> Change Intensity Map.html`, `<Project> Executive Readout.html`, `<Project> Talking Points.md`. Re-runs refuse to clobber; pass `--force` to regenerate.

6. **QA.** Open (or headless-render) both HTML files: heat table sorts, matrix renders, area drill-downs open, every theme board shows WHO/WHAT/HOW and its script. Hand-check one area's intensity math (volume = its impact count; depth = mean of severity×complexity over its scored impacts). Confirm every theme's impact references resolved (the script warns on misses — fix them, don't ship warnings). Read the talking points aloud once: if a sentence can't be said in one breath, tighten it. Report where the files landed.

## Notes
- Requires `openpyxl` only if you extend to xlsx; the bundled renderer is pure stdlib. HTML outputs are single self-contained files with zero runtime dependencies.
- Intensity uses the CIA's ratified scores. Unscored impacts count toward **volume** but not **depth** — never invent scores to fill gaps; flag heavily-unscored areas to the user instead.
- Keep `roles_impacted` names aligned with SHA `stakeholder_group` names so the WHO panels reconcile (suite convention).
- Reuse for any project by swapping the records + `project.json`.
