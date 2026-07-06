# Persona & journey methodology (portable OCM)

## Why rationalize

Two failure modes dominate persona work on change programs:

1. **One persona per job title.** OCM segments by *who lives the same change and needs the same treatment*, not by org chart. If two roles receive the same comms, the same training, and face the same system shift, they are **one persona with sub-variants** — not two. A store manager and a store associate facing the same new POS are one persona and two *training sub-audiences*.
2. **Persona count beyond operable span.** Fifteen personas means fifteen comms variants, fifteen training paths, fifteen readiness scorecards. Programs act on roughly **4–8 segments** because the change network, sponsor roadshows, and training waves have to be *operated*, not just authored. A wide flat list collapses into a few buckets in practice anyway — define the buckets deliberately.

A persona is a **design tool**; a segment is an **operating unit**. Rich role-level detail earns its keep in training design and day-in-the-life work — the cost shows up only when the same wide list is used to run comms, sponsorship, and engagement. The answer is neither "keep them all flat" nor "collapse and lose the detail." It is **tiered, and differentiated by purpose**.

## The tiered model

| Tier | What it gets | Who qualifies |
|---|---|---|
| **1 — Deep persona** | Full profile + current→future journey map + before/after day-in-the-life narrative | The most-impacted archetypes: high change intensity AND (large population OR pivotal to adoption) |
| **2 — Lightweight profile** | Profile card only (archetype, roles covered, goals, pain points, top impacts) — no journey/DITL | Materially impacted but the change experience is simpler, or evidence is thinner |
| **3 — Reference-only** | A row in the register: name, roles covered, one-line archetype | Peripherally impacted roles that must not be dropped from the crosswalk but need no dedicated treatment |

Typical shape: 2–3 Tier 1, 2–3 Tier 2, the rest Tier 3. Every source role lands in exactly one persona's `roles_covered` — nothing dropped, nothing double-counted. If a role genuinely straddles two personas, assign it to its **primary** persona and note the secondary in the archetype description.

## Rationalization criteria

Cluster roles into a persona when they share a **distinct core change experience** (usually a distinct core system/process shift). Then tier each persona on:

1. **Change intensity** — derived from the CIA: the severity × complexity of the impacts touching the persona's roles. High intensity = multiple severity ≥ 4 impacts or a fundamental ways-of-working shift. Record as High / Medium / Low in `change_intensity`.
2. **Population size** — headcount covered (`population_estimate`). A high-volume, high-churn frontline population is a training-at-scale priority even when each individual change is moderate.
3. **Distinctiveness of change experience** — does this group's journey differ enough from every other persona's to justify separate treatment? If the journey would read the same as another persona's, merge them.

Guard against **false precision**: splitting thin evidence into distinct archetypes asserts differentiation the data doesn't support. Low-confidence profiles stay at Tier 2/3 until validated.

## Journey-map anatomy

A journey is 4–7 **stages** — the chronological arc of the persona's core workflow through the change (e.g., Plan → Order → Receive → Count → Reconcile). Per stage:

- **stage** — short label.
- **current** — the pain / friction today. Must trace to a CIA `current_state` or a sourced quote — not invented.
- **future** — the future-state moment. Must trace to a CIA `future_state`. Where the future state is assumed rather than confirmed, say so.
- **emotion_current / emotion_future** — one word each (e.g., Frustrated → Confident). Together across stages these form the **emotion curve**; expect a dip mid-journey (go-live disruption) before the payoff — a curve that only goes up is a credibility flag.
- **support** — the change-support cue for that moment: the specific training, job aid, comms, or coaching intervention that catches the persona there. This is what makes the journey actionable rather than decorative.

## Day-in-the-life rules (Tier 1 only)

- **Concrete and time-anchored.** Hour-by-hour blocks over a realistic workday ("06:30 — walks the floor with the printed par sheet"), not abstractions.
- **Before/after paired.** Each narrative is two columns of the same day — today vs. future — so the reader can see exactly which hours change and which don't. Most of a workday does NOT change; showing the unchanged parts is what makes it believable.
- **Sourced.** Timeline blocks come from transcripts, interviews, or shadowing — where you have not validated time allocation, label the narrative as pending validation rather than presenting it as observed.

## Traps

- **Persona bloat** — one persona per role/title. Cluster by change experience.
- **Demographic fluff** — age, hobbies, stock photos, invented family details. In OCM contexts a persona is defined by what changes in their work, not who they are at home. Include tenure/context only when it drives a change decision (e.g., high churn → training-at-scale).
- **Marketing-style personas** — aspiration and brand-affinity framing. OCM personas exist to target comms, training, and support; every field should feed one of those.
- **Invented backstory to fill thin profiles** — a named character needs a sourced verbatim quote or none at all; label inferred parts as inferred.
- **The single-individual misread** — state explicitly that each persona represents an archetype (many people), not one literal employee, so decisions aren't read as being about a person.
- **Journeys with no support cues** — a journey map without the change-support column is a poster, not a plan.
