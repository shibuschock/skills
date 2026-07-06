# Schemas

Two files drive the renderer: `project.json` (shared shape across the OCM suite) and `network_plan.json` (this skill's canonical dataset). Claude writes both; the user never hand-edits JSON.

## project.json

```json
{
  "project_name": "Acme ERP",
  "business_units": ["Retail", "Finance", "Supply Chain"],
  "locations": ["HQ", "Plant", "Distribution Center"],
  "brand": {
    "navy": "#162B75",
    "magenta": "#EE2C81",
    "font": "Calibri, system-ui, sans-serif",
    "footer": "Acme — Confidential"
  }
}
```

- `project_name` — required; prefixes output filenames.
- `brand` — optional; any key overrides `DEFAULT_BRAND` in the renderer.
- `business_units` / `locations` — used to sanity-check roster coverage (a BU with zero roster rows is a design gap worth flagging).

## network_plan.json

```json
{
  "network": { ... },
  "cadence": [ ... ],
  "roster": [ ... ]
}
```

### network (the operating model)

```json
{
  "name": "Acme ERP Change Network",
  "purpose": "Embed trusted voices in every impacted team to translate, surface, advocate, and support.",
  "sizing_basis": "~1 champion per 25 impacted employees; every impacted team/site has at least one.",
  "tiers": [
    {
      "tier": "Sponsor",
      "who": "VP Operations",
      "role": "Visible authorization, recognition, unblocks nomination stalls.",
      "time_commitment": "Quarterly touchpoint + phase gates"
    },
    {
      "tier": "Change Lead",
      "who": "One per business unit, manager level",
      "role": "Coordinates BU champions; first escalation point.",
      "time_commitment": "~5% of working time"
    },
    {
      "tier": "Champion",
      "who": "Frontline peers in each impacted team/site",
      "role": "Cascade messages, collect feedback, support adoption locally.",
      "time_commitment": "10-15% of working time, varying by phase"
    }
  ],
  "selection_criteria": [
    "Works in the affected area and is personally impacted",
    "Trusted, credible peer — influence over seniority",
    "Has capacity; manager informed and supportive",
    "Willing — confirmed, not voluntold",
    "Constructive engagement — skeptics welcome, active detractors are not"
  ],
  "time_by_phase": [
    {"phase": "Foundation / Design", "time": "~5-10%", "activities": "Briefings, initial team conversations"},
    {"phase": "Build & Test", "time": "~10-15%", "activities": "Briefings, UAT support, feedback collection"},
    {"phase": "Training & Go-Live", "time": "~15-20%", "activities": "Training reinforcement, floor support"},
    {"phase": "Hypercare", "time": "~10-15%", "activities": "Issue surfacing, adoption support, peer coaching"}
  ],
  "recognition": [
    "Named acknowledgment in sponsor communications",
    "Participation documented as professional development",
    "Milestone recognition at phase gates and go-live"
  ],
  "nomination": {
    "nominated_by": "BU leadership",
    "deadline": "2026-08-15",
    "workflow": [
      "OCM defines criteria and seat map",
      "Leadership nominates by deadline (nomination email + pre-filled workbook)",
      "OCM screens against criteria; confirms willingness + manager support",
      "Onboarding session; seat moves to Onboarded"
    ]
  }
}
```

All `network` fields render into the dashboard's Design tab and the workbook. Keep them plain-language — they double as onboarding content. Omit what the engagement doesn't use (e.g., `time_by_phase` for a light 1–4 hrs/month network — then put the flat commitment in the tier).

### cadence (array — the operating rhythm)

```json
{
  "name": "Change Network Briefing",
  "frequency": "Monthly",
  "duration": "30 min",
  "audience": "All champions",
  "owner": "OCM team",
  "purpose": "Program updates, talking points, one clear ask, round robin"
}
```

- `frequency` — free text, but use consistent values (Monthly, Bi-weekly, Weekly, Quarterly, Always on, After each briefing) so the cadence calendar groups cleanly.
- `duration`, `audience`, `owner` optional.

### roster (array — one object per SEAT, filled or open)

```json
{
  "id": 1,
  "name": "Jordan Lee",
  "role_title": "Inventory Analyst",
  "tier": "Champion",
  "business_unit": "Retail",
  "location": "HQ",
  "team": "Store Operations",
  "email": "jordan.lee@example.com",
  "status": "Confirmed",
  "headcount_covered": 30,
  "nominated_by": "Retail Director",
  "notes": ""
}
```

| Field | Req | Rules |
|---|---|---|
| `id` | no | Auto-numbered if omitted. |
| `name` | no | **Blank for an Open seat — never invent a name.** |
| `role_title` | no | The person's day job. |
| `tier` | yes | Must match a `network.tiers[].tier` value. |
| `business_unit` | yes | Align to SHA stakeholder-group / CIA `business_unit` names. |
| `location` | no | Site/campus; drives the coverage view. |
| `team` | no | The group this seat represents (the coverage unit). |
| `email` | no | Only if actually provided. |
| `status` | yes | One of `Open`, `Candidate`, `Nominated`, `Confirmed`, `Onboarded`, `Departed`. `Candidate` = a person has been identified (volunteered, named conditionally, or suggested) but not yet formally nominated — use it instead of stuffing candidate names into `notes` or overstating them as `Nominated`. A Candidate seat may carry a `name`; it does not count as filled. |
| `headcount_covered` | no | Impacted employees this seat covers. **Blank if unknown — never estimate silently.** |
| `nominated_by` | no | Who named them. |
| `notes` | no | Caveats, shared coverage, replacement pending, etc. |

### Derived by the renderer (don't hand-compute)

- Summary tiles: total seats, filled vs open, candidate count, % filled, onboarded count, total headcount covered.
- Coverage by BU (and by location): seats, filled, open, candidate, headcount covered, champion-to-headcount ratio.
- Coverage GAP flag: any BU/location with open or candidate seats (not yet secured) or zero seats.
- Cadence calendar grouping by frequency.

## No fabrication

An Open seat with a blank name is correct. A blank `headcount_covered` is correct. An invented name, email, headcount, or deadline is a defect. (A nomination deadline that is explicitly proposed as an OCM design decision and confirmed with the user is not an invented deadline — see SKILL.md step 3.)
