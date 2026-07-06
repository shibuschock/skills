# training_strategy.json — schema

One JSON object. All string fields are plain text. Empty/omitted optional fields are fine — **never invent a value to fill one** (unknowns go in `open_questions`).

```jsonc
{
  "meta": {
    "program": "Acme ERP",                       // program name (display)
    "workforce_types": ["Frontline Retail", "Office Professional"],  // the audience segments the strategy addresses
    "go_live_reference": "Phased: Wave 1 Q2, Wave 2 Q4",             // single date or wave description; text
    "prepared_by": "",                            // optional
    "date": "2026-07-06"                          // optional, ISO
  },

  "principles": [                                 // 4–7 entries
    {
      "principle": "Role-based",                  // short name
      "statement": "Built around what each role does, not generic system tours.",
      "implication": "Curricula are assembled per learner group; no one-size-fits-all courses."  // "so we will…"
    }
  ],

  "modality_strategy": [                          // exactly one entry per workforce type in meta.workforce_types
    {
      "workforce_type": "Frontline Retail",
      "primary_modalities": ["In-app guidance", "Job aids", "Microlearning"],
      "secondary_modalities": ["Huddle ILT"],     // optional
      "rationale": "Hard to release from the floor; needs task-level help at the moment of need."
    }
  ],

  "governance": [                                 // who owns what
    {
      "role": "Training workstream lead",         // role, not person
      "owns": "Strategy, TNA, curriculum design, readiness gates",
      "named_person": ""                          // optional; only if the client supplies a name
    }
  ],

  "resourcing": {
    "core_team": "Small core team: training lead + 2 instructional designers; sized in the TNA stage.",
    "multipliers": "Train-the-trainer; super-users/champions deliver and reinforce locally.",
    "vendor_stance": "Vendor acceptable for content development surge; process knowledge stays in-house."
  },

  "build_vs_buy": [
    {
      "category": "LMS",                          // e.g., LMS, in-app guidance, authoring tool, generic content
      "stance": "Use existing LMS",               // Build | Buy | Use existing | Open question
      "rationale": "Corporate LMS already deployed to all workforce types."
    }
  ],

  "measurement": {
    "approach": "Kirkpatrick L1–L4; completion and competency thresholds feed the go/no-go readiness gate per wave.",
    "links": ["Detailed L1–L4 plan: training rollout skill output", "Adoption metrics: adoption-metrics-builder"]
  },

  "phasing": [                                    // ordered; offsets relative to go-live, not calendar dates
    {
      "phase": "Train-the-Trainer",
      "timing": "T-90 to T-60",                   // free text offset or wave label
      "description": "Certify local trainers and champions on core content."
    }
  ],

  "risks": [
    {
      "risk": "Frontline learners cannot be released for training during peak season.",
      "mitigation": "Microlearning + in-app guidance reduce classroom time; schedule around peak.",
      "owner": "Operations leadership"            // role-level fine
    }
  ],

  "assumptions": [
    "Sandbox environment available 90 days before each go-live."
  ],

  "open_questions": [                             // unknowns — the no-fabrication outlet
    {
      "question": "Which in-app guidance tool (digital adoption platform) will be licensed?",
      "needed_from": "IT / program leadership",
      "needed_by": "Before content development starts"
    }
  ]
}
```

Required: `meta.program`, `meta.workforce_types`, `principles` (≥1), `modality_strategy` (one per workforce type). Everything else optional but recommended.

## project.json (shared shape across the OCM suite)

```jsonc
{
  "project_name": "Acme ERP",
  "business_units": ["Retail", "Finance"],
  "locations": ["HQ", "Stores"],
  "brand": {
    "navy": "#162B75",                            // primary
    "magenta": "#EE2C81",                         // accent
    "font": "Calibri, system-ui, sans-serif",
    "footer": "Acme — Confidential"
  }
}
```
