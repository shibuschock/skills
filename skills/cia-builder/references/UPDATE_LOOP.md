# Incremental update loop — refresh a CIA from new transcripts

The CIA is a living dataset, not a one-shot build. When new workshops/interviews land,
**don't rebuild from scratch** — extract only what's new and merge it in. Keep
`cia_records.json` as the canonical dataset between runs (store it next to the outputs).

## Steps

1. **Identify what's new.** Keep a short "processed transcripts" note (a list at the top of
   `cia_records.json` is fine, or a sidecar file). Compare it to the transcripts/folders the
   user points you at; anything not on the list is unprocessed. **Present the list and confirm
   before extracting.**

2. **Extract only the new records.** For each new transcript, produce CIA records against
   `references/CIA_SCHEMA.md` into `new_records.json`. Same rules as a fresh build (6 dimensions,
   one Primary, score only what was scored, populate optional fields only where supported).
   For 3+ transcripts, dispatch one subagent per transcript (Agent tool), each given the
   schema, the heuristics, and the existing impact titles+areas for dedup awareness; merge their
   JSON chunks.

3. **Merge — dedup + enrich, never overwrite.**
   ```
   python3 scripts/cia_merge.py --base cia_records.json --incoming new_records.json \
                                --out cia_records.json --report merge_report.md
   ```
   - **Duplicate** (same area + near-identical title) → skipped.
   - **Enrich** (same impact, the new transcript adds detail) → blank fields filled; list fields
     (`value_levers`, `training_modality`, `dimensions`) unioned; already-populated fields left alone.
   - **New** → appended.
   Read `merge_report.md` and sanity-check the dispositions. Tune `--threshold` (default 0.88) if
   distinct impacts are colliding or near-duplicates aren't matching.

4. **Re-render and report.**
   ```
   python3 scripts/cia_render.py cia    --records cia_records.json --config project.json --outdir OUT
   python3 scripts/cia_render.py readme --config project.json --outdir OUT
   ```
   Update the processed-transcripts note. Report: total impacts old → new (+N new, M enriched,
   K skipped), transcripts processed, outputs regenerated.

## Notes
- The merge is title+area based and conservative by design. If two genuinely different impacts
  share a title, rename one before merging. If an impact should be *replaced* rather than enriched,
  edit `cia_records.json` directly — the merge never deletes.
