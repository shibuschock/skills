# Readout Methodology

Portable OCM method for the executive readout package. Three parts: how intensity is derived (script's job), how themes are constructed (Claude's job), and how talking points are written (Claude's job).

## 1. Change-intensity derivation (script-computed — never hand-scored)

Aggregation unit: the **functional area** (falls back to `l1_process` when `functional_area` is blank). Per area:

- **Volume** = the impact count (all in-scope impacts mapped to the area).
- **Depth** = the mean **impact score** (severity × complexity, 1–25) over the area's *scored* impacts. Unscored impacts count toward volume, not depth — never invent scores.
- **Total change load** (the intensity index) = the **sum** of impact scores across the area — one number that reflects both how many things change and how hard each one is. This drives the ranking and the heat coloring.

Depth bands (per-impact-average thresholds, matching the CIA's severity ramp):

| Band | Mean score |
|---|---|
| Critical | 20+ |
| High | 12–19 |
| Medium | 5–11 |
| Low | under 5 |

Heat coloring on the ranked table uses **quartiles of total load** across areas (Most change / High / Moderate / Light), so the palette always differentiates regardless of the project's absolute scores.

**Zero-impact caution:** an area with no impacts is *not* automatically "no change" — it may be covered elsewhere, deferred, out of scope, or a genuine extraction gap. Say why it's empty; never let a blank read as "safe."

### Volume × Depth quadrant matrix

Plot each area: X = volume, Y = depth (mean score). Splits: X at the **median volume** across areas; Y at **12** (the High threshold). Quadrant labels and the strategy they imply:

- **Broad & Deep — priority focus** (high volume, high depth): flagship OCM investment — sponsorship, dedicated coaching, sequenced training.
- **Narrow & Deep** (low volume, high depth): surgical plays — role redesign, targeted coaching for the few roles hit hard.
- **Broad & Shallow** (high volume, low depth): scale plays — mass comms, self-serve training, standard job aids.
- **Watch** (low volume, low depth): light touch; monitor for drift.

## 2. Theme construction (Claude-authored)

- **Cluster by story, not org chart.** A theme is a narrative an executive can retell ("planning becomes a formal discipline"), not a department. One theme may span areas; one area may feed two themes.
- **4–7 themes.** Fewer than 4 means you're summarizing, not clustering; more than 7 means the audience can't hold them.
- **Each theme carries three things:** *what's changing* (the current→future shift at theme level), *who feels it* (the roles, from the records), and *the so-what* (why leadership should care / what could stall).
- **Traceability is non-negotiable.** Every theme lists the impact ids (or exact titles) behind it. Every sentence in the theme must be supportable by those records. Unclustered high-severity impacts are a defect — either widen a theme or add one.
- Lead with the deepest change, not the biggest system. Sentiment patterns (negative/cautious clusters) are theme material.

## 3. Talking-points register (Claude-authored)

The crib sheet is what a leader **says**, not slide prose:

- **Spoken, not written.** Read each sentence aloud — if it can't be said in one breath, split or cut it.
- **No jargon, no system names as heroes.** "The team stops re-keying orders," not "the solution leverages integrated order orchestration."
- **Two beats per theme:** *what's changing* (the plain-language takeaway) then *so what* (the consequence, the risk of inaction, or the ask). The so-what is the part leaders actually need — never skip it.
- **Explain the why — don't read the slide.** The script complements the visual, it doesn't duplicate it.
- Concrete over abstract: name the roles, the habit that ends, the habit that starts.
- **The spoken register applies to `whats_changing` too** — one plain sentence per idea, not slide prose. If it reads like a bullet on a deck, rewrite it as something a leader would say.
- **Naming real sponsors or leaders in scripts is fine when they're on the record** — i.e., named in the source materials or decisions. Don't invent or guess names.

## 4. Readout composition

Order the readout: **open with the intensity picture** (where the change concentrates — the map earns the room's attention), then **walk the themes** (who/what/how boards, deepest first), then **close with the asks** (decisions, sponsorship moves, resources). The exec summary at the top states the single headline the audience should leave with.
