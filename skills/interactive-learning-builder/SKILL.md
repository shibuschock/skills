---
name: interactive-learning-builder
description: Build creative, interactive learning objects for ANY project or change program — gamified quizzes (scored, instant feedback, branching, pass badge) and microlearning flashcard decks (flip cards, spaced-repetition-lite) — rendered as self-contained interactive HTML that opens from any browser/Drive link AND reports completion+score to an LMS when run inside one. Optional --scorm flag packages the same HTML as a SCORM 1.2 zip for LMS upload with tracking. The interactive twin of training-content-builder: reads the same module objectives/assessment from curriculum.json and slots into the training suite. Use when the user asks for gamification, a quiz/knowledge check, microlearning, flashcards, an interactive or engaging training activity, an e-learning object, or a SCORM package.
---

# Interactive Learning Builder

Turn a module's objectives into **engaging, interactive learning objects** — not documents. Self-contained HTML (zero dependencies, opens anywhere), with an optional SCORM wrapper for LMS tracking. The creative/interactive twin of `training-content-builder` within the training suite.

## Read first
- `../_training-shared/project-context.example.json` — copy it per project, swap the values, and read the project's copy (brand colors/font/footer, audiences, tone). **If no per-project copy exists, create one** from the example, filling it from the conversation and any upstream artifacts. Note: this is a different file from the suite's `project.json` renderer config (brand keys `navy`/`magenta` = primary/accent) — this skill's `--context` flag takes the context file, whose brand keys are `primary`/`accent`.
- `../_training-shared/references/LEARNING-METHODOLOGY.md` — §4 (Bloom's), §5 (microlearning), §6 (andragogy).
- `references/FORMATS.md` — design patterns for each format (this is the creative core — read it).
- `references/OBJECT_SCHEMA.md` — the `learning_object.json` spec shape.
- `references/SCORM.md` — what the SCORM option does + LMS notes.

## Input
- **One module** from `curriculum.json` (preferred): its `learning_objectives`, `assessment`, `audience`. Or the user describes the activity directly.

## Workflow
1. **Pick format + scope.** Gamified quiz, flashcard deck, or both. Confirm which module/objectives it covers.
2. **Design with the methodology.** Write items that measure objectives at the right Bloom level (Apply for most hands-on system tasks). Apply the `FORMATS.md` patterns — meaningful feedback (not just right/wrong), microlearning chunking, retrieval practice. Keep learner language plain and short.
3. **Author the spec.** Produce a `learning_object.json` per `OBJECT_SCHEMA.md` (you write the JSON; the script renders it). Don't fabricate system specifics — placeholder `[CONFIRM: …]` in question/answer text.
4. **Render** (Windows: `python`; else `python3`):
   ```
   python scripts/render_object.py --spec learning_object.json --context <project-context>.json --outdir OUT
   ```
   `--context` MUST point at the **project's own copy** of the context file — never at `../_training-shared/project-context.example.json`, or the object ships with "Acme ERP" branding and the Acme footer on client content. Add `--scorm` to also produce an LMS-ready SCORM 1.2 zip:
   ```
   python scripts/render_object.py --spec learning_object.json --context <project-context>.json --outdir OUT --scorm
   ```
   Output: `OUT/<id>.html` (always), `OUT/<id>_scorm.zip` (with `--scorm`).
5. **QA via live render (required).** Open the HTML in a browser (or headless screenshot). Confirm: questions/cards work, feedback shows, score/badge appears, flashcards flip and the progress/mastery counter moves, branding applied, mobile layout holds. Spot-check answers against the objectives.

## Output
- `<id>.html` — self-contained interactive learning object (share via Drive link).
- `<id>_scorm.zip` — optional SCORM 1.2 package for LMS upload (same content + completion/score tracking).

## Notes
- The HTML is dependency-free and works offline; the same file silently reports to an LMS when launched inside one, so you don't maintain two versions.
- **Flashcard SCORM scoring:** a card counts as *mastered* only after TWO "Got it" ratings (across visits — Leitner-lite spaced repetition), and `score.raw` = cards mastered. So a first-pass perfect review reports **score 0** with status `completed` — that is by design, not a failure. Either explain this to the LMS owner up front, or use the quiz format when the client needs scored tracking.
- The renderer consumes only `project_name` and `brand` (`primary`, `accent`, `font`, `footer`) from the context file — other fields inform authoring, not rendering.
- Don't invent system screen/field details — placeholder for SME confirmation. Specs containing `[CONFIRM:` or `[PENDING` tags render with a visible "DRAFT — contains unconfirmed items" banner so drafts can't ship to learners unnoticed.
- Composable: standalone (describe the activity) or chained (module from `curriculum.json`). For document deliverables (guides, job aids) use `training-content-builder`; for prose polish use `stop-slop`.
