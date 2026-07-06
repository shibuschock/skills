# training-strategy-builder

Project-agnostic Claude skill (Capgemini OCM suite) that builds a **Training Strategy** for any change program — the strategic layer upstream of the training needs analysis. Outputs an Excel strategy-on-a-page register and a self-contained interactive HTML strategy document.

- **Decides:** principles, modality strategy by workforce type, governance, resourcing, build-vs-buy, measurement approach (Kirkpatrick), phasing relative to go-live, risks/assumptions/open questions.
- **Does not decide:** module lists, hours, role-to-course mapping — those are TNA/curriculum-stage outputs (see `training-needs-builder`).
- **Contents:** `SKILL.md` (workflow) · `references/METHODOLOGY.md` + `references/SCHEMA.md` · `scripts/strategy_render.py` (stdlib + openpyxl, no-clobber, `--force`) · `examples/` (Acme ERP).

Try it: ask Claude to *"build a training strategy for my program"* — it gathers the basics conversationally, writes the JSON, and renders. See `OCM-SUITE-README.md` in the skills folder for suite conventions.
