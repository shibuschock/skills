---
name: tom-vro-builder
description: Build a Target Operating Model (TOM) and Value Realization Office (VRO) approach for ANY transformation program from a Change Impact Assessment — producing an accelerator capability slide (PPTX), a TOM approach doc (Word), VRO registers (Excel: benefits register + value-at-risk), and a self-contained TOM dashboard (HTML). Applies a portable 6-step method (Ingest → Map → Reshape → Prioritize → Surface → Generate), the 8 TOM dimensions, the VRO 4-tier model, cross-functional value streams, and benefits-realization rules (baseline source + owner per KPI). Use when the user asks to build/design/model a target operating model, future ways of working, a value realization office or benefits register, or an operating-model accelerator — or to turn a CIA into a TOM/VRO scoping deliverable — for any project.
---

# TOM / VRO Builder

Turn a **Change Impact Assessment** (and current/future-state notes) into a **Target Operating Model + Value Realization** approach for any program, and generate four deliverables: an **accelerator slide (PPTX)**, a **TOM approach doc (Word)**, **VRO registers (Excel)**, and a **TOM dashboard (HTML)**.

Claude does the analysis and fills in a structured `tom_blueprint.json`; bundled scripts render the deliverables. This skill is **conversational**: gather inputs in plain language, write the config + blueprint yourself, and run the scripts yourself — the user never edits JSON or runs a terminal.

## Workflow — the 6-step method

Read `references/METHODOLOGY.md`, `references/TOM_SCHEMA.md`, and `references/VRO_REGISTER.md` first. Then work the six steps, populating `tom_blueprint.json` as you go (shape = `examples/tom_blueprint.example.json`). Write `project.json` from `examples/project.example.json` (brand, BUs, optional logo).

1. **Ingest** — read the CIA (the `cia-builder` output is ideal — its Excel/JSON, or a dashboard) plus any fit-gap / transcript inputs. Pull the functional areas with their **impact counts**, roles, and severity into the blueprint baseline.
2. **Map** — for each functional area, map the lifecycle and the cross-functional **value streams**; note where the new system changes inputs, outputs, roles, timing, and decisions.
3. **Reshape** — assess across the **8 TOM dimensions** (current state + future-state questions) and **test coherence** across them.
4. **Prioritize** — rank functional areas by **people-impact density & severity** (from the CIA counts); assign a priority; drop or fold low-people-impact areas (e.g. pure technical/migration work).
5. **Surface** — the new **roles & seats** the model implies, the **value-at-risk** from open/assumed gaps, and **AI role-shifts** (producing → approving). Draft the **benefits register** (each KPI names a baseline source + owner).
6. **Generate & QA** — run the scripts:
   ```
   python3 scripts/tom_slide.py  --config project.json --blueprint tom_blueprint.json --outdir OUT
   python3 scripts/tom_render.py --config project.json --blueprint tom_blueprint.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> TOM Accelerator.pptx`, `<Project> TOM Approach.docx`, `<Project> VRO Registers.xlsx`, `<Project> TOM Dashboard.html`. Open them (or headless-render the HTML) and confirm the counts trace back to the input CIA. Report where the files were written.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate (e.g. after an incremental update).
- Requires `python-pptx`, `python-docx`, `openpyxl`.
- The accelerator slide builds on a **blank branded deck** — no client template needed. Brand comes from `project.json`; an optional `brand.logo_path` places a logo top-right.
- The six capability icons are **bundled** in `assets/icons/` (transparent gradient PNGs). `scripts/gen_tom_icons.py` regenerates them only if you want a different style — it probes for a headless browser and, if none is found, keeps the bundled icons.
- **No fabricated counts or metrics.** Impact counts come from the CIA; benefit targets stay blank until baselined. American English.
- Upstream skill: `cia-builder` (produces the CIA this consumes). Companion: `sha-builder` (stakeholders).
