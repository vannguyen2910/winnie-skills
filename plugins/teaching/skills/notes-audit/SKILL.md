---
name: notes-audit
description: Audit the speaker notes of a slide outline (*-slide-outline.md) and report which slides need a real example, are too thin or too long for their time, or break the notes format. Report only, never edits. Use when Winnie says "notes-audit", "audit speaker notes", "kiểm tra speaker notes", or wants to check an outline before teaching.
---

# notes-audit

Audit the speaker notes of a slide outline. Input: path to a `*-slide-outline.md`, or a lesson folder. Read and report only; do not edit the outline, the lesson or the deck.

Rules to read before judging (Drive): `/Users/winnie.nguyen/library/CloudStorage/GoogleDrive-nguyenphuctuongvan@gmail.com/My Drive/03_Mentoring/_system/rules/slide-deck-rules.md` (Speaker notes rule, Title and kicker copy) and `.../_system/rules/vi-voice.md` for any Vietnamese.

## 1. Run the mechanical check

```
python3 ~/.claude/skills/notes-audit/notes-audit.py <outline.md>
```

Per slide it reports verbatim (`>`) lines, bullets, spoken words, estimated spoken minutes, missing `Ví dụ` fields, bracketed stage directions, and slides with no verbatim line. It also flags Title and Kicker copy that breaks the Title and kicker rule (Title over 6 words, Kicker with a Phần/Buổi number, Kicker repeating Title).

It also checks the outline's structure against the rules: layout names outside the fixed catalogue (`DESIGN METHOD`, `ACTIVITY`, `COMPARISON`, `SECTION` are drift), a missing `Ví dụ` or `Câu hỏi hay gặp` field on any slide, Visual hint prefixes (DIAGRAM `SCHEMATIC`, IMAGE `REAL`, PRACTICE `TWO CARDS`, Q&A `SPLIT`), definition slides (`NUMBERED · What is ...`: Kicker `Định nghĩa`, Title ending `là gì?`, What/Why/When rows, no `Where AI helps` row), presenter instructions inside notes bullets, and whether the AGENDA lines match the SECTION DIVIDER titles in the same order. `[to confirm]` markers and `[n]` citations are not counted as bracketed stage directions.

## 2. Judge what the script cannot

Read the outline and its paired `*-lesson.md` if there is one. For every concept slide (`NUMBERED`, `COMPARE`, `FORMULA`, `STATEMENT`, `DIAGRAM`, `PROCESS`, `QUOTE`):

1. **Needs an example?** Yes when the notes explain an idea with no concrete situation, number, artifact or outcome. No when the slide only names, sequences or transitions.
2. **Does the lesson already hold one?** Search the lesson file first and point to it. The lesson is the source of truth, so an example belongs there before the outline.
3. **Is the example first?** The situation comes before the concept name.
4. **Is the transfer explicit?** The notes end with a question or line tying the example to the learner's own project.
5. **Is one example enough?** A concept used in several contexts needs a second, different example.

## 3. Report

Vietnamese, headings in English. One table, then a short list.

| Slide | Layout | Vấn đề | Đề xuất |
|---|---|---|---|

- **Cần ví dụ:** each slide with the kind of example needed (one line, no invented case).
- **Format:** slides with missing fields, stage directions, or over length.
- **Timing:** total estimated minutes against the lesson's session table.
- **Sync:** anything that would also need a change in `*-lesson.md`.

## Rules

- Never fill in an example as if it were real. If you suggest one, label it `bản nháp`.
- No mentee, company or cohort names in suggestions.
- No specific AI tool names; use "AI chat tool", "AI coding tool".
- Do not rewrite notes. Offer to, and wait.
