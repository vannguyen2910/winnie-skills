#!/usr/bin/env python3
"""Self-check: python3 test_friction.py"""
import friction as f

findings = {"journeys": [{"code": "J1", "title": "Journey 1", "screens": [["a", "Home"], ["b", "Pay"], ["c", "Later"]]}]}
data = {"source": "screenshots", "screens": {
    "J1-01": {"marks": [{"a": "tap", "x": .1, "y": .2, "extra": True},
                        {"a": "swipe", "x": 0, "y": 0, "w": 1, "h": 1, "dir": "up", "times": 2},
                        {"a": "input", "note": "typed off screen", "chars": 6}]},
    "J1-02": {"explore": True, "verified": True, "marks": [{"a": "tap", "x": .5, "y": .5}]}}}
names = f.screen_names(findings)
assert f.check(data, names) == []

bad = {"source": "guess", "screens": {"J9-01": {"marks": [{"a": "hold", "x": 2, "y": 0}, {"a": "tap"}]}}}
assert len(f.check(bad, names)) == 5, f.check(bad, names)

v = f.view(data, findings)
assert v["bands"]["J1"].startswith("Task only: Taps 1 · Swipes 2 · Inputs 1 (6 chars) · Extra 1 · Screens not counted: 1"), v["bands"]
assert "Exploration, counted separately: Taps 1" in v["bands"]["J1"] and "Screens to verify: 1" in v["bands"]["J1"]
assert v["screens"]["J1-01"]["offs"] == ["Off screenshot, In · 6 chars: typed off screen"]

board = "<body><script>let x = 1, bottom = top + SH;</script></body>"
once = f.inject(board, v)
assert f.inject(once, v) == once and once.count(f.START) == 1, "running twice must not stack layers"
for broken in ("<body></body>", "const FRICTION = {};" + board):
    try:
        f.inject(broken, v); raise AssertionError("should refuse: " + broken)
    except ValueError:
        pass

md = "# T\n\n## Friction counts\n\nold\n\n## After\n\nkeep\n"
new = f.section(data, findings, "../b.html")
out = f.put_section(md, new)
assert "old" not in out and "## After\n\nkeep" in out and f.put_section(out, new) == out
assert f.put_section("# T\n", new).count("## Friction counts") == 1
assert "| **Total** | **1** | **2** | **1 (6 chars)** | **1** | |" in new and "| **Total explored** | **1** | **0** | **0** | |" in new
print("ok")
