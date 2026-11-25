---
name: heuristic-evaluation
description: "Audit the current experience of a product from screenshots inside an AI Product Workspace project: check every screen against Nielsen's 10 heuristics, rate each problem on the 0 to 4 severity scale, say which screen and which spot on it has the problem, cross-check the owner's own possible breakdowns, write work/heuristic-evaluation/index.md, then draw all screens on a pan-and-zoom whiteboard (HTML) grouped by journey with one sticky note and one pin per finding. Use when the user says validate the current experience, heuristic evaluation, UX audit, usability review of screenshots, 'đánh giá heuristic', 'audit trải nghiệm hiện tại', sticky notes on screenshots, or wants issues placed on the screen where they happen, even if they do not say 'skill'."
license: MIT
---

# Heuristic evaluation of the current experience

Screen-by-screen expert review of an existing product, written for a product workspace folder (has `AGENTS.md`, `standards/`, `work/`). Two outputs: a Markdown file and a whiteboard. Read `AGENTS.md` first: its rules win over this skill.

## Why this shape
A finding is only useful if the owner can open the screen and see the problem. So every finding names the screen and the spot on it, and the whiteboard puts a pin on that spot. Severity is a proposal from screenshots only: nobody has tapped anything and no user was involved, so the owner decides.

## Before you start
1. Read `AGENTS.md`, `standards/principle-checks.md` (the 10 heuristics) and `standards/severity-levels.md` (0 to 4). Read `../toolkit/rules/ai-rules.md` if it exists; if the toolkit folder is missing, say so and carry on from `AGENTS.md` and `standards/`.
2. **Get the screens.** The screens can come from three places; ask which if it is not clear:
   - Already in the project, usually `work/assets/<journey>/NN-name.jpg`: go straight to the steps.
   - Only as a screen recording: run the `screens-from-recording` skill first. Do not start the audit until the owner has confirmed the extracted, blurred screens.
   - A few loose images (pasted or in a folder): propose the journey and file names, put them in `work/assets/journey-<n>-<name>/`, and continue.
   Screens with readable personal data are not input: ask the owner to blur them first.
3. The flows in `work/current-user-flow/` give the screen codes (J1 · 01) and the owner's possible breakdowns; reuse both. If there are no flows, name the journeys and number the screens in order, and say so.
4. Never read `_personal/` or `work/sources/_raw-private/`.

## Where the files go
Everything for one evaluation lives in one folder, `work/heuristic-evaluation/`, so the report shows it as one document:

| File | What it is |
|---|---|
| `index.md` | The findings document (from `references/evaluation-template.md`). Its front matter has `embed: true` and `media: ["heuristic-whiteboard.html"]`, so the whiteboard shows on the same page. |
| `findings.json` | The same findings as data, for the whiteboard. |
| `heuristic-whiteboard.html` | The generated whiteboard. Reads the screenshots from `../assets/`. |

Do not leave loose `heuristic-*` files in `work/`.

## Steps
1. **Look at every screen, one by one,** at full size. Note only what is visible. Blurred areas (personal data) are not judged. If something needs a tap to know, write it as a question for the owner, do not rate it.
2. **Write findings.** One finding per problem. Each has: a tag, the screen(s), where on the screen, what the user sees (quote real on-screen text), the heuristic(s) broken, severity 0 to 4 and one line why. Rules:
   - Tags are continuous across the whole file: `UX-01`, `UX-02`... Do not restart per journey and do not put the journey in the tag.
   - Write the full heuristic name (Visibility of system status), not the code (P1).
   - Level 3 and 4 need a reason. Level 4 means the main task is blocked or money or data is lost: do not use it without that evidence.
   - Quote only text that is on the screen. Never invent a figure or a user reaction.
3. **Write `work/heuristic-evaluation/index.md`** from `references/evaluation-template.md`. Keep exactly its sections. Write the body for readers, as the project's shared AI rules say: no file paths, tool or skill names, or item codes (O1, H2...) in the text; the `UX-` tags are the only codes. Say things in plain words, and keep file names only in the front matter. Do not add sections for limits, cross-journey findings, to-test lists or what works, unless the owner asks.
4. **Cross-check the owner's possible breakdowns** (from the flow pages): confirmed, partly, or not checkable, with the tag. List new problems the owner did not name.
5. **Build the whiteboard.** Write a findings JSON (schema in `references/whiteboard-data.md`; a full example is in `examples/grab-food-delivery.json`), then run:
   ```
   python3 <this skill>/scripts/build_whiteboard.py work/heuristic-evaluation/findings.json --out-dir work/heuristic-evaluation
   ```
   The build also checks the JSON against the markdown (see "Keep the markdown and the whiteboard in sync"). Pin positions are fractions (0 to 1) of the screenshot width and height. Estimate them by looking at the screen; they are estimates, say so, and let the owner correct them.
6. **Tell the owner:** where the files are, the severity counts, which findings rest on one screen only, that pin positions are estimates, and that the report was or was not rebuilt (`../toolkit/tools/build-report.py`; if the toolkit is missing, say it was not).

## The whiteboard
One HTML file. Journeys are bands of screens in order. Each finding is one sticky note beside its screen (where on the screen, what the user sees, principle, severity) with a numbered pin on the exact spot and a line from pin to note. Note colour is severity. Controls: scroll or drag to move, Ctrl/⌘ + scroll or pinch to zoom, click a note or pin to follow it, a Journey dropdown to filter, `0` to fit all.

Known limits, tell the owner when it matters:
- The Claude preview pane loads only small files (about 0.7 MB). The script embeds 200 px fallback copies of the screenshots to stay under that, so in the pane the screens are blurry. A normal browser reads the full-quality images from `work/assets/` (keep that folder next to the whiteboard folder). To get sharp screenshots, open the file in the browser: `open work/heuristic-evaluation/heuristic-whiteboard.html`.
- The embedding step uses macOS `sips`. Without it the script warns and the board needs the assets folder.
- The board is a separate copy of the findings: see "Keep the markdown and the whiteboard in sync" below.

## Keep the markdown and the whiteboard in sync
`work/heuristic-evaluation/index.md` (what people read) and `work/heuristic-evaluation/findings.json` (what draws the board) hold the same findings. **Whenever a finding changes in one, change it in the other in the same turn, then rebuild the board.** That covers adding, dropping, renumbering, re-rating, changing a principle, and moving a pin or note.

The build script enforces it. It compares the finding rows of the markdown (tag, principle names, severity) with the JSON on every build, looking for `index.md` in the output folder (or the file you pass with `--check-md`). On a mismatch it still writes the board, lists each difference and exits with code 2. Treat exit 2 as not finished: fix whichever side is wrong and run it again until it prints "markdown and JSON agree". Use `--no-check` only for a throwaway build.

The check does not compare the free text (where, what the user sees, why). When you edit those words, edit them in both files yourself.

## Hard rules
- The AI drafts, the owner decides. Keep the findings under a heading marked "(AI draft)" only if the project hides drafts in its report; the owner's checked version goes in the last section.
- Do not create finding items in `insights/findings/` and never set a finding to resolved: only when the owner asks, and then use `new-item.py`.
- No item codes (O1, H1, F1...) in the body text.
- One evaluator is a limit: say it once to the owner in chat, and suggest a second pass.

## Output checklist
- [ ] Every screen was looked at; each finding names a screen and a spot.
- [ ] Tags run `UX-01`... without gaps or repeats; full heuristic names; severity 0 to 4.
- [ ] Level 3 and 4 have a reason; level 4 has evidence.
- [ ] Cross-check table lists every owner breakdown.
- [ ] Build printed "markdown and JSON agree" (exit 0), and free-text edits were made in both files.
- [ ] Whiteboard built, validator passed, Journey filter works, pins checked by eye on a few screens.
