# Adoption measurement methodology

Portable OCM method for designing an adoption & success metric set. Read this before writing `metrics_plan.json`.

## The metric ladder

Every adoption question climbs four rungs. A credible metric set covers **all four** — a set that stops at usage is measuring logins, not change.

| Ladder level | Question it answers | Example metrics |
|---|---|---|
| **System Usage** | Are people in the new system at all? | Login rate (Day 7/14/30), transaction volume through the new system vs. workarounds, feature utilization |
| **Behavior/Proficiency** | Are they working the new way, competently? | Process compliance rate (designed future-state path vs. legacy workaround), error/rework rate, workaround incidence, time-to-proficiency, help-desk ticket trend, stabilization curve (time back to baseline productivity) |
| **Process Outcomes** | Is the process performing better? | Cycle time, first-pass yield, throughput, data quality/accuracy, exception backlog |
| **Business Value** | Is the case for change being realized? | The value levers from the business case / CIA (e.g., stockout reduction, inventory turns, cost avoidance). Usually owned by Finance/process owners — include for alignment, mark ownership honestly. |

**Pre-go-live categories** sit in front of the ladder and are legitimate metrics in their own right:
- **Engagement** — sponsor visibility index, change-network activation rate, briefing/workshop attendance, pulse response rate.
- **Readiness** — stakeholder readiness score (pulse anchors), training completion, impact-mitigation coverage (% of high-severity impacts with a completed mitigation plan), leadership cascade completion, go/no-go composite.

Tag each metric with a `category` (Engagement / Readiness / Adoption / Business Outcome) **and** a `ladder_level` (Engagement/Readiness metrics take ladder level `Readiness Input`).

## Leading vs lagging

- **Leading** indicators predict adoption before value shows up: engagement, readiness, usage, early behavior signals (workarounds, tickets). They are actionable — a red leading metric triggers an intervention.
- **Lagging** indicators confirm outcomes after the fact: process outcomes, business value.
- Rule of thumb: a healthy set is weighted toward leading indicators early (Phase 0 → hypercare) and shifts weight to lagging as the program stabilizes. If everything in the plan is lagging, the change team has no steering wheel.

## Baseline / target / threshold discipline

- **Never invent a number.** Baselines come from measured current state; targets come from the client, the business case, or a genuinely standard benchmark (e.g., ≥90% training completion pre-go-live is a defensible OCM standard; "≥37% pulse favorability" is not). **A blank baseline or target is correct; an invented one is a defect.**
- Baselines for perception metrics come from the first pulse survey — plan for it explicitly ("establish baseline at first pulse").
- Targets without a measurement method are wishes. Every target must be measurable from the named source.
- Distinguish **target** (where we want to be) from **thresholds** (`threshold_amber`, `threshold_red` — where we escalate). Thresholds drive the RAG status and the escalation path in the measurement plan.

## RAG thresholds

- Green: at/above target trajectory. Amber: below target but above red threshold — owner investigates, reports cause. Red: below red threshold — escalate per the measurement plan's escalation path (named forum, named decision-maker).
- For trend metrics (ticket volume, workaround incidence), RAG on the **trend direction**, not the absolute number.
- Set thresholds only where a target exists; a metric still establishing its baseline has no RAG.

## Measurement cadence

- Match cadence to volatility and cost of collection: system telemetry can be weekly/daily during hypercare; pulse surveys monthly-to-quarterly (survey fatigue is real); business value quarterly.
- Metrics have **activation timing** — not everything starts on day one. Note when each metric starts (e.g., "first pulse", "go-live", "go-live + 2 weeks", "hypercare exit").
- The `measurement_plan` block names the reporting cadence, the review forum (e.g., steering committee, change-team weekly), and the escalation path for reds.

## Instrumenting sources

Every metric names a concrete source/instrument, and it must exist (or have a plan to exist):
- **System telemetry** — login/usage analytics, transaction logs, feature adoption reports. Confirm with the platform team what is actually instrumentable before promising it.
- **Pulse surveys** — small anchor question set repeated each wave for trendability; readiness/confidence/sentiment.
- **Help desk / support** — ticket volume, categories, trend; a cheap and honest behavior signal.
- **Process KPIs / operational reporting** — cycle time, error rates, accuracy; usually owned outside the change team — record the real owner.
- **Observation / audit** — floor walks, spot checks, change-agent feedback for compliance and workaround detection.

## Anti-patterns

- **Vanity metrics** — numbers that always go up and inform no decision (cumulative emails sent, total training seats offered). If a metric can't trigger an action, cut it.
- **Measuring activity, not adoption** — attendance and completion are inputs, not adoption. Keep them (as Engagement/Readiness) but never present them as evidence people are working the new way.
- **Usage ≠ adoption** — logins prove access, not behavior. Pair every usage metric with a behavior/compliance metric.
- **Metric sprawl** — a menu can be broad, but recommend a small activation set (6–10) for leadership reporting; more metrics than owners is a plan that won't be run.
- **Orphan metrics** — no owner, no source, no cadence = not a metric, a hope. Every row has all three.
- **Target theater** — retro-fitting targets to whatever the data shows, or setting targets before a baseline exists.
- **Ignoring the business case** — if the CIA names value levers, the metric set must trace to them; adoption measurement that never touches value is self-referential.
