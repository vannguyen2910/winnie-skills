---
name: heuristic-evaluation
description: "Heuristic UX audit of app screenshots (Nielsen, severity 0-4) in a product workspace, with a sticky-note whiteboard. Use for UX audit, usability review, 'đánh giá heuristic', 'audit trải nghiệm'."
license: MIT
---

# Heuristic evaluation of the current experience

Screen-by-screen expert review of an existing product in a product workspace folder (has `AGENTS.md`, `standards/`, `work/`). `AGENTS.md` rules win over this skill. Severity is a proposal from screenshots only (nobody tapped anything, no user was involved), so the owner decides.

## Before you start
1. Read `AGENTS.md`, `standards/principle-checks.md` (the 10 heuristics), `standards/severity-levels.md` and `../toolkit/rules/ai-rules.md` (if there is no toolkit, say so and carry on). Never read `_personal/` or `work/sources/_raw-private/`.
2. Get the screens (ask where they are if unclear):
   - In the project, usually `work/assets/<journey>/NN-name.jpg`: go on.
   - Only a screen recording: run `screens-from-recording` first, and wait until the owner has confirmed the blurred screens.
   - Loose images: propose journey and file names, then put them in `work/assets/journey-<n>-<name>/`.
   - Readable personal data on a screen: ask the owner to blur it first.
3. Take screen codes (J1 · 01) and the owner's possible breakdowns from `work/current-user-flow/`. With no flows, name the journeys, number the screens in order, and say so.

## Files
All in `work/heuristic-evaluation/` (no loose `heuristic-*` files in `work/`):
- `index.md`: the findings document people read.
- `findings.json`: the same findings as data.
- `heuristic-whiteboard.html`: generated from the JSON, shown inside `index.md`.

## Steps
1. **Look at every screen** at full size. Judge only what is visible, not blurred areas. Anything that needs a tap to know is a question for the owner, not a rated finding.
2. **Write findings**, one per problem: tag, screen(s), spot on the screen, what the user sees, heuristic(s), severity 0 to 4 with one line why.
   - Tags `UX-01`, `UX-02`... run through the whole file: no gaps, no repeats, no restart per journey.
   - Write full heuristic names (Visibility of system status), not codes (P1).
   - Quote only on-screen text. Never invent a figure or a user reaction.
   - Level 4 means the main task is blocked or money or data is lost: use it only with that evidence.
3. **Write `index.md`** from `references/evaluation-template.md`, keeping its front matter and exactly its sections (add limits, cross-journey, to-test or what-works sections only if asked). The body is for readers: no file paths, tool or skill names, or item codes (O1, H2...); `UX-` tags are the only codes.
4. **Cross-check every owner breakdown**: confirmed, partly or not checkable, with the tag. List new problems the owner did not name.
5. **Build the whiteboard.** Write `findings.json` (schema and board behaviour: `references/whiteboard-data.md`; example: `examples/grab-food-delivery.json`), then run:
   ```
   python3 <this skill>/scripts/build_whiteboard.py work/heuristic-evaluation/findings.json --out-dir work/heuristic-evaluation
   ```
   Done only when it prints "markdown and JSON agree". Then open the board, try the Journey filter and check a few pins by eye.
6. **Rebuild the report** with `../toolkit/tools/build-report.py` (not possible without the toolkit), then tell the owner: where the files are, severity counts, which findings rest on one screen only, that pin positions are estimates to correct, whether the report was rebuilt, and (once) that one evaluator is a limit, so a second pass helps.

If `work/heuristic-evaluation/friction.json` exists, the rebuild removes the friction layer: run the `friction-count` script again afterwards.

## Keep markdown and JSON in sync
Any change to a finding (add, drop, renumber, re-rate, principle, words, pin) goes into `index.md` and `findings.json` in the same turn, then rebuild. Exit code 2 means they differ: fix the wrong side and run again. The script compares only tags, principles and severity, so check edited text in both files yourself. `--no-check` is for throwaway builds.

## Hard rules
- The AI drafts, the owner decides: their checked version goes in the last section. Mark the findings "(AI draft)" only if the project hides drafts in its report.
- Create items in `insights/findings/` only when the owner asks, with `new-item.py`. Never set a finding to resolved unless asked.
