#!/usr/bin/env python3
"""Báo các card không cùng cấp: div bo 22px có nền đen, vàng hoặc tím nhạt.
Dùng: python3 check_cards.py <thư mục slides>. Thoát mã 1 nếu có lỗi.
Node trong sơ đồ (rộng <= 300px) được bỏ qua; kiểm tay chỉ một node gốc đen."""
import re, sys, pathlib

BAD = re.compile(r'background:\s*#(1a1325|f5d028|eae0ff)', re.I)
bad = 0
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.html")):
    for m in re.finditer(r'<div[^>]*border-radius:\s*22px[^>]*>', p.read_text()):
        tag = m.group(0)
        w = re.search(r'(?<!-)width:(\d+)px', tag)
        if BAD.search(tag) and not (w and int(w.group(1)) <= 300):
            print(f"{p.name}: card không cùng cấp -> {tag[:110]}")
            bad += 1
sys.exit(1 if bad else 0)
