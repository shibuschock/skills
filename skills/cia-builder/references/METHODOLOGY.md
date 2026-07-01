# OCM Methodology — Change Impact Assessment (CIA)

Portable OCM method. Apply these rules when extracting records.

## What the CIA captures
A **change impact** is a *current → future change to how people work*, triggered by the new system/process — **not** a technology changelog. Every impact records the human/organizational consequence (process, role, data, skills, mindset). Technology is the *trigger*, not a category.

## The 6 Change Dimensions (MECE, multi-label + one Primary)
Each impact is tagged with every dimension that **materially** applies, plus exactly one **Primary** (the load-bearing one). The six answer distinct questions:

| Dimension | Question | Tag when | Not when (→ goes to) |
|---|---|---|---|
| **Role/Accountability** | WHO owns/decides/approves | ownership, decision rights, or sign-off moves/created | a task is just done differently (→ Ways of Working) |
| **Process/Policy** | by WHAT RULE (codified) | a codified procedure, SOP, control, stage-gate, compliance rule changes | informal lived workflow (→ Ways of Working) |
| **Ways of Working** | HOW work flows (lived) | workflow sequence, cadence, handoffs, manual↔system mode changes | a documented rule (→ Process/Policy) |
| **Data/Decision Inputs** | with WHAT INFORMATION | data, reports, visibility, metrics, master data, system-of-record changes | the workflow consuming it (→ Ways of Working) |
| **Skills/Capability** | WHAT NEW COMPETENCY | the *work* demands a genuinely new competency/discipline | **just learning to operate the new tool — that's TRAINING, not Skills** |
| **Mindset/Culture** | WHAT BELIEF/TRUST | adoption depends on trust, buy-in, ceding control | a teachable skill (→ Skills/Capability) |

**Decisive Skills test:** *would this still be a skill gap if the person were already fluent in the software?* If no → it's training, don't tag Skills.
**Impact vs response:** training/comms/engagement are *responses* (Mitigation field). Never tag a dimension just because a response is needed.
**Primary:** "if you could manage only one, which defines what this impact fundamentally is?" Exactly one per impact; the rest are secondary.

## CIA scoring
- **Severity** (1–5): magnitude of the change for affected roles.
- **Complexity** (1–5): how hard the change is.
- `severity_label` (5 Critical … 1 Minimal) and `impact_score` (= complexity × severity) are **derived** — do not supply.
- **Priority**: Critical / High / Medium / Low (sequencing signal).
- **Sentiment**: stakeholder sentiment toward the change (Positive / Mixed / Neutral / Negative / Cautious).
- **No fabricated metrics:** if a session wasn't scored, leave severity/complexity/priority blank rather than inventing.

## Scope (disposition)
`In Scope` (default) · `Out of Scope - Adjacent` (tracked for awareness; mitigation owned outside the program) · `Gap - Requirement Unconfirmed` (no confirmed requirement). Out-of-scope/gap items stay tracked but are flagged.

## Optional analytical layers
Use these only when the engagement actually works this way; otherwise leave the fields blank and the tabs won't appear.

- **Future-State Status** — label each impact `Discussed-Confirmed` (agreed in a session), `Discussed-Pending` (raised, not settled), or `Assumed` (no confirmation — inferred design). Don't overstate certainty: a vendor-pitched option or a "would be nice" is not Confirmed. If unset, the renderer infers `Assumed` unless there's a `workshop_reference`/`evidence_source`.
- **TOM Shifts** — name the operating-model transition a cluster of impacts belongs to (e.g. "Sourcing → proactive planner"). Define the controlled list in `project.json` `tom_shifts`; each becomes a tile + printable one-pager.
- **Value Realization** — tag impacts with `value_levers` (benefit names) and define the vocabulary in `project.json` `benefits`. **Non-monetary** by design — target metrics like "% reduction in stockouts", not dollars. Don't invent metrics; a benefit with no mapped impacts is flagged as a coverage gap. "At risk" = mapped impacts with Mixed/Negative sentiment and complexity ≥ 4.
- **Training Needs** — `training_modality`, `estimated_training_hours`, `access_constraints` per impact. The dashboard pivots these by audience/role. Capability gaps are *Skills* dimensions; learning to operate the tool is training, not a Skills tag (see the decisive test above).
- **Workshop / staleness** — `last_reviewed` + `workshop_reference` drive a staleness flag (older than `training.stale_days`, default 30) so you can see what to bring back to the next session.

## Reconciling with the SHA
Stakeholder analysis lives in the separate `sha-builder` skill. Keep CIA `roles_impacted` role names consistent with the SHA `stakeholder_group` names, so an impact's affected roles map cleanly to stakeholder groups and the two datasets don't drift.

## Style
American English. Source every claim to the transcript. Don't fabricate metrics, dollar figures, or scores for unscored sessions. Don't explicitly write "no representation in [meeting]" — phrase as an open follow-up instead.
