# SHA record schema

`sha_records.json` is a JSON array. One object per **stakeholder group / role**. Fields:

| Field | Required | Notes |
|---|---|---|
| `stakeholder_group` | yes | Group or role name (e.g. "Store Leadership"). No commas in the name. |
| `business_unit` | yes | BU from `project.json`. |
| `location` | rec. | Site/location (e.g. "HQ", "Plant", or "Both"). |
| `category` | rec. | Grouping (e.g. "Operations Leadership", "Finance"). |
| `group_description` | yes | What the group does, size, where based. |
| `influence` | yes* | 1–5 — power to affect the change's success. |
| `interest` | yes* | 1–5 — how much the change affects them / their stake. |
| `assessment_status` | cond. | \*Set to `"Not yet assessed"` to record an identified group **without** `influence`/`interest` (e.g. no interview coverage yet). Required whenever those scores are absent; the validator errors on missing scores only when this field is also absent. Unassessed groups appear in the table/xlsx and in a "Pending assessment" list under the grid — they are not plotted as dots. |
| `influence_rationale` / `interest_rationale` | rec. | Why those ratings. |
| `impact_from_change` | rec. | How their work changes. |
| `impact_rationale` | opt. | Why. |
| `decision_authority` | rec. | What they sign off / decide. |
| `current_sentiment` | opt. | Positive / Mixed / Neutral / Negative / Cautious. |
| `key_pain_points` | rec. | Current frustrations / risks. |
| `communication_preferences` | opt. | How to reach them. |
| `engagement_strategy` | opt. | Tactics. **Leading quadrant is auto-corrected to the Influence×Interest grid; omit it to auto-fill the quadrant.** |
| `training_preferences` | opt. | Constraints (scheduling, hands-on, etc.). |
| `main_point_of_contact` | rec. | Named POC. |
| `change_champion` | opt. | Nominated champion. |
| `additional_notes` | opt. | Anything else. |
| `follow_up_needed` | opt. | Open follow-up. Don't write "no representation in [meeting]" — phrase as an action. |

**Derived automatically** (do NOT supply): `id`, the Engagement Strategy quadrant (Manage Closely / Keep Satisfied / Keep Informed / Monitor) from Influence × Interest (High if ≥4).

See `examples/sha_records.example.json`.
