---
name: friction-count
description: "Count taps, swipes, inputs and extra steps in an app's current experience, mark them on the heuristic whiteboard and table them for task analysis. Use for friction metric, interaction cost, tap count, 'đếm tap', 'đếm thao tác', 'tính friction'."
license: MIT
---

# Friction count for the current experience

Counts how many actions a task takes today, in a product workspace folder (has `AGENTS.md`, `work/`). `AGENTS.md` rules win over this skill. Counts show physical effort only: keep any cognitive effort rating beside them. No weighted score, unless the owner names a model they have checked in the source.

Draft method: used on one project so far.

## Before you start
1. Read `AGENTS.md` and `context/data-rules.md`. Never read `_personal/` or `work/sources/_raw-private/`. A recording or screen with readable name, address, phone or payment details: ask for a blurred copy. If the data rules say the AI does not collect or analyse data, say so and let the owner choose who counts.
2. Needs `work/heuristic-evaluation/findings.json` and `heuristic-whiteboard.html`. Missing: run `heuristic-evaluation` first (this skill draws on its board).
3. Agree with the owner: the goal of each journey, and the evidence. A recording (`"source": "recording"`) beats screenshots (`"screenshots"`: estimates, usually minimums).

## Counting rules
| Measure | Counts as 1 |
|---|---|
| Tap | One touch that triggers something |
| Swipe | One scroll or swipe gesture |
| Input | One field filled; note typed characters |
| Extra step | Any action the goal could be reached without. A flag on an action already counted, never added on top |

- An action belongs to the screen where it is done. Done on a screen that was not captured: put it on the nearest screen with a note and no position.
- Waiting counts as zero. A screen with no action gets `"marks": []`; a screen you cannot judge gets no entry.
- Count only what the evidence shows. With screenshots: a tap or input is shown by the next screen; count one swipe where a screen has clearly moved. Never invent an option tick, a typed text or a pop-up.
- **Compare timestamps first.** Screens from another sitting are often the owner looking around, not the task: set `"explore": true`, which counts them apart.

## Steps
1. Look at every screen at readable size (tiling several with `ffmpeg` saves tokens). Positions are fractions of one screenshot; check that markers do not hide the button label.
2. Write `work/heuristic-evaluation/friction.json` (format: `references/friction-data.md`), every entry `"verified": false`.
3. Run, giving the task analysis document if the owner wants tables there:
   ```
   python3 <this skill>/scripts/friction.py work/heuristic-evaluation/friction.json --md <task analysis index.md>
   ```
   It owns the `## Friction counts` section and the friction layer of the board: change `friction.json` and run again, never edit either by hand. Without that heading yet, the section is added at the end of the file; move it where it belongs and later runs keep it there.
4. Open the board in a browser, choose Friction, and check markers screen by screen.
5. Add a row to the AI-use log if the project has one. Rebuild the report if the toolkit exists.
6. Tell the owner: totals per journey, every judgement call (extra steps, exploration, off-screen actions), and that pin and marker positions are estimates.

Rebuilding the heuristic whiteboard removes the friction layer. The data is safe: run step 3 again.

Set `"verified": true` only for screens the owner says they checked.
