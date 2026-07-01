# tom-vro-builder

A Claude skill — the **TOM Agent accelerator**. Turns a **Change Impact Assessment** into a **Target Operating Model + Value Realization** approach for **any project**, and generates four deliverables:

- **Accelerator slide** → `<Project> TOM Accelerator.pptx` (6 capability cards, gradient icons; builds on a blank branded deck — no client template needed)
- **TOM approach doc** → `<Project> TOM Approach.docx` (8 dimensions + prioritized functional groups + value streams + roles + value-at-risk)
- **VRO registers** → `<Project> VRO Registers.xlsx` (benefits register + value-at-risk + VRO tiers)
- **TOM dashboard** → `<Project> TOM Dashboard.html` (self-contained interactive overview)

## How it works
Claude reads the CIA + notes and fills a structured `tom_blueprint.json` (guided by the bundled methodology + schema); Python scripts render the four deliverables. Claude gathers inputs conversationally and runs the scripts. See `SKILL.md`.

## The 6-step method
**Ingest** (CIA → baseline) → **Map** (lifecycles + value streams) → **Reshape** (8 TOM dimensions) → **Prioritize** (by people-impact) → **Surface** (roles, value-at-risk, AI shifts) → **Generate** (the four deliverables).

## Methodology baked in
- **8 TOM dimensions** (incl. Guest/Service Outcomes and Locations & Sourcing) with a coherence check.
- **VRO 4-tier model** (Strategic / Operational / Adoption / Behavioral).
- Cross-functional **value streams**; prioritization by people-impact density.
- **Benefits register** rules — baseline source + owner per KPI; value-at-risk from open gaps.
- Standards-anchored (PMI/APMG benefits realization; Operating Model Canvas / POLISM).

## Layout
```
tom-vro-builder/
  SKILL.md
  README.md
  references/
    METHODOLOGY.md          # 6 steps, 8 dimensions, VRO tiers, value streams, prioritization
    TOM_SCHEMA.md           # project.json + tom_blueprint.json fields
    VRO_REGISTER.md         # benefits register + value-at-risk rules
  scripts/
    tom_slide.py            # accelerator PPTX (blank branded deck; python-pptx)
    tom_render.py           # Word + Excel + HTML (python-docx + openpyxl)
    gen_tom_icons.py        # OPTIONAL icon regenerator (probes for a headless browser)
  assets/icons/             # 6 bundled gradient PNG icons
  examples/
    project.example.json
    tom_blueprint.example.json
```

Requires `python-pptx`, `python-docx`, `openpyxl`. Python 3.9+, cross-platform.
Upstream: **`cia-builder`**. Companion: **`sha-builder`**.
