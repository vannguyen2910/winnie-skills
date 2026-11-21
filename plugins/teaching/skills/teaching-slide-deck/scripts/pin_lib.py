"""Click-reveal helpers for inline Slides decks (no `format` key in deck.json).

A reveal needs each block to be `position:absolute` with `data-build-in="rise N"`.
These helpers turn a flow container's direct children into pinned blocks.

    from pin_lib import kids, pin, endof, balanced
    s = open("slide.html", encoding="utf-8").read()
    start = s.index('<div style="display:grid')          # the container to replace
    end = endof(s, start)
    el = s[start:end]
    cards = [el[a:b] for a, b in kids(el, el.index(">") + 1)]
    pinned = "\n".join(pin(c, 96 + 584 * i, 330, 560, 440, i + 1, drop=[r"flex:1;?"]) for i, c in enumerate(cards))
    s = s[:start] + pinned + s[end:]
    assert balanced(s)

Only <div> and <svg> children are returned by kids(); wrap a lone <p> in a <div style="margin:0"> first.
"""
import re

_TAG = re.compile(r"<(/?)(div|svg)\b[^>]*?(/?)>", re.S)


def endof(s, start):
    """Index just after the element that opens at s[start] (div or svg)."""
    name = re.match(r"<(div|svg)\b", s[start:]).group(1)
    depth = 0
    for m in re.finditer(r"<(/?)%s\b[^>]*?(/?)>" % name, s[start:], re.S):
        if m.group(2) == "/":
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced element")


def kids(s, open_end):
    """(start, end) of each direct <div>/<svg> child of the container whose content begins at open_end."""
    out, i = [], open_end
    while True:
        m = re.compile(r"\s*(</[a-z0-9]+>|<(div|svg)\b)", re.S).match(s, i)
        if not m:
            # skip over other tags/text (p, span, comments)
            nxt = re.compile(r"<(div|svg)\b|</div>", re.S).search(s, i)
            if not nxt:
                return out
            i = nxt.start()
            m = re.compile(r"(</div>|<(div|svg)\b)").match(s, i)
        if m.group(1).startswith("</"):
            return out
        a = m.start(1)
        b = endof(s, a)
        out.append((a, b))
        i = b


def pin(el, left, top, width, height=None, order=None, drop=()):
    """Return `el` (a <div>/<svg> string) pinned at left/top/width(/height), with click order `order`."""
    m = re.match(r"<(div|svg)\b([^>]*)>", el, re.S)
    tag, attrs = m.group(1), m.group(2)
    sm = re.search(r'style="([^"]*)"', attrs)
    style = sm.group(1) if sm else ""
    for pat in drop:
        style = re.sub(pat, "", style)
    geo = "box-sizing:border-box; position:absolute; left:%dpx; top:%dpx; width:%dpx;" % (left, top, width)
    if height:
        geo += " height:%dpx;" % height
    rest = style.strip().strip(";").strip()
    style = geo + (" " + rest + ";" if rest else "")
    attrs = re.sub(r'\s*style="[^"]*"', "", attrs)
    attrs = attrs.rstrip().rstrip("/")
    attrs += ' style="%s"' % style
    if order:
        attrs += ' data-build-in="rise %d"' % order
    return "<%s%s>" % (tag, attrs) + el[m.end():]


def balanced(s):
    return len(re.findall(r"<div\b", s)) == len(re.findall(r"</div>", s))
