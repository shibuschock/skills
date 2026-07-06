# Capgemini OCM Skill Suite

A library of project-agnostic Claude skills for organizational change management (OCM) practitioners. Each skill turns raw engagement inputs (transcripts, workshop notes, interviews) into client-ready deliverables — Excel workbooks, self-contained interactive HTML dashboards, and PPTX/Word documents — through a conversational workflow: Claude gathers what it needs in plain language, writes the JSON data files itself, and runs the bundled Python renderers itself. The practitioner never hand-edits JSON or touches a terminal.

## The pipeline

```
transcripts/interviews
   │
   ├─► cia-builder ──► cia_records.json ──► CIA xlsx + dashboard
   │                        │
   ├─► sha-builder ──► sha_records.json ──► SHA xlsx + dashboard (Influence×Interest grid)
   │                        │
   │        ┌───────────────┴───────────────┐
   │        ▼                               ▼
   ├─► tom-vro-builder ──► TOM pptx/docx   comms-toolkit ──► comms grid + dashboard
   │       + VRO registers                     + coverage matrix (GAP flags)
   │
   ├─► downstream skills (consume cia/sha records where available):
   │   change-network-builder · adoption-metrics-builder ·
   │   readiness-pulse-builder · persona-journey-builder ·
   │   ocm-playbook-builder · ocm-readout-builder
   │
   └─► training chain: training-strategy-builder ──► training-needs-builder
       ──► curriculum-architect ──► training-content-builder +
       interactive-learning-builder ──► training-rollout-builder
       (shared methodology in _training-shared; chain contract in its ARTIFACTS.md)
```

Skills chain through shared JSON files. Name alignment is the contract:
- CIA `roles_impacted` ↔ SHA `stakeholder_group`
- comms `audiences[].name` ↔ SHA `stakeholder_group`
- comms `coverage[].impact` ↔ CIA `title`

Run `scripts/validate_chain.py` (bundled in cia-builder, sha-builder, and comms-toolkit) to machine-check schemas and this alignment before rendering.

## Core skills

| Skill | Input | Output |
|---|---|---|
| `cia-builder` | current/future-state transcripts | Change Impact Assessment: xlsx + HTML dashboard; 6 MECE Change Dimensions, severity×complexity, optional TOM/Value/Training/Workshop layers |
| `sha-builder` | interviews/stakeholder notes | Stakeholder Assessment: xlsx + HTML dashboard with Mendelow Influence×Interest grid |
| `tom-vro-builder` | the CIA | Target Operating Model pptx + approach docx + VRO registers xlsx + dashboard |
| `comms-toolkit` | the CIA/SHA | Comms master grid xlsx, 5-tab dashboard, coverage matrix with GAP escalation, Markdown vehicle templates, plain-language QA |
| `change-network-builder` | network design + roster | Champion roster xlsx + dashboard (coverage by BU/location, GAP flags), nomination/onboarding/touchpoint templates |
| `adoption-metrics-builder` | metrics plan (+ CIA) | Adoption metrics menu xlsx + dashboard (metric ladder, leading/lagging, RAG); flags uncovered value levers / high-severity impacts |
| `readiness-pulse-builder` | survey design or results | DESIGN: pulse survey guide xlsx (question bank); ANALYZE: readiness readout HTML (dimension×segment heat, wave deltas, anonymity suppression) |
| `persona-journey-builder` | personas (+ CIA/SHA) | Tiered persona register xlsx + interactive explorer (journeys, emotion curves, day-in-the-life) |
| `ocm-playbook-builder` | playbook plan (+ CIA) | 90-day tactical plan xlsx + playbook HTML (30/60/90 swimlanes, cadences, handoff checklist, GAP flags) |
| `ocm-readout-builder` | the CIA (+ SHA) | Change Intensity Map HTML (derived, never hand-scored), executive readout with who/what/how boards, leader talking points |
| `training-strategy-builder` | program shape (+ CIA/SHA) | Training strategy xlsx + HTML (principles, modality-by-workforce matrix, governance, phasing, risks) — upstream of the TNA |
| `training-needs-builder` | the CIA or raw notes | TNA matrix (`training_needs.json`) + TNA xlsx/dashboard; no hours (curriculum-stage) |
| `curriculum-architect` | `training_needs.json` | Curriculum blueprint (`curriculum.json`) + curriculum xlsx/blueprint HTML (paths, modules, Bloom objectives, 70-20-10) |
| `training-content-builder` | one module from `curriculum.json` | Facilitator/participant guides, job aid, slide outline, in-app script, assessment items (markdown) |
| `interactive-learning-builder` | module objectives from `curriculum.json` | Interactive HTML quizzes/flashcards, optional SCORM 1.2 zip |
| `training-rollout-builder` | `curriculum.json` + needs | Rollout plan xlsx/dashboard (waves from go-live, readiness gates, Kirkpatrick L1–L4, reinforcement) |

## Design conventions (apply to every skill in the suite)

- **Self-contained folders.** Each skill ships everything it needs (`SKILL.md` + `references/` + `scripts/` + `examples/`). Shared code (`validate_chain.py`, merge scripts, render scaffolding) is deliberately *copied*, not imported across skills — so a skill can be zipped and handed to any practitioner. When fixing shared code, sync the copies; the canonical source is noted in each file's docstring (default: cia-builder).
- **Nothing client-specific.** Examples use "Acme ERP". Branding (colors/font/footer) comes from `project.json` `brand` and defaults to a Capgemini-adjacent palette.
- **JSON is the canonical dataset.** `*_records.json` persists between runs; incremental updates merge via `*_merge.py` (see each skill's `UPDATE_LOOP.md`), never rebuild from scratch.
- **No fabrication.** A blank field is correct; an invented score, metric, or coverage row is a defect. Unscored sessions stay unscored; unmapped impacts are GAPs.
- **Reconcile from canonical sources before generating.** Renderers and any derived artifact read the canonical `*_records.json` — never a previously derived artifact (a rollup built off a retired field produces wrong numbers). When sources conflict, confirm which is authoritative and reconcile before generating downstream outputs.
- **Human decisions are read-only to automation.** Persisted human reconciliation/mapping decisions (role↔persona crosswalks, merge/dedup rulings, scope calls) live in their own file that scripts and re-extraction read but never overwrite. Automated rollups drift without this.
- **Renderers never clobber.** Re-runs refuse to overwrite outputs unless `--force`.
- **QA before done.** Validate (`validate_chain.py`), render, then open/headless-screenshot the HTML and spot-check against source.
- **Dependencies:** `openpyxl` everywhere; `python-pptx` + `python-docx` for tom-vro-builder. Dashboards are single-file HTML with zero runtime dependencies.

## Getting started (practitioner)

1. Copy the skill folder(s) into `~/.claude/skills/`.
2. In Claude Code, ask in plain language, e.g. *"Build a CIA for my project from these workshop transcripts."*
3. Claude will ask for project basics, extract records, validate, render, and QA — and tell you where the files landed.
