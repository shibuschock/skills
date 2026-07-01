#!/usr/bin/env python3
"""
sha_merge.py — merge a batch of newly-extracted SHA records into an existing
dataset (dedup + enrich, never silently overwrite). Stdlib only.

Usage:
  python3 sha_merge.py --base sha_records.json --incoming new_records.json \
                       --out sha_records.json [--report merge_report.md] [--threshold 0.90]

Matching: an incoming record matches an existing one when they share the same
business_unit (case-insensitive) AND their stakeholder_group names are
near-identical (SequenceMatcher ratio >= threshold). On a match the existing row
is *enriched* — blank fields get filled — but populated fields are left untouched.
Unmatched incoming records are appended as new. Nothing is deleted.
"""
import argparse, difflib, json, re

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", str(s or "").lower())).strip()

def is_blank(v):
    return v is None or v == "" or v == [] or v == {}

def gname(r):
    return r.get("stakeholder_group") or r.get("group") or r.get("role")

def find_match(rec, base, threshold):
    bu = norm(rec.get("business_unit") or rec.get("bu"))
    name = norm(gname(rec))
    best, best_r = None, 0.0
    for b in base:
        if norm(b.get("business_unit") or b.get("bu")) != bu:
            continue
        r = difflib.SequenceMatcher(None, name, norm(gname(b))).ratio()
        if r > best_r:
            best, best_r = b, r
    return (best, best_r) if best_r >= threshold else (None, best_r)

def enrich(target, incoming):
    """Fill blanks only. Return list of changed field names."""
    changed = []
    for k, v in incoming.items():
        if is_blank(v):
            continue
        if is_blank(target.get(k)):
            target[k] = v; changed.append(k)
    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--incoming", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report")
    ap.add_argument("--threshold", type=float, default=0.90)
    a = ap.parse_args()

    base = json.load(open(a.base, encoding="utf-8"))
    incoming = json.load(open(a.incoming, encoding="utf-8"))
    added, enriched, dup = [], [], []

    for rec in incoming:
        match, ratio = find_match(rec, base, a.threshold)
        if match is None:
            base.append(rec); added.append(gname(rec) or "(unnamed)")
        else:
            ch = enrich(match, rec)
            (enriched if ch else dup).append((gname(rec) or "(unnamed)", ch))

    json.dump(base, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    summary = f"{len(added)} new, {len(enriched)} enriched, {len(dup)} duplicate (skipped); total now {len(base)}"
    print(summary)
    if a.report:
        lines = ["# SHA merge report", "", f"- {summary}", "",
                 f"**Base:** `{a.base}`  **Incoming:** `{a.incoming}`  **Out:** `{a.out}`  **Threshold:** {a.threshold}", ""]
        if added:
            lines += ["## New (appended)", ""] + [f"- {t}" for t in added] + [""]
        if enriched:
            lines += ["## Enriched (blank fields filled)", ""] + [f"- {t} — filled: {', '.join(ch)}" for t, ch in enriched] + [""]
        if dup:
            lines += ["## Duplicate (no change)", ""] + [f"- {t}" for t, _ in dup] + [""]
        open(a.report, "w", encoding="utf-8").write("\n".join(lines))
        print(f"report -> {a.report}")

if __name__ == "__main__":
    main()
