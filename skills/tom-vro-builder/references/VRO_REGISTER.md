# VRO — Benefits Register & Value-at-Risk

The VRO's two core artifacts. Both are non-negotiable-format outputs; keep them honest.

## Benefits register
One row per benefit from the business case, mapped to how it will actually be measured. Fields:
`benefit`, `kpi`, `baseline_source`, `owner`, `target`, `timeline`.

Rules:
- **Every KPI names a `baseline_source`** — the system or report the "before" number comes from. Without a captured baseline there is no "before" to measure go-live against.
- **Every KPI names an `owner`** — a single accountable person/role. No owner is the biggest benefits-realization failure mode.
- `target` **stays blank until baselined** — do not invent target numbers.
- Prefer **non-monetary** operational KPIs (e.g. "% reduction in stockouts", "inventory turns", "business days to close"), not dollar figures.
- Adoption **leading indicators** (usage, workaround rate, training completion, confidence) belong in the register alongside the lagging financial benefits, as early signals a benefit line is slipping.

## Value-at-risk register
One row per material open/assumed gap that threatens a benefit. Fields:
`cluster`, `benefit_at_risk`, `why`, `source_gap`.

Rules:
- Source each cluster from the **fit-gap / CIA** — a gap that stays open is an early warning that a benefit line is slipping.
- `source_gap` records the disposition (e.g. Assumed / Unconfirmed) so the VRO can track closure through design & build.
- Keep it to the **material** clusters — the few gaps that carry the largest benefit at risk, not every open item.

## How they connect
The benefits register is the *forward* view (what value we expect and how we'll know); the value-at-risk register is the *risk* view (which benefits are exposed by unresolved design). Review them together: a benefit with mapped value-at-risk and low confidence is where VRO attention goes first.
