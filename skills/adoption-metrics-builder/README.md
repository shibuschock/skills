# adoption-metrics-builder

Project-agnostic Claude skill (Capgemini OCM suite) that builds an **adoption & success measurement package** for any change program: an Excel metrics menu (metric register + measurement plan) and a self-contained interactive HTML adoption dashboard. Optionally ingests `cia_records.json` from `cia-builder` to map metrics to value levers and high-severity impacts, flagging coverage GAPs.

- `SKILL.md` — conversational workflow (Claude writes the JSON and runs the script).
- `references/METHODOLOGY.md` — metric ladder, leading/lagging, baseline/target discipline, RAG, anti-patterns.
- `references/SCHEMA.md` — `metrics_plan.json` fields.
- `scripts/metrics_render.py` — renderer (stdlib + openpyxl):
  ```
  python metrics_render.py --plan metrics_plan.json --config project.json [--cia cia_records.json] --outdir OUT [--force]
  ```
- `examples/` — "Acme ERP" sample config and plan.

Training-effectiveness (Kirkpatrick) evaluation lives in the training skills, not here.
