# ocm-playbook-builder

Project-agnostic Claude skill: builds an **OCM Playbook + 90-day tactical plan** for any change program — an Excel activity register plus a self-contained interactive HTML playbook (summary tiles, 30/60/90 swimlane by workstream, filterable activity table, cadence/governance panel, handoff checklist).

Part of the Capgemini OCM skill suite (see `../OCM-SUITE-README.md`). Chains with `cia-builder` / `sha-builder` / `comms-toolkit`: pass `--cia cia_records.json` and high-severity impacts with no mitigation activity are flagged as GAPs.

**Use it:** ask Claude, e.g. *"Build an OCM playbook and 90-day plan for my program."* Claude gathers the basics, writes `project.json` + `playbook.json`, and runs:

```
python scripts/playbook_render.py --plan playbook.json --config project.json [--cia cia_records.json] --outdir OUT
```

Requires `openpyxl`. Outputs never overwrite without `--force`. See `SKILL.md` for the workflow, `references/METHODOLOGY.md` for the method, `references/SCHEMA.md` for the data shapes, `examples/` for a full sample.
