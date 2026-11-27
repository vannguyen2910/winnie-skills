# friction.json

Lives in `work/heuristic-evaluation/`, next to `findings.json`, which supplies journey codes and screen names.

```json
{
  "source": "screenshots",
  "remarks": "Optional paragraph printed above the tables, for example which screens come from another sitting.",
  "journeys": { "J1": { "title": "Find and order", "goal": "put a drink in the basket" } },
  "screens": {
    "J1-01": { "verified": false, "note": "Shown in the table", "marks": [
      { "a": "tap", "x": 0.10, "y": 0.20 },
      { "a": "swipe", "x": 0.05, "y": 0.30, "w": 0.90, "h": 0.40, "dir": "up", "times": 2, "extra": true },
      { "a": "input", "x": 0.10, "y": 0.08, "w": 0.80, "h": 0.05, "chars": 6 },
      { "a": "tap", "note": "closed a pop-up that has no screenshot" }
    ] },
    "J1-02": { "verified": false, "explore": true, "marks": [] }
  }
}
```

| Field | Meaning |
|---|---|
| `source` | `recording` or `screenshots`; sets the warning on the board and above the tables |
| `screens.<id>` | Screen id as on the whiteboard (`J1-01`). No entry shows "Not counted" |
| `marks` | One per action, in the order done. `[]` means counted, no actions |
| `a` | `tap`, `swipe` or `input` |
| `x`, `y` | Fractions 0 to 1 of the screenshot. Tap: its centre. Swipe and input: top left corner, with `w`, `h` |
| `note` on a mark | Replaces the position when the action is on a screen that was not captured |
| `dir`, `times` | Swipe only: `up`, `down`, `left`, `right`; `times` defaults to 1 |
| `chars` | Input only: typed characters |
| `extra` | The goal could be reached without this action. Not allowed on an `explore` screen |
| `explore` | Looking around outside the task; counted apart |
| `verified` | `true` only after the owner has checked the screen |

On the board, taps are blue circles (`T1`), swipes purple dashed boxes (`S ↑ ×2`), inputs teal boxes (`In · 6 chars`), and extra steps carry `+ EXTRA`. Red and yellow are left to severity.
