# SCORM option — what it is and when to use it

**SCORM** is the standard packaging format most corporate LMSs accept (SuccessFactors, Cornerstone, Docebo, Moodle, etc.). A SCORM package is just a zip containing your HTML plus a manifest the LMS reads; the HTML talks back to the LMS to record **completion status** and **score**.

## What this skill produces
- **Always:** a self-contained `<id>.html`. The same file silently reports to an LMS *if* it's launched inside one — so you don't keep two versions.
- **With `--scorm`:** additionally `<id>_scorm.zip` (SCORM **1.2** — the most widely supported version), containing `index.html` + `imsmanifest.xml`. Upload that zip to the LMS.

## What gets tracked (SCORM 1.2)
- **Quiz:** `lesson_status` = `passed` / `failed` (vs the `pass_threshold`), plus `score.raw` (number correct), `score.max`.
- **Flashcards:** `lesson_status` = `completed` when the deck is finished; `score.raw` = cards mastered. *Mastered* = rated "Got it" **twice** (across visits — spaced repetition), so a first-pass perfect review reports score 0 with status `completed`. Warn the LMS owner, or use the quiz format for scored tracking.

## When to use it
- **Use `--scorm`** only when the client needs completion/scores recorded in their LMS (compliance, audit, reporting).
- **Skip it** for everything else — the plain HTML on a Drive link is simpler, opens instantly, and works offline. Most reinforcement/microlearning doesn't need LMS tracking.

## Notes & limits
- SCORM 1.2 only (no SCORM 2004 sequencing, no xAPI/cmi5). That covers the large majority of LMS upload needs; if a client specifically requires xAPI, that's a future addition.
- Test the zip in the target LMS before rollout — LMSs vary in strictness. The plain HTML can always be QA'd in a browser first.
- The HTML has zero runtime dependencies, so the SCORM package is self-contained too.
