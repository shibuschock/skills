---
name: ocm-playbook-builder
description: Build an OCM Playbook + 90-day tactical plan for ANY change program — an Excel activity register plus a self-contained interactive HTML playbook (summary tiles, 30/60/90 swimlane by workstream, filterable activity table, cadence/governance panel, handoff checklist). Bakes in a portable OCM method - workstreams (leadership & sponsorship, comms, change network, training, readiness & adoption measurement, sustainment), 30/60/90 phasing, activity design discipline (every activity has an owner, output, and done test), cadences, decision/escalation paths, and clean-handoff structure. Consumes cia_records.json / sha_records.json / comms_plan.json when available to seed activities and flag high-severity impacts with no mitigation activity as GAPs. Use when the user asks for an OCM playbook, change playbook, 90-day plan, tactical plan, change management plan, OCM workplan, or handoff plan.
---

# OCM Playbook Builder

Turn engagement context (program phase, timeline, team, upstream artifacts) into an **OCM Playbook + 90-day tactical plan** — an **Excel activity register + interactive HTML playbook** — for any project. Claude does the planning; a bundled Python script does the rendering. Nothing is hardcoded to a client; everything drives off a small `project.json` and a `playbook.json` that Claude fills in.

This skill is **conversational**: gather what you need in plain language, write the config and plan files yourself, and run the scripts yourself. The user should never have to hand-edit JSON or run a terminal.

## Workflow

1. **Gather the basics** (ask only for what's missing):
   - **Program phase** — where is the program (mobilization, design, build, test, deploy, hypercare)?
   - **Where "today" sits** — what week/month is the program in right now? The plan window can't be anchored without it; don't infer it from milestone lists.
   - **Go-live horizon** — when is go-live (or the next major milestone)? Real date or "roughly N months out"?
   - **OCM team** — who is on the change team (names/roles), and who will own this plan day-to-day? Is a **handoff** coming (consultant → client lead)?
   - **Upstream artifacts** — does a CIA (`cia_records.json`), SHA (`sha_records.json`), or comms plan (`comms_plan.json`) exist? Ask for their paths; they seed the plan.
   - Brand preferences (colors/font/footer) if the user has them.

   Then **write `project.json`** yourself (shape: `examples/project.example.json`).

2. **Read the references before planning** (they define every field and rule):
   - `references/METHODOLOGY.md` — workstream anatomy, 30/60/90 phasing logic, activity design rules, cadence & governance, handoff discipline, anti-patterns.
   - `references/SCHEMA.md` — `playbook.json` fields.

3. **Build the plan.** Write `playbook.json`: workstreams, phased activities (each with owner, output, done test, dependencies), cadences, escalation path, handoff structure.
   - **Phasing:** 30/60/90 is the default, but wave-aligned custom phase labels (e.g. "Mobilize", "Wave 1 Readiness") are equally valid — adapt to the program timeline rather than forcing 30/60/90 onto it. The swimlane and phase filter pick up whatever labels you use.
   - **Seed from upstream artifacts** where they exist: high-severity CIA impacts (severity ≥ 4) should each have at least one mitigation/readiness activity with the impact's exact `title` in `linked_impacts`; SHA resistant/high-influence stakeholders drive engagement activities; the comms plan's cadence rows become `cadences` entries rather than duplicated activities.
   - **No fabricated dates.** If real dates are known, anchor `meta.start_reference` to one and use week numbers relative to it. If not, use week numbers only ("Week 1" = plan start) — never invent calendar dates.
   - **Do not fabricate content** — an activity without a confirmed owner gets `"owner": "TBD"`, or, when the role is known but the person isn't, `"<Role> (name TBD)"` (e.g. `"Internal OCM Lead (name TBD)"`). Both are flagged by the renderer (any owner containing "TBD" counts); that is correct — an invented name is a defect, and the role-known form keeps the tile from overstating what's actually open.

4. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/playbook_render.py --plan playbook.json --config project.json --outdir OUT
   python3 scripts/playbook_render.py --plan playbook.json --config project.json --cia cia_records.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> OCM Tactical Plan.xlsx` (Activities register + By Workstream + Cadence sheets) and `<Project> OCM Playbook.html` (summary tiles, 30/60/90 swimlane, filterable activity table, cadence/governance panel, handoff checklist). With `--cia`, high-severity impacts with no linked activity are flagged as **GAP** in the dashboard — resolve them by adding activities, not by hiding the flag.

5. **QA.** Open the HTML (or headless-render it) and confirm: tiles are right, the swimlane shows every workstream×phase, filters work, GAPs (if any) are legitimate, cadences and handoff render. Spot-check activities against the sources. Report where the files were written and any remaining GAPs/TBD owners.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate.
- Requires `openpyxl` (`pip install openpyxl`). The HTML is a single self-contained file with zero runtime dependencies.
- Keep `playbook.json` as the canonical dataset between runs — update it and re-render (with `--force`) rather than editing outputs.
- Name alignment is the contract with the rest of the suite: `linked_impacts` entries must match CIA `title` values exactly.
- Reuse for any project by swapping `project.json` + `playbook.json`.
