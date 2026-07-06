---
name: comms-toolkit
description: Turn a change program (ideally its CIA) into a running change-communications operation for ANY project — producing a comms master grid (Excel), a self-contained interactive comms dashboard (HTML), and a comms-by-impact coverage matrix that flags uncovered impacts as GAPs. Bakes in a portable method: audience segmentation (Champions/Managers/Org-wide/BU-specific/SteerCo), a channel mix + cadence (the "What's Changing" email arc, newsletter, town halls, champion touchpoints, the manager cascade 24h/48h pattern, SteerCo updates, sponsor videos, pulse surveys), an approval/QA gate with reviewer SLA and plain-language standard, crisis comms (T+24h/T+72h/T+14d), and ADKAR alignment. Bundles portable Markdown templates and a plain-language QA checker. Use when the user asks to build/create a comms plan, communications toolkit, change comms, stakeholder comms, comms calendar/matrix, manager cascade, town hall pack, crisis comms, or coverage matrix.
---

# Comms Toolkit

Turn a change program — ideally its **CIA** (change impact assessment) — into a running
**communications operation**: a **comms master grid (Excel)**, a **self-contained interactive
dashboard (HTML)**, and a **coverage matrix** that guarantees every impact maps to a comm
vehicle and flags the ones that don't as **GAPs**. Claude gathers inputs in plain language,
writes the config itself, and runs the scripts itself — the user never hand-edits JSON or
touches a terminal. Nothing is hardcoded to a client; everything drives off a small
`project.json` + `comms_plan.json`.

## Workflow

1. **Gather the basics** (ask only for what's missing): project name, business units,
   locations, and — if the user has brand preferences — colors/font/footer. Ask where they want
   the outputs. Then **write `project.json`** yourself (shape: `examples/project.example.json`).

2. **Read the references before building** (they define every field and rule):
   - `references/METHODOLOGY.md` — audiences, channel/cadence, the coverage+GAP rule, the
     approval gate, crisis framework, ADKAR, plain-language standard.
   - `references/SCHEMA.md` — the exact `project.json` + `comms_plan.json` fields.

3. **Build the comms plan.** With the user, define **audiences** (Champions / Managers /
   Org-wide / BU-specific / SteerCo — or their own), a **channel mix + cadence**, and a few
   weeks of **activities** (default to the "What's Changing" Ep.1→3 arc + a town hall + a
   manager cascade). Add the **approval_gate** (reviewer SLA, named reviewers) and **crisis**
   scenarios. Then write `comms_plan.json` yourself (shape: `examples/comms_plan.example.json`).
   Populate `coverage[]` only where you can map an impact to a vehicle — an unmapped impact is a
   **GAP**, not something to invent coverage for.

4. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/comms_render.py --config project.json --plan comms_plan.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> Comms Master Grid.xlsx` and `<Project> Comms Dashboard.html`
   (tabs: Comms Calendar, Coverage, Audience × Channel, Approval Gate, Crisis Comms).

5. **Check coverage against the CIA** (if a CIA exists — from the `cia-builder` skill):
   ```
   python3 scripts/coverage_matrix.py --cia cia_records.json --plan comms_plan.json \
                                      --config project.json --outdir OUT
   ```
   Emits `<Project> Coverage Matrix.xlsx` with every uncovered impact flagged **GAP** and prints
   the gap count. **Any gap is an escalation trigger** — surface it, don't paper over it.

6. **Draft from templates + QA.** For each vehicle, start from `assets/templates/` (see
   `references/TEMPLATES.md`), fill the `{{placeholders}}`, then QA the plain-language standard:
   ```
   python3 scripts/comms_qa.py --file your_draft.md
   ```
   Aim for reading grade **5–7**, sentences under ~25 words, no jargon/slop. Then route the
   draft through the `approval_gate` before it sends.

7. **Validate the chain.** Machine-check audience/channel references and CIA/SHA alignment:
   ```
   python3 scripts/validate_chain.py --comms comms_plan.json [--cia cia_records.json] [--sha sha_records.json]
   ```
   Fix every ERROR (unknown audience/channel references, coverage rows matching no CIA impact). Review WARNs.

8. **QA the dashboard.** Open the HTML (or headless-render it) and confirm the tabs render, the
   calendar filters, the coverage tab highlights gaps in red, and the audience × channel matrix
   populates. Report where the files were written and the gap count.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate (e.g. after an incremental update).
- Requires `openpyxl` (`pip install openpyxl`) for the xlsx outputs; `comms_qa.py` is stdlib-only.
  The HTML dashboard is a single self-contained file with zero runtime dependencies.
- Every script has a `--config`/`--plan`/`--outdir` CLI and prints where it wrote its outputs.
- Reuse for any project by swapping `project.json` + `comms_plan.json`.
- **Impacts come from the CIA** (`cia-builder`) and **audiences from the SHA** (`sha-builder`) —
  keep `coverage[].impact` titles aligned with CIA `title`s and `audiences[].name` aligned with
  SHA stakeholder-group names so the datasets don't drift.
- Don't invent coverage, metrics, or dates. A tracked GAP is correct; fabricated coverage is a defect.
- **Dates convention:** when the program has no calendar anchor (milestones are only relative, e.g. "Wave 1 — Month 6"), agree an anchor date for week 1 with the user, or schedule by week numbers in titles and put a placeholder ISO date with a note that it's a placeholder. Never silently invent real dates.
