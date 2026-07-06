---
name: change-network-builder
description: Build a change champion / change agent network package for ANY project — network operating model (tiers, selection criteria, time commitment, cadence, recognition), a champion roster with coverage-by-BU analysis, an Excel workbook plus a self-contained interactive HTML dashboard, and ready-to-fill Markdown templates (leadership nomination email, champion onboarding agenda, monthly touchpoint agenda). Bakes in a portable OCM method — sizing ratios, influence-over-seniority selection, tiered network model, operating rhythm, sustainment. Use when the user asks to build, design, set up, or refresh a change network, change champions, change agents, a champion nomination process, champion roster, or a network operating model — for any new or existing project.
---

# Change Network Builder

Turn engagement inputs (org structure, BU/location lists, stakeholder analysis, leadership conversations) into a **Change Champion Network package** — an **Excel roster workbook + interactive HTML dashboard + nomination/onboarding/touchpoint templates** — for any project. Claude does the network design and roster extraction; a bundled Python script does the rendering. Nothing is hardcoded to a client; everything drives off a small `project.json` that Claude fills in.

This skill is **conversational**: gather what you need in plain language, write the config and plan files yourself, and run the scripts yourself. The user should never have to hand-edit JSON or run a terminal.

## Workflow

1. **Gather the project basics** (ask only for what's missing): project name, business units, locations, roughly how many people are impacted per BU (drives network sizing), whether champions already exist or are being nominated fresh, and — if the user has brand preferences — colors/font/footer. Then **write `project.json`** yourself (use `examples/project.example.json` as the shape).

2. **Read the references before designing** (they define every field and rule):
   - `references/METHODOLOGY.md` — sizing ratios, selection criteria, tiered model, operating rhythm, recognition, failure modes.
   - `references/SCHEMA.md` — `network_plan.json` fields (network design + roster + cadence + nomination workflow).

3. **Design the network and write `network_plan.json`.** Define the tiers (sponsor, change lead, champions per BU/site — adapt names to the client's language), selection criteria, time commitment by phase, the meeting cadence, the recognition approach, and the nomination workflow. Size the champion count from impacted headcount using the ratios in METHODOLOGY.md. Populate the `roster` array from whatever the user has — named champions, or `status: "Open"` seats where nominations are still needed. **Do not fabricate — an Open seat is correct; an invented name, headcount, or email is a defect.** If someone has been identified but not formally nominated (volunteered, conditionally named), use `status: "Candidate"` — not Nominated. If the inputs contain no calendar anchor (no kickoff date, no milestone dates), the nomination deadline is a **proposed OCM design decision**, not a fact to find: propose a reasonable date, mark it as proposed in the plan and in your summary, and confirm it with the user — that is design, not fabrication. If per-group headcounts are unknown, leave `headcount_covered` blank — collecting them is exactly what the nomination workbook is for. If a SHA exists (`sha_records.json` from sha-builder), align roster `business_unit` / group names to the SHA stakeholder groups.

4. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/network_render.py --plan network_plan.json --config project.json --outdir OUT
   ```
   Output in `OUT/`: `<Project> Change Network Roster.xlsx` (Roster + Coverage sheets) and `<Project> Change Network Dashboard.html` (summary tiles, filterable roster, coverage-by-BU, cadence calendar, network design).

5. **Fill the templates.** Copy from `assets/templates/` and replace every `{{placeholder}}` with real project content — never leave a placeholder in a deliverable:
   - `nomination_email.md` — leadership ask for champion names + team sizes.
   - `champion_onboarding_agenda.md` — first-session agenda for new champions.
   - `champion_monthly_touchpoint.md` — recurring 30-minute briefing agenda (status → one clear ask → signals → cascade verbs → round robin).

6. **Update later (incremental).** The `network_plan.json` is the canonical dataset between runs. When nominations come back, edit the roster entries (Open → Candidate → Nominated → Confirmed → Onboarded), then re-render with `--force`. Don't rebuild the design from scratch.

7. **QA.** Open the HTML (or headless-render it) and confirm the tabs/filters work, the coverage view flags gaps, and the tiles match the roster. Check the xlsx opens with both sheets populated. Spot-check that no seat was invented. Report where the files were written.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate.
- Requires `openpyxl` (`pip install openpyxl`). The HTML output is a single self-contained file with zero runtime dependencies.
- Coverage %, open-seat counts, and champion-to-headcount ratios are computed by the renderer — don't hand-compute them.
- **A blank Champion Ratio column is by design, not a defect**, until per-group headcounts come back via the nomination workbook — the ratio only computes where `headcount_covered` is known. Expect it (and the "Headcount covered" tile) to be blank on a first render.
- Reuse for any project by swapping `project.json` + `network_plan.json`.
- **Stakeholder analysis is a separate skill** (`sha-builder`). Keep roster group names consistent with SHA stakeholder-group names so the two stay reconciled.
