# Whiteboard data (findings JSON)

Input of `scripts/build_whiteboard.py`. Save it as `work/heuristic-evaluation/findings.json` in the project. Full example: `../examples/grab-food-delivery.json`.

```json
{
  "title": "Grab - Current Experience",
  "subtitle": "Grab food delivery, Vietnam · iPhone · app v33437965",
  "assetsBase": "../assets/",
  "journeys": [
    { "title": "Journey 1 - Find and order", "code": "J1", "dir": "journey-1-find-and-order",
      "screens": [["01-grab-home", "Grab home"], ["02-food-section", "Food section"]] }
  ],
  "findings": [
    { "n": 1, "sev": 2, "at": "J1-01", "pr": ["P8"],
      "t": "Home screen is crowded",
      "where": "Service grid, tab bar badges",
      "sees": "About ten service icons in two rows, red dots on three tabs.",
      "pins": [["J1-01", 0.50, 0.26], ["J1-01", 0.89, 0.84]] }
  ]
}
```

| Field | Meaning |
|---|---|
| `journeys[].code` | Short code, for example `J1`. Screen ids are `<code>-<number>` in order, from `01`. |
| `journeys[].dir` | Folder under `work/assets/`. Each screen is `<dir>/<file>.jpg`. |
| `journeys[].screens` | `[file name without .jpg, label]` in journey order. |
| `assetsBase` | Path from the whiteboard folder to the assets folder. Default `../assets/`. |
| `findings[].n` | Number. The tag is `UX-` plus the number with two digits. Continuous across journeys. |
| `findings[].sev` | 0 to 4. Colours: 0 grey, 1 yellow, 2 orange, 3 red, 4 deep red. |
| `findings[].at` | Screen id that carries the sticky note. Spread notes over screens so no screen holds more than about three. |
| `findings[].pr` | Heuristic codes `P1` to `P10`. The board prints the full names. |
| `findings[].t` | Short title for the note (about eight words). |
| `findings[].where` | Part of the screen. |
| `findings[].sees` | What the user sees, short (two or three sentences). |
| `findings[].pins` | `[screen id, x, y]`: x and y are fractions (0 to 1) of the screenshot width and height. One pin per spot; a finding on several screens has a pin on each. |

The script checks that screens exist, pins are inside the image, severity is 0 to 4, principles are valid and numbers are not repeated, then prints what to fix.

A finding whose pins are on another journey's screen keeps its note in its own `at` journey. With the Journey filter on, that pin is hidden because its note is hidden.
