---
name: readiness-pulse-builder
description: Design change-readiness pulse surveys and analyze their results for ANY project. Two modes — DESIGN builds the instrument (readiness dimensions, anchor + rotating questions from a curated bank, Likert scale, audience segments, cadence, anonymity/comms plan) and renders a Pulse Survey Guide xlsx; ANALYZE takes fielded results (csv or aggregated numbers) and renders a self-contained Readiness Readout HTML dashboard with dimension tiles, a dimension-by-segment RAG heat table, and wave-over-wave deltas. Use when the user asks to create, design, build, or analyze a pulse survey, readiness survey, change readiness assessment, culture pulse, survey questions, or a readiness readout for any project.
---

# Readiness Pulse Builder

Design a **change-readiness pulse survey** and, once it has been fielded, render a **readiness readout dashboard** — for any project. Claude does the design and data-shaping; a bundled Python script does the rendering. Nothing is hardcoded to a client; everything drives off a small `project.json` that Claude fills in.

This skill is **conversational**: gather what you need in plain language, write the config and data files yourself, and run the script yourself. The user should never have to hand-edit JSON or run a terminal.

Two modes. Ask which one the user needs (or infer: "build a survey" → DESIGN; "here are the results" → ANALYZE).

## Mode A — DESIGN (build the instrument)

1. **Gather the project basics** (ask only for what's missing): project name, where the program is in its lifecycle (foundation / design / build / pre-go-live / hypercare), audience segments to report by (business unit, location, role type, wave), fielding cadence, and any brand preferences. Write `project.json` (shape: `examples/project.example.json`).

2. **Read the references before designing**:
   - `references/METHODOLOGY.md` — readiness dimensions, question-design rules, cadence, anonymity threshold, closing the loop.
   - `assets/QUESTION_BANK.md` — ~30 ready-to-use questions by dimension + open-text prompts.

3. **Select and tailor the questions.** Keep the survey to **8–12 items (3–5 minutes)**: ~5 anchor items (one per core dimension, never reworded between waves) + 3–5 rotating items matched to the current phase + 1–2 open-text prompts. Tailor wording to the project (program name, "the new system") but keep one concept per item. Confirm the selection with the user.

4. **Write `pulse_design.json`** (shape: `examples/pulse_design.example.json`; fields: `references/SCHEMA.md`) — dimensions, questions, scale, segments, cadence, `anonymity_threshold` (default 5), and the comms/anonymity plan.

5. **Render** (run it yourself; `python` on Windows, `python3` elsewhere):
   ```
   python scripts/pulse_render.py design --design pulse_design.json --config project.json --outdir OUT
   ```
   Output: `<Project> Pulse Survey Guide.xlsx` — Questions tab + Admin Plan tab (cadence, segments, thresholds, comms plan).

6. **QA.** Open the xlsx (or list its sheets programmatically), confirm every selected question appears with the right dimension/scale/anchor flag, and report where the file landed.

## Mode B — ANALYZE (render the readout)

1. **Get the results.** The user pastes numbers, points to a csv/xlsx export, or gives aggregated means. Establish: wave label + date, invited count, and per-segment `n` and per-question mean (or a 1–5 response distribution). If raw row-level data is provided, aggregate it yourself by segment.

2. **Write `pulse_results.json`** (shape: `examples/pulse_results.example.json`). Include every prior wave already captured so deltas render — keep this file as the canonical dataset between waves and append new waves to it.

3. **No fabrication.** Never invent scores, response counts, benchmark values, or open-text themes. A missing question or segment stays missing; the renderer handles blanks. If the user asks "how does this compare to benchmark?", say there is no benchmark data unless they supply one.

4. **Render:**
   ```
   python scripts/pulse_render.py results --results pulse_results.json --design pulse_design.json --config project.json --outdir OUT
   ```
   Output: `<Project> Readiness Readout.html` — self-contained, no external dependencies: response-rate strip, readiness tiles by dimension, dimension × segment heat table with RAG coloring, wave-over-wave deltas (when ≥2 waves), open-text themes. **Segments with `n` below `anonymity_threshold` are suppressed and flagged, never scored** — do not work around this by quoting their numbers in chat either.

5. **QA.** Open or headless-render the HTML; confirm tiles, heat table RAG colors, deltas, and that any below-threshold segment shows as suppressed. Spot-check two or three cells against the source numbers. Report where the file landed and the two or three most decision-relevant findings (lowest dimension, biggest drop, any suppressions).

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate.
- Requires `openpyxl` (`pip install openpyxl`) for DESIGN mode; RESULTS mode is pure stdlib.
- Reverse-scored items (`"reverse": true`) are flipped by the renderer before averaging — never pre-flip them in the data.
- Interpretation guidance (gaps vs averages, movement vs point-in-time, escalation thresholds) lives in `references/METHODOLOGY.md` — read it before writing the readout narrative.
- If an SHA exists, build segments as rollups of SHA `stakeholder_group` names sized to clear the anonymity threshold (see `references/METHODOLOGY.md` §4) — don't field tiny SHA groups as segments; document the segment → SHA-group mapping so results reconcile with the stakeholder analysis.
