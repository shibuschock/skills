# change-network-builder

A project-agnostic Claude skill that builds a **Change Champion Network package**: network operating model (tiers, selection criteria, time commitment, cadence, recognition, nomination workflow), a champion roster with coverage-by-BU/location analysis, an Excel workbook, a self-contained interactive HTML dashboard, and ready-to-fill Markdown templates (nomination email, onboarding agenda, monthly touchpoint).

Part of the Capgemini OCM Skill Suite (see `../OCM-SUITE-README.md`).

## How it works

1. Claude gathers project basics conversationally and writes `project.json`.
2. Claude designs the network per `references/METHODOLOGY.md` (sizing ratios, influence-over-seniority selection, tiered model, operating rhythm) and writes `network_plan.json` per `references/SCHEMA.md`. Open seats stay open — nothing is invented.
3. Claude runs the renderer:
   ```
   python3 scripts/network_render.py --plan network_plan.json --config project.json --outdir OUT
   ```
   Output: `<Project> Change Network Roster.xlsx` + `<Project> Change Network Dashboard.html`.
4. Claude fills the templates in `assets/templates/` with real project content.

## Files

- `SKILL.md` — the conversational workflow Claude follows.
- `references/METHODOLOGY.md` — the champion-network method.
- `references/SCHEMA.md` — `network_plan.json` + `project.json` field definitions.
- `scripts/network_render.py` — renderer (stdlib + openpyxl; `--force` to overwrite).
- `assets/templates/` — nomination email, onboarding agenda, monthly touchpoint.
- `examples/` — "Acme ERP" sample config + plan.

## Requirements

`pip install openpyxl`. The dashboard is a single HTML file with zero runtime dependencies.
