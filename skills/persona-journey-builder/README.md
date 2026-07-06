# persona-journey-builder

Project-agnostic Claude skill (part of the Capgemini OCM skill suite) that builds a **tiered change-persona set** — personas, current→future user journeys, and day-in-the-life narratives — from CIA/SHA data or interview notes.

- **Input:** `cia_records.json` / `sha_records.json` (from cia-builder / sha-builder) or user-provided source material, plus a small `project.json`.
- **Output:** `<Project> Personas.xlsx` (Persona Register + Journey Moments) and `<Project> Personas & Journeys.html` (self-contained interactive explorer).
- **Method:** tiered model (Tier 1 deep persona + journey + DITL / Tier 2 lightweight profile / Tier 3 reference-only), rationalization by change experience — not one persona per role. No fabrication: journey moments trace to CIA impacts or sourced material.

Start with `SKILL.md` for the workflow; `references/METHODOLOGY.md` and `references/SCHEMA.md` define the rules and fields. Render with:

```
python scripts/persona_render.py --records personas.json --config project.json [--cia cia_records.json] --outdir OUT
```

Requires `openpyxl`. Re-runs refuse to overwrite outputs unless `--force`.
