# Bundled templates — `assets/templates/`

Portable Markdown templates with `{{placeholders}}`. They are drafting starters, not
auto-generated output — Claude fills the placeholders from the program's confirmed content,
then runs `comms_qa.py` on the draft before it enters the approval gate.

| Template | Use for | Key placeholders |
|---|---|---|
| `email_whats_changing.md` | The "What's Changing" email arc (Ep.1 Awareness → Ep.2 Process → Ep.3 Training) | `episode_number`, `episode_theme`, `adkar_layer`, `what_is_changing`, `why_it_matters`, `action_1/2` |
| `newsletter.md` | Monthly newsletter | `month_year`, `progress_update`, `spotlight_story`, `whats_next`, `milestone_countdown` |
| `town_hall_faq.md` | Town hall pack (run of show + FAQ + holding line) | `event_date`, `key_message_1..3`, `faq_q1..3`, `holding_line`, `single_call_to_action` |
| `manager_cascade.md` | Manager pre-brief / cascade (24h/48h pattern, ADKAR Desire) | `topic`, `milestone`, `talking_point_1..3`, `team_specific_change`, `feedback_channel`, `cascade_deadline` |
| `steerco_update.md` | Steering Committee comms update | `period`, `one_line_status`, `activities_sent`, `coverage_gaps`, `risk_1/2`, `decision_1/2` |
| `crisis_holding_statement.md` | Crisis comms (T+24h / T+72h / T+14d) | `scenario`, `holding_statement`, `substantive_update`, `recovery_message`, `approver` |

## How to use them
1. Copy the template text for the vehicle you're drafting.
2. Replace every `{{placeholder}}` with confirmed content. Leave nothing in braces.
3. Pull shared values (`{{project_name}}`, `{{footer}}`) from `project.json`.
4. For `steerco_update.md`, fill `{{coverage_gaps}}` from `coverage_matrix.py` output.
5. **QA the draft:** `python3 scripts/comms_qa.py --file your_draft.md` — hit reading grade 5–7,
   sentences under ~25 words, no slop.
6. Route through the `approval_gate` before sending.

## Placeholder convention
- `{{snake_case}}` — a single value to replace.
- HTML comments (`<!-- ... -->`) are author guidance; delete them from the final send.
- Templates are American-English and brand-neutral; the footer line carries `{{footer}}` from
  `project.json` (e.g. "Acme — Confidential").
