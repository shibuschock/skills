# Creative format design patterns

The pedagogy behind each interactive format. Read before authoring a `learning_object.json`. This is the creative core — the schema/script just render what you design here.

---

## Gamified quiz

A knowledge check that engages, not just tests. Game elements serve learning — don't bolt them on.

**Design principles**
- **Meaningful feedback over points.** The teaching moment is the feedback after each answer — explain *why*. Points/badges are motivation, not the lesson.
- **Apply-level stems.** "A guest wants a refund but has no receipt — what do you do?" beats "Which button issues a refund?" Match the module's Bloom level.
- **Plausible distractors.** Wrong options should reflect real mistakes people make (pull from the CIA `change_considerations` / known friction).
- **Instant feedback.** Reveal right/wrong immediately, with the rationale. The renderer locks the answer and shows it.
- **Pass threshold = mastery gate.** Set `pass_threshold` to the real bar (e.g. 0.8). The pass badge ("Go-Live Ready") signals readiness; retry is always available.
- **Short.** 5–10 items for frontline. Long quizzes kill engagement.

**Light gamification that works:** progress bar, running score, a pass badge, retry-to-improve. **Avoid:** punitive scoring, time pressure on safety-critical tasks, leaderboards that shame low performers.

---

## Microlearning / flashcards

Bite-sized retrieval practice — ideal for high-turnover frontline who can't sit in long courses.

**Design principles**
- **One idea per card.** Front = a prompt/cue; back = the answer. If the back needs paragraphs, it's not a flashcard — make it a job aid.
- **Retrieval, not recognition.** Front should make the learner *recall* ("Steps to void a transaction?"), then flip to check — not "Here are the steps" with nothing to retrieve.
- **Spaced repetition.** The renderer surfaces "needs review" cards first on return visits (Leitner-lite, stored in the browser). Encourage repeat short sessions over one long cram.
- **Chunk to ~7–12 cards** per deck. Split bigger topics into multiple decks.
- **Pair with the real task.** Microlearning reinforces; it doesn't replace first-time hands-on practice (the 70% — see methodology §2).

**Good uses:** terminology, key steps, do/don't rules, policy thresholds, "what to say when…". **Poor uses:** first-time complex procedures (use ILT/in-app guidance), anything needing deep explanation.

---

## When to reach past these two formats

| Need | Better fit |
|---|---|
| Judgment / "what would you do" with consequences | Branching scenario (future addition to this skill) |
| Point-of-need steps while working | Job aid / in-app guidance → `training-content-builder` |
| Polished graphics / infographic | Canva MCP |
| Explainer / demo video | `remotion-best-practices` / `video-use` skills |
| Tracked completion in a client LMS | Render here with `--scorm` |

Pick the lightest format that meets the objective. Interactivity is a means to learning, not a goal — don't gamify what a 30-second job aid would solve.
