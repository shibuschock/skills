# readiness-pulse-builder

Project-agnostic Claude skill for OCM practitioners: design a change-readiness pulse survey and render analysis readouts of results. Part of the Capgemini OCM skill suite (see `../OCM-SUITE-README.md`).

- **DESIGN mode** → `<Project> Pulse Survey Guide.xlsx` (question set + admin/comms plan) from `pulse_design.json`
- **ANALYZE mode** → `<Project> Readiness Readout.html` (self-contained dashboard: dimension tiles, dimension × segment RAG heat table, wave-over-wave deltas, open-text themes, minimum-n suppression) from `pulse_results.json`

Contents: `SKILL.md` (workflow) · `references/METHODOLOGY.md` (dimensions, question rules, cadence, anonymity, interpretation) · `references/SCHEMA.md` (JSON shapes) · `assets/QUESTION_BANK.md` (~30 items) · `scripts/pulse_render.py` (renderer; stdlib + openpyxl) · `examples/` ("Acme ERP", 2 waves).

Use conversationally in Claude Code: *"Design a readiness pulse for my project"* or *"Here are the pulse results — build the readout."* No fabrication: the renderer and workflow never invent scores or benchmarks, and segments below the anonymity threshold are suppressed.
