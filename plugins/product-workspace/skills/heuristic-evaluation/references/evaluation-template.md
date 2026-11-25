---
type: "heuristic-evaluation"
title: "Heuristic evaluation of the current experience"
stage: "Discover"
status: "draft"
summary: "Screen-by-screen check of <product> (<N> screens, <N> journeys) against Nielsen's 10 heuristics, with a 0 to 4 severity for each problem. The findings are an AI draft from the screenshots only and still need the owner's check."
supports: []
embed: true
media:
  - "heuristic-whiteboard.html"
---

# Heuristic evaluation of the current experience

<Product> · <country> · <device> · <app version> · <language> · walk-through of <date>.

## 1. What this is

A first pass at "Validate the current experience". Every screen of the journeys is checked against the 10 heuristics in `standards/principle-checks.md` and every problem is rated with `standards/severity-levels.md`. Screen references (J1 · 01 and so on) are the same as in `work/current-user-flow/`, and the images are in `work/assets/`.

**The whiteboard** (`heuristic-whiteboard.html`, in this folder) draws the same findings on the screens, one sticky note and one pin per finding. Open it in a normal browser for sharp screenshots. The findings are also kept in `findings.json`; when a finding changes here, change it there too and rebuild the whiteboard.

**How it was made:** all <N> screenshots were looked at one by one and compared with the owner's possible breakdowns in the flow diagrams.

## 2. Summary

| Severity | Count | What it means here |
|---|---|---|
| 4 Catastrophe | 0 | <one line, or "No screen blocks the main task by itself in the screenshots"> |
| 3 Major | | <the problems in a few words> |
| 2 Minor | | <kind of problems> |
| 1 Cosmetic | | <kind of problems> |

## 3. Findings

### Journey 1: <name>

| Tag | Screen | Where on the screen | What the user sees | Principle | Sev | Why this level |
|---|---|---|---|---|---|---|
| UX-01 | J1 · 01 <name> | <part of the screen> | <what is visible, quoted text in “ ”> | <Full heuristic name; second one if needed> | 2 | <one line> |

### Journey 2: <name>

(same table, tags continue: UX-14, UX-15, ...)

## 4. Cross-check with your possible breakdowns

| Flow | Your breakdown | Result from the screens | See |
|---|---|---|---|
| <flow> | 1 <short text> | Confirmed / Partly: <why> / Not checkable: <why> | UX-01 |

**New problems that were not in your list:** UX-xx, UX-xx.

## 5. Findings (verified)

*Empty. The checked version goes here after the owner reviews section 3: which findings to keep, change or drop, their own severity, and a second evaluator if there is one. Then ask the AI tool to create the finding items.*
