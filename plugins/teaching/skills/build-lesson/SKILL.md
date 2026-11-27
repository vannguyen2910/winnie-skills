---
name: build-lesson
description: "Build a new lesson in <03_Mentoring>: brief for approval first, then lesson and slide outline, review, judge, site rebuild. Use for 'build lesson', 'tạo lesson mới', 'soạn bài mới'."
argument-hint: '<topic or lesson slug> [stage: foundation|discover|define|develop|deliver|leader-level] [for: <mentee or "class">] [level: junior|senior|mixed]'
---

# Build a lesson

Build a lesson: $ARGUMENTS

## Where this runs

This skill works only inside `<03_Mentoring>`. `<03_Mentoring>` là thư mục Mentoring trên Google Drive của máy này, tìm bằng:

```bash
ls -d ~/Library/CloudStorage/GoogleDrive-*/"My Drive"/03_Mentoring
```

Every path below is relative to that folder; run every command from it. If the session is not working there, say so and stop. Read its `CLAUDE.md` first.

This command has two stages with a hard gate between them. Stage A produces a brief and stops. Stage B runs only after the user approves the brief in chat. Never skip the gate, even when the request looks small (Rule WF-5). Chat with the user in Vietnamese.

## Language (decided 2026-10-11)

New lessons are written in **Vietnamese**. Existing lessons written in English stay as they are until the user asks for a rewrite.

- **Vietnamese:** the brief, the lesson body, the slide outline's on-slide text and speaker notes, activity instructions, homework text.
- **English:** file and folder names, slugs, front matter keys and tags (WF-4), section headings and slide titles/kickers (vi-voice rule 1), and professional terms kept in English per vi-voice rule 4.
- **Skills to use, in this order:**
  1. `vi-voice`: load before drafting anything. It sets voice, term list and phrases to avoid. Where it conflicts with the writing style guide, vi-voice.md wins.
  2. `vietnamese-voice-dictionary`: when the user's own words (a brief, a correction, a note) look like speech-to-text errors, resolve them with it before using them. Ask once if a word is ambiguous.
  3. `vietnamese-transcript-cleaner`: when the source material in A1 is a raw transcript or caption file.
  4. `vietnamese-copy-polish`: after drafting, run it over the on-slide text and any text a learner reads: missing diacritics, long sentences, filler, en and em dashes, weak hooks. It is a final check, not a rewrite of the teaching content.

## Stage A: Brief (always first)

### A1. Find what already exists

1. Search `library/lessons/**/materials/` and `library/frameworks/` and `library/guides/` for the topic. If a lesson already exists, this is an update, not a new lesson: say so, list what exists (lesson, outline, deck, `draft` status, last sync date) and propose only the delta.
2. Read the neighbours: the lesson before and after in the programme (`previous-session`, `next-session` front matter, the relevant `programs/*/README.md` or coaching plan), so the handoffs are real.
3. Look in `source/` and `_inbox/` for raw material on the topic (WF-1, WF-6). Do not move anything.
4. If the lesson is for one mentee, read their `mentee.md`, plan and latest recap for context. That context shapes the examples, but it must not appear by name in the lesson (see CLAUDE.md, General lesson conventions). Apply WF-2 if the idea came from a private session: generalise, and record `source: adapted-from-private-session` in front matter.

### A2. Ground the content

Teach what is in the user's own material first. Where the lesson needs a claim, a statistic or a method that is not in their files, run the `teaching:topic-research` skill (or `topic-research` in the teaching plugin). It searches, checks each claim against its source, and writes `learning/research.md` in the lesson folder with a verification status per claim and the learning values. Record each source with author, year and sample size where the source gives them. Do not state a number without a source. Separate what a source found from what the author infers. Where something is Winnie's own teaching method, mark it as such and do not invent supporting research.

### A3. Write the brief

Save to `library/lessons/<stage>/<slug>/materials/<slug>-brief.md` (create the lesson folder only if the user has confirmed the stage and slug; ask once if either is unclear, offering 2 or 3 options with a recommendation, per WF-3). Use exactly:

```markdown
---
title: ""
type: lesson
audience: ux-class | private-training
level: beginner | intermediate | advanced
duration: "90 min"
---

## Purpose
One sentence: what the learner can do after this session that they could not before.

## Structure
1. Block name, minutes: what it covers (one line each). For a class lesson use the theory-first shape: Open, Theory (3 to 4 parts, 40 minutes or less), Bridge, Practice (30 minutes or more), Close
...
(timings sum to the duration with a stated buffer)

## Learning objectives
3 to 5, each starting with a Bloom verb and observable.

## Key decisions
- Running example and why
- Where AI appears and where it does not (manual before AI)
- What is cut, and what is deferred to another lesson
- Open questions for Winnie
```

Also list, in the brief, the sources found in A2 and anything marked `[to confirm]`.

### A4. Gate

Show the brief in chat and stop. Do not create the lesson, the outline or a deck. The user replies "looks good" or edits inline and says "build it". Anything less than a clear yes is not approval.

## Stage B: Build (only after approval)

### B1. Scaffold

Create `library/lessons/<stage>/<slug>/{materials,slides,assets,_archive}` if missing. Start from `_system/learning templates/_template-lesson.md` and `_system/learning templates/_template-slide-outline.md`, not a blank page. Front matter: `draft: true`, tags only from the WF-4 vocabulary (2 to 5, one audience, one level), `program`, `level`, `duration`, `previous-session`, `next-session`.

### B2. Write the lesson (`<slug>-lesson.md`, source of truth)

Follow the sections of `_template-lesson.md` (mentoring-rules.md Rules LP-1 and LP-3): Overview, Learning Objectives, Materials Needed, Pre-Class Preparation, Run-of-Show (Open, Theory block, Bridge, Practice block, Close), Practice Dataset (optional), AI in Practice, Assessment, Further Resources. Older lessons use `Session Plan` and `Core Content`: do not copy that shape, and do not convert them unless asked. Rules that always apply:

- **Vietnamese paper style:** objective, third person, no "bạn" or "mình" in the lesson file (speaker notes in the outline use "mình"), no imperatives, a Limitations note, numbered references [n] for every figure (vi-voice.md). Sources can stay in their original language; the claim is written in Vietnamese.
- **No spoken filler and no translated-sounding phrases:** check the "Bỏ khỏi văn bản chính thức" and "Cụm dịch từ tiếng Anh cần tránh" tables in vi-voice.md before saving.
- **No tool names:** write "AI chat tool", "AI coding tool", "your AI tool". Never introduce Claude, ChatGPT, Cursor, Copilot or similar.
- **No mentee or student names**, no cohort or identifying detail.
- **Manual before AI:** the learner does the thinking before AI helps. AI assists, the learner decides.
- **AI in Practice** section is mandatory (LP-4): a try-this prompt, a critical-thinking prompt, a prompt tip, an ethics note.
- Timings sum to the stated duration, with the buffer written down.
- **No minutes in headings.** Lesson, phase, practice-step and template headings carry no duration, such as "(8 phút)" or "· 20 phút ·". Write the time on its own line under the heading (`**Time:** 8 phút`), or in a timing table. Slides carry no minutes except a MILESTONE number (vi-voice rule 3).
- Anything uncertain stays marked `[to confirm]`; do not smooth it over.

### B3. Write the slide outline (`<slug>-slide-outline.md`) in the same response

Apply the sync rule in CLAUDE.md: both files are written together and never left out of sync. Use the layout catalogue in `_system/rules/slide-deck-rules.md`. Never invent a layout type. Every slide has the standard fields (Kicker, Title, On-slide, Speaker notes as 3 to 6 bullets, Visual hint). The COVER slide follows the locked block in the template. Update the slide count in the `## Slide structure` line and the MILESTONE `Num:` values to match the lesson's phase timings.

### B4. Review before reporting

Run the `teaching:review-mentoring` skill's checks on the pair, or apply its checklist inline: the session is theory first then practice (Theory block 40 minutes or less with no activity inside, Bridge and cheat sheet present, Practice at least 30 minutes and unbroken, every theory concept used by an activity; mentoring-rules.md Rule LP-3), objectives match activities, timings sum, handoffs from and to neighbouring lessons are consistent, outline matches lesson, QA-2 checklist (mentoring-rules.md). Then run the language pass from the Language section: `vietnamese-copy-polish` on on-slide text, and the vi-voice.md tables on the lesson body. Fix what is wrong, and list what you could not fix.
When Winnie corrects a Vietnamese line, add the before and after to `vi-voice.md` so the fix applies next time (that rule is in CLAUDE.md).

Then, in this order:

1. **Judge.** Start the `teaching:lesson-judge` agent. Give it the lesson folder path and nothing about your own choices, so it judges the files and not the intent. It writes `materials/_review/judge-YYYY-MM-DD.md`. Fix the hard-rule failures (Layer C) and lesson/outline mismatches it finds, except matches that are Winnie's call (for example inside a quoted reference). Bring its other Critical and Improvement findings to Winnie: do not change teaching content to raise a score. Run it once, again only if Winnie asks. If the agent is not available, say so; do not score the lesson yourself instead.
2. **Loop check.** Apply the `teaching:learning-loop` skill to the lesson, the outline and the practice sheet if there is one. Report only: change nothing until Winnie accepts a fix.

### B5. Deck

Visuals for the outline's DIAGRAM, COMPARE and IMAGE slides come first. Run the `teaching:slide-visuals` skill (or `slide-visuals` in the teaching plugin) on the outline: it draws schematic diagrams through diagram-design, asks for a Figma link for real screens, asks permission before any outside image, saves them in the lesson's `assets/`, links each one from its slide, and logs every source in `assets/SOURCES.md`.

A deck is a separate step. Do not generate deck HTML in this command. State exactly what is needed: the outline path, the slide count, and the nearest existing deck folder to copy support files from (`deck-stage.js`, `image-slot.js` and `support.js` live in each lesson's own `slides/` folder, with the design tokens in `slides/_ds/`; a few older lessons have a `tokens.css` there instead; there is no shared theme folder). The built deck, once it exists, goes directly in `slides/` as an `.html` file (not `_archive/`, not nested), per CLAUDE.md.

### B6. Rebuild and report

Run `python3 _system/scripts/build-home.py` (site rebuild rule in CLAUDE.md) and report the lesson card or page line for this lesson. Then report:

- files created or changed, with paths
- the sync check result (lesson vs outline: slide count, timings)
- open `[to confirm]` items and review findings
- the judge report path, its top 3 issues and scores (the rubric is a v0.1 draft, not yet calibrated)
- the Loop check lines
- what waits on the user: approve to mark `draft: false`, build the deck, add `programs:` line if the programme page needs it, assign it to the mentee's `lessons:` mapping in `mentee.md` when relevant
