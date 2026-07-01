# OCM Methodology — Stakeholder Assessment (SHA)

Portable OCM method. Apply these rules when extracting records.

## What the SHA captures
A **stakeholder record** is one group or role affected by (or able to affect) the change. It captures who they are, how the change hits them, how much power and stake they have, their current sentiment and pain points, who owns the relationship, and how to engage them.

## Influence × Interest engagement grid (Mendelow)
Rate each group on two 1–5 scales:
- **Influence** — power to affect the change's success (budget, decision rights, ability to block or accelerate).
- **Interest** — how much the change affects them / how much they care (stake in the outcome).

The **Engagement Strategy** quadrant is *derived* (High if ≥ 4):

| | High interest | Low interest |
|---|---|---|
| **High influence** | **Manage Closely** | **Keep Satisfied** |
| **Low influence** | **Keep Informed** | **Monitor** |

You may write specific tactics in `engagement_strategy`; the renderer fixes the leading quadrant to match the grid. If omitted, it's set to the derived quadrant.

## Scoring discipline
- Rate Influence and Interest from evidence in the transcript, with a one-line rationale for each where possible.
- **No fabricated ratings:** if a group's influence/interest wasn't discussed, note it as a follow-up rather than inventing a score.
- **Sentiment**: Positive / Mixed / Neutral / Negative / Cautious — the group's current disposition toward the change.

## What good stakeholder records include
- `impact_from_change` — how their day-to-day actually changes (the "so what" for them).
- `decision_authority` — what they sign off or control (feeds the engagement plan).
- `key_pain_points` — current frustrations/risks the change touches.
- `main_point_of_contact` and `change_champion` — the relationship owners.
- `communication_preferences` / `training_preferences` — how to reach and enable them.

## Reconciling with the CIA
Change-impact analysis lives in the separate `cia-builder` skill. Keep SHA `stakeholder_group` names consistent with the CIA `roles_impacted` names, so a stakeholder group maps cleanly to the impacts affecting it and the two datasets don't drift.

## Style
American English. Source every claim to the transcript. Don't fabricate ratings or metrics. Don't explicitly write "no representation in [meeting]" — phrase as an open follow-up (`follow_up_needed`) instead.
