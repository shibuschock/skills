#!/usr/bin/env python3
"""
validate_chain.py — schema + cross-skill consistency checks for the OCM suite.

Validates whichever files you pass; cross-checks alignment when two or more
are given:
  CIA roles_impacted  <->  SHA stakeholder_group
  comms audiences[].name  <->  SHA stakeholder_group
  comms coverage[].impact / impact_id  <->  CIA title / position

Usage:
  python validate_chain.py [--cia cia_records.json] [--sha sha_records.json]
                           [--comms comms_plan.json]

Exit code 0 = clean (warnings allowed), 1 = errors found.
Identical copies of this script ship in cia-builder, sha-builder, and
comms-toolkit (skills stay self-contained). Canonical source: cia-builder.
"""
import argparse, json, re, sys

DIMENSIONS = {"Role/Accountability", "Process/Policy", "Ways of Working",
              "Data/Decision Inputs", "Skills/Capability", "Mindset/Culture"}
SENTIMENTS = {"Positive", "Mixed", "Neutral", "Negative", "Cautious"}
PRIORITIES = {"Critical", "High", "Medium", "Low"}
SCOPES = {"In Scope", "Out of Scope - Adjacent", "Gap - Requirement Unconfirmed"}
FS_STATUS = {"Discussed-Confirmed", "Discussed-Pending", "Assumed"}

errors, warnings, match_warns = [], [], []


def err(msg):  errors.append(msg)
def warn(msg): warnings.append(msg)
def mwarn(msg): match_warns.append(msg)  # role/group name-mismatch warnings (summarized)


def load(path, label):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        err(f"{label}: cannot read {path}: {e}")
        return None


def split_roles(s):
    if isinstance(s, list):
        return [str(x).strip() for x in s if str(x).strip()]
    out = []
    for part in str(s or "").replace(";", ",").split(","):
        part = part.strip()
        if part:
            out.append(part)
    return out


def norm_name(s):
    """Normalize a role/group name for cross-file matching: lowercase, strip
    parenthetical qualifiers, strip ' - <location>' suffixes, singularize a
    trailing plural 's'."""
    s = str(s or "").lower().strip()
    s = re.sub(r"\(.*?(\)|$)", "", s)          # parenthetical qualifiers (incl. unclosed)
    s = re.sub(r"\s+-\s+.*$", "", s)           # " - <location>" suffix
    s = re.sub(r"\s+", " ", s).strip()
    if s.endswith("s") and not s.endswith("ss"):
        s = s[:-1]
    return s


def score_ok(v):
    try:
        return 1 <= int(v) <= 5
    except (TypeError, ValueError):
        return False


def check_cia(records):
    if not isinstance(records, list):
        err("CIA: cia_records.json must be a JSON array")
        return
    for i, r in enumerate(records, 1):
        tag = f"CIA #{i} ({r.get('title', '?')!r})"
        for f in ("title", "functional_area", "business_unit", "current_state",
                  "future_state", "process_change", "roles_impacted",
                  "dimensions", "primary_dimension"):
            if not r.get(f):
                err(f"{tag}: missing required field '{f}'")
        dims = r.get("dimensions") or []
        bad = [d for d in dims if d not in DIMENSIONS]
        if bad:
            err(f"{tag}: unknown dimension(s) {bad}")
        pd = r.get("primary_dimension")
        if pd and pd not in dims:
            err(f"{tag}: primary_dimension {pd!r} not in dimensions")
        for f in ("severity", "complexity"):
            if r.get(f) not in (None, "") and not score_ok(r[f]):
                err(f"{tag}: {f} must be 1-5, got {r[f]!r}")
        if r.get("priority") and r["priority"] not in PRIORITIES:
            err(f"{tag}: priority {r['priority']!r} not in {sorted(PRIORITIES)}")
        if r.get("sentiment") and r["sentiment"] not in SENTIMENTS:
            err(f"{tag}: sentiment {r['sentiment']!r} not in {sorted(SENTIMENTS)}")
        if r.get("scope") and r["scope"] not in SCOPES:
            err(f"{tag}: scope {r['scope']!r} not in {sorted(SCOPES)}")
        if r.get("future_state_status") and r["future_state_status"] not in FS_STATUS:
            err(f"{tag}: future_state_status {r['future_state_status']!r} invalid")
        for f in ("id", "severity_label", "impact_score"):
            if f in r:
                warn(f"{tag}: derived field '{f}' supplied — the renderer computes it")


def check_sha(records):
    if not isinstance(records, list):
        err("SHA: sha_records.json must be a JSON array")
        return
    seen = set()
    for i, r in enumerate(records, 1):
        tag = f"SHA #{i} ({r.get('stakeholder_group', '?')!r})"
        for f in ("stakeholder_group", "business_unit", "group_description"):
            if not r.get(f):
                err(f"{tag}: missing required field '{f}'")
        # influence/interest may be absent only for identified-but-unassessed
        # groups, which must carry assessment_status (e.g. "Not yet assessed")
        for f in ("influence", "interest"):
            if not r.get(f) and not r.get("assessment_status"):
                err(f"{tag}: missing '{f}' (score it, or set assessment_status "
                    f"to e.g. 'Not yet assessed')")
        name = r.get("stakeholder_group", "")
        if "," in name:
            err(f"{tag}: stakeholder_group contains a comma (breaks role matching)")
        if name in seen:
            err(f"{tag}: duplicate stakeholder_group")
        seen.add(name)
        for f in ("influence", "interest"):
            if r.get(f) is not None and not score_ok(r[f]):
                err(f"{tag}: {f} must be 1-5, got {r[f]!r}")
        if r.get("current_sentiment") and r["current_sentiment"] not in SENTIMENTS:
            err(f"{tag}: current_sentiment {r['current_sentiment']!r} invalid")


def check_comms(plan):
    if not isinstance(plan, dict):
        err("Comms: comms_plan.json must be a JSON object")
        return
    aud_ids, aud_names = set(), set()
    for a in plan.get("audiences", []):
        aud_ids.add(str(a.get("id", "")))
        aud_names.add(a.get("name", ""))
        if not a.get("name"):
            err("Comms: audience missing 'name'")
    chan_names = {c.get("name", "") for c in plan.get("channels", [])}
    for i, act in enumerate(plan.get("activities", []), 1):
        tag = f"Comms activity #{i} ({act.get('title', '?')!r})"
        a = str(act.get("audience", ""))
        if a and a not in aud_ids and a not in aud_names:
            err(f"{tag}: audience {a!r} not in audiences")
        ch = act.get("channel", "")
        if ch and ch not in chan_names:
            err(f"{tag}: channel {ch!r} not in channels")
    for i, cov in enumerate(plan.get("coverage", []), 1):
        a = str(cov.get("audience", ""))
        if a and a not in aud_ids and a not in aud_names:
            err(f"Comms coverage #{i}: audience {a!r} not in audiences")
        if not cov.get("impact") and not cov.get("impact_id"):
            err(f"Comms coverage #{i}: needs 'impact' or 'impact_id'")


def cross_cia_sha(cia, sha):
    groups = {r.get("stakeholder_group", "") for r in sha}
    groups_norm = {norm_name(g) for g in groups}
    unmatched = {}
    for r in cia:
        for role in split_roles(r.get("roles_impacted")):
            if norm_name(role) not in groups_norm:
                unmatched.setdefault(role, 0)
                unmatched[role] += 1
    for role, n in sorted(unmatched.items(), key=lambda kv: -kv[1]):
        mwarn(f"Chain: CIA role {role!r} ({n} impact(s)) has no SHA stakeholder_group")
    used = {norm_name(role) for r in cia for role in split_roles(r.get("roles_impacted"))}
    for g in sorted(groups):
        if norm_name(g) not in used:
            mwarn(f"Chain: SHA group {g!r} appears in no CIA roles_impacted")


def cross_comms_sha(plan, sha):
    groups = {norm_name(r.get("stakeholder_group", "")) for r in sha}
    for a in plan.get("audiences", []):
        name = a.get("name", "")
        if name and norm_name(name) not in groups:
            mwarn(f"Chain: comms audience {name!r} does not match a SHA stakeholder_group "
                  f"(fine for synthetic segments like 'Org-wide')")


def cross_comms_cia(plan, cia):
    titles = {r.get("title", "").lower(): i for i, r in enumerate(cia, 1)}
    covered = set()
    for i, cov in enumerate(plan.get("coverage", []), 1):
        imp, iid = cov.get("impact"), cov.get("impact_id")
        if iid is not None:
            try:
                iid = int(iid)
            except (TypeError, ValueError):
                err(f"Comms coverage #{i}: impact_id {iid!r} is not an integer")
                continue
            if not (1 <= iid <= len(cia)):
                err(f"Comms coverage #{i}: impact_id {iid} out of range (CIA has {len(cia)})")
            else:
                covered.add(iid)
        elif imp:
            hit = titles.get(str(imp).lower())
            if hit is None:
                err(f"Comms coverage #{i}: impact {imp!r} matches no CIA title")
            else:
                covered.add(hit)
    missing = [r.get("title") for i, r in enumerate(cia, 1) if i not in covered]
    if plan.get("coverage") and missing:
        warn(f"Chain: {len(missing)} CIA impact(s) absent from comms coverage: "
             + "; ".join(missing[:5]) + ("…" if len(missing) > 5 else ""))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cia")
    p.add_argument("--sha")
    p.add_argument("--comms")
    a = p.parse_args()
    if not (a.cia or a.sha or a.comms):
        p.error("pass at least one of --cia / --sha / --comms")

    cia = load(a.cia, "CIA") if a.cia else None
    sha = load(a.sha, "SHA") if a.sha else None
    comms = load(a.comms, "Comms") if a.comms else None

    if isinstance(cia, list):   check_cia(cia)
    if isinstance(sha, list):   check_sha(sha)
    if isinstance(comms, dict): check_comms(comms)
    if isinstance(cia, list) and isinstance(sha, list):   cross_cia_sha(cia, sha)
    if isinstance(comms, dict) and isinstance(sha, list): cross_comms_sha(comms, sha)
    if isinstance(comms, dict) and isinstance(cia, list): cross_comms_cia(comms, cia)

    for w in warnings:
        print(f"WARN  {w}")
    shown = match_warns if len(match_warns) <= 10 else match_warns[:10]
    for w in shown:
        print(f"WARN  {w}")
    if len(match_warns) > 10:
        print(f"WARN  Chain: ...and {len(match_warns) - 10} more role/group mismatch "
              f"warning(s) ({len(match_warns)} total). Mostly vocabulary drift - "
              f"consider aliases or a rollup; see SKILL.md notes on keeping "
              f"CIA/SHA/comms names aligned.")
    n_warn = len(warnings) + len(match_warns)
    print(f"\n{len(errors)} error(s), {n_warn} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
