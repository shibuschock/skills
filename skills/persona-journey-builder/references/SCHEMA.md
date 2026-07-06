# personas.json schema

`personas.json` is a JSON array. One object per **change persona** (a rationalized archetype covering one or more roles — see METHODOLOGY.md).

Alternatively, wrap the array in an object to carry file-level options:

```json
{
  "role_aliases": { "Plant Manager": "Plant Managers", "DC Inventory Control": "Inventory Control Supervisors" },
  "personas": [ ... ]
}
```

`role_aliases` (optional) is a map of alias → canonical role name, used to absorb singular/plural/synonym drift between CIA `roles_impacted` and persona `roles_covered`. Aliases are applied when building the CIA cross-check, so aliased variants dedupe to the canonical name. Persona fields:

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Persona name. Functional segment labels work well ("Plan & Buy — Planners & Buyers"). |
| `tier` | yes | 1, 2, or 3. Tier 1 = deep persona + journey + day-in-the-life; Tier 2 = lightweight profile; Tier 3 = reference-only. |
| `archetype` | yes | 1–3 sentence description of the shared change experience that defines this persona (the core system/process shift). For Tier 3 a single line is enough. |
| `roles_covered` | yes | Array of role names folded into this persona. **Must align exactly to CIA `roles_impacted` / SHA `stakeholder_group` names** — this is the crosswalk. Each source role appears in exactly one persona. |
| `population_estimate` | rec. | Approximate headcount covered (number or string like "~450"). Blank if unknown — don't invent. |
| `change_intensity` | rec. | High / Medium / Low — judged from CIA severity×complexity of the impacts touching `roles_covered`. |
| `top_impacts` | rec. | Array of CIA impact **titles** (verbatim) that most shape this persona's journey. This is the traceability spine — every journey moment should connect to one of these or to cited source material. |
| `goals` | rec. | Array — what this persona is trying to accomplish in their work (job-relevant, not aspirational fluff). |
| `pain_points` | rec. | Array — current-state frictions. Trace to CIA `current_state` / SHA `key_pain_points` or sourced quotes. |
| `quote` | opt. | A sourced verbatim quote (with attribution context). Omit rather than invent. |
| `sentiment` | opt. | Positive / Mixed / Neutral / Negative / Cautious (from SHA `current_sentiment` where available). |
| `confidence` | opt. | High / Medium / Low — evidence depth behind this profile. |
| `journey` | Tier 1 (opt. Tier 2) | Array of stage objects — see below. |
| `day_in_life` | Tier 1 only | `{ "before": [...], "after": [...] }` — see below. |
| `day_in_life_status` | opt. | `"observed"` or `"reconstructed — pending validation"`. Rendered as a small tag on the day-in-the-life panel. Use "reconstructed — pending validation" when the timeline is a plausible reconstruction (no hour-anchored observation data), per METHODOLOGY.md. Omit and no tag renders. |

## `journey[]` stage object

| Field | Required | Notes |
|---|---|---|
| `stage` | yes | Short stage label (e.g., "Order", "Month-end close"). 4–7 stages per journey. |
| `current` | yes | Today's friction/pain at this stage — traced to a CIA impact or source. |
| `future` | yes | The future-state moment — traced to a CIA `future_state`. |
| `emotion_current` | rec. | One word (e.g., "Frustrated", "Resigned"). |
| `emotion_future` | rec. | One word (e.g., "Confident", "Anxious"). The curve should be honest — include the mid-journey dip. |
| `support` | rec. | The change-support cue: the specific training/job aid/comms/coaching that catches the persona at this moment. |

## `day_in_life` (Tier 1 only)

`before` and `after` are parallel arrays of time-anchored blocks describing the *same* workday today vs. future. Each block is either a string (`"06:30 — Walks the floor with the printed count sheet"`) or an object `{ "time": "06:30", "activity": "..." }`. Keep unchanged blocks in both columns — the contrast is the point.

**Derived automatically** (do NOT supply): `id`, tier labels, journey stage numbering, the CIA role cross-check (when `--cia` is passed).

# project.json (shared shape)

Same shape as the rest of the suite:

```json
{
  "project_name": "Acme ERP",
  "business_units": ["Retail", "Finance"],
  "brand": {
    "navy": "#162B75",
    "magenta": "#EE2C81",
    "font": "Calibri, system-ui, sans-serif",
    "footer": "Acme — Confidential"
  }
}
```

All `brand` keys are optional; defaults are the suite palette. See `examples/project.example.json` and `examples/personas.example.json`.
