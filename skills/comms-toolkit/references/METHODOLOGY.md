# Change-Communications Methodology (portable)

Portable method for running a change program's communications as an operation, not a
one-off announcement. Apply these when building `comms_plan.json` with the user.

## 1. Audience segmentation
Segment before you plan a single message. Five reusable segments (rename/extend per project):

| Segment | Who | Why they're distinct |
|---|---|---|
| **Champions** | Named local advocates | Cascade locally; feed sentiment back; get earlier, deeper detail. |
| **Managers** | People leaders | Pre-brief and run team cascades; carry the "why us" (ADKAR Desire). |
| **Org-wide** | All impacted employees | Broad awareness + consistent baseline. |
| **BU-specific** | A business unit / function / location | Process detail that only applies to them. |
| **Steering Committee** | Sponsors + program leadership | Governance: coverage, risk, decisions — not awareness. |

Each audience is `{id, name, description}`. Reference audiences by `id` (or name) everywhere else.

## 2. Channel mix + cadence
Match the vehicle to the job. A healthy mix:

- **Email series** — the workhorse. Run the **"What's Changing" arc**: **Ep.1 Awareness** (why), **Ep.2 Process** (how your work changes), **Ep.3 Training** (your path + go-live). Weekly.
- **Monthly newsletter** — progress, wins, countdown, FAQ. Keeps momentum between milestones.
- **Town halls** — live demo + Q&A; surfaces real concerns.
- **Champion touchpoints** — biweekly two-way sync; early-warning radar.
- **Manager cascade** — see the 24h/48h pattern below.
- **SteerCo updates** — coverage, sentiment, risk, decisions.
- **Sponsor video scripts** — the visible-sponsor moments.
- **Pulse surveys** — measure awareness/desire; feed the next refresh.

**Sequencing:** weekly activity beat, **monthly refresh cadence** (re-plan the next month from what pulse + champions tell you). Each activity is one `activities[]` row.

### Manager cascade — the 24h / 48h pattern
The cascade is how **Desire** gets built. Sequence every milestone message this way:
- **24h BEFORE** the org-wide message: managers get talking points + FAQ (pre-brief).
- **Day of:** managers run the team conversation in their own words.
- **48h AFTER:** managers report sentiment + open questions back up the chain (post-brief).

## 3. Comms-by-impact coverage (and the GAP rule)
**Every CIA change impact must map to at least one comm vehicle.** Record the mapping in
`coverage[]` (`impact` / `impact_id` → `vehicle` + `audience`). Run `scripts/coverage_matrix.py`
against the CIA to cross-check.

> **Non-negotiable:** an impact with no covering vehicle is a **GAP**. Gaps are the escalation
> trigger — surface them to the SteerCo, don't bury them. A `coverage[]` row with
> `status: "gap"` is an explicit, tracked gap (vehicle intended but not yet built).

## 4. Approval / QA gate
No message sends unreviewed. The gate: **draft → route → reviewer SLA → send.**
Define it once in `approval_gate` (`draft_by`, `route`, `sla_hours` e.g. 48, `send`, named
`reviewers[]`). Reviewers check four things:
- **Factual** — matches the confirmed design (BU SME).
- **Tone** — right for the audience; on-brand (Change Lead).
- **Scope-leak** — nothing promised that isn't in scope (Change Lead).
- **Sensitivity** — nothing that lands badly for people/legal (Sponsor).

**Plain-language standard:** reading grade **5–7**, sentences under ~25 words, de-slopped
(no jargon/AI-slop). Enforce with `scripts/comms_qa.py` before routing.

## 5. Crisis comms
Pre-agree activation scenarios (e.g. **vendor/partner delay**, **data incident**, **exec
departure**) so no one drafts under pressure. Each scenario carries a three-beat sequence:
- **T+24h holding statement** — acknowledge, confirm it's contained/under review, promise a dated update. Don't speculate or blame.
- **T+72h substantive** — facts in plain language, cause, remediation, any action people must take.
- **T+14d recovery** — confirm resolution, publish safeguards, thank people, resume normal cadence.

Store as `crisis[]` (`scenario`, `holding_24h`, `substantive_72h`, `recovery_14d`). In a real
crisis the SLA is waived — route straight to the approver for immediate sign-off.

## 6. ADKAR alignment
Map vehicles to the layer they move:
- **Awareness** — org-wide email Ep.1, town halls, newsletter.
- **Desire** — **manager cascade** (the load-bearing layer), sponsor video, champion touchpoints.
- **Knowledge** — email Ep.2/Ep.3, town-hall demo, training comms.
Reinforcement/Ability live mostly in the **training** workstream, not comms — hand off, don't duplicate.

## Reconciling with the CIA / SHA
- **CIA** (`cia-builder`) is the source of impacts to cover. Keep `coverage[].impact` titles
  aligned with CIA `title`s so `coverage_matrix.py` matches cleanly (it also matches by 1-based `impact_id`).
- **SHA** (`sha-builder`) is the source of audiences. Keep `audiences[].name` consistent with
  SHA stakeholder-group names so engagement strategy and comms don't drift.

## Style
American English. Plain language over polish. Source claims to the program's confirmed design —
don't announce a decision that isn't made. Don't invent metrics or dates.
