# Schema — project.json + tom_blueprint.json

## project.json (config)
| Key | Notes |
|---|---|
| `project_name` | Used in output filenames + titles. |
| `business_units` / `locations` | Arrays; context for the analysis. |
| `brand` | Optional. `navy`, `cyan`, `accent`, `card_bg`, `card_br`, `text_dk`, `text_md`, `font`, `footer`. Any omitted key falls back to a default. `logo_path` (absolute path to a PNG) places a logo top-right on the slide. |

## tom_blueprint.json
The structured model the 6 steps populate; the scripts render it. All top-level keys are arrays/objects; any omitted section is simply skipped in the outputs. See `examples/tom_blueprint.example.json`.

### `accelerator` (drives the PPTX slide)
| Field | Notes |
|---|---|
| `title` / `subtitle` | Left-panel title + italic subtitle. |
| `value_statement` | Paragraph at top-right of the slide (also opens the Word doc). |
| `capabilities_header` | The line above the cards (e.g. "Our TOM Agent's capabilities:"). |
| `capabilities` | Exactly 6 objects: `{icon, lead, rest}`. `icon` ∈ `funnel, map, shapes, ranking, discover, output` (bundled). `lead` is the bold verb; `rest` continues the sentence. |

### `functional_groups` (Word table + HTML tiles; ranked by priority then impact_count)
`{area, rolls_up[], impact_count, priority, lifecycle, value_streams[]}` — `priority` ∈ Critical/High/Medium/Low. `impact_count` comes from the CIA.

### `value_streams`
`{name, stages[]}` — cross-functional streams rendered as `stage → stage → …`.

### `tom_dimensions` (Word + HTML table)
`{dimension, current_state, future_state_questions}` — one per TOM dimension (up to 8).

### `roles_and_seats`
`{name, why, owner}` — new roles/seats the model implies (owner may be blank until named).

### `value_at_risk`
`{cluster, benefit_at_risk, why, source_gap}` — leading risk indicators from open/assumed gaps.

### `vro_tiers` (Excel "VRO Tiers" sheet)
`{tier, focus, owner, cadence}` — the 4 VRO tiers.

### `benefits_register` (Excel "Benefits Register" sheet)
`{benefit, kpi, baseline_source, owner, target, timeline}` — **each KPI must name a `baseline_source` and an `owner`**; `target` stays blank until baselined. See `references/VRO_REGISTER.md`.
