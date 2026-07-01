#!/usr/bin/env python3
"""
gen_tom_icons.py — (OPTIONAL) regenerate the six TOM Agent capability icons as
transparent PNGs (Direction B: navy->cyan gradient line). The icons are already
bundled in assets/icons/, so this is only needed to change their style/color.

Renders each icon via a headless Chromium-family browser (probes chrome/chromium/
edge across platforms). If no browser is found, it exits cleanly and the bundled
PNGs remain in place. Cross-platform; stdlib only.

Output -> ../assets/icons/ic_<name>.png
"""
import os, shutil, subprocess, sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent.parent / "assets" / "icons"
SIZE = 360

ICONS = {
    "funnel": '<path d="M4 5h16l-6 7v6l-4 1.8v-7.8z"/>'
              '<circle class="f" cx="8.5" cy="3" r=".8"/><circle class="f" cx="12" cy="3" r=".8"/>'
              '<circle class="f" cx="15.5" cy="3" r=".8"/>',
    "map": '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>'
           '<circle class="f" cx="15" cy="11" r="1.3"/>',
    "shapes": '<rect x="3" y="11.5" width="8.5" height="8.5" rx="1.2"/>'
              '<circle cx="16.2" cy="15.7" r="4.3"/><path d="M11 3l3.8 6H7.2z"/>',
    "ranking": '<path d="M5 20V8M11 20V4M17 20v-8"/><path d="M20.5 6.5l1 1-1 1"/>',
    "discover": '<circle cx="10" cy="10.5" r="6"/><path d="M14.5 15L20.5 21"/>'
                '<path class="f" d="M18.5 2.2l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
    "output": '<path d="M6 3h8l4.5 4.5V21H6z"/><path d="M14 3v4.5h4.5"/>'
              '<path d="M9 12.5h6M9 15.5h6M9 18.5h4"/>'
              '<path class="f" d="M19.5 1.8l.6 1.6 1.6.6-1.6.6-.6 1.6-.6-1.6-1.6-.6 1.6-.6z"/>',
}

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;background:transparent}}
.wrap{{width:{sz}px;height:{sz}px;display:flex;align-items:center;justify-content:center}}
svg{{width:{inner}px;height:{inner}px;fill:none;stroke:url(#grad);stroke-width:1.7;
     stroke-linecap:round;stroke-linejoin:round;color:#12ABDB;overflow:visible}}
.f{{fill:currentColor;stroke:none}}
</style></head><body><div class="wrap">
<svg viewBox="0 0 24 24"><defs><linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0E2841"/><stop offset="1" stop-color="#12ABDB"/></linearGradient></defs>
{inner_svg}</svg></div></body></html>"""

CANDIDATES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

def find_browser():
    for c in CANDIDATES:
        if os.path.sep in c or (":" in c):
            if os.path.exists(c):
                return c
        else:
            p = shutil.which(c)
            if p:
                return p
    return None

def main():
    ASSET.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    if not browser:
        print("No Chromium-family browser found; keeping the bundled icons in", ASSET)
        return
    for name, inner in ICONS.items():
        html_path = ASSET / f"_{name}.html"
        png_path = ASSET / f"ic_{name}.png"
        html_path.write_text(HTML.format(sz=SIZE, inner=int(SIZE * 0.84), inner_svg=inner), encoding="utf-8")
        subprocess.run([
            browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--window-size={SIZE},{SIZE}", "--default-background-color=00000000",
            f"--screenshot={png_path}", html_path.as_uri(),
        ], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  {'OK ' if png_path.exists() else 'FAIL'} {png_path.name}")
        html_path.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
