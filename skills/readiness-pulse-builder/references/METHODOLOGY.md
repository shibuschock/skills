# Readiness Pulse Methodology

Portable OCM method for pulse-survey design and interpretation. Read this before selecting questions (DESIGN) and before writing any readout narrative (ANALYZE).

## 1. Readiness dimensions (ADKAR-aligned)

Every question maps to exactly one dimension. The six dimensions:

| Dimension | What it measures | ADKAR anchor |
|---|---|---|
| **Awareness** | Do people understand *why* the change is happening and what the program is? | Awareness |
| **Understanding** | Do they know *how their own role and processes* will change? | Awareness → Knowledge bridge |
| **Leadership Confidence** | Do they trust sponsors/leaders to make good decisions and stay the course? | Desire, Reinforcement |
| **Capability** | Do they feel they will have (or have) the skills, training, and support to perform? | Knowledge, Ability |
| **Workload & Capacity** | Do they have the time and bandwidth to prepare and learn alongside the day job? | Ability (the most common hard bottleneck) |
| **Sentiment & Trust** | Buy-in, perceived fairness, voice, belief the promised value will arrive on the promised timeline | Desire |

Culture is not a separate assessment — it lives inside Sentiment & Trust (fairness, voice, trust-in-execution) and moderates the whole readiness curve. If the engagement has a known cultural fault line (e.g., a group that feels deprioritized by phasing), add targeted Sentiment & Trust items for it rather than a separate culture survey.

## 2. Question design rules

- **Likert 1–5** for all scored items: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree. Keep the scale identical across every wave — comparability is the whole point.
- **One concept per item.** "I understand the change and support it" is two questions; split or cut. Reword double-barreled bank items before fielding.
- **Anchor vs rotating.** ~5 anchor items (one per core dimension) appear in every wave, wording frozen, to build the trendline. Rotating items (3–5) match the current phase. Never reword an anchor between waves — a reworded anchor is a new question and breaks the trend.
- **Reverse-scored items — use with caution.** They catch straight-lining but confuse frontline respondents and complicate scoring. Prefer zero reverse items in a short pulse; if one is used, mark `"reverse": true` so the renderer flips it (score′ = scale_max + 1 − score). Never pre-flip in the data.
- **Pair scaled items with open text.** 1–2 open-text prompts per pulse, no more. The open text explains *why* a number moved; the number tells you *where* to read the open text.
- **Length discipline: 8–12 items, 3–5 minutes.** Beyond ~15 items, completion and data quality drop.
- **Tense:** pre-go-live items use future tense ("I will be able to…"); switch to present tense post-go-live. That tense switch is an allowed anchor edit — note it in the wave label.

## 3. Cadence

| Program stage | Frequency | Focus |
|---|---|---|
| Foundation / Design | Baseline, then quarterly | Awareness, initial sentiment baseline |
| Build & Test | Monthly | Understanding, readiness progression |
| Training & Go-Live | Bi-weekly | Capability, confidence, training effectiveness |
| Hypercare | Weekly → bi-weekly | Proficiency, adoption barriers, support needs |

Field a **baseline before major comms/training land** — without it, later waves have no reference point. For multi-wave deployments, pulse each wave's population as its go-live approaches rather than the whole org on one calendar.

## 4. Response-rate and anonymity discipline

- **Anonymity is a promise, not a preference.** State it in the invite; report at group level only; individual responses never disclosed.
- **Minimum-n suppression threshold:** never report a segment with fewer than the `anonymity_threshold` responses (default **n < 5** — set higher for sensitive climates). The renderer enforces this in the dashboard; you must also honor it in chat and in any narrative — do not name or characterize a suppressed segment's scores.
- **Segments are rollups, not the SHA list.** Survey segments are ROLLUPS of SHA stakeholder groups, sized so each clears the anonymity threshold — never field an n=1 (or near-threshold) SHA group as its own segment. Document the segment → SHA-group mapping in the design notes so results can be traced back to the stakeholder analysis.
- **Response rate is itself a signal.** Below ~50%, results are directional at best — investigate distribution, timing, and trust before interpreting scores. Report the rate alongside every wave.
- **Escalation thresholds** (adapt per engagement): any anchor mean < 3.0 → intervention plan; any segment < 2.5 on a capability item → targeted engagement; response rate < 50% → distribution review; open-text theme with 3+ mentions → theme analysis and response.

## 5. Interpreting results

- **Movement beats point-in-time.** A 3.4 that was 2.9 last wave is a different story than a 3.4 that was 3.9. Once two waves exist, lead the readout with deltas, not levels.
- **Segment always; never lead with the org-wide average.** Averages hide exactly the groups a pulse exists to protect. A healthy overall mean with one segment in the red is a red finding.
- **Read gaps between dimensions, not just low scores.** High buy-in (Sentiment) with low fairness/voice = people want in but feel shut out. High Awareness with low Understanding = comms are landing but role-level detail isn't. High everything with low Workload & Capacity = the plan is fine and the calendar isn't.
- **Don't over-read small movements.** With modest n, ±0.2 is noise. Flag deltas ≥ 0.3 as meaningful; treat smaller ones as "watch."
- **No benchmarks unless supplied.** There is no universal "good" readiness score. Compare a segment to itself over time and to peer segments in the same wave — never to an invented industry number.

## 6. Close the loop (non-negotiable)

Fielding a pulse creates an obligation. If people give data and see nothing happen, the next wave's response rate is the penalty. After every wave:

1. **Within ~1 week:** share a short "you said / we heard" summary with respondents — top findings, honestly stated, including the uncomfortable ones.
2. **Name the actions:** 2–3 concrete responses to what surfaced, with owners. "We heard training time is the issue; we are protecting X hours per person before go-live."
3. **Next wave, report back:** open the invite with what changed because of the last pulse.

The comms/anonymity plan in `pulse_design.json` should capture: who announces, distribution channel, reminder schedule, the anonymity statement, and the results-feedback commitment.

## 7. Works councils, unions, and consent

When any part of the audience is represented (union, works council) or the climate is surveillance-sensitive, the instrument needs consent groundwork before fielding:

- **Labor-relations review before fielding.** Have labor relations review the instrument — and stewards or the works council where local rules require it — before anything goes out. In some jurisdictions fielding without works-council approval is a violation, not just a misstep.
- **Commit in writing to aggregate-only reporting.** Put the commitment in the comms plan and the invite: group-level results only, individual responses never disclosed, no drill-down below the threshold.
- **Raise the anonymity threshold above the default.** In represented or surveillance-sensitive climates, the default minimum-n is not enough — set it higher and record the rationale.
- **Say what it isn't.** State explicitly in the survey invitation that this is not performance telemetry — it measures readiness for the change, not individuals, and no one's response reaches a manager.

## 8. Deskless administration

Frontline and deskless workers won't get an email link at a desk. Design the channel for the point of work:

- **QR posters** at the point of work (break room, line entrance, time clock) linking straight to the survey.
- **Huddle kiosks or shared tablets** for teams without personal devices, with completion built into an existing huddle.
- **Paper fallback** where devices fail (gloved, wet, or no-signal environments) — with a defined collection-and-entry path that preserves anonymity.
- **Completion time is paid time, budgeted on shift** — not squeezed in at rate on the line. 3–5 minutes per person is a scheduling line item, not a favor.
- **Windows and reminders span all shift rotations.** A survey window sized for day-shift desk workers misses 2nd and 3rd shift; extend the window and time reminders so every rotation gets equal opportunity to respond.
