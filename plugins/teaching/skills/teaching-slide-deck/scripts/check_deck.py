#!/usr/bin/env python3
"""Check a downloaded Slides deck for the rules a machine can verify.

    python3 check_deck.py <project dir with deck.json and slides/>
    python3 check_deck.py --self-test

Exits 1 when there is an ERROR. Looks are not checked: preview them separately.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

DARK = ("#1a1325", "#4a24c4", "#6b3fee", "var(--ink)", "var(--purple)", "var(--purple-deep)", "var(--sienna)")
YELLOW = ("#f5d028", "var(--yellow)", "var(--ochre)")
DIVIDER_ID = re.compile(r"^(divider|d\d)")


def background(section_tag):
    m = re.search(r"(?<![-\w])background(?:-color)?\s*:\s*([^;\"]+)", section_tag)
    return m.group(1).strip().lower() if m else ""


def check(project):
    project = Path(project)
    deck = json.loads((project / "deck.json").read_text(encoding="utf-8"))
    inline = "format" not in deck
    out, visible = [], []
    for sid in deck["order"]:
        path = project / "slides" / f"{sid}.html"
        if not path.exists():
            out.append(("ERROR", sid, "listed in deck.json but the file is not here"))
            visible.append((sid, ""))
            continue
        text = path.read_text(encoding="utf-8")
        body = re.sub(r"<aside>.*?</aside>", "", text, flags=re.S)
        opens, closes = len(re.findall(r"<div\b", text)), text.count("</div>")
        if opens != closes:
            out.append(("ERROR", sid, f"{opens} <div> but {closes} </div>"))
        sections = re.findall(r"<section\b[^>]*>", body)
        if len(sections) != 1 or f'id="{sid}"' not in (sections[0] if sections else ""):
            out.append(("ERROR", sid, f'needs exactly one <section id="{sid}">'))
            continue
        hidden = bool(re.search(r"\shidden[\s>=]", sections[0]))
        bg = background(sections[0]) if inline else ""
        if bg.startswith(YELLOW) and not DIVIDER_ID.match(sid):
            out.append(("WARN" if hidden else "ERROR", sid, "yellow background is only for section dividers"))
        if not hidden:
            visible.append((sid, bg))
        if not inline:
            continue
        no_svg = re.sub(r"<svg\b.*?</svg>", "", body, flags=re.S)
        for size in re.findall(r"font-size\s*:\s*([\d.]+)px", no_svg):
            if float(size) < 24:
                out.append(("ERROR", sid, f"font-size {size}px is under 24px"))
        styles = " ".join(re.findall(r'style="([^"]*)"', body))
        for pattern, what in ((r"var\(", "var()"), (r"repeat\(", "repeat()"), (r"minmax\(", "minmax()"),
                              (r"[\d.](?:em|rem)\b(?!\w)", "em or rem unit")):
            if what == "em or rem unit":
                hit = re.search(r":\s*-?[\d.]+(?:em|rem)\b", styles) and not re.search(r"letter-spacing\s*:\s*-?[\d.]+em", styles)
            else:
                hit = re.search(pattern, styles)
            if hit:
                out.append(("ERROR", sid, f"{what} is not supported in an inline deck"))
        if re.search(r"max-width\s*:", styles):
            out.append(("WARN", sid, "max-width: use width in an inline deck"))
        for style in re.findall(r'style="([^"]*position\s*:\s*absolute[^"]*)"', body):
            top = re.search(r"(?<![-\w])top\s*:\s*([\d.]+)px", style)
            height = re.search(r"(?<![-\w])height\s*:\s*([\d.]+)px", style)
            if top and height:
                bottom = float(top.group(1)) + float(height.group(1))
                if bottom > 1080:
                    out.append(("ERROR", sid, f"pinned block ends at {bottom:g}px, off the 1080px canvas"))
                elif bottom > 952:
                    out.append(("WARN", sid, f"pinned block ends at {bottom:g}px, past the 952px margin"))
    for (a, bg_a), (b, bg_b) in zip(visible, visible[1:]):
        if bg_a.startswith(DARK) and bg_b.startswith(DARK):
            out.append(("ERROR", b, f"dark background right after dark slide {a}"))
    if not inline:
        out.append(("WARN", "deck", "deck has a format key: colour, font and CSS checks were skipped"))
    return out


def self_test():
    def run(slides):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "slides").mkdir()
            (root / "deck.json").write_text(json.dumps({"order": list(slides)}))
            for sid, html in slides.items():
                (root / "slides" / f"{sid}.html").write_text(html)
            return check(root)

    def slide(sid, bg="#ffffff", inner="", attrs=""):
        return f'<section id="{sid}"{attrs} style="background:{bg}">{inner}<aside>n</aside></section>'

    clean = run({"cover": slide("cover"), "divider-01": slide("divider-01", "#f5d028"),
                 "q": slide("q", "#1a1325"), "skip": slide("skip", "#4a24c4", attrs=" hidden"),
                 "w": slide("w")})
    assert clean == [], clean
    bad = run({
        "a": slide("a", "#1a1325"),
        "b": slide("b", "#4a24c4"),
        "c": slide("c", "#f5d028"),
        "d": slide("d", inner='<div><p style="font-size:18px">x</p>'),
        "e": slide("e", inner='<div style="position:absolute; top:900px; height:300px; width:var(--w)"></div>'),
    })
    found = " | ".join(f"{s}:{m}" for level, s, m in bad if level == "ERROR")
    for needle in ("b:dark background", "c:yellow", "d:1 <div> but 0", "d:font-size 18px", "e:pinned block", "e:var()"):
        assert needle in found, (needle, found)
    print("self-test ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    elif len(sys.argv) == 2:
        results = check(sys.argv[1])
        for level, sid, message in results:
            print(f"{level:5} {sid}: {message}")
        errors = sum(level == "ERROR" for level, _, _ in results)
        print(f"\n{errors} ERROR, {len(results) - errors} WARN")
        sys.exit(1 if errors else 0)
    else:
        print(__doc__)
        sys.exit(2)
