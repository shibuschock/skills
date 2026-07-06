---
name: training-content-builder
description: Develop training materials for a single curriculum module, for ANY project or change program — turning one module from curriculum.json into ready-to-use deliverables: a facilitator guide, participant guide/workbook, job aid / quick-reference, slide outline, in-app guidance script, and assessment items, all aligned to the module's learning objectives and written in the project's tone (plain, learner-friendly language). Step 3 of the training suite (Develop). Use when the user asks to write/build/draft training content, a facilitator or leader guide, participant materials, a job aid, quick reference, e-learning storyboard, or assessment questions for a training module.
---

# Training Content Builder

Build the actual **training materials** for one module — aligned to its objectives, in the project's voice. Step 3 (Develop) of the training suite. Run once per module.

## Read first
- `../_training-shared/project-context.example.json` — copy it per project, swap the values, and read the project's copy (tone, audiences, brand, modalities). **If no per-project copy exists, create one** from the example, filling it from the conversation and any upstream artifacts (`project.json`, the CIA). Note: `project.json` (the suite's renderer config; brand slots literally named `navy`/`magenta` = primary/accent) is a different file with a different job — it does not carry tone/audiences.
- `../_training-shared/references/LEARNING-METHODOLOGY.md` — §4 (Bloom's verbs), §5 (modalities), §6 (andragogy).
- `references/CONTENT_TEMPLATES.md` — the deliverable templates.

## Input
- **One module object** from `curriculum.json` (preferred): its `learning_objectives`, `audience`, `modality_blend`, `assessment`, `content_outline`, and any `non_training_gates`. If absent, ask for the module's objectives + audience + duration.
- **`cia_records.json`** (when the engagement has one) — the impacts' `change_considerations` (resistance history, union positions, workaround culture) feed the facilitator guide's "common questions & pushback" and make distractors/talk tracks real. Read the module's `maps_to_impacts` records at minimum.

## Workflow
1. **Pick the module + confirm scope.** Which module, and which deliverables does the user want? (Default set below — ask before generating all of them. **If running unattended/batch with nobody to ask, produce the full default set and note that in the output.**)
2. **Anchor on the objectives.** Every piece of content must serve a stated learning objective. If content doesn't map to an objective, cut it (or flag a missing objective back to the curriculum).
3. **Write to the audience + modality.** Frontline = short, visual, point-of-need, plain language. Leads/support and office/professional roles = more depth, exceptions, judgment. Match the module's `modality_blend`.
4. **Generate the requested deliverables** from the templates:
   - **Facilitator guide** — timing, talk track, demo steps, practice activities, discussion prompts, answer keys.
   - **Participant guide / workbook** — what the learner keeps; steps, screenshots placeholders, practice space, key reminders.
   - **Job aid / quick reference** — one-page, point-of-need, the steps only.
   - **Slide outline** — section-by-section, one idea per slide, speaker notes (not full slide build — that's a deck tool).
   - **In-app guidance script** — step prompts/tooltips for the digital adoption overlay.
   - **Assessment items** — questions/tasks that measure the objectives at the right Bloom level, with answer key + mastery threshold.
5. **Flag placeholders.** Screenshots, exact field names, system specifics → mark `[SCREENSHOT: …]` / `[CONFIRM: …]`. Design decisions not yet made (hardware choice, pending policy) → mark `[PENDING-DECISION: …]` — content gated on a decision, not an SME-confirmable fact. Never invent system screen details as fact.
6. **Apply tone + QA.** American English, plain language, the project's voice. Consider running the `stop-slop` skill on the prose. Confirm every deliverable covers all objectives and nothing extra.

## Output
- One file per deliverable under `modules/<module-id>/` (e.g. `facilitator-guide.md`, `participant-guide.md`, `job-aid.md`, `slides-outline.md`, `assessment.md`). Markdown, ready to format in the client's template.
- **Where `modules/` lives:** under the outdir the user agreed for the engagement (the same working folder as `curriculum.json` unless told otherwise) — confirm it once, then keep all modules under it so steps 3–4 of the suite can find them.
- **`modules/<module-id>/README.md`** — the module's open-items register: every `[SCREENSHOT:]` / `[CONFIRM:]` / `[PENDING-DECISION:]` tag, plus any `non_training_gates` ("do not deliver until…") carried from the curriculum.

## Notes
- Don't fabricate system specifics (screens, field names, button labels) — placeholder them for SME confirmation.
- For polished prose, hand off to `stop-slop` / `humanizer`; for the actual slide deck, hand off to a deck tool. This skill produces the *content*, structured and on-objective.
- Composable: standalone (give it objectives) or chained (module from curriculum.json).
