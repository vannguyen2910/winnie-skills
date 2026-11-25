#!/usr/bin/env python3
"""Build the heuristic-evaluation whiteboard (one HTML file) from a findings JSON.

Usage:
  python3 build_whiteboard.py findings.json --out-dir work/heuristic-whiteboard [--assets-dir work/assets] [--no-embed]

Reads templates/whiteboard.html (next to this script's parent folder), checks the JSON,
embeds small fallback copies of the screenshots (needs macOS `sips`), writes
<out-dir>/heuristic-whiteboard.html and, if missing, <out-dir>/index.md.
"""
import argparse, base64, glob, html, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "templates", "whiteboard.html")
PRI = {"P1": "Visibility of system status", "P2": "Match between system and the real world", "P3": "User control and freedom",
       "P4": "Consistency and standards", "P5": "Error prevention", "P6": "Recognition rather than recall",
       "P7": "Flexibility and efficiency of use", "P8": "Aesthetic and minimalist design",
       "P9": "Help users recognise, diagnose and recover from errors", "P10": "Help and documentation"}
PRINCIPLES = set(PRI)
EMBED_WIDTH, EMBED_QUALITY, SIZE_WARN_KB = 200, 38, 600  # the Claude preview refuses files above roughly 0.7 MB


def check(d):
    errs = []
    screens = {}
    for j in d["journeys"]:
        for i, (file, label) in enumerate(j["screens"], 1):
            screens[f'{j["code"]}-{i:02d}'] = (j["dir"], file)
    seen = set()
    for f in d["findings"]:
        tag = f'finding {f.get("n")}'
        if f["n"] in seen: errs.append(f"{tag}: duplicate number")
        seen.add(f["n"])
        if f["sev"] not in (0, 1, 2, 3, 4): errs.append(f"{tag}: severity must be 0 to 4")
        if f["at"] not in screens: errs.append(f'{tag}: unknown screen "{f["at"]}" in "at"')
        for c in f["pr"]:
            if c not in PRINCIPLES: errs.append(f"{tag}: unknown principle {c} (use P1 to P10)")
        if not f["pins"]: errs.append(f"{tag}: needs at least one pin")
        for s, x, y in f["pins"]:
            if s not in screens: errs.append(f'{tag}: unknown pin screen "{s}"')
            if not (0 <= x <= 1 and 0 <= y <= 1): errs.append(f"{tag}: pin {s} x,y must be between 0 and 1")
        for k in ("t", "where", "sees"):
            if not f.get(k): errs.append(f"{tag}: missing {k}")
    return screens, errs


def check_md(d, md_path):
    """Compare the finding rows of the markdown (tag, principle names, severity) with the JSON."""
    rows = {}
    for line in open(md_path, encoding="utf-8"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 7 and re.fullmatch(r"UX-\d+", c[0]):
            rows[int(c[0][3:])] = (c[4], c[5])
    errs = []
    want = {f["n"]: f for f in d["findings"]}
    for n in sorted(set(rows) | set(want)):
        tag = f"UX-{n:02d}"
        if n not in rows: errs.append(f"{tag} is in the JSON but not in the markdown"); continue
        if n not in want: errs.append(f"{tag} is in the markdown but not in the JSON"); continue
        names, sev = rows[n]
        if sev != str(want[n]["sev"]): errs.append(f"{tag}: severity is {sev} in the markdown but {want[n]['sev']} in the JSON")
        json_names = "; ".join(PRI[c] for c in want[n]["pr"])
        if names != json_names: errs.append(f'{tag}: principle is "{names}" in the markdown but "{json_names}" in the JSON')
    return errs


def embed(d, assets_dir):
    if not shutil.which("sips"):
        print("warning: `sips` not found, no fallback images embedded (the board then needs the assets folder to load)")
        return {}
    out, tmp = {}, tempfile.mkdtemp()
    for j in d["journeys"]:
        for file, _ in j["screens"]:
            key = f'{j["dir"]}/{file}.jpg'
            src = os.path.join(assets_dir, key)
            if not os.path.exists(src):
                print(f"warning: missing image {src}")
                continue
            dst = os.path.join(tmp, key.replace("/", "__"))
            subprocess.run(["sips", "--resampleWidth", str(EMBED_WIDTH), "-s", "formatOptions", str(EMBED_QUALITY), src, "--out", dst],
                           check=True, capture_output=True)
            out[key] = "data:image/jpeg;base64," + base64.b64encode(open(dst, "rb").read()).decode()
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def js(obj):  # safe inside <script>
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--assets-dir")
    ap.add_argument("--no-embed", action="store_true")
    ap.add_argument("--check-md", help="markdown file to compare with the JSON (default: <out-dir>/../heuristic-evaluation.md if it exists)")
    ap.add_argument("--no-check", action="store_true", help="skip the markdown comparison")
    a = ap.parse_args()
    d = json.load(open(a.data, encoding="utf-8"))
    _, errs = check(d)
    if errs:
        print("Fix these first:\n- " + "\n- ".join(errs)); sys.exit(1)
    md = a.check_md or os.path.join(a.out_dir, "..", "heuristic-evaluation.md")
    drift = [] if a.no_check or not os.path.exists(md) else check_md(d, md)
    os.makedirs(a.out_dir, exist_ok=True)
    assets = a.assets_dir or os.path.join(a.out_dir, "..", "assets")
    imgs = {} if a.no_embed else embed(d, assets)
    t = open(TEMPLATE, encoding="utf-8").read()
    t = t.replace("__TITLE__", html.escape(d["title"])).replace("__DATA__", js(d)).replace("__IMGS__", js(imgs))
    out = os.path.join(a.out_dir, "heuristic-whiteboard.html")
    open(out, "w", encoding="utf-8").write(t)
    kb = os.path.getsize(out) // 1024
    print(f"wrote {out} ({kb} KB, {len(d['findings'])} findings, {len(imgs)} embedded images)")
    if kb > SIZE_WARN_KB: print(f"warning: above {SIZE_WARN_KB} KB, the Claude preview pane may refuse to open it (a normal browser is fine)")
    idx = os.path.join(a.out_dir, "index.md")
    if not os.path.exists(idx):
        n = len(d["findings"])
        open(idx, "w", encoding="utf-8").write(f'''---
type: "heuristic-evaluation"
title: "Heuristic evaluation whiteboard"
stage: "Discover"
status: "draft"
summary: "A whiteboard of the screens grouped by journey. Each usability problem is one sticky note with a pin on the exact spot of the screen. Pan and zoom to explore. Draft: findings are not yet checked by the owner."
supports: []
embed: true
media:
  - "heuristic-whiteboard.html"
---

# Heuristic evaluation whiteboard

The same {n} findings as in `work/heuristic-evaluation.md`, drawn on a board. Each sticky note holds one finding: where on the screen, what the user sees, the heuristic and the severity. The numbered pin marks the spot. Note colour shows severity.

**How to use it:** scroll or drag to move, Ctrl or ⌘ plus scroll (or pinch) to zoom, click a note or pin to follow it, use the Journey list to filter, press 0 to fit all.

For sharp screenshots open the file in a normal browser. The screenshots are read from `work/assets/`, so keep that folder next to this one.
''')
        print(f"wrote {idx}")
    if drift:
        print(f"\nThe markdown ({os.path.normpath(md)}) and the JSON disagree. Update both so they match, then rebuild:\n- " + "\n- ".join(drift))
        sys.exit(2)
    if os.path.exists(md) and not a.no_check: print("markdown and JSON agree")


if __name__ == "__main__":
    main()
