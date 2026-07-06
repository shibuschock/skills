# OCM Playbook Methodology (portable)

The playbook is the OCM team's operating document: **what happens, when, who owns it, how you'll know it worked, and how decisions get made** — for a bounded window (typically 90 days), anchored to the program's real milestones.

## Playbook anatomy — the six workstreams

Every playbook organizes activities under workstreams. The default set (adapt names, don't drop coverage):

1. **Leadership & Sponsorship** — sponsor activation, sender architecture (who signs/opens what), leadership alignment sessions, milestone updates to senior leaders. The sponsor is a *role with scripted moments*, not a name on a slide.
2. **Communications** — the comms runway: awareness series, newsletters, town halls, review/approval gates. If a comms plan exists (`comms_plan.json`), the playbook *references* its cadence — don't duplicate every send as an activity; carry the recurring vehicles as cadences and only put one-off or gated comms moments in the activity list.
3. **Change Network** — champion/agent identification, onboarding, recurring touchpoints, two-way feedback loop. A working guardrail worth stealing: *impacted-audience comms go out only after the change network has seen them*.
4. **Training** — strategy → curriculum → materials → delivery, worked **backward from go-live** so training lands ahead of it ("no one goes live cold"). Gate-based: Training Strategy locked → Curriculum locked → materials built → environment ready → delivery.
5. **Readiness & Adoption Measurement** — pulse surveys (including short pre-meeting pulses that steer agendas), readiness criteria per milestone, adoption metrics definition before go-live.
6. **Sustainment** — hypercare support model, reinforcement plan, knowledge transfer, and the handoff itself.

A small program may merge workstreams (e.g., Network into Comms); never merge away Measurement or Sustainment — those are the two that vanish when plans get squeezed.

## 30/60/90 phasing logic

Default phasing (adapt to the program's real beats — **don't force it**):

- **Days 1–30 — Mobilize & Assess.** Stand up the team and cadences, confirm the sponsor/sender architecture, baseline what exists (CIA/SHA/comms), identify the change network, lock guardrails and the approval gate.
- **Days 31–60 — Build & Engage.** Build the assets (training strategy/curriculum, comms series, network onboarding), run the first engagement cycle, first pulse, first leadership milestone moment.
- **Days 61–90 — Execute & Measure.** Run the rhythm at full tempo, measure (pulse, readiness criteria), course-correct, and prepare the roll-forward or handoff.

**Adapt when:** the program is mid-flight (skip "mobilize" — start at the current beat); go-live falls inside the window (back-load toward readiness/cut-over); a re-baseline happened (first phase is re-anchoring comms: *reinforce the new dates, never re-announce a slip*).

**Anchoring rule:** anchor everything to `meta.start_reference` and week numbers (Week 1–13). Use real calendar dates only when the program schedule confirms them. A plan built on invented dates is worse than one built on relative weeks — it looks authoritative and is wrong.

## Activity design rules

Every activity must carry three things or it doesn't go in the plan:

- **Owner** — one named person (or "TBD", visibly flagged — never a team name hiding no one).
- **Output** — the tangible thing produced (a sent email, a locked strategy doc, a completed session, survey results).
- **Done test** — how you'd verify it happened ("agenda sent + session held + notes filed", "48h review gate cleared and email sent"). If you can't write the done test, the activity is too vague — split or sharpen it.

Also: dependencies are explicit (`depends_on`); prep time is real (an activity that needs 2 days of prep starts 2 days earlier or names a prep sub-activity); recurring rhythm items are **cadences, not activities** (see below); and each high-severity CIA impact gets at least one activity carrying it in `linked_impacts`.

## Cadence & governance

Cadences are the standing rhythm — they live in their own register, not the activity list:

- **Weekly OCM standup** — the team's working session (status, blockers, next 2 weeks).
- **Biweekly sponsor touchpoint** — keep the sponsor active, tee up sponsor moments.
- **SteerCo / program governance** — OCM slot on the program's existing forum; don't invent a parallel one.
- **Change network touchpoint** — typically monthly, 30 min, preceded by a pre-meeting pulse.
- **Periodic plan refresh** — monthly: status pass + roll the window forward. A playbook nobody reopens is dead (see anti-patterns).

**Escalation path** — decisions must have a home. Define 2–4 levels: what the OCM lead decides alone → what goes to the sponsor → what goes to SteerCo, each with a trigger ("any comms slip > 1 week", "any change to public go-live dates") and a named decision authority.

## Handoff discipline

If the plan will transfer (consultant → client lead, lead → successor), build the handoff from day one. A clean OCM handoff doc contains:

1. **Why this version exists** — what changed since the last baseline and why.
2. **The anchor timeline** — the canonical schedule it's reconciled against, named by file.
3. **What changed vs. the prior version** — numbered, honest (including corrected mistakes).
4. **Open items needing the recipient's input** — explicit questions, not vague "TBDs".
5. **Resolved-this-version list** — decisions already made, so they aren't relitigated.
6. **What did NOT change** — carries forward, so the recipient doesn't re-verify everything.
7. **Backup coverage** — who acts when the owner is out; gates still apply.

## Anti-patterns

- **Activity theater** — long lists of "engage stakeholders"-grade items with no output or done test. Volume is not a plan.
- **Plans without owners** — "OCM team" as owner means nobody. One name per activity.
- **Playbooks nobody reopens** — no refresh cadence, so it's stale by week 3. Build the monthly refresh in as a cadence with an owner.
- **Fabricated precision** — invented calendar dates, invented approver names, invented training hours. Blank/TBD beats wrong.
- **Duplicating the comms plan** — re-listing every newsletter send as an activity. Reference the comms plan; carry vehicles as cadences.
- **Re-announcing slips** — after a re-baseline, comms restate the new timeline as settled; they don't apologize it back into the news.
- **Handoff as an afterthought** — a plan the author can run but nobody else can. The done test for the whole playbook: *could someone else pick it up cold?*
