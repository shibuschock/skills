# ocm-readout-builder

Project-agnostic Claude skill (Capgemini OCM suite) that turns a CIA — and optionally an SHA — into an executive readout package:

1. **Change Intensity Map** (HTML) — ranked heat table of which areas change most vs least, a Volume×Depth quadrant matrix, and drill-down to the impacts behind each area. Derived from the CIA's severity×complexity scores; never hand-scored.
2. **Executive Readout** (HTML) — exec summary, intensity snapshot, and one WHO/WHAT/HOW board per theme with a spoken talking-points panel.
3. **Talking Points** (Markdown) — the leader crib sheet, ready for docx conversion.

Inputs: `cia_records.json` (required, from cia-builder), `sha_records.json` (optional, from sha-builder), `project.json`, and a Claude-authored `readout.json` (4–7 executive themes, each traceable to impacts).

See `SKILL.md` for the workflow, `references/` for the methodology and schema, `examples/` for Acme ERP sample files. Renderer is pure Python stdlib.
