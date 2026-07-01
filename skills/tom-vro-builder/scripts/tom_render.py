#!/usr/bin/env python3
"""
tom_render.py — from tom_blueprint.json + project.json, render three deliverables
for ANY project:
  1. <Project> TOM Approach.docx   — 8 TOM dimensions + prioritized functional groups
                                      + value streams + new roles/seats + value-at-risk.
  2. <Project> VRO Registers.xlsx  — Benefits Register (baseline source + owner per KPI)
                                      + Value-at-Risk + VRO operating tiers.
  3. <Project> TOM Dashboard.html  — self-contained interactive overview.

Usage:
  python3 tom_render.py --config project.json --blueprint tom_blueprint.json --outdir OUT

Requires python-docx + openpyxl. HTML output is dependency-free. Cross-platform.
"""
import argparse, html, json
from pathlib import Path

DEF_BRAND = {"navy": "#0E2841", "cyan": "#12ABDB", "magenta": "#EE2C81",
             "font": "Calibri, system-ui, sans-serif", "footer": "Confidential"}
PRI_RANK = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "": 4}


def brand(project):
    b = dict(DEF_BRAND); b.update(project.get("brand", {}) or {})
    return b


def sorted_groups(bp):
    g = list(bp.get("functional_groups", []))
    g.sort(key=lambda r: (PRI_RANK.get(r.get("priority", ""), 4), -int(r.get("impact_count") or 0)))
    return g


# --------------------------------------------------------------------------- Word
def build_docx(bp, project, outdir):
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    b = brand(project); pname = project.get("project_name", "Project")
    navy = RGBColor(*bytes.fromhex(b["navy"].lstrip("#")))
    doc = Document()
    normal = doc.styles["Normal"].font; normal.name = "Calibri"; normal.size = Pt(10.5)

    def h(text, size=15, space_before=10):
        p = doc.add_paragraph(); r = p.add_run(text); r.bold = True
        r.font.size = Pt(size); r.font.color.rgb = navy
        p.paragraph_format.space_before = Pt(space_before); p.paragraph_format.space_after = Pt(4)
        return p

    def table(headers, rows, widths=None):
        t = doc.add_table(rows=1, cols=len(headers)); t.style = "Light Grid Accent 1"
        for i, htext in enumerate(headers):
            c = t.rows[0].cells[i]; c.text = ""
            r = c.paragraphs[0].add_run(htext); r.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = navy
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                cells[i].text = ""
                rr = cells[i].paragraphs[0].add_run(str(val)); rr.font.size = Pt(9.5)
        if widths:
            for row in t.rows:
                for i, w in enumerate(widths):
                    row.cells[i].width = Inches(w)
        return t

    title = doc.add_paragraph(); tr = title.add_run(f"{pname} — Target Operating Model Approach")
    tr.bold = True; tr.font.size = Pt(20); tr.font.color.rgb = navy
    if bp.get("accelerator", {}).get("value_statement"):
        doc.add_paragraph(bp["accelerator"]["value_statement"])

    h("Functional groups — prioritized by people-impact")
    table(["Functional Area", "Rolls up", "Impacts", "Priority", "Lifecycle / process to map"],
          [[g.get("area", ""), ", ".join(g.get("rolls_up", [])), g.get("impact_count", ""),
            g.get("priority", ""), g.get("lifecycle", "")] for g in sorted_groups(bp)],
          widths=[1.4, 1.6, 0.7, 0.9, 2.4])

    if bp.get("value_streams"):
        h("Cross-functional value streams")
        for vs in bp["value_streams"]:
            p = doc.add_paragraph(style="List Bullet")
            p.add_run(vs.get("name", "") + ": ").bold = True
            p.add_run(" → ".join(vs.get("stages", [])))

    h("Target Operating Model — eight dimensions")
    table(["Dimension", "Current state", "Future-state questions"],
          [[d.get("dimension", ""), d.get("current_state", ""), d.get("future_state_questions", "")]
           for d in bp.get("tom_dimensions", [])], widths=[1.6, 2.6, 2.6])

    if bp.get("roles_and_seats"):
        h("New roles & seats the model implies")
        table(["Role / seat", "Why it's needed", "Owner"],
              [[r.get("name", ""), r.get("why", ""), r.get("owner", "")] for r in bp["roles_and_seats"]],
              widths=[1.8, 3.4, 1.6])

    if bp.get("value_at_risk"):
        h("Value-at-risk (from open / assumed gaps)")
        table(["Cluster", "Benefit at risk", "Why it matters", "Source gap"],
              [[v.get("cluster", ""), v.get("benefit_at_risk", ""), v.get("why", ""), v.get("source_gap", "")]
               for v in bp["value_at_risk"]], widths=[1.6, 1.6, 2.4, 1.2])

    # footer
    sec = doc.sections[0]
    fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = fp.add_run(b["footer"]); fr.font.size = Pt(8); fr.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    out = Path(outdir) / f"{pname} TOM Approach.docx"; doc.save(str(out)); return out


# --------------------------------------------------------------------------- Excel
def build_xlsx(bp, project, outdir):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    b = brand(project); pname = project.get("project_name", "Project")
    navyfill = PatternFill("solid", fgColor=b["navy"].lstrip("#"))
    thin = Side(style="thin", color="D9D9D9"); border = Border(thin, thin, thin, thin)
    wb = Workbook(); first = True

    def sheet(name, headers, rows, widths):
        nonlocal first
        ws = wb.active if first else wb.create_sheet(); first = False
        ws.title = name[:31]; ws.append(headers)
        for ci, _ in enumerate(headers, 1):
            c = ws.cell(1, ci); c.font = Font(bold=True, color="FFFFFF", size=11)
            c.fill = navyfill; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = border
        ws.row_dimensions[1].height = 26; ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"
        for row in rows:
            ws.append(row)
        for ci, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(ci)].width = w
            for cell in ws[get_column_letter(ci)][1:]:
                cell.alignment = Alignment(wrap_text=True, vertical="top"); cell.border = border; cell.font = Font(size=10)

    sheet("Benefits Register",
          ["Benefit", "KPI", "Baseline Source", "Owner", "Target", "Timeline"],
          [[r.get("benefit", ""), r.get("kpi", ""), r.get("baseline_source", ""), r.get("owner", ""),
            r.get("target", ""), r.get("timeline", "")] for r in bp.get("benefits_register", [])],
          [30, 30, 26, 22, 18, 18])
    sheet("Value at Risk",
          ["Cluster", "Benefit at Risk", "Why It Matters", "Source Gap"],
          [[r.get("cluster", ""), r.get("benefit_at_risk", ""), r.get("why", ""), r.get("source_gap", "")]
           for r in bp.get("value_at_risk", [])], [28, 26, 40, 22])
    if bp.get("vro_tiers"):
        sheet("VRO Tiers",
              ["Tier", "Focus", "Owner", "Cadence"],
              [[r.get("tier", ""), r.get("focus", ""), r.get("owner", ""), r.get("cadence", "")]
               for r in bp["vro_tiers"]], [16, 46, 24, 20])

    out = Path(outdir) / f"{pname} VRO Registers.xlsx"; wb.save(str(out)); return out


# --------------------------------------------------------------------------- HTML
def build_html(bp, project, outdir):
    b = brand(project); pname = project.get("project_name", "Project")
    e = lambda s: html.escape(str(s or ""))
    groups = sorted_groups(bp)
    pri_color = {"Critical": "#b40020", "High": "#d35400", "Medium": "#1d6fb8", "Low": "#6b7280"}

    cards = "".join(
        f'<div class="gcard" style="border-top-color:{pri_color.get(g.get("priority",""),"#156082")}">'
        f'<div class="gh">{e(g.get("area"))}</div>'
        f'<div class="gm"><span class="v">{e(g.get("impact_count"))}</span> impacts · '
        f'<b style="color:{pri_color.get(g.get("priority",""),"#333")}">{e(g.get("priority"))}</b></div>'
        f'<div class="gr">{e(", ".join(g.get("rolls_up", [])))}</div>'
        f'<div class="gl">{e(g.get("lifecycle"))}</div></div>' for g in groups)

    def rows(items, keys):
        return "".join("<tr>" + "".join(f"<td>{e(it.get(k))}</td>" for k in keys) + "</tr>" for it in items)

    dim_rows = rows(bp.get("tom_dimensions", []), ["dimension", "current_state", "future_state_questions"])
    var_rows = rows(bp.get("value_at_risk", []), ["cluster", "benefit_at_risk", "why", "source_gap"])
    ben_rows = rows(bp.get("benefits_register", []), ["benefit", "kpi", "baseline_source", "owner"])
    streams = "".join(f'<li><b>{e(v.get("name"))}</b>: {e(" → ".join(v.get("stages", [])))}</li>'
                      for v in bp.get("value_streams", []))

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{e(pname)} — TOM</title><style>
:root{{--navy:{b['navy']};--cyan:{b['cyan']};--ink:#1d2433;--mut:#6b7280;--line:#e5e7eb;--bg:#f5f6f8}}
*{{box-sizing:border-box}}body{{margin:0;font-family:{b['font']};color:var(--ink);background:var(--bg);font-size:14px}}
header{{background:linear-gradient(135deg,var(--navy),#0E2841);color:#fff;padding:20px 30px}}
header h1{{margin:0;font-size:1.2rem}}header .sub{{opacity:.85;font-size:.85rem;margin-top:3px}}
.wrap{{max-width:1400px;margin:0 auto;padding:20px 30px 70px}}
h2{{color:var(--navy);font-size:1.02rem;margin:26px 0 10px;border-bottom:2px solid var(--line);padding-bottom:5px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
.gcard{{background:#fff;border:1px solid var(--line);border-top:4px solid var(--navy);border-radius:12px;padding:13px 15px}}
.gh{{font-weight:700;color:var(--navy)}}.gm{{margin:4px 0;color:var(--mut);font-size:.82rem}}.gm .v{{font-size:1.3rem;font-weight:800;color:var(--ink)}}
.gr{{font-size:.76rem;color:var(--mut);margin-top:4px}}.gl{{font-size:.78rem;margin-top:6px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
th{{background:var(--navy);color:#fff;text-align:left;padding:9px 11px;font-size:.74rem}}
td{{padding:9px 11px;border-top:1px solid var(--line);font-size:.82rem;vertical-align:top}}
ul{{line-height:1.6}}footer{{text-align:center;color:var(--mut);font-size:.72rem;padding:18px}}
</style></head><body>
<header><h1>{e(pname)} — Target Operating Model</h1><div class="sub">{e(len(groups))} functional groups · {e(len(bp.get('tom_dimensions',[])))} TOM dimensions</div></header>
<div class="wrap">
<h2>Functional groups — prioritized by people-impact</h2><div class="tiles">{cards}</div>
{"<h2>Cross-functional value streams</h2><ul>"+streams+"</ul>" if streams else ""}
<h2>TOM dimensions</h2><table><thead><tr><th>Dimension</th><th>Current state</th><th>Future-state questions</th></tr></thead><tbody>{dim_rows}</tbody></table>
{"<h2>Value-at-risk</h2><table><thead><tr><th>Cluster</th><th>Benefit at risk</th><th>Why it matters</th><th>Source gap</th></tr></thead><tbody>"+var_rows+"</tbody></table>" if var_rows else ""}
{"<h2>Benefits register</h2><table><thead><tr><th>Benefit</th><th>KPI</th><th>Baseline source</th><th>Owner</th></tr></thead><tbody>"+ben_rows+"</tbody></table>" if ben_rows else ""}
</div><footer>{e(b['footer'])}</footer></body></html>"""
    out = Path(outdir) / f"{pname} TOM Dashboard.html"; out.write_text(doc, encoding="utf-8"); return out


def _guard(outdir, names, force):
    """Refuse to overwrite existing deliverables unless --force is set."""
    import os, sys
    existing = [n for n in names if os.path.exists(os.path.join(outdir, n))]
    if existing and not force:
        sys.exit("Refusing to overwrite existing output(s) in %r:\n  %s\n"
                 "Re-run with --force to overwrite, or choose a different --outdir."
                 % (outdir, "\n  ".join(existing)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--blueprint", required=True)
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--force", action="store_true", help="overwrite existing outputs in --outdir")
    a = ap.parse_args()
    Path(a.outdir).mkdir(parents=True, exist_ok=True)
    project = json.load(open(a.config, encoding="utf-8"))
    bp = json.load(open(a.blueprint, encoding="utf-8"))
    _pn = project.get("project_name", "Project")
    _guard(a.outdir, [f"{_pn} TOM Approach.docx", f"{_pn} VRO Registers.xlsx", f"{_pn} TOM Dashboard.html"], a.force)
    print("Word  ->", build_docx(bp, project, a.outdir))
    print("Excel ->", build_xlsx(bp, project, a.outdir))
    print("HTML  ->", build_html(bp, project, a.outdir))


if __name__ == "__main__":
    main()
