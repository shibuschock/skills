# Data file schemas

Three JSON files. Claude writes all of them; the user never edits JSON.

## project.json (shared shape across the OCM suite)

```json
{
  "project_name": "Acme ERP",
  "client": "Acme Corp",
  "program_description": "ERP transformation across retail and finance",
  "business_units": ["Retail Ops", "Finance", "Supply Chain"],
  "locations": ["East Campus", "West Campus"],
  "brand": {
    "navy": "#162B75",
    "magenta": "#EE2C81",
    "font": "Calibri, system-ui, sans-serif",
    "footer": "Confidential"
  }
}
```

`brand` is optional; omitted keys fall back to `DEFAULT_BRAND` in the renderer.

## pulse_design.json (DESIGN mode)

```json
{
  "instrument_name": "Acme ERP Readiness Pulse",
  "scale": {
    "points": 5,
    "labels": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
  },
  "dimensions": ["Awareness", "Understanding", "Leadership Confidence",
                 "Capability", "Workload & Capacity", "Sentiment & Trust"],
  "questions": [
    {
      "id": "Q1",
      "dimension": "Awareness",
      "text": "I understand the objectives and purpose of the program.",
      "scale": "likert5",
      "reverse": false,
      "anchor": true,
      "use_when": "Every wave"
    }
  ],
  "segments": ["Retail Ops", "Finance", "Supply Chain", "Store Leadership"],
  "cadence": [
    {"phase": "Foundation / Design", "frequency": "Baseline, then quarterly", "focus": "Awareness, sentiment baseline"}
  ],
  "anonymity_threshold": 5,
  "comms_plan": {
    "announced_by": "Program sponsor",
    "distribution": "Email link via managers; QR poster for frontline",
    "reminders": "Day 3 and day 6; survey open 8 business days",
    "anonymity_statement": "Responses are anonymous; results reported at group level only; groups under 5 responses are never reported.",
    "results_feedback": "You-said/we-heard summary to all respondents within 1 week; actions named with owners; next invite opens with what changed."
  }
}
```

Field rules:
- `id` unique; keep anchor IDs stable across waves.
- `dimension` must be one of `dimensions`.
- `scale`: `"likert5"` | `"yesno"` | `"open"`. Only `likert5` items are scored in the readout.
- `reverse`: `true` means high raw score = bad signal; renderer flips it (6 − score on a 5-point scale) before averaging.
- `anchor`: `true` = appears every wave, wording frozen.
- `anonymity_threshold`: integer; segments with `n` below this are suppressed in the readout. Default 5.

## pulse_results.json (ANALYZE mode)

Canonical dataset — append new waves, never rebuild.

```json
{
  "anonymity_threshold": 5,
  "waves": [
    {
      "label": "Wave 1 — Baseline",
      "date": "2026-04-15",
      "invited": 420,
      "segments": [
        {
          "name": "Retail Ops",
          "n": 96,
          "scores": {
            "Q1": 3.6,
            "Q2": [4, 12, 30, 38, 12]
          }
        }
      ],
      "open_text_themes": [
        {"theme": "Not enough time to train during shifts", "mentions": 14,
         "sample_quote": "There's no way I can learn this during peak season."}
      ]
    }
  ]
}
```

Field rules:
- `scores` keys must match question `id`s in `pulse_design.json`; only `likert5` questions are scored. A score value is **either** a mean (number, 1–5) **or** a distribution (array of counts, index 0 = scale point 1); the renderer computes the mean from a distribution.
- Provide raw (unflipped) values for reverse items — the renderer flips.
- `n` per segment is required; `invited` per wave enables the response-rate strip.
- Omit what you don't have (a question a segment wasn't asked, `invited`, themes). **Never fabricate** a score, count, or theme.
- `anonymity_threshold` here overrides the design file's value if both are present; if neither, default 5.
- Wave order in the array = chronological order; deltas compare each wave to the previous one.
