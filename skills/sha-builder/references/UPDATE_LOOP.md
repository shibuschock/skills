# Incremental update loop — refresh an SHA from new interviews

The SHA is a living dataset. When new interviews/workshops land, **don't rebuild from scratch** —
extract only what's new and merge it in. Keep `sha_records.json` as the canonical dataset between
runs (store it next to the outputs).

## Steps

1. **Identify what's new.** Keep a short "processed sources" note. Compare it to the transcripts/notes
   the user points you at; anything not on the list is unprocessed. **Present the list and confirm
   before extracting.**

2. **Extract only the new records.** For each new source, produce SHA records against
   `references/SHA_SCHEMA.md` into `new_records.json`. Same rules as a fresh build (Influence/Interest
   1–5 from evidence; populate optional fields only where supported).

3. **Merge — dedup + enrich, never overwrite.**
   ```
   python3 scripts/sha_merge.py --base sha_records.json --incoming new_records.json \
                                --out sha_records.json --report merge_report.md
   ```
   - **Duplicate** (same BU + near-identical stakeholder-group name) → skipped.
   - **Enrich** (same group, the new source adds detail) → blank fields filled; populated fields left alone.
   - **New** → appended.
   Read `merge_report.md` and sanity-check. Tune `--threshold` (default 0.90) if distinct groups are
   colliding or near-duplicates aren't matching.

4. **Re-render and report.**
   ```
   python3 scripts/sha_render.py sha    --records sha_records.json --config project.json --outdir OUT
   python3 scripts/sha_render.py readme --config project.json --outdir OUT
   ```
   Update the processed-sources note. Report: total groups old → new (+N new, M enriched, K skipped).

## Notes
- Stakeholder records are few enough that hand-editing `sha_records.json` and re-running is also fine.
- The merge never deletes. To *replace* a record rather than enrich it, edit `sha_records.json` directly.
