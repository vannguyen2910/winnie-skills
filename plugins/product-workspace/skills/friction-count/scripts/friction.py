#!/usr/bin/env python3
"""Add the friction layer to the heuristic whiteboard and write the count tables.

  python3 friction.py work/heuristic-evaluation/friction.json --md work/task-analysis/index.md

Reads findings.json (journeys and screen names) and heuristic-whiteboard.html next to friction.json.
Run it again after the whiteboard is rebuilt: the layer is replaced, never stacked.
Without --md only the board is written. Format of friction.json: ../references/friction-data.md
"""
import argparse, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADDON = os.path.join(HERE, "..", "templates", "friction-layer.html")
START, END = "<!-- friction:start -->", "<!-- friction:end -->"
ANCHOR = re.compile(r"bottom = top \+ SH(?: \+ \d+ /\*friction\*/)?;")
ARROW = {"up": "↑", "down": "↓", "left": "←", "right": "→"}
SOURCES = {
    "recording": "Drafted by AI from a screen recording. Touches are not shown in the recording, so taps and swipes are inferred from screen changes.",
    "screenshots": "**Estimates, not measurements.** Drafted by AI from screenshots, not from a recording. Only actions that the screens give evidence of are counted, so the real numbers are probably higher, especially swipes.",
}


def screen_names(findings):
    return {f'{j["code"]}-{i:02d}': label for j in findings["journeys"] for i, (_, label) in enumerate(j["screens"], 1)}


def check(data, names):
    errs = []
    if data.get("source") not in SOURCES:
        errs.append('"source" must be "recording" or "screenshots"')
    for sid, e in data.get("screens", {}).items():
        if sid not in names:
            errs.append(f"{sid}: unknown screen")
        for i, m in enumerate(e.get("marks", []), 1):
            at, a = f"{sid} mark {i}", m.get("a")
            if a not in ("tap", "swipe", "input"):
                errs.append(f"{at}: action must be tap, swipe or input")
            if "x" not in m:
                if not m.get("note"): errs.append(f"{at}: needs a position, or a note if it is off screenshot")
            else:
                keys = ("x", "y") if a == "tap" else ("x", "y", "w", "h")
                if not all(isinstance(m.get(k), (int, float)) and 0 <= m[k] <= 1 for k in keys):
                    errs.append(f"{at}: {', '.join(keys)} must be fractions from 0 to 1")
            if a == "swipe" and m.get("dir") not in ARROW: errs.append(f"{at}: dir must be up, down, left or right")
            if not (isinstance(m.get("times", 1), int) and m.get("times", 1) > 0): errs.append(f"{at}: times must be 1 or more")
            if not (isinstance(m.get("chars", 0), int) and m.get("chars", 0) >= 0): errs.append(f"{at}: chars must be 0 or more")
            if m.get("extra") and e.get("explore"): errs.append(f"{at}: an exploration screen has no extra steps")
        if "marks" not in e: errs.append(f'{sid}: needs "marks" ([] means counted, no actions)')
    return errs


def count(marks):
    c = dict(tap=0, swipe=0, input=0, chars=0, extra=0)
    for m in marks:
        n = m.get("times", 1) if m["a"] == "swipe" else 1
        c[m["a"]] += n
        if m["a"] == "input": c["chars"] += m.get("chars", 0)
        if m.get("extra"): c["extra"] += n
    return c


def totals(entries):
    t = count([])
    for e in entries:
        for k, v in count(e["marks"]).items(): t[k] += v
    return t


def labels(marks):
    out, taps = [], 0
    for m in marks:
        if m["a"] == "tap":
            taps += 1; out.append(f"T{taps}")
        elif m["a"] == "swipe":
            out.append("S " + ARROW[m["dir"]] + (f' ×{m["times"]}' if m.get("times", 1) > 1 else ""))
        else:
            out.append("In" + (f' · {m["chars"]} chars' if m.get("chars") else ""))
    return out


def inputs(c):
    return f'{c["input"]} ({c["chars"]} chars)' if c["chars"] else str(c["input"])


def view(data, findings):
    """Everything the board shows, already counted, so the page only draws."""
    screens, bands = {}, {}
    for sid, e in data["screens"].items():
        c, explore = count(e["marks"]), bool(e.get("explore"))
        lines = [f'Tap {c["tap"]} · Swipe {c["swipe"]}', f"Input {inputs(c)}" + ("" if explore else f' · Extra {c["extra"]}')]
        offs = [f'Off screenshot, {l}{" + EXTRA" if m.get("extra") else ""}: {m["note"]}'
                for m, l in zip(e["marks"], labels(e["marks"])) if "x" not in m]
        screens[sid] = dict(explore=explore, lines=lines, offs=offs, status="Verified" if e.get("verified") is True else "To verify",
                            marks=[dict(m, label=l) for m, l in zip(e["marks"], labels(e["marks"])) if "x" in m])
    for j in findings["journeys"]:
        ids = [f'{j["code"]}-{i:02d}' for i in range(1, len(j["screens"]) + 1)]
        have = [data["screens"][i] for i in ids if i in data["screens"]]
        if not have:
            bands[j["code"]] = "Friction not counted yet"; continue
        main = totals([e for e in have if not e.get("explore")])
        ex = [e for e in have if e.get("explore")]
        text = ("Task only: " if ex else "") + f'Taps {main["tap"]} · Swipes {main["swipe"]} · Inputs {inputs(main)} · Extra {main["extra"]}'
        if len(ids) > len(have): text += f" · Screens not counted: {len(ids) - len(have)}"
        if ex:
            x = totals(ex)
            text += f'   |   Exploration, counted separately: Taps {x["tap"]} · Swipes {x["swipe"]} · Inputs {inputs(x)}'
        todo = sum(e.get("verified") is not True for e in have)
        if todo: text += f"   |   Screens to verify: {todo}"
        bands[j["code"]] = text
    return dict(source=data["source"], screens=screens, bands=bands)


def room(v):
    """Pixels needed under a screen for its strip (generous estimate, about 30 characters per note line)."""
    return max([115 + 20 * s["explore"] + sum(6 + 19 * math.ceil(len(o) / 30) for o in s["offs"]) for s in v["screens"].values()] or [115])


def inject(board, v):
    if "const FRICTION" in board:
        raise ValueError("this board has hand-written friction code: rebuild it with the heuristic-evaluation script first")
    board = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", board, flags=re.S)
    board, n = ANCHOR.subn(f"bottom = top + SH + {room(v)} /*friction*/;", board)
    if n != 1 or "</body>" not in board:
        raise ValueError("the whiteboard layout is not the one this script knows; check the heuristic-evaluation template")
    data = json.dumps(v, ensure_ascii=False).replace("</", "<\\/")
    layer = open(ADDON, encoding="utf-8").read().replace("__FRICTION__", data)
    head, tail = board.rsplit("</body>", 1)
    return f"{head}{START}\n{layer}{END}\n</body>{tail}"


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def section(data, findings, board_link):
    names = screen_names(findings)
    ids = [i for i in names if i in data["screens"]]
    done = sum(data["screens"][i].get("verified") is True for i in ids)
    out = ["## Friction counts", "", SOURCES[data["source"]] + f" {done} of {len(ids)} counted screens are verified. They describe the current experience only.", "",
           "| Measure | Counts as 1 |", "|---|---|", "| Tap | One touch that triggers something |", "| Swipe | One scroll or swipe gesture |",
           "| Input | One field filled, with the typed characters |", "| Extra step | Any action the task could be done without. It is already included in the other columns |", ""]
    if data.get("remarks"): out += [data["remarks"], ""]
    out += [f"The markers on each screen are on the [whiteboard]({board_link}): choose the Friction view.", ""]
    for j in findings["journeys"]:
        mine = [i for i in ids if i.split("-")[0] == j["code"]]
        if not mine: continue
        meta = data.get("journeys", {}).get(j["code"], {})
        out += ["### " + meta.get("title", j["title"]), ""]
        if meta.get("goal"): out += [f'**Goal used for extra steps:** {meta["goal"]}.', ""]
        for explore in (False, True):
            group = [i for i in mine if bool(data["screens"][i].get("explore")) == explore]
            if not group: continue
            if explore: out += ["**Exploration, not part of the task** (do not add these to the total above)", ""]
            extra = [] if explore else ["Extra"]
            head = ["Screen", "Tap", "Swipe", "Input", *extra, "Note"]
            out += ["| " + " | ".join(head) + " |", "|---" * len(head) + "|"]
            for i in group:
                e = data["screens"][i]; c = count(e["marks"])
                row = [f'{i[-2:]} {names[i]}', c["tap"], c["swipe"], inputs(c), *([] if explore else [c["extra"]]), e.get("note", "")]
                out.append("| " + " | ".join(cell(x) for x in row) + " |")
            t = totals([data["screens"][i] for i in group])
            row = ["Total explored" if explore else "Total", t["tap"], t["swipe"], inputs(t), *([] if explore else [t["extra"]])]
            out.append("| " + " | ".join(f"**{x}**" for x in row) + " | |")
            out.append("")
        missing = sum(i.split("-")[0] == j["code"] for i in names) - len(mine)
        if missing: out += [f"Screens not counted yet: {missing}.", ""]
    return "\n".join(out)


def put_section(text, new):
    """Replace the existing section (up to the next level-2 heading) or add it at the end."""
    found = re.search(r"^## Friction counts[ \t]*$.*?(?=^## |\Z)", text, flags=re.M | re.S)
    if found: return text[:found.start()] + new + "\n" + text[found.end():]
    return text.rstrip("\n") + "\n\n" + new


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", help="friction.json")
    ap.add_argument("--md", help="markdown file that gets the '## Friction counts' section")
    a = ap.parse_args()
    folder = os.path.dirname(os.path.abspath(a.data))
    board_path = os.path.join(folder, "heuristic-whiteboard.html")
    try:
        data = json.load(open(a.data, encoding="utf-8"))
        findings = json.load(open(os.path.join(folder, "findings.json"), encoding="utf-8"))
        errs = check(data, screen_names(findings))
        if errs: sys.exit("Fix these first:\n- " + "\n- ".join(errs))
        # build both outputs before writing either, so a failure leaves the files as they were
        board = inject(open(board_path, encoding="utf-8").read(), view(data, findings))
        md = None
        if a.md:
            link = os.path.relpath(board_path, os.path.dirname(os.path.abspath(a.md))).replace(os.sep, "/")
            md = put_section(open(a.md, encoding="utf-8").read(), section(data, findings, link))
    except (OSError, ValueError) as err:
        sys.exit(f"Stopped, nothing written: {err}")
    open(board_path, "w", encoding="utf-8").write(board)
    print(f"wrote {board_path}")
    if md is not None:
        open(a.md, "w", encoding="utf-8").write(md)
        print(f"wrote {a.md}")
    for code, text in view(data, findings)["bands"].items(): print(f"{code}: {text}")


if __name__ == "__main__":
    main()
