#!/usr/bin/env python3
"""Đưa card nền đen, vàng hoặc tím nhạt về trắng khi chúng nằm trong một hàng card.
Dùng: python3 fix_cards.py <thư mục slides> [--apply]
Không có --apply thì chỉ báo. Card đứng một mình (node gốc của sơ đồ) bị bỏ qua và được liệt kê."""
import re, sys, pathlib

BG = re.compile(r'background:\s*#(1a1325|f5d028|eae0ff)', re.I)
CARD = re.compile(r'<div[^>]*border-radius:\s*22px[^>]*>', re.I)

def span(t, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', t[start:]):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            return start, start + m.end()
    raise ValueError("div không cân")

def to_light(sub):
    sub = BG.sub('background:#FFFFFF', sub, count=1)
    def p(m):
        tag = m.group(0)
        fs = re.search(r'font-size:(\d+)px', tag)
        size = int(fs.group(1)) if fs else 28
        def rc(mm):
            c = mm.group(1).lower()
            if c in ("ffffff", "ffffffcc"):
                return "color:#" + ("1A1325" if size >= 34 else "3D3552")
            if c == "f5d028":
                return "color:#6B3FEE" if "Syne" in tag else "color:#4A24C4"
            return mm.group(0)
        return re.sub(r'color:#([0-9a-fA-F]{6,8})', rc, tag)
    sub = re.sub(r'<p [^>]*>', p, sub)
    sub = re.sub(r'<h3 [^>]*>', p, sub)
    sub = re.sub(r'fill="#(?:FFFFFF|F5D028|ffffff|f5d028)"', 'fill="#1A1325"', sub)
    return sub.replace("#ffffff66", "#00000026").replace("#FFFFFF66", "#00000026")

def siblings(t, idx):
    """Số card 22px khác cùng top (pinned) hoặc cùng cha trực tiếp."""
    tag = CARD.match(t, idx).group(0)
    top = re.search(r'top:(\d+)px', tag)
    n = 0
    for m in CARD.finditer(t):
        if m.start() == idx:
            continue
        other = re.search(r'top:(\d+)px', m.group(0))
        if top and other and top.group(1) == other.group(1):
            n += 1
    return n

def parent_row_count(t, idx):
    # lùi tới thẻ div cha chưa đóng
    depth = 0
    for m in reversed(list(re.finditer(r'<div\b|</div>', t[:idx]))):
        depth += 1 if m.group(0) == '</div>' else -1
        if depth < 0:
            ps, pe = span(t, m.start())
            inner = t[m.end():pe]
            return len(re.findall(r'<div[^>]*border-radius:\s*22px', inner))
    return 0

def main():
    root, apply = pathlib.Path(sys.argv[1]), "--apply" in sys.argv
    for p in sorted(root.glob("*.html")):
        t = p.read_text(); changed = 0; skipped = 0
        pos = 0
        while True:
            m = next((x for x in CARD.finditer(t, pos) if BG.search(x.group(0))), None)
            if not m:
                break
            s, e = span(t, m.start())
            pos = m.end()
            w = re.search(r'(?<!-)width:(\d+)px', m.group(0))
            h = re.search(r'(?<!-)height:(\d+)px', m.group(0))
            if (w and int(w.group(1)) <= 330) or (h and int(h.group(1)) <= 130):
                continue  # node trong sơ đồ, kiểm tay
            wide = w and int(w.group(1)) >= 1000  # dải callout rộng cũng không được nổi riêng
            row = wide or parent_row_count(t, m.start()) >= 2 or siblings(t, m.start()) >= 1
            if not row:
                skipped += 1
                print(f"{p.name}: bỏ qua (đứng một mình, có thể là node gốc) {m.group(0)[:80]}")
                continue
            changed += 1
            if apply:
                t = t[:s] + to_light(t[s:e]) + t[e:]
                pos = s
        if changed:
            print(f"{p.name}: {changed} card {'đã đổi' if apply else 'cần đổi'}")
            if apply:
                p.write_text(t)

main()
