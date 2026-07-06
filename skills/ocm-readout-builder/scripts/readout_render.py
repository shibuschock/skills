#!/usr/bin/env python3
"""
ocm-readout-builder — render an executive readout package for ANY project from
CIA records + a Claude-authored readout.json.

Outputs (self-contained, zero runtime dependencies):
  <Project> Change Intensity Map.html   ranked heat table + Volume x Depth
                                        quadrant matrix + per-area impact drill
  <Project> Executive Readout.html      exec summary, intensity snapshot, one
                                        WHO/WHAT/HOW board + spoken script per theme
  <Project> Talking Points.md           the crib sheet (markdown, docx-ready)

Method (see references/METHODOLOGY.md): per functional area, volume = impact
count, depth = mean severity x complexity over scored impacts, total change
load = sum of scores. Intensity is DERIVED from the CIA — never hand-scored.
Theme prose comes from readout.json (Claude-authored, traceable to impacts).

Usage:
  python3 readout_render.py --cia cia_records.json --readout readout.json \
      --config project.json [--sha sha_records.json] --outdir OUT [--force]

Only stdlib. Cross-platform.
"""
import argparse, datetime, html, json, os, re, sys

DEFAULT_BRAND = {"navy": "#162B75", "magenta": "#EE2C81", "orange": "#F08301",
                 "teal": "#04A577", "coral": "#FF533C",
                 "font": "Calibri, system-ui, sans-serif", "footer": "Confidential"}
# depth bands over the per-impact mean score (severity x complexity, 1-25)
BANDS = [(20, "Critical", "#9E2B25"), (12, "High", "#CC6A33"),
         (5, "Medium", "#E8B85C"), (0, "Low", "#7FBCA8")]
LOAD_BANDS = [("Most change", "#9E2B25"), ("High", "#CC6A33"),
              ("Moderate", "#E8B85C"), ("Light", "#7FBCA8")]
NONE_COLOR = "#ECEAE5"
DEPTH_SPLIT = 12  # matrix Y split = the High threshold

E = html.escape

# --------------------------------------------------------------------- helpers
def g(rec, *keys, default=""):
    for k in keys:
        if k in rec and rec[k] not in (None, ""):
            return rec[k]
    return default

def as_int(v):
    try: return int(float(v))
    except Exception: return None

def score(rec):
    s = as_int(g(rec, "impact_score"))
    if s: return s
    sev, cx = as_int(g(rec, "severity")), as_int(g(rec, "complexity"))
    return sev * cx if (sev and cx) else None

def norm_name(s):
    """Normalize a role/group name for joining: strip ' - <location>' suffixes, lowercase."""
    return re.sub(r"\s+-\s+.*$", "", str(s or "")).strip().lower()

def split_roles(v):
    if isinstance(v, (list, tuple)): return [str(x).strip() for x in v if str(x).strip()]
    return [s.strip() for s in re.split(r"[;,/]| and ", str(v or "")) if s.strip()]

def dark_text(col):
    h = col.lstrip("#")
    r, gr, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (0.299 * r + 0.587 * gr + 0.114 * b) > 150

def quartiles(vals):
    s = sorted(v for v in vals if v)
    if not s: return [0, 0, 0]
    def q(p):
        i = p * (len(s) - 1); lo = int(i); hi = min(lo + 1, len(s) - 1)
        return s[lo] * (1 - (i - lo)) + s[hi] * (i - lo)
    return [q(0.25), q(0.5), q(0.75)]

def band(mean_score, n):
    if n == 0: return ("None", NONE_COLOR)
    for lo, lbl, col in BANDS:
        if mean_score >= lo: return (lbl, col)
    return ("Low", BANDS[-1][2])

def load_band(total, thr):
    if not total: return ("None", NONE_COLOR)
    t1, t2, t3 = thr
    i = 0 if total >= t3 else (1 if total >= t2 else (2 if total >= t1 else 3))
    return LOAD_BANDS[i]

# --------------------------------------------------------------------- derive
def normalize(records):
    out = []
    for i, r in enumerate(records, 1):
        rr = dict(r)
        rr["_id"] = r.get("id", i)
        rr["_score"] = score(r)
        rr["_area"] = str(g(r, "functional_area", "area") or g(r, "l1_process") or "Unassigned").strip()
        rr["_in_scope"] = not str(g(r, "scope", default="In Scope")).lower().startswith("out")
        out.append(rr)
    return out

def derive_areas(recs):
    """Per functional area: volume, depth (mean score), total change load."""
    by = {}
    for r in recs:
        if r["_in_scope"]:
            by.setdefault(r["_area"], []).append(r)
    areas = []
    for name, rs in by.items():
        scored = [r["_score"] for r in rs if r["_score"]]
        mean = round(sum(scored) / len(scored), 1) if scored else 0.0
        lbl, col = band(mean, len(rs))
        areas.append({
            "name": name, "volume": len(rs), "scored": len(scored),
            "depth": mean, "total": sum(scored), "band": lbl, "color": col,
            "crit_high": sum(1 for r in rs if str(g(r, "priority")).strip() in ("Critical", "High")
                             or (r["_score"] or 0) >= 12),
            "impacts": sorted(rs, key=lambda z: -(z["_score"] or 0)),
        })
    thr = quartiles([a["total"] for a in areas])
    for a in areas:
        a["load_band"], a["load_color"] = load_band(a["total"], thr)
    areas.sort(key=lambda a: -a["total"])
    vols = sorted(a["volume"] for a in areas)
    vol_split = vols[len(vols) // 2] if vols else 0  # median volume
    return areas, vol_split

def sha_lookup(sha_records):
    """normalized stakeholder_group -> short annotation string."""
    look = {}
    for r in sha_records or []:
        name = str(g(r, "stakeholder_group", "group", "name")).strip()
        if not name: continue
        bits = []
        for k, lab in (("influence", "influence"), ("interest", "interest")):
            v = g(r, k)
            if v: bits.append("%s %s" % (lab, v))
        disp = g(r, "current_disposition", "disposition", "current_sentiment", "stance", "sentiment")
        if disp: bits.append(str(disp))
        look[norm_name(name)] = " · ".join(str(b) for b in bits)
    return look

def resolve_theme_impacts(theme, recs):
    """Match a theme's impact_ids / impact_titles to records; return (matches, misses)."""
    by_id = {str(r["_id"]): r for r in recs}
    by_title = {str(g(r, "title")).strip().lower(): r for r in recs}
    matches, misses = [], []
    for i in theme.get("impact_ids") or []:
        r = by_id.get(str(i))
        (matches if r else misses).append(r if r else "id %s" % i)
    for t in theme.get("impact_titles") or []:
        r = by_title.get(str(t).strip().lower())
        (matches if r else misses).append(r if r else "title '%s'" % t)
    # dedupe, keep order
    seen, out = set(), []
    for r in matches:
        if id(r) not in seen:
            seen.add(id(r)); out.append(r)
    return out, misses

# --------------------------------------------------------------------- html shell
def shell(title, sub, brand, body):
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title><style>
:root{--navy:%s;--magenta:%s;--bg:#F5F6F8;--border:#E0E4EA;--dark:#333;
--shadow:0 2px 10px rgba(20,30,60,.08);--font:%s}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--dark);font-family:var(--font);font-size:15px}
header{background:var(--navy);color:#fff;padding:18px 26px}
header h1{margin:0;font-size:20px}header .sub{opacity:.85;font-size:13px;margin-top:3px}
.wrap{max-width:1200px;margin:0 auto;padding:20px 24px 60px}
.card{background:#fff;border:1px solid var(--border);border-radius:10px;box-shadow:var(--shadow);padding:18px;margin-bottom:18px}
h2{color:var(--navy);font-size:17px;margin:4px 0 12px}h3{color:var(--navy);margin:0 0 6px}
table{border-collapse:collapse;width:100%%;font-size:14px}
th,td{padding:7px 9px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}
th{color:var(--navy);white-space:nowrap;cursor:pointer;user-select:none}
td.num,th.num{text-align:right}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;color:#fff;font-size:12px;font-weight:600}
.pill.dk{color:#222}.muted{color:#6b7480}.note{font-size:13px;color:#6b7480;line-height:1.5;margin-top:8px}
.chip{display:inline-block;background:#EEF1F7;color:var(--navy);border-radius:999px;padding:2px 10px;font-size:12.5px;margin:2px 4px 2px 0}
.drill{display:none;background:#F8F9FC}.drill.on{display:table-row}
.drill td{padding:10px 14px}
.imp{border-bottom:1px dashed var(--border);padding:5px 0;font-size:13.5px}
.board{display:grid;grid-template-columns:1fr 1.4fr 1.2fr;gap:14px;margin:12px 0}
.panel{background:#F8F9FC;border:1px solid var(--border);border-radius:8px;padding:12px}
.panel .hd{font-weight:700;color:var(--navy);font-size:13px;letter-spacing:.4px;margin-bottom:7px}
.script{background:var(--navy);color:#fff;border-radius:8px;padding:14px 16px;line-height:1.55;margin-top:10px}
.script .hd{color:var(--magenta);font-weight:700;font-size:13px;letter-spacing:.4px;margin-bottom:6px}
.asks{margin-top:10px}.asks li{margin:3px 0}
.tag{color:var(--magenta);font-weight:700;font-size:12px;letter-spacing:.5px}
footer{color:#8a93a0;font-size:12px;text-align:center;padding:14px}
@media(max-width:860px){.board{grid-template-columns:1fr}}
</style></head><body>
<header><h1>%s</h1><div class="sub">%s</div></header>
<div class="wrap">%s</div><footer>%s</footer>
<script>
document.querySelectorAll('tr[data-drill]').forEach(function(tr){tr.addEventListener('click',function(){
  var d=document.getElementById(tr.dataset.drill);if(d)d.classList.toggle('on');});});
function sortTbl(th){var t=th.closest('table'),tb=t.tBodies[0],k=+th.dataset.c,
 rows=[].slice.call(tb.querySelectorAll('tr[data-drill]'));
 var dir=th.dataset.d==='1'?-1:1;th.dataset.d=dir===1?'1':'-1';
 rows.sort(function(a,b){var x=a.cells[k].dataset.v||a.cells[k].textContent,
  y=b.cells[k].dataset.v||b.cells[k].textContent;
  return (isNaN(x-y)?x.localeCompare(y):(x-y))*dir;});
 rows.forEach(function(r){var d=document.getElementById(r.dataset.drill);tb.appendChild(r);if(d)tb.appendChild(d);});}
document.querySelectorAll('th[data-c]').forEach(function(th){th.addEventListener('click',function(){sortTbl(th);});});
</script></body></html>""" % (E(title), brand["navy"], brand["magenta"], brand["font"],
                              E(title), sub, body, E(brand["footer"]))

# --------------------------------------------------------------------- intensity map
def matrix_svg(areas, vol_split, brand):
    W, H, PAD = 760, 460, 50
    max_v = max([a["volume"] for a in areas] + [1]) * 1.15
    def X(v): return PAD + (v / max_v) * (W - PAD - 20)
    def Y(d): return H - PAD - (d / 25.0) * (H - PAD - 20)
    sx, sy = X(vol_split), Y(DEPTH_SPLIT)
    s = ['<svg viewBox="0 0 %d %d" style="width:100%%;max-width:%dpx;font-family:inherit">' % (W, H, W)]
    s.append('<rect x="%d" y="20" width="%d" height="%d" fill="#fff" stroke="#E0E4EA"/>' % (PAD, W - PAD - 20, H - PAD - 20))
    s.append('<line x1="%.1f" y1="20" x2="%.1f" y2="%d" stroke="#cbd2dc" stroke-dasharray="5 4"/>' % (sx, sx, H - PAD))
    s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#cbd2dc" stroke-dasharray="5 4"/>' % (PAD, sy, W - 20, sy))
    q = '<text x="%.1f" y="%.1f" fill="#9aa3b0" font-size="12" font-weight="600" text-anchor="%s">%s</text>'
    s.append(q % (W - 26, sy - 8, "end", "Broad &amp; Deep — priority focus"))
    s.append(q % (PAD + 6, sy - 8, "start", "Narrow &amp; Deep"))
    s.append(q % (W - 26, H - PAD - 8, "end", "Broad &amp; Shallow"))
    s.append(q % (PAD + 6, H - PAD - 8, "start", "Watch"))
    for a in areas:
        x, y = X(a["volume"]), Y(min(a["depth"], 25))
        r = max(6, (a["volume"] ** 0.5) * 2.6)
        s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%scc" stroke="%s"><title>%s — volume %d, depth %.1f (%s)</title></circle>'
                 % (x, y, r, a["color"], a["color"], E(a["name"]), a["volume"], a["depth"], a["band"]))
        s.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="#333">%s</text>' % (x + r + 3, y + 4, E(a["name"][:26])))
    s.append('<text x="%d" y="%d" fill="#6b7480" font-size="12">Volume (impact count) →</text>' % (PAD, H - 14))
    s.append('<text x="16" y="%d" fill="#6b7480" font-size="12" transform="rotate(-90 16 %d)">Depth (mean severity × complexity) →</text>' % (H - PAD, H - PAD))
    s.append("</svg>")
    return "".join(s)

def intensity_body(project, areas, vol_split, total):
    rows = []
    for i, a in enumerate(areas, 1):
        dk = " dk" if dark_text(a["load_color"]) else ""
        drill = "".join('<div class="imp"><b>%s</b> <span class="muted">— %s · score %s · %s</span></div>'
                        % (E(g(r, "title")), E(", ".join(split_roles(g(r, "roles_impacted"))) or "roles n/a"),
                           r["_score"] or "unscored", E(g(r, "process_change", "future_state")[:180]))
                        for r in a["impacts"])
        rows.append('<tr data-drill="d%d"><td>%d</td><td><b>%s</b></td>'
                    '<td class="num" data-v="%d"><b>%d</b></td><td class="num" data-v="%d">%d</td>'
                    '<td class="num" data-v="%s">%s</td>'
                    '<td data-v="%s"><span class="pill%s" style="background:%s">%s</span></td>'
                    '<td class="num" data-v="%d">%d</td></tr>'
                    '<tr class="drill" id="d%d"><td colspan="7">%s</td></tr>'
                    % (i, i, E(a["name"]), a["total"], a["total"], a["volume"], a["volume"],
                       a["depth"], a["depth"], a["load_band"], dk, a["load_color"], a["load_band"],
                       a["crit_high"], a["crit_high"], i, drill))
    legend = "".join('<span class="chip" style="background:%s;color:%s">%s</span>'
                     % (c, "#222" if dark_text(c) else "#fff", l) for l, c in LOAD_BANDS)
    return """
<div class="card"><h2>Which areas change most — ranked by total change load</h2>
<div class="note" style="margin:0 0 8px">Total change load = the sum of every impact's severity × complexity in the area,
so it reflects <b>both</b> how many things change <b>and</b> how hard each one is. Click a row for the impacts behind it;
click a column header to re-sort. %s in-scope impacts across %d areas. %s</div>
<table><thead><tr><th data-c="0">#</th><th data-c="1">Area</th><th class="num" data-c="2">Total load</th>
<th class="num" data-c="3">Impacts</th><th class="num" data-c="4">Depth (mean score)</th>
<th data-c="5">Heat</th><th class="num" data-c="6">Crit+High</th></tr></thead><tbody>%s</tbody></table></div>
<div class="card"><h2>Volume × Depth — change strategy quadrants</h2>%s
<div class="note">Bubble size = impact count; color = depth band (Critical 20+ / High 12+ / Medium 5+ / Low).
Splits: volume at the median (%d impacts), depth at 12 (the High threshold).
<b>Broad &amp; Deep</b>: flagship OCM investment. <b>Narrow &amp; Deep</b>: surgical coaching / role redesign.
<b>Broad &amp; Shallow</b>: scale plays — mass comms, self-serve training. <b>Watch</b>: light touch, monitor.</div></div>
<div class="card"><h2>Method</h2><div class="note">Derived from the CIA records at generation time — never hand-scored.
Volume = impact count. Depth = mean severity × complexity over the area's scored impacts (unscored impacts count toward
volume only). Heat shading = quartiles of total load. An area with few or no impacts is not automatically "no change" —
confirm whether it is covered elsewhere, deferred, out of scope, or an extraction gap.</div></div>
""" % (total, len(areas), legend, "".join(rows), matrix_svg(areas, vol_split, DEFAULT_BRAND), vol_split)

# --------------------------------------------------------------------- executive readout
def theme_board(idx, theme, matches, sha):
    roles = []
    for r in matches:
        for role in split_roles(g(r, "roles_impacted")):
            if role not in roles: roles.append(role)
    who = "".join('<span class="chip">%s%s</span>'
                  % (E(ro), (' <span class="muted">(%s)</span>' % E(sha[norm_name(ro)])) if norm_name(ro) in sha and sha[norm_name(ro)] else "")
                  for ro in roles) or '<span class="muted">No roles recorded.</span>'
    what = '<div style="line-height:1.5">%s</div>' % E(theme.get("whats_changing", ""))
    what += "".join('<div class="imp">%s <span class="muted">[score %s]</span></div>'
                    % (E(g(r, "title")), r["_score"] or "—") for r in matches)
    hows = []
    for r in matches:
        m = g(r, "mitigation")
        if m and m not in hows: hows.append(m)
    how = "".join('<div class="imp">%s</div>' % E(m) for m in hows) or '<span class="muted">No mitigations recorded — flag as a gap.</span>'
    asks = theme.get("asks") or []
    ask_html = ('<div class="asks"><span class="tag">ASKS</span><ul>%s</ul></div>'
                % "".join("<li>%s</li>" % E(a) for a in asks)) if asks else ""
    return """<div class="card"><h2>Theme %d — %s</h2>
<div class="board">
<div class="panel"><div class="hd">WHO feels it</div>%s</div>
<div class="panel"><div class="hd">WHAT is changing</div>%s</div>
<div class="panel"><div class="hd">HOW we support it</div>%s</div>
</div>
<div class="script"><div class="hd">SAY THIS — the so-what</div>%s</div>%s</div>""" % (
        idx, E(theme.get("title", "")), who, what, how, E(theme.get("so_what_script", "")), ask_html)

def readout_body(project, readout, areas, themes_matched, sha, total):
    meta = readout.get("meta", {})
    parts = []
    if readout.get("exec_summary"):
        parts.append('<div class="card"><h2>Executive summary</h2><div style="line-height:1.6;font-size:15.5px">%s</div></div>'
                     % E(readout["exec_summary"]))
    top = areas[:5]
    snap = "".join('<tr><td><b>%s</b></td><td class="num">%d</td><td class="num">%d</td><td class="num">%.1f</td>'
                   '<td><span class="pill%s" style="background:%s">%s</span></td></tr>'
                   % (E(a["name"]), a["total"], a["volume"], a["depth"],
                      " dk" if dark_text(a["load_color"]) else "", a["load_color"], a["load_band"]) for a in top)
    parts.append("""<div class="card"><h2>Where the change concentrates</h2>
<div class="note" style="margin:0 0 8px">Top areas by total change load (derived from the CIA — see the Change Intensity Map for the full picture). %d in-scope impacts.</div>
<table><thead><tr><th>Area</th><th class="num">Total load</th><th class="num">Impacts</th><th class="num">Depth</th><th>Heat</th></tr></thead>
<tbody>%s</tbody></table></div>""" % (total, snap))
    for i, (theme, matches) in enumerate(themes_matched, 1):
        parts.append(theme_board(i, theme, matches, sha))
    closing = readout.get("asks") or []
    if closing:
        parts.append('<div class="card"><h2>What we need from this group</h2><ul class="asks">%s</ul></div>'
                     % "".join("<li>%s</li>" % E(a) for a in closing))
    return "".join(parts)

# --------------------------------------------------------------------- talking points md
def talking_points_md(project, readout, themes_matched):
    meta = readout.get("meta", {})
    L = ["# %s — Leader Talking Points" % project.get("project_name", "Project"), "",
         "*%s · %s · %s*" % (meta.get("audience", ""), meta.get("occasion", ""),
                             meta.get("date", datetime.date.today().isoformat())), "",
         "Explain the why — don't read the slide. For each theme: the takeaway leaders need, then the so-what to say out loud.", ""]
    if readout.get("exec_summary"):
        L += ["## The headline", "", readout["exec_summary"], ""]
    for i, (theme, matches) in enumerate(themes_matched, 1):
        L += ["## %d. %s" % (i, theme.get("title", "")), "",
              "**What's changing —** %s" % theme.get("whats_changing", ""), "",
              "**Say this —** %s" % theme.get("so_what_script", ""), ""]
        if theme.get("asks"):
            L += ["**Asks:**"] + ["- %s" % a for a in theme["asks"]] + [""]
        if matches:
            L += ["*Backed by: %s*" % "; ".join(g(r, "title") for r in matches), ""]
    if readout.get("asks"):
        L += ["## Closing asks", ""] + ["- %s" % a for a in readout["asks"]] + [""]
    return "\n".join(L)

# --------------------------------------------------------------------- cli
def _guard(outdir, names, force):
    """Refuse to overwrite existing deliverables unless --force is set."""
    existing = [n for n in names if os.path.exists(os.path.join(outdir, n))]
    if existing and not force:
        sys.exit("Refusing to overwrite existing outputs in %s (use --force):\n  %s"
                 % (outdir, "\n  ".join(existing)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cia", required=True)
    ap.add_argument("--readout", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--sha")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    project = json.load(open(a.config, encoding="utf-8"))
    brand = dict(DEFAULT_BRAND); brand.update(project.get("brand") or {})
    pn = project.get("project_name", "Project")
    names = ["%s Change Intensity Map.html" % pn, "%s Executive Readout.html" % pn,
             "%s Talking Points.md" % pn]
    _guard(a.outdir, names, a.force)

    recs = normalize(json.load(open(a.cia, encoding="utf-8")))
    readout = json.load(open(a.readout, encoding="utf-8"))
    sha = sha_lookup(json.load(open(a.sha, encoding="utf-8"))) if a.sha else {}
    in_scope = [r for r in recs if r["_in_scope"]]
    areas, vol_split = derive_areas(recs)

    # unscored-CIA guard: severity-dependent views degenerate silently otherwise
    scored_n = sum(1 for r in in_scope if r["_score"])
    banner = ""
    if in_scope and scored_n <= 0.2 * len(in_scope):
        msg = "CIA is unscored — severity-dependent views are not meaningful; score the CIA first"
        print("WARNING: %s (%d of %d in-scope impacts scored)" % (msg, scored_n, len(in_scope)))
        banner = ('<div class="card" style="background:#FCF1DB;border:2px solid #D9932F">'
                  '<b style="color:#8A5A00;font-size:15px">&#9888; %s.</b>'
                  '<div class="note" style="color:#8A5A00">Only %d of %d in-scope impacts carry severity/complexity, '
                  'so depth, total change load, heat bands, and quadrant placement default to zero — they do not mean '
                  '"low change."</div></div>' % (E(msg), scored_n, len(in_scope)))

    themes_matched, warn = [], []
    for t in readout.get("themes", []):
        m, miss = resolve_theme_impacts(t, recs)
        themes_matched.append((t, m))
        for x in miss:
            warn.append("theme '%s': unresolved %s" % (t.get("title", "?"), x))
    nthemes = len(themes_matched)
    if not (4 <= nthemes <= 7):
        warn.append("%d themes — methodology calls for 4-7" % nthemes)

    gen = datetime.date.today().isoformat()
    meta = readout.get("meta", {})
    sub = "%s · %s · derived from the live CIA · generated %s" % (
        E(meta.get("audience", "Leadership")), E(meta.get("occasion", "Readout")), gen)
    with open(os.path.join(a.outdir, names[0]), "w", encoding="utf-8") as f:
        f.write(shell("%s Change Intensity Map" % pn,
                      "Which areas are experiencing the most vs least change · generated %s" % gen,
                      brand, banner + intensity_body(project, areas, vol_split, len(in_scope))))
    with open(os.path.join(a.outdir, names[1]), "w", encoding="utf-8") as f:
        f.write(shell("%s Executive Readout" % pn, sub, brand,
                      banner + readout_body(project, readout, areas, themes_matched, sha, len(in_scope))))
    with open(os.path.join(a.outdir, names[2]), "w", encoding="utf-8") as f:
        f.write(talking_points_md(project, readout, themes_matched) + "\n")

    print("Wrote to %s:" % a.outdir)
    for n in names: print("  " + n)
    print("Areas: %d | in-scope impacts: %d | themes: %d" % (len(areas), len(in_scope), nthemes))
    for t, m in themes_matched:
        print("theme '%s' -> %s" % (t.get("title", "?"),
                                    "; ".join(str(g(r, "title")) for r in m) or "(no impacts resolved)"))
    if a.sha:
        troles = set()
        for t, m in themes_matched:
            for r in m:
                for ro in split_roles(g(r, "roles_impacted")):
                    troles.add(norm_name(ro))
        matched = sum(1 for ro in troles if ro in sha)
        print("SHA join: %d of %d roles matched" % (matched, len(troles)))
        if matched == 0:
            print("WARN: --sha given but no roles matched any SHA stakeholder_group — check name alignment")
    for w in warn: print("WARN: " + w)

if __name__ == "__main__":
    main()
