---
name: persona-journey-builder
description: Build change personas, current-to-future user journeys, and day-in-the-life narratives for ANY project — producing an Excel persona register plus a self-contained interactive HTML explorer (persona cards by tier, journey maps with emotion curves, before/after day-in-the-life panels). Bakes in a portable OCM method - a tiered persona model (Tier 1 deep persona + journey + day-in-the-life, Tier 2 lightweight profile, Tier 3 reference-only role list) with rationalization criteria so you get a small operable persona set instead of one persona per role. Ingests cia_records.json and sha_records.json when available so personas trace to evidenced change impacts. Use when the user asks for personas, user journeys, a journey map, day in the life, day-in-the-life narratives, persona rationalization, or change archetypes for a program.
---

# Persona & Journey Builder

Turn a CIA/SHA (or raw interview notes) into a **tiered change-persona set with user journeys and day-in-the-life narratives** — an **Excel register + interactive HTML explorer** — for any project. Claude does the clustering and writing; a bundled Python script does the rendering. Nothing is hardcoded to a client; everything drives off a small `project.json`.

This skill is **conversational**: gather what you need in plain language, write the config and records files yourself, and run the scripts yourself. The user should never have to hand-edit JSON or run a terminal.

## Workflow

1. **Gather the project basics** (ask only for what's missing): project name, business units, and — if the user has brand preferences — colors/font/footer. Ask whether a CIA (`cia_records.json`) and SHA (`sha_records.json`) exist and where; ask where outputs should go. Then **write `project.json`** yourself (use `examples/project.example.json` as the shape).

2. **Read the references before building** (they define every field and rule):
   - `references/METHODOLOGY.md` — the tiered persona model, rationalization criteria, journey-map anatomy, day-in-the-life rules, and the traps to avoid.
   - `references/SCHEMA.md` — every field of `personas.json`.

3. **Ingest the upstream data when available.**
   - From `cia_records.json`: `roles_impacted` + `role_changes` seed the candidate role list and per-role change descriptions; impacts (current_state → future_state, severity, complexity, sentiment) seed journey moments and change intensity.
   - From `sha_records.json`: `stakeholder_group`, `group_description`, `key_pain_points`, `current_sentiment` enrich the profiles.
   - Without CIA/SHA, work from user-provided interviews/notes — but every journey pain point and future-state moment must still trace to a source.

4. **Rationalize to a small tiered persona set.** Do NOT create one persona per role. Cluster roles that live the same change experience into ~4–8 personas, then tier them (see METHODOLOGY.md): **Tier 1** (deep persona + journey + day-in-the-life) for the most-impacted archetypes; **Tier 2** (lightweight profile); **Tier 3** (reference-only role list). Every CIA role must land in exactly one persona's `roles_covered` — nothing dropped, nothing double-counted. Present the proposed cut to the user for confirmation before writing the full detail.

5. **Write `personas.json`.** One object per persona, per `references/SCHEMA.md`. **No fabrication:** journey pain points and future-state moments must trace to CIA impacts or user-provided source material — an invented moment is a defect. Cite CIA titles in `top_impacts`. Where evidence is thin, leave the field blank or mark the persona lower-confidence rather than inventing backstory.

6. **Render** (run it yourself; `python3`, or `python` on Windows):
   ```
   python3 scripts/persona_render.py --records personas.json --config project.json [--cia cia_records.json] --outdir OUT
   ```
   Output in `OUT/`: `<Project> Personas.xlsx` (Persona Register + Journey Moments sheets) and `<Project> Personas & Journeys.html`. When `--cia` is given, the renderer cross-checks that every persona's `roles_covered` maps to CIA roles and flags unmapped high-severity roles (console + a banner in the HTML). Fix flags before delivering.

7. **QA.** Open the HTML (or headless-render it) and confirm: cards group by tier, clicking a card opens the full detail, each Tier-1 persona shows its journey (current→future rows with emotion indicators) and the before/after day-in-the-life panel. Spot-check journey moments against the CIA. Report where the files were written.

## Notes
- **Won't overwrite:** re-running refuses to clobber existing outputs in `--outdir`; pass `--force` to regenerate.
- Requires `openpyxl` (`pip install openpyxl`). The HTML output is a single self-contained file with zero runtime dependencies.
- `roles_covered` names must match CIA `roles_impacted` / SHA `stakeholder_group` names exactly — name alignment is the contract that keeps the suite reconciled.
- Personas are archetypes representing many people, not literal individuals — say so in the deliverable. Named characters (if used) belong at the profile level with sourced quotes only.
- Reuse for any project by swapping the upstream data + `project.json`.
