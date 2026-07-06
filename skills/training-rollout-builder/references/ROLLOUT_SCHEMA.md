# Rollout plan schema

`rollout_plan.json` is the structured twin of the `rollout_plan.md` narrative (see `ROLLOUT_MEASUREMENT.md` for the markdown structure — both are produced; the JSON feeds `scripts/rollout_render.py`). It is a JSON object with these keys:

## `go_lives` — array
One per go-live event. **Dates are optional** — if unknown, leave `date` blank; everything else anchors on week offsets, never invented dates.

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable ref, e.g. `GL-1`. Waves point at this. |
| `label` | yes | e.g. "Acme ERP go-live — all BUs". |
| `business_units` | rec. | Which BUs cut over at this event. |
| `date` | opt. | ISO date if confirmed; blank/omit otherwise (renderer shows "GL" as the anchor). |
| `offset_weeks` | opt. | **Multi-go-live spacing without dates**: weeks after the FIRST go-live (GL-1 = `0`; e.g. GL-2 = `8` means GL-1 + 8 weeks). When every referenced go-live carries an offset, the renderer plots all waves on ONE absolute week axis with a marker per go-live. When offsets are absent, the renderer instead groups the timeline into one section per go-live — it never collapses waves onto `go_lives[0]`. |

## `waves` — array
One per delivery wave. Windows are expressed **backward from go-live in weeks** (positive numbers = weeks before GL).

| Field | Required | Notes |
|---|---|---|
| `id` | yes | `W0`, `W1`, … One super-user wave **per go-live**, sequenced first within that go-live (W0 for GL-1; later go-lives get their own super-user/TTT wave). |
| `name` | yes | e.g. "Super-user enablement". |
| `go_live_ref` | yes | A `go_lives` id. |
| `audiences` | yes | Array of audience names (match needs/curriculum audiences). |
| `business_units` | yes | Array. |
| `locations` | opt. | Array; PLACEHOLDER if unknown. |
| `modules` | yes | Array of curriculum module `id`s delivered in this wave. |
| `delivery_mode` | yes | e.g. ILT / VILT / in-app. |
| `headcount` | opt. | Number or PLACEHOLDER string — never invented. |
| `start_weeks_before_golive` | yes | e.g. `6` = window opens GL−6 wks. |
| `end_weeks_before_golive` | yes | e.g. `4` = window closes GL−4 wks. Use `0` for at-go-live. |
| `sessions` | opt. | Array of `{ "module", "audience", "format", "facilitator", "notes" }` for scheduled sessions. |
| `notes` | opt. | Constraints honored (shift work, peak season, etc.). |

## `super_user_plan` — object
`{ "selection_criteria", "track" (module id or description), "role_at_golive", "role_after", "ratio" }` — the 20% social band. `ratio` e.g. "1 super-user per 10 learners (PLACEHOLDER)".

## `comms_touchpoints` — array
Training-specific comms only. `{ "timing" (e.g. "GL−3 wks"), "audience", "message", "channel" }`. Broad change comms live in the CIA/SHA work — reference, don't duplicate.

## `readiness_criteria` — array
Per audience, the go/no-go training gate. `{ "audience", "criteria": [strings], "gate" (what "trained and ready" means / what it unlocks) }`.

## `program_gates` — array
Program-level preconditions (funding, policy decisions, steering thresholds) that don't belong to one audience. `{ "gate", "source_need" (opt. TN id or module id it came from), "blocks" (opt. array of wave/go-live ids) }`. Carry the curriculum's `non_training_gates` here (or into `site_gates`) so nothing flagged upstream is lost.

## `site_gates` — array (site-keyed)
Per-site preconditions (union commitment, hardware readiness, sandbox access). `{ "site", "gates": [strings], "source_need" (opt.) }`.

## `deferred_modules` — array
Modules intentionally NOT scheduled. `{ "module" (curriculum module id), "reason" }`. Rendered as an explicit "not scheduled — gated" list so gated modules (e.g. `status: "gated — do not build"`) read as deliberate, not as omissions.

## `measurement` — array
Kirkpatrick L1–L4. `{ "level": "L1|L2|L3|L4", "label", "metric", "method", "owner", "timing", "value_lever" (L3/L4: the CIA value lever it evidences; blank otherwise) }`.

## `reinforcement` — array
Spaced sustainment schedule. `{ "timing" (e.g. "GL+2 wks"), "activity", "audience", "owner" }`. Include new-hire onboarding for high-turnover audiences.

## `risks_assumptions` — array of strings
Training-specific risks + assumptions to confirm. Flag all PLACEHOLDERs.

## Rules
- **No fabricated dates or headcounts.** Offsets are structural; dates only when the user confirmed them.
- Every wave `modules` id must exist in `curriculum.json` — or appear in `deferred_modules` with a reason.
- Super-users always precede their population — checked **per go-live** (each go-live's super-user/TTT wave comes first within that go-live).
- Every curriculum `non_training_gates` entry must land in `program_gates`, `site_gates`, or an audience's `readiness_criteria`.
- L4 measurement rows should carry a `value_lever` so training evaluation connects to value realization.
