#!/usr/bin/env python3
"""
adoption-metrics-builder — render an adoption & success measurement package for
ANY project from a structured metrics plan (designed by Claude):
  - "<Project> Adoption Metrics Menu.xlsx"  (Metric Register + Measurement Plan sheets)
  - "<Project> Adoption Dashboard.html"     (self-contained: tiles by ladder level,
    filterable register, leading/lagging split, coverage/GAP view when --cia given)

Usage:
  python3 metrics_render.py --plan metrics_plan.json --config project.json [--cia cia_records.json] --outdir OUT [--force]

Only stdlib + openpyxl. Cross-platform. Output HTML has no external dependencies.
Shared conventions (no-clobber, DEFAULT_BRAND) follow the suite canonical source: cia-builder.
"""
import argparse, datetime, html, json, os, sys

LADDER = ["Readiness Input", "System Usage", "Behavior/Proficiency", "Process Outcomes", "Business Value"]
CATEGORIES = ["Engagement", "Readiness", "Adoption", "Business Outcome"]
LADDER_COLORS = {"Readiness Input": "#7A4FBE", "System Usage": "#04A577",
                 "Behavior/Proficiency": "#F08301", "Process Outcomes": "#FF533C",
                 "Business Value": "#162B75"}
DEFAULT_BRAND = {"navy": "#162B75", "magenta": "#EE2C81", "orange": "#F08301",
                 "teal": "#04A577", "coral": "#FF533C", "font": "Calibri, system-ui, sans-serif",
                 "footer": "Confidential"}

def g(rec, *keys, default=""):
    for k in keys:
        if k in rec and rec[k] not in (None, ""):
            return rec[k]
    return default

def as_list(v):
    if v is None or v == "": return []
    if isinstance(v, (list, tuple)): return [str(x).strip() for x in v if str(x).strip()]
    return [s.strip() for s in str(v).replace(";", ",").split(",") if s.strip()]

def _guard(path, force):
    if os.path.exists(path) and not force:
        sys.exit(f"Refusing to overwrite existing output: {path} (pass --force to regenerate)")

# ----------------------------------------------------------------------------- normalize
def normalize(plan):
    metrics = []
    for i, m in enumerate(plan.get("metrics", []), 1):
        lvl = g(m, "ladder_level")
        if lvl not in LADDER: lvl = "Readiness Input"
        cat = g(m, "category")
        if cat not in CATEGORIES: cat = "Adoption"
        ind = g(m, "indicator_type").title()
        if ind not in ("Leading", "Lagging"): ind = ""
        metrics.append({
            "id": g(m, "id", default=f"M{i}"),
            "name": g(m, "name"),
            "category": cat, "ladder_level": lvl, "indicator_type": ind,
            "description": g(m, "description"),
            "how_measured": g(m, "how_measured"),
            "source": g(m, "source"), "owner": g(m, "owner"),
            "baseline": g(m, "baseline"), "target": g(m, "target"),
            "threshold_amber": g(m, "threshold_amber"), "threshold_red": g(m, "threshold_red"),
            "cadence": g(m, "cadence"), "start_tracking": g(m, "start_tracking"),
            "value_levers": as_list(m.get("value_levers")),
            "linked_impacts": as_list(m.get("linked_impacts")),
            "active": bool(m.get("active")),
            "notes": g(m, "notes"),
        })
    return metrics, plan.get("measurement_plan", {})

def coverage(metrics, cia_records, config):
    """Return (lever_rows, impact_rows). Each row: {name, metrics[], gap}."""
    levers = []
    seen = set()
    for b in config.get("benefits", []):
        n = g(b, "benefit")
        if n and n not in seen: seen.add(n); levers.append(n)
    for r in cia_records:
        for n in as_list(r.get("value_levers")):
            if n not in seen: seen.add(n); levers.append(n)
    lever_rows = []
    for lv in levers:
        hits = [m["id"] + " " + m["name"] for m in metrics if lv in m["value_levers"]]
        lever_rows.append({"name": lv, "metrics": hits, "gap": not hits})
    impact_rows = []
    scored = 0
    for r in cia_records:
        try:
            sev = int(float(r.get("severity")))
            scored += 1
        except (TypeError, ValueError): sev = 0
        if sev < 4: continue
        t = g(r, "title")
        hits = [m["id"] + " " + m["name"] for m in metrics if t in m["linked_impacts"]]
        impact_rows.append({"name": t, "severity": sev, "bu": g(r, "business_unit", "bu"),
                            "metrics": hits, "gap": not hits})
    unscored = bool(cia_records) and scored < max(1, len(cia_records) // 10)
    return lever_rows, impact_rows, unscored

# ----------------------------------------------------------------------------- xlsx
REG_COLS = [("id", "ID", 8), ("name", "Metric", 30), ("category", "Category", 14),
            ("ladder_level", "Ladder Level", 18), ("indicator_type", "Leading/Lagging", 14),
            ("description", "Description", 42), ("how_measured", "How Measured", 36),
            ("source", "Data Source / Instrument", 28), ("owner", "Owner", 20),
            ("baseline", "Baseline", 14), ("target", "Target", 20),
            ("threshold_amber", "Amber Threshold", 16), ("threshold_red", "Red Threshold", 16),
            ("cadence", "Cadence", 20), ("start_tracking", "Start Tracking", 18),
            ("value_levers", "Value Levers", 24), ("linked_impacts", "Linked Impacts", 30),
            ("active", "Activation Set", 12), ("notes", "Notes", 28)]

def write_xlsx(path, metrics, mplan, brand):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    navy = brand["navy"].lstrip("#")
    thin = Side(style="thin", color="D9D9D9"); border = Border(thin, thin, thin, thin)
    wb = Workbook(); ws = wb.active; ws.title = "Metric Register"
    ws.append([c[1] for c in REG_COLS])
    for ci in range(1, len(REG_COLS) + 1):
        c = ws.cell(1, ci); c.font = Font(bold=True, color="FFFFFF", size=11)
        c.fill = PatternFill("solid", fgColor=navy)
        c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = border
    ws.freeze_panes = "C2"; ws.row_dimensions[1].height = 26
    ws.auto_filter.ref = f"A1:{get_column_letter(len(REG_COLS))}1"
    for m in metrics:
        row = []
        for key, _, _ in REG_COLS:
            v = m.get(key, "")
            if isinstance(v, bool): v = "Yes" if v else ""
            if isinstance(v, list): v = ", ".join(v)
            row.append(v)
        ws.append(row)
    for ci, col in enumerate(REG_COLS, 1):
        L = get_column_letter(ci); ws.column_dimensions[L].width = col[2]
        for cell in ws[L][1:]:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = border; cell.font = Font(size=10)

    ws2 = wb.create_sheet("Measurement Plan")
    rows = [("Reporting cadence", g(mplan, "reporting_cadence")),
            ("Review forum", g(mplan, "review_forum")),
            ("Escalation path", g(mplan, "escalation")),
            ("Baseline approach", g(mplan, "baseline_approach")),
            ("Data collection notes", g(mplan, "data_collection_notes"))]
    ws2.append(["Element", "Approach"])
    for ci in (1, 2):
        c = ws2.cell(1, ci); c.font = Font(bold=True, color="FFFFFF", size=11)
        c.fill = PatternFill("solid", fgColor=navy); c.border = border
    for r in rows:
        ws2.append(list(r))
    ws2.column_dimensions["A"].width = 24; ws2.column_dimensions["B"].width = 90
    for row in ws2.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = border; cell.font = Font(size=10)
    wb.save(path)

# ----------------------------------------------------------------------------- html
TEMPLATE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>%%TITLE%%</title>
<style>
:root{--navy:%%NAVY%%;--mag:%%MAG%%;--ink:#1d2433;--mut:#6b7280;--line:#e5e7eb;--bg:#f5f6f8}
*{box-sizing:border-box}body{margin:0;font-family:%%FONT%%;color:var(--ink);background:var(--bg);font-size:14px}
header{background:linear-gradient(135deg,var(--navy),#0E2841);color:#fff;padding:18px 28px}
header h1{margin:0;font-size:1.15rem;font-weight:700}header .sub{opacity:.85;font-size:.85rem;margin-top:3px}
.wrap{max-width:1500px;margin:0 auto;padding:18px 28px 80px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:16px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;border-top:4px solid var(--navy);cursor:pointer}
.card .v{font-size:1.6rem;font-weight:800;color:var(--navy)}
.card .l{font-size:.72rem;color:var(--mut);text-transform:uppercase;letter-spacing:.04em;margin-top:2px}
.card .s{font-size:.72rem;color:var(--mut);margin-top:4px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0 10px}
.bar select,.bar input{padding:7px 10px;border:1px solid var(--line);border-radius:7px;font:inherit;background:#fff}
.bar input{flex:1;min-width:180px}
.btn{background:var(--navy);color:#fff;border:none;border-radius:7px;padding:8px 14px;cursor:pointer;font:inherit}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}
th{background:var(--navy);color:#fff;text-align:left;padding:9px 10px;font-size:.78rem;text-transform:uppercase;letter-spacing:.03em}
td{padding:9px 10px;border-top:1px solid var(--line);vertical-align:top;font-size:.85rem}
tr.mrow{cursor:pointer}tr.mrow:hover td{background:#f0f3fa}
tr.detail td{background:#fafbfd;font-size:.83rem}
.pill{display:inline-block;padding:2px 9px;border-radius:99px;font-size:.72rem;font-weight:700;color:#fff}
.lead{background:#04A577}.lag{background:#6b7280}
.gap{background:#c62828}.ok{background:#04A577}
.blank{color:#b45309;font-style:italic}
.dl{display:grid;grid-template-columns:170px 1fr;gap:4px 12px;margin:4px 0}
.dl b{color:var(--mut);font-weight:600;font-size:.76rem;text-transform:uppercase}
h2{font-size:1rem;margin:26px 0 8px;color:var(--navy)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:900px){.split{grid-template-columns:1fr}}
footer{color:var(--mut);font-size:.75rem;margin-top:36px;text-align:center}
.tabbtns{display:flex;gap:6px;margin:18px 0 0}
.tabbtns button{padding:9px 16px;border:1px solid var(--line);border-bottom:none;background:#e9ecf2;border-radius:8px 8px 0 0;cursor:pointer;font:inherit;font-weight:600;color:var(--mut)}
.tabbtns button.on{background:#fff;color:var(--navy)}
.tabpane{display:none}.tabpane.on{display:block}
</style></head><body>
<header><h1>%%TITLE%%</h1><div class="sub">%%SUB%%</div></header>
<div class="wrap">
<div class="tiles" id="tiles"></div>
<div class="tabbtns" id="tabbtns"></div>
<div class="tabpane on" id="pane-register">
  <div class="bar">
    <input id="q" placeholder="Search metrics...">
    <select id="fcat"><option value="">All categories</option></select>
    <select id="flvl"><option value="">All ladder levels</option></select>
    <select id="find"><option value="">Leading + Lagging</option><option>Leading</option><option>Lagging</option></select>
    <select id="fact"><option value="">All metrics</option><option value="1">Activation set only</option></select>
    <button class="btn" onclick="reset()">Reset</button>
  </div>
  <table><thead><tr><th>ID</th><th>Metric</th><th>Category</th><th>Ladder Level</th><th>L/L</th><th>Source</th><th>Owner</th><th>Baseline</th><th>Target</th><th>Cadence</th></tr></thead>
  <tbody id="tb"></tbody></table>
  <h2>Leading vs Lagging</h2>
  <div class="split"><div><table><thead><tr><th>Leading indicators</th></tr></thead><tbody id="leadtb"></tbody></table></div>
  <div><table><thead><tr><th>Lagging indicators</th></tr></thead><tbody id="lagtb"></tbody></table></div></div>
  <h2>Measurement plan</h2><div class="card" style="cursor:default" id="mplan"></div>
</div>
<div class="tabpane" id="pane-coverage">%%COVERAGE%%</div>
<footer>%%FOOTER%% · Generated %%DATE%% · adoption-metrics-builder</footer>
</div>
<script>
const M=%%METRICS%%, MP=%%MPLAN%%, LADDER=%%LADDER%%, LCOL=%%LCOL%%, HASCOV=%%HASCOV%%;
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const blank=v=>v?esc(v):'<span class="blank">not set</span>';
function tiles(){const t=document.getElementById('tiles');let h=`<div class="card" onclick="reset()"><div class="v">${M.length}</div><div class="l">Total metrics</div><div class="s">${M.filter(m=>m.active).length} in activation set</div></div>`;
 for(const lv of LADDER){const n=M.filter(m=>m.ladder_level===lv).length;
  h+=`<div class="card" style="border-top-color:${LCOL[lv]}" onclick="pick('${lv}')"><div class="v">${n}</div><div class="l">${esc(lv)}</div><div class="s">${M.filter(m=>m.ladder_level===lv&&m.indicator_type==='Leading').length} leading</div></div>`;}
 t.innerHTML=h;}
function pick(lv){document.getElementById('flvl').value=lv;show('register');draw();}
function opts(id,vals){const s=document.getElementById(id);for(const v of vals){const o=document.createElement('option');o.textContent=v;s.appendChild(o);}}
function detail(m){return `<div class="dl"><b>Description</b><span>${esc(m.description)}</span><b>How measured</b><span>${blank(m.how_measured)}</span><b>Source</b><span>${esc(m.source)}</span><b>Owner</b><span>${esc(m.owner)}</span><b>Baseline</b><span>${blank(m.baseline)}</span><b>Target</b><span>${blank(m.target)}</span><b>Amber / Red</b><span>${blank(m.threshold_amber)} / ${blank(m.threshold_red)}</span><b>Cadence</b><span>${blank(m.cadence)}</span><b>Start tracking</b><span>${blank(m.start_tracking)}</span><b>Value levers</b><span>${esc(m.value_levers.join(', '))||'—'}</span><b>Linked impacts</b><span>${esc(m.linked_impacts.join('; '))||'—'}</span><b>Notes</b><span>${esc(m.notes)||'—'}</span></div>`;}
function draw(){const q=document.getElementById('q').value.toLowerCase(),c=document.getElementById('fcat').value,l=document.getElementById('flvl').value,i=document.getElementById('find').value,a=document.getElementById('fact').value;
 const tb=document.getElementById('tb');tb.innerHTML='';
 M.forEach((m,ix)=>{if(c&&m.category!==c)return;if(l&&m.ladder_level!==l)return;if(i&&m.indicator_type!==i)return;if(a&&!m.active)return;
  if(q&&!(m.name+' '+m.description+' '+m.source+' '+m.owner+' '+m.id).toLowerCase().includes(q))return;
  const tr=document.createElement('tr');tr.className='mrow';tr.onclick=()=>{const d=document.getElementById('d'+ix);d.style.display=d.style.display==='none'?'':'none';};
  tr.innerHTML=`<td><b>${esc(m.id)}</b></td><td><b>${esc(m.name)}</b>${m.active?' ★':''}</td><td>${esc(m.category)}</td><td><span class="pill" style="background:${LCOL[m.ladder_level]}">${esc(m.ladder_level)}</span></td><td><span class="pill ${m.indicator_type==='Leading'?'lead':'lag'}">${esc(m.indicator_type)}</span></td><td>${esc(m.source)}</td><td>${esc(m.owner)}</td><td>${blank(m.baseline)}</td><td>${blank(m.target)}</td><td>${blank(m.cadence)}</td>`;
  tb.appendChild(tr);
  const dr=document.createElement('tr');dr.className='detail';dr.id='d'+ix;dr.style.display='none';
  dr.innerHTML=`<td colspan="10">${detail(m)}</td>`;tb.appendChild(dr);});
 for(const[id,type]of[['leadtb','Leading'],['lagtb','Lagging']]){const el=document.getElementById(id);
  el.innerHTML=M.filter(m=>m.indicator_type===type).map(m=>`<tr><td><b>${esc(m.id)}</b> ${esc(m.name)} <span class="pill" style="background:${LCOL[m.ladder_level]}">${esc(m.ladder_level)}</span></td></tr>`).join('')||'<tr><td>—</td></tr>';}
}
function reset(){for(const id of['fcat','flvl','find','fact'])document.getElementById(id).value='';document.getElementById('q').value='';draw();}
function show(name){document.querySelectorAll('.tabpane').forEach(p=>p.classList.toggle('on',p.id==='pane-'+name));
 document.querySelectorAll('.tabbtns button').forEach(b=>b.classList.toggle('on',b.dataset.t===name));}
(function(){opts('fcat',[...new Set(M.map(m=>m.category))]);opts('flvl',LADDER.filter(l=>M.some(m=>m.ladder_level===l)));
 const tb=document.getElementById('tabbtns');
 tb.innerHTML=`<button class="on" data-t="register" onclick="show('register')">Metric Register</button>`+(HASCOV?`<button data-t="coverage" onclick="show('coverage')">Coverage${document.querySelectorAll('#pane-coverage .gap').length?' ⚠':''}</button>`:'');
 const mp=document.getElementById('mplan');
 mp.innerHTML=`<div class="dl"><b>Reporting cadence</b><span>${blank(MP.reporting_cadence)}</span><b>Review forum</b><span>${blank(MP.review_forum)}</span><b>Escalation</b><span>${blank(MP.escalation)}</span><b>Baseline approach</b><span>${blank(MP.baseline_approach)}</span><b>Data collection</b><span>${blank(MP.data_collection_notes)}</span></div>`;
 ['q','fcat','flvl','find','fact'].forEach(id=>document.getElementById(id).addEventListener(id==='q'?'input':'change',draw));
 tiles();draw();})();
</script></body></html>"""

def coverage_html(lever_rows, impact_rows, unscored=False):
    def pill(gap):
        return '<span class="pill gap">GAP — no metric</span>' if gap else '<span class="pill ok">Covered</span>'
    h = ['<h2>Value lever coverage</h2>',
         '<table><thead><tr><th>Value lever</th><th>Status</th><th>Metrics</th></tr></thead><tbody>']
    for r in lever_rows:
        h.append(f'<tr><td><b>{html.escape(r["name"])}</b></td><td>{pill(r["gap"])}</td>'
                 f'<td>{html.escape("; ".join(r["metrics"])) or "—"}</td></tr>')
    if not lever_rows:
        h.append('<tr><td colspan="3">No value levers found in the CIA.</td></tr>')
    h.append('</tbody></table><h2>High-severity impact coverage (severity ≥ 4)</h2>'
             '<table><thead><tr><th>Impact</th><th>Sev</th><th>BU</th><th>Status</th><th>Metrics</th></tr></thead><tbody>')
    for r in impact_rows:
        h.append(f'<tr><td><b>{html.escape(r["name"])}</b></td><td>{r["severity"]}</td>'
                 f'<td>{html.escape(r["bu"])}</td><td>{pill(r["gap"])}</td>'
                 f'<td>{html.escape("; ".join(r["metrics"])) or "—"}</td></tr>')
    if unscored:
        h.append('<tr><td colspan="5"><div class="warn-banner" style="background:#FFF3CD;'
                 'border:1px solid #E0A800;border-left:4px solid #E0A800;color:#7A5C00;'
                 'padding:10px 14px;border-radius:4px;font-weight:600">'
                 '&#9888; high-severity coverage not evaluated &mdash; CIA unscored; '
                 'score the CIA first</div></td></tr>')
    elif not impact_rows:
        h.append('<tr><td colspan="5">No high-severity impacts in the CIA.</td></tr>')
    h.append('</tbody></table>')
    return "".join(h)

def write_html(path, metrics, mplan, brand, title, sub, cov_html, has_cov):
    out = (TEMPLATE
           .replace("%%TITLE%%", html.escape(title)).replace("%%SUB%%", html.escape(sub))
           .replace("%%NAVY%%", brand["navy"]).replace("%%MAG%%", brand["magenta"])
           .replace("%%FONT%%", brand["font"]).replace("%%FOOTER%%", html.escape(brand["footer"]))
           .replace("%%DATE%%", datetime.date.today().isoformat())
           .replace("%%COVERAGE%%", cov_html)
           .replace("%%METRICS%%", json.dumps(metrics))
           .replace("%%MPLAN%%", json.dumps(mplan))
           .replace("%%LADDER%%", json.dumps(LADDER))
           .replace("%%LCOL%%", json.dumps(LADDER_COLORS))
           .replace("%%HASCOV%%", "true" if has_cov else "false"))
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)

# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--cia", default=None)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    with open(a.plan, encoding="utf-8") as f: plan = json.load(f)
    with open(a.config, encoding="utf-8") as f: config = json.load(f)
    cia_records = []
    if a.cia:
        with open(a.cia, encoding="utf-8") as f: cia_records = json.load(f)

    brand = dict(DEFAULT_BRAND); brand.update(config.get("brand") or {})
    project = config.get("project_name", "Project")
    metrics, mplan = normalize(plan)
    if not metrics:
        sys.exit("metrics_plan.json contains no metrics.")

    has_cov = bool(a.cia)
    cov_html = ""
    if has_cov:
        lever_rows, impact_rows, unscored = coverage(metrics, cia_records, config)
        cov_html = coverage_html(lever_rows, impact_rows, unscored)
        if unscored:
            print("WARNING: high-severity coverage not evaluated - CIA records lack "
                  "numeric severity scores; score the CIA first.", file=sys.stderr)

    os.makedirs(a.outdir, exist_ok=True)
    xlsx_path = os.path.join(a.outdir, f"{project} Adoption Metrics Menu.xlsx")
    html_path = os.path.join(a.outdir, f"{project} Adoption Dashboard.html")
    _guard(xlsx_path, a.force); _guard(html_path, a.force)

    write_xlsx(xlsx_path, metrics, mplan, brand)
    sub = f"{project} — Adoption & Success Metrics · {len(metrics)} metrics"
    write_html(html_path, metrics, mplan, brand, f"{project} Adoption Dashboard", sub, cov_html, has_cov)
    print(f"Wrote: {xlsx_path}")
    print(f"Wrote: {html_path}")
    if has_cov:
        gaps = cov_html.count('pill gap')
        print(f"Coverage view included ({gaps} GAP row(s)).")

if __name__ == "__main__":
    main()
