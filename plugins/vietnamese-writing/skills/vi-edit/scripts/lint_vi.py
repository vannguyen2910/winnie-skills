#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lint tiếng Việt theo quy tắc cứng của vi-voice.

Dùng:
    python3 lint_vi.py <file hoặc thư mục> [...]  [--notes-only] [--slide-only] [--json]

Nhận file .md/.txt (kiểm toàn bộ), file slide .html (tách chữ trên slide và <aside> speaker notes),
hoặc thư mục (quét mọi .html và .md trong đó). Thoát với mã 1 nếu có lỗi mức ERROR.

Chỉ bắt các lỗi máy kiểm được. Giọng văn, độ tự nhiên và việc đọc to vẫn phải do người và skill vi-voice quyết.
"""
import argparse, html, json, os, re, sys

# Bảng "Cụm dịch từ tiếng Anh cần tránh" của vi-voice-rules.md, cộng các cụm đã bị Winnie sửa về sau.
TRANSLATED = [
    "đánh trọng số", "chốt phase", "chốt câu", "AI hỗ trợ ở đâu", "con trỏ về", "trỏ về",
    "ứng viên", "làm mượt", "đào sâu", "kiểm tra chéo", "anonymise", "rút gọn mạnh nhất",
    "tránh tốn", "lặp lại được", "bị trôi", "từ con số không", "từ số không", "lan sang",
    "cổng kiểm", "phá luật", "luật bị phá", "vật để test", "tuỳ chỉnh ở rìa",
    "đóng AI lại", "đỡ nó", "nới implementation",
    "chọn vấn đề đáng giải", "đưa input rõ ràng", "cùng định nghĩa requirement",
]
TRANSLATED_RE = [(re.compile(r"\bverify\b", re.I), "verify → kiểm tra"),
                 (re.compile(r"(?<![\w-])draft(?![\w:.-])", re.I), "draft → soạn nháp / bản nháp"),
                 (re.compile(r"\bAI tool\b"), "AI tool → công cụ AI")]
# Chữ đệm khi nói
FILLER = ["thì á", "thì là", "cho nên là", "tại vì", "nói chung là", "kiểu như", "có nghĩa là", "Nhớ nha", "Đúng rồi!"]
FILLER_RE = [(re.compile(r"(?<![\wÀ-ỹ])(nha|hả)(?![\wÀ-ỹ])"), "từ cuối câu: nha / hả"),
             (re.compile(r"(?<![\wÀ-ỹ])ờ(?![\wÀ-ỹ])"), "chữ đệm: ờ"),
             (re.compile(r"\bcái (folder|prototype|file|tool|slide)\b", re.I), "lặp 'cái' trước danh từ")]
AI_TOOLS = re.compile(r"\b(ChatGPT|Cursor|Copilot|Gemini|DALL[·.]?E|Midjourney)\b")
DASH = re.compile(r"[–—]")
DURATION = re.compile(r"\b\d+\s*(phút|min)\b", re.I)
HDR_Q = re.compile(r"^\s*(?:[>\-*]\s*)?Câu hỏi cho (lớp|bạn)", re.I)
MOLDS = [re.compile(r"[Kk]hông phải [^.;\n]{2,60}, ?(mà|cũng không phải)"),
         re.compile(r"AI (làm|soạn)[^.;\n]{2,40}, (designer|bạn|chúng ta) (làm|kiểm)")]


def split_html(text):
    m = re.search(r"<aside>(.*?)</aside>", text, re.S)
    notes = m.group(1) if m else ""
    body = re.sub(r"<aside>.*?</aside>", "", text, flags=re.S)
    body = re.sub(r"<(svg|style|script)[\s\S]*?</\1>", "", body)
    runs = [html.unescape(r).replace("\xa0", " ").strip() for r in re.findall(r">([^<>]+)<", body)]
    runs = [r for r in runs if r]
    n = re.sub(r"<br\s*/?>", "\n", notes)
    n = html.unescape(re.sub(r"<[^>]+>", "", n)).replace("\xa0", " ")
    return runs, [l.strip() for l in n.split("\n") if l.strip()]


def check_line(line, where, kind, out):
    def add(level, msg): out.append((level, where, msg, line[:110]))
    for t in TRANSLATED:
        if t.lower() in line.lower(): add("ERROR", f"cụm dịch cần tránh: '{t}'")
    for rx, label in TRANSLATED_RE:
        if rx.search(line): add("ERROR", f"cụm cần tránh: {label}")
    for t in FILLER:
        if t.lower() in line.lower(): add("ERROR", f"chữ đệm: '{t}'")
    for rx, label in FILLER_RE:
        if rx.search(line): add("ERROR", label)
    if DASH.search(line): add("ERROR", "có dấu gạch dài (en/em dash), thay bằng dấu phẩy, hai chấm hoặc chấm")
    if AI_TOOLS.search(line): add("WARN", "tên công cụ AI cụ thể, dùng 'công cụ AI' trừ khi là tên nguồn trích")
    if kind == "slide" and DURATION.search(line):
        add("WARN", "thời lượng trên slide (chỉ để trong notes và slide MILESTONE của activity)")
    if HDR_Q.search(line) and "?" not in line:
        add("ERROR", "'Câu hỏi cho lớp' phải là câu hỏi, thiếu dấu ?")
    for rx in MOLDS:
        if rx.search(line): add("WARN", "khuôn câu bị hạn chế ('Không phải X, mà Y' / 'AI làm X, bạn làm Y')")
    if kind == "slide" and len(line.split()) > 24 and not line.startswith("http"):
        add("WARN", f"dòng trên slide dài {len(line.split())} từ (nên đọc được trong một cái nhìn)")


def staccato(lines, where, out):
    # ba câu cụt liên tiếp (<= 4 từ mỗi câu) trong cùng một dòng
    for l in lines:
        s = [x.strip() for x in re.split(r"(?<=[.!?])\s+", l) if x.strip()]
        run = 0
        for x in s:
            run = run + 1 if len(x.split()) <= 4 else 0
            if run >= 3:
                out.append(("WARN", where, "chuỗi câu cụt (3 câu ngắn liên tiếp)", l[:110])); break


def pronouns(notes, where, out):
    txt = " ".join(notes)
    cu = len(re.findall(r"chúng ta", txt, re.I))
    # 'mình' chỉ tính khi chỉ người nói/nhóm, bỏ 'của mình', 'bản thân mình', 'cho mình'
    mi = len(re.findall(r"(?<!của )(?<!cho )\b[Mm]ình\b(?! sẽ ở)", txt))
    if cu and mi:
        out.append(("WARN", where, f"notes trộn 'chúng ta' ({cu}) và 'mình' ({mi}); chọn một cho cả deck", ""))


def lint_text(path, text, args):
    out = []
    if path.endswith(".html"):
        runs, notes = split_html(text)
        sid = os.path.basename(path)
        if not args.notes_only:
            for r in runs: check_line(r, sid + " [slide]", "slide", out)
        if not args.slide_only:
            for n in notes: check_line(n, sid + " [notes]", "notes", out)
            staccato(notes, sid + " [notes]", out)
            pronouns(notes, sid + " [notes]", out)
    else:
        lines = text.splitlines()
        start = 0
        if lines and lines[0].strip() == "---":  # bỏ qua YAML front matter
            for j in range(1, len(lines)):
                if lines[j].strip() == "---": start = j + 1; break
        for i, l in enumerate(lines, 1):
            if i <= start or l.strip().startswith("```"): continue
            check_line(l, f"{os.path.basename(path)}:{i}", "notes", out)
    return out


def collect(paths):
    for p in paths:
        if os.path.isdir(p):
            for r, _, fs in os.walk(p):
                for f in sorted(fs):
                    if f.endswith((".html", ".md")) and "node_modules" not in r: yield os.path.join(r, f)
        else:
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--notes-only", action="store_true")
    ap.add_argument("--slide-only", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = []
    for f in collect(a.paths):
        try: res += lint_text(f, open(f, encoding="utf-8").read(), a)
        except (UnicodeDecodeError, OSError) as e: print(f"skip {f}: {e}", file=sys.stderr)
    if a.json: print(json.dumps([dict(level=l, where=w, msg=m, text=t) for l, w, m, t in res], ensure_ascii=False, indent=1))
    else:
        for l, w, m, t in res: print(f"{l:5} {w}: {m}" + (f"\n        “{t}”" if t else ""))
        e = sum(1 for r in res if r[0] == "ERROR"); w = len(res) - e
        print(f"\n{e} lỗi (ERROR), {w} cảnh báo (WARN)")
    sys.exit(1 if any(r[0] == "ERROR" for r in res) else 0)


if __name__ == "__main__":
    main()
