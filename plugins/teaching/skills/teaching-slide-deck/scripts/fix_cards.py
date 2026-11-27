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

COLOR = re.compile(r'(?<![-\w])(color:\s*)(#[0-9a-fA-F]{3,8}|white\b)', re.I)
OWN_BG = re.compile(r'(?<![-\w])background(?:-color)?:\s*(?!#fff(?:fff)?\b|white\b|none\b|transparent\b)[#\w]', re.I)
VOID = {"br", "img", "hr", "input"}

def light_text(tag, is_card):
    """Đổi chữ trắng hoặc vàng trong một thẻ sang màu đọc được trên nền trắng."""
    fs = re.search(r'font-size:\s*(\d+)px', tag)
    size = int(fs.group(1)) if fs else 28
    def rc(m):
        c = m.group(2).lower()
        if c in ("#fff", "#ffffff", "#ffffffcc", "white"):
            return m.group(1) + ("#1A1325" if is_card or size >= 34 else "#3D3552")
        if c == "#f5d028":
            return m.group(1) + ("#6B3FEE" if "Syne" in tag else "#4A24C4")
        return m.group(0)
    return COLOR.sub(rc, tag)

def to_light(sub):
    sub = BG.sub('background:#FFFFFF', sub, count=1)
    stack = []  # (tên thẻ, đang nằm trong khối có nền riêng)
    def walk(m):
        tag, name = m.group(0), m.group(2).lower()
        if m.group(1):  # thẻ đóng
            while stack and stack.pop()[0] != name:
                pass
            return tag
        is_card = not stack
        keep = bool(stack) and (stack[-1][1] or bool(OWN_BG.search(tag)))
        if name not in VOID and not tag.endswith("/>"):
            stack.append((name, keep))
        return tag if keep else light_text(tag, is_card)
    sub = re.sub(r'<(/?)([a-zA-Z][\w-]*)[^>]*>', walk, sub)
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

def self_test():
    card = ('<div style="width:848px; height:280px; border-radius:22px; background:#1a1325; color:#fff">'
            '<p style="font-size:24px;color:#fff">Probe</p><p style="font-size:28px;color:#FFF">a</p>'
            '<h3 style="font-size:40px;color:#ffffff">b</h3><ul><li style="color: white">c</li></ul>'
            '<p style="font-size:28px">d <span style="color:#ffffffcc">e</span></p>'
            '<div style="background:#4a24c4"><p style="color:#fff">pill</p></div>'
            '<p style="font-size:24px;color:#F5D028">f</p></div>')
    out = to_light(card)
    inside_pill = '<div style="background:#4a24c4"><p style="color:#fff">pill</p></div>'
    assert inside_pill in out, "chữ trắng trên khối nền đậm trong card phải giữ nguyên:\n" + out
    left = re.findall(r'(?<![-\w])color:\s*(?:#fff(?:fff(?:cc)?)?(?![0-9a-f])|white\b)', out.replace(inside_pill, ''), re.I)
    assert not left, f"còn chữ trắng trên card trắng: {left}\n{out}"
    assert 'color:#1A1325">Probe' not in out and 'color:#3D3552">Probe' in out, out
    assert 'color:#1A1325">b' in out and 'color:#4A24C4">f' in out, out
    assert out.startswith('<div') and 'background:#FFFFFF; color:#1A1325"' in out, out
    print("self-test ok")

def main():
    if sys.argv[1:] == ["--self-test"]:
        return self_test()
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
