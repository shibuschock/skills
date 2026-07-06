---
name: adoption-metrics-builder
description: Build an adoption & success measurement package for ANY change program — a metrics menu (Excel register + measurement plan) plus a self-contained interactive HTML adoption dashboard. Bakes in a portable OCM measurement method - the metric ladder (system usage → behavior/proficiency → process outcomes → business value), leading vs lagging indicators, baseline/target/threshold discipline (no invented targets), RAG thresholds, and cadence/ownership. Optionally ingests cia_records.json to map metrics to CIA value levers and high-severity impacts, flagging coverage GAPs. Use when the user asks for adoption metrics, success metrics, adoption measurement, a measurement framework or measurement plan, usage metrics, KPIs for change adoption, or an adoption dashboard.
---

# Adoption Metrics Builder

Turn a change program's context (and optionally its CIA) into an **adoption & success measurement package**: an **Excel metrics menu + measurement plan** and a **self-contained interactive HTML dashboard** with coverage/GAP analysis. Claude does the metric design; a bundled Python script does the rendering. Nothing is hardcoded to a client; everything drives off a small `project.json`.

This skill is **conversational**: gather what you need in plain language, write the config and plan files yourself, and run the script yourself. The user should never have to hand-edit JSON or run a terminal.

**Scope note:** training-effectiveness measurement (Kirkpatrick L1–L4) lives in a separate training skill. This skill covers the broader adoption/behavior/outcome ladder — a single training-completion or training-effectiveness metric may appear here as a readiness input, but curriculum-level evaluation design does not.

## Workflow

1. **Gather the project basics** (ask only for what's missing): project name, business units, go-live timing/phases, what systems/processes are changing, who owns measurement (change team, PMO, process owners), and brand preferences if any. Then **write `project.json`** yourself (shape: `examples/project.example.json`).

2. **Read the references before designing metrics** (they define every field and rule):
   - `references/METHODOLOGY.md` — the metric ladder, leading/lagging, baseline/target/threshold discipline, cadence, instrumentation, RAG, anti-patterns.
   - `references/SCHEMA.md` — `metrics_plan.json` fields.

3. **Optionally ingest the CIA.** If the engagement has a `cia_records.json` (from `cia-builder`), read it and use it to ground the metric set: propose at least one metric per **value lever** (`value_levers` / `benefits`) and per **high-severity impact** (severity ≥ 4), populating each metric's `value_levers` and `linked_impacts` fields with the exact CIA names/titles. Unmapped levers/impacts are GAPs — the dashboard will flag them; leave real gaps visible rather than inventing metrics to paper over them.

4. **Design the metric set and write `metrics_plan.json`.** One object per metric, spanning the ladder (don't stop at usage metrics). Apply the rules: classify each as Leading or Lagging; name the concrete data source/instrument and an owner; set cadence. **Do not fabricate baselines or targets — a blank is correct, an invented number is a defect.** Targets only where the client or a standard threshold genuinely supports them. Include the `measurement_plan` block (reporting cadence, review forum, escalation path).

5. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/metrics_render.py --plan metrics_plan.json --config project.json [--cia cia_records.json] --outdir OUT
   ```
   Output in `OUT/`: `<Project> Adoption Metrics Menu.xlsx` (Metric Register + Measurement Plan sheets) and `<Project> Adoption Dashboard.html` (summary tiles by ladder level, filterable register, leading/lagging split, and — when `--cia` is given — a coverage view flagging value levers and high-severity impacts with no metric as GAP).

6. **QA.** Open the HTML (or headless-render it) and confirm tiles, filters, and the coverage view work; open the xlsx and spot-check a few rows. Confirm no invented baselines/targets slipped in. Report where the files were written.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate.
- Requires `openpyxl` (`pip install openpyxl`). The HTML is a single self-contained file with zero runtime dependencies.
- Keep `metrics_plan.json` as the canonical dataset between runs — when the client activates metrics or sets baselines, update the JSON and re-render with `--force`.
- Name alignment is the contract with the rest of the suite: metric `value_levers` must match CIA `benefits[].benefit` / record `value_levers` exactly; `linked_impacts` must match CIA record `title` exactly.
