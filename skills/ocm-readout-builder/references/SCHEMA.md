# readout.json Schema

A single JSON object authored by Claude from `cia_records.json` (+ optional `sha_records.json`). See `examples/readout.example.json`.

```json
{
  "meta": {
    "audience": "Executive Steering Committee",
    "occasion": "Design readout",
    "date": "2026-07-06",
    "presenter": ""
  },
  "exec_summary": "One short paragraph: the headline the audience should leave with.",
  "themes": [
    {
      "title": "Planning becomes a formal discipline",
      "whats_changing": "Theme-level current→future summary — what leaders need to know, 2-4 sentences.",
      "so_what_script": "The spoken so-what. Conversational, one breath per sentence. What a leader would actually SAY.",
      "impact_ids": [1, 2],
      "impact_titles": ["Optional alternative: exact CIA titles instead of ids"],
      "asks": ["Optional: the decision/sponsorship/resource ask tied to this theme"]
    }
  ],
  "asks": ["Optional program-level closing asks (decisions, sponsorship moves)"]
}
```

## Rules

- `meta.audience` and `meta.occasion` required; `date`/`presenter` optional.
- `exec_summary` optional but recommended.
- `themes`: 4–7 objects. Required per theme: `title`, `whats_changing`, `so_what_script`, and at least one of `impact_ids` / `impact_titles`.
- `impact_ids` reference the CIA record `id` field (or the 1-based record index when records carry no explicit `id` — the same numbering cia-builder's renderer assigns).
- `impact_titles` must match CIA `title` values exactly (case-insensitive match is applied).
- The renderer warns on any reference that doesn't resolve — fix before shipping.
- WHO / HOW panels are **derived** by the renderer from the referenced records (`roles_impacted`, `mitigation`) — don't restate them in the JSON.

## project.json (shared shape)

Same file cia-builder uses — reuse the project's existing one:

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

Only `project_name` is required; brand keys default to the suite palette (navy `#162B75`, magenta `#EE2C81`).

## Inputs

- `cia_records.json` (required) — array of CIA records; see cia-builder `references/CIA_SCHEMA.md`. Fields used here: `title`, `functional_area`/`l1_process`, `business_unit`, `severity`, `complexity`, `roles_impacted`, `current_state`, `future_state`, `process_change`, `mitigation`, `sentiment`, `scope`, `priority`.
- `sha_records.json` (optional) — SHA records; the renderer joins `stakeholder_group` to CIA `roles_impacted` to annotate WHO panels with influence/interest/disposition.
