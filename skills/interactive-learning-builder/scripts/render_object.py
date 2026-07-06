#!/usr/bin/env python3
"""
Render a learning object (gamified quiz or microlearning flashcards) into a
self-contained interactive HTML file. The HTML works standalone (open from a
file/Drive link) AND reports completion + score to an LMS when launched inside
a SCORM 1.2 runtime. With --scorm, also emit an LMS-ready SCORM 1.2 zip.

Usage:
  python render_object.py --spec learning_object.json --context <project-context>.json --outdir OUT [--scorm]

No third-party dependencies (standard library only).
"""
import argparse, json, html, zipfile
from pathlib import Path


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def brand_from_context(ctx):
    ctx = ctx if isinstance(ctx, dict) else {}
    b = ctx.get("brand", {})
    project_name = ctx.get("project_name", "Training")
    return {
        "primary": b.get("primary", "#0070AD"),
        "accent": b.get("accent", "#12ABDB"),
        "font": b.get("font", "Calibri, system-ui, sans-serif"),
        "footer": b.get("footer", project_name + " — Confidential"),
    }


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root{--primary:__PRIMARY__;--accent:__ACCENT__;--font:__FONT__;
        --ink:#1b1f23;--muted:#5b6470;--line:#e4e8ee;--bg:#f5f7fa;--ok:#1a8a4f;--no:#c2403d;}
  *{box-sizing:border-box}
  body{margin:0;font-family:var(--font);color:var(--ink);background:var(--bg);
       -webkit-font-smoothing:antialiased;line-height:1.5}
  .wrap{max-width:720px;margin:0 auto;padding:24px 18px 64px}
  header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:6px}
  h1{font-size:1.25rem;margin:0;color:var(--primary)}
  .sub{color:var(--muted);font-size:.85rem;margin:0 0 16px}
  .bar{height:8px;background:var(--line);border-radius:99px;overflow:hidden;margin-bottom:20px}
  .bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--primary),var(--accent));
         transition:width .35s ease}
  .card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px;
        box-shadow:0 1px 3px rgba(20,30,50,.05)}
  .q{font-size:1.08rem;font-weight:600;margin:0 0 16px}
  .opts{display:flex;flex-direction:column;gap:10px}
  .opt{display:flex;gap:10px;align-items:flex-start;border:1.5px solid var(--line);border-radius:10px;
       padding:12px 14px;cursor:pointer;background:#fff;text-align:left;font:inherit;color:inherit;
       transition:border-color .15s,background .15s}
  .opt:hover{border-color:var(--accent)}
  .opt[aria-pressed="true"]{border-color:var(--primary);background:#f0f7fc}
  .opt.correct{border-color:var(--ok);background:#eaf7ef}
  .opt.wrong{border-color:var(--no);background:#fbeceb}
  .opt .mk{font-weight:700;min-width:1.2em}
  .fb{margin-top:14px;padding:12px 14px;border-radius:10px;font-size:.92rem;display:none}
  .fb.show{display:block}
  .fb.good{background:#eaf7ef;color:#155e36}
  .fb.bad{background:#fbeceb;color:#8f2e2b}
  .row{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-top:18px}
  button.btn{font:inherit;font-weight:600;border:0;border-radius:10px;padding:11px 18px;cursor:pointer;
        background:var(--primary);color:#fff}
  button.btn.ghost{background:#fff;color:var(--primary);border:1.5px solid var(--line)}
  button.btn:disabled{opacity:.45;cursor:not-allowed}
  .pill{font-size:.8rem;color:var(--muted)}
  /* flashcards */
  .deck{perspective:1200px}
  .flip{position:relative;min-height:230px;cursor:pointer}
  .face{position:absolute;inset:0;backface-visibility:hidden;display:flex;flex-direction:column;
        justify-content:center;padding:26px;border-radius:14px;border:1px solid var(--line);background:#fff}
  .face.back{transform:rotateY(180deg);background:#f0f7fc}
  .flip.flipped .front{transform:rotateY(180deg)}
  .flip.flipped .back{transform:rotateY(360deg)}
  .front,.back{transition:transform .5s}
  .face .lbl{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:8px}
  .face .txt{font-size:1.1rem;font-weight:600}
  .face .hint{margin-top:10px;font-size:.85rem;color:var(--muted);font-weight:400}
  .tap{font-size:.8rem;color:var(--muted);margin-top:8px;text-align:center}
  /* result */
  .result{text-align:center;padding:30px 22px}
  .score{font-size:2.4rem;font-weight:800;color:var(--primary);margin:6px 0}
  .badge{display:inline-flex;align-items:center;gap:8px;font-weight:700;padding:8px 16px;border-radius:99px;
         background:linear-gradient(90deg,var(--primary),var(--accent));color:#fff;margin:8px 0 4px}
  .verdict{font-size:1rem;margin:6px 0 18px}
  footer{margin-top:26px;text-align:center;color:var(--muted);font-size:.72rem}
  .obj{font-size:.78rem;color:var(--muted);margin-top:10px}
  .draftbn{background:#fff4e0;border:1.5px solid #c47f17;color:#8a5a0b;border-radius:10px;
           padding:10px 14px;font-size:.85rem;font-weight:700;margin:0 0 16px;text-align:center}
</style>
</head>
<body>
<div class="wrap">
  <header><h1>__TITLE__</h1><span class="pill" id="counter"></span></header>
  <p class="sub" id="subtitle"></p>
  <div class="bar"><i id="prog"></i></div>
__DRAFT_BANNER__
  <div id="stage" class="card" aria-live="polite"></div>
  <footer>__FOOTER__</footer>
</div>

<script type="application/json" id="LO_DATA">/*__DATA__*/</script>
<script>
/* ---------- minimal SCORM 1.2 wrapper (no-ops when not in an LMS) ---------- */
var SCORM=(function(){
  var api=null,found=false,init=false;
  function find(w){var n=0;while(w&&!w.API&&w.parent&&w.parent!=w&&n<12){w=w.parent;n++;}return w?w.API:null;}
  function get(){if(found)return api;var w=window;api=find(w);
    if(!api&&w.opener)api=find(w.opener);found=true;return api;}
  return{
    start:function(){var a=get();if(a&&!init){try{a.LMSInitialize("");init=true;
        a.LMSSetValue("cmi.core.lesson_status","incomplete");a.LMSCommit("");}catch(e){}}},
    complete:function(status,raw,max){var a=get();if(!a)return;try{
        if(raw!=null){a.LMSSetValue("cmi.core.score.raw",String(raw));
          a.LMSSetValue("cmi.core.score.min","0");a.LMSSetValue("cmi.core.score.max",String(max));}
        a.LMSSetValue("cmi.core.lesson_status",status);a.LMSCommit("");}catch(e){}},
    finish:function(){var a=get();if(a&&init){try{a.LMSFinish("");}catch(e){}}}
  };
})();
window.addEventListener("load",function(){SCORM.start();});
window.addEventListener("unload",function(){SCORM.finish();});

var DATA=JSON.parse(document.getElementById("LO_DATA").textContent);
var stage=document.getElementById("stage"),prog=document.getElementById("prog"),
    counter=document.getElementById("counter"),subtitle=document.getElementById("subtitle");
subtitle.textContent=DATA.audience?("For: "+DATA.audience):"";
var LETTERS="ABCDEFGH";
function setProg(p){prog.style.width=Math.round(p*100)+"%";}
function el(t,c,h){var e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;}

/* ===================== QUIZ ===================== */
function runQuiz(){
  var i=0,score=0,items=DATA.items||[],thr=(DATA.pass_threshold!=null?DATA.pass_threshold:0.8);
  function render(){
    var q=items[i];counter.textContent=(i+1)+" / "+items.length;setProg(i/items.length);
    stage.innerHTML="";
    stage.appendChild(el("p","q",(q.bloom?'<span class="pill">'+q.bloom+'</span><br>':'')+escapeHtml(q.question)));
    var multi=(q.type==="multiple");
    var opts=el("div","opts");var chosen=[];
    (q.options||[]).forEach(function(o,idx){
      var b=el("button","opt");b.type="button";b.setAttribute("aria-pressed","false");
      b.innerHTML='<span class="mk">'+LETTERS[idx]+'</span><span>'+escapeHtml(o.text)+'</span>';
      b.onclick=function(){
        if(b.dataset.locked)return;
        if(multi){var on=b.getAttribute("aria-pressed")==="true";b.setAttribute("aria-pressed",(!on).toString());
          var p=chosen.indexOf(idx);if(p>=0)chosen.splice(p,1);else chosen.push(idx);}
        else{chosen=[idx];check();}
      };
      opts.appendChild(b);
    });
    stage.appendChild(opts);
    var fb=el("div","fb");stage.appendChild(fb);
    var row=el("div","row");
    var hint=el("span","pill",multi?"Select all that apply":"Pick one");
    var next=el("button","btn",i<items.length-1?"Next":"See results");next.disabled=true;next.style.display="none";
    row.appendChild(hint);row.appendChild(next);stage.appendChild(row);
    if(multi){var sub=el("button","btn ghost","Submit answer");row.insertBefore(sub,next);
      sub.onclick=function(){if(chosen.length)check();};}

    function check(){
      var btns=opts.querySelectorAll(".opt");
      var correctIdx=[];(q.options||[]).forEach(function(o,idx){if(o.correct)correctIdx.push(idx);});
      var right=correctIdx.length===chosen.length&&correctIdx.every(function(x){return chosen.indexOf(x)>=0;});
      btns.forEach(function(bb,idx){bb.dataset.locked="1";
        if(q.options[idx].correct)bb.classList.add("correct");
        else if(chosen.indexOf(idx)>=0)bb.classList.add("wrong");});
      if(right)score++;
      var msg=(chosen.length===1&&q.options[chosen[0]]&&q.options[chosen[0]].feedback)?q.options[chosen[0]].feedback:
              (right?(q.feedback_correct||"Correct."):(q.feedback_incorrect||"Not quite — review the highlighted answer."));
      fb.className="fb show "+(right?"good":"bad");fb.innerHTML=(right?"✓ ":"✕ ")+escapeHtml(msg);
      hint.style.display="none";if(multi&&sub)sub.style.display="none";
      next.disabled=false;next.style.display="";
      next.onclick=function(){i++;if(i<items.length)render();else results();};
    }
  }
  function results(){
    setProg(1);counter.textContent="Done";
    var pct=items.length?score/items.length:0;var passed=pct>=thr;
    stage.className="card result";
    stage.innerHTML='<div class="score">'+score+" / "+items.length+'</div>'+
      '<div class="verdict">'+Math.round(pct*100)+'% correct</div>'+
      (passed?'<div class="badge">★ Passed — Go-Live Ready</div>':'<div class="verdict">Pass mark is '+Math.round(thr*100)+'%. Give it another go.</div>')+
      (DATA.objectives&&DATA.objectives.length?'<div class="obj">Covers: '+DATA.objectives.map(escapeHtml).join("; ")+'</div>':'');
    var row=el("div","row");row.style.justifyContent="center";
    var again=el("button","btn ghost","Try again");again.onclick=function(){i=0;score=0;stage.className="card";render();};
    row.appendChild(again);stage.appendChild(row);
    SCORM.complete(passed?"passed":"failed",score,items.length);
  }
  render();
}

/* ===================== FLASHCARDS ===================== */
function runCards(){
  var items=DATA.items||[],id=DATA.id||"lo",seen={};
  var key="ilb:"+id;var box={};try{box=JSON.parse(localStorage.getItem(key)||"{}");}catch(e){box={};}
  function save(){try{localStorage.setItem(key,JSON.stringify(box));}catch(e){}}
  function mastered(){var m=0;items.forEach(function(_,k){if((box[k]||0)>=2)m++;});return m;}
  var order=items.map(function(_,k){return k;}).sort(function(a,b){return (box[a]||0)-(box[b]||0);});
  var pos=0;
  function render(){
    if(pos>=order.length){return done();}
    var k=order[pos],c=items[k];
    counter.textContent="Card "+(pos+1)+" / "+order.length+" · mastered "+mastered()+"/"+items.length;
    setProg(Object.keys(seen).length/items.length);
    stage.className="card deck";stage.innerHTML="";
    var flip=el("div","flip");
    var front=el("div","face front",'<div class="lbl">Prompt</div><div class="txt">'+escapeHtml(c.front)+'</div>'+
        (c.hint?'<div class="hint">Hint: '+escapeHtml(c.hint)+'</div>':''));
    var back=el("div","face back",'<div class="lbl">Answer</div><div class="txt">'+escapeHtml(c.back)+'</div>');
    flip.appendChild(front);flip.appendChild(back);
    flip.onclick=function(){flip.classList.toggle("flipped");rate.style.display=flip.classList.contains("flipped")?"flex":"none";};
    stage.appendChild(flip);
    stage.appendChild(el("div","tap","Tap the card to flip"));
    var rate=el("div","row");rate.style.display="none";
    var review=el("button","btn ghost","Needs review");
    var got=el("button","btn","Got it ✓");
    review.onclick=function(){seen[k]=1;box[k]=0;save();adv();};
    got.onclick=function(){seen[k]=1;box[k]=(box[k]||0)+1;save();adv();};
    rate.appendChild(review);rate.appendChild(got);stage.appendChild(rate);
    function adv(){pos++;render();}
  }
  function done(){
    setProg(1);counter.textContent="Done";stage.className="card result";
    stage.innerHTML='<div class="badge">★ Deck complete</div>'+
      '<div class="verdict">Mastered '+mastered()+' of '+items.length+' cards</div>'+
      '<div class="obj">Come back later — cards you marked “needs review” show first next time (spaced repetition).</div>';
    var row=el("div","row");row.style.justifyContent="center";
    var again=el("button","btn ghost","Review again");
    again.onclick=function(){pos=0;seen={};order=items.map(function(_,k){return k;}).sort(function(a,b){return (box[a]||0)-(box[b]||0);});render();};
    row.appendChild(again);stage.appendChild(row);
    SCORM.complete("completed",mastered(),items.length);
  }
  render();
}

function escapeHtml(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){
  return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}

if(DATA.format==="flashcards")runCards();else runQuiz();
</script>
</body>
</html>
"""

IMSMANIFEST = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="__ID__-manifest" version="1.2"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
    http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata><schema>ADL SCORM</schema><schemaversion>1.2</schemaversion></metadata>
  <organizations default="__ID__-org">
    <organization identifier="__ID__-org">
      <title>__TITLE__</title>
      <item identifier="__ID__-item" identifierref="__ID__-res">
        <title>__TITLE__</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="__ID__-res" type="webcontent" adlcp:scormtype="sco" href="index.html">
      <file href="index.html"/>
    </resource>
  </resources>
</manifest>
"""


def render_html(spec, brand):
    data = json.dumps(spec, ensure_ascii=False)
    # Draft guard: unconfirmed placeholders in the spec get a visible banner
    # (quiz and flashcards alike) so drafts can't ship to learners unnoticed.
    is_draft = ("[CONFIRM:" in data) or ("[PENDING" in data)
    banner = ('  <div class="draftbn">DRAFT &mdash; contains unconfirmed items '
              '([CONFIRM]/[PENDING]). Resolve with the SME before releasing to learners.</div>'
              if is_draft else "")
    return (HTML_TEMPLATE
            .replace("__DRAFT_BANNER__", banner)
            .replace("__TITLE__", html.escape(spec.get("title", "Learning Object")))
            .replace("__PRIMARY__", brand["primary"])
            .replace("__ACCENT__", brand["accent"])
            .replace("__FONT__", brand["font"])
            .replace("__FOOTER__", html.escape(brand["footer"]))
            .replace("/*__DATA__*/", data))


def build_scorm(outdir, oid, title, html_str):
    manifest = (IMSMANIFEST
                .replace("__ID__", oid)
                .replace("__TITLE__", html.escape(title)))
    zpath = Path(outdir) / (oid + "_scorm.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("index.html", html_str)
        z.writestr("imsmanifest.xml", manifest)
    return zpath


def main():
    ap = argparse.ArgumentParser(description="Render a learning object to interactive HTML (+ optional SCORM).")
    ap.add_argument("--spec", required=True, help="learning_object.json")
    ap.add_argument("--context", help="project context json (for brand/project name)")
    ap.add_argument("--outdir", default="OUT")
    ap.add_argument("--scorm", action="store_true", help="also emit a SCORM 1.2 zip")
    a = ap.parse_args()

    spec = load_json(a.spec)
    ctx = load_json(a.context) if a.context and Path(a.context).exists() else {}
    brand = brand_from_context(ctx)

    fmt = spec.get("format", "quiz")
    if fmt not in ("quiz", "flashcards"):
        raise SystemExit('format must be "quiz" or "flashcards" (got %r)' % fmt)
    if not spec.get("items"):
        raise SystemExit("spec has no items")
    oid = spec.get("id", "learning-object")

    Path(a.outdir).mkdir(parents=True, exist_ok=True)
    html_str = render_html(spec, brand)
    hpath = Path(a.outdir) / (oid + ".html")
    hpath.write_text(html_str, encoding="utf-8")
    print("HTML  ->", hpath)

    if a.scorm:
        zpath = build_scorm(a.outdir, oid, spec.get("title", oid), html_str)
        print("SCORM ->", zpath)


if __name__ == "__main__":
    main()
