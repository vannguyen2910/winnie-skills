---
name: vietnamese-voice-dictionary
description: "Sửa từ bị voice-to-text nghe nhầm ('ghiếp H' = GitHub) bằng từ điển tự học. Dùng khi tin nhắn có từ vô nghĩa, hoặc 'nghe nhầm', 'ý tôi là', 'nhớ từ này'."
license: MIT
compatibility: Python 3.8+ standard library only. Optional Claude Code hook for automatic use.
metadata:
  author: ducpt
  homepage: https://ducpt.com
  version: "1.0.0"
---

# Vietnamese Voice Dictionary

People who dictate to an AI agent in Vietnamese get the same technical words misheard again and again. This skill keeps a small dictionary of "heard as" and "meant" pairs so the agent reads the message the way the speaker meant it, and so a correction made once is never needed twice.

The dictionary holds vocabulary only, never the content of conversations.

## Step 1. Apply the dictionary

When a message has words that look like a dictation error, run:

```bash
python3 "<this skill>/scripts/tu_dien.py" sua "<message exactly as received>"
python3 "<this skill>/scripts/tu_dien.py" sua "<message>" --json
```

It prints the corrected text, the words it fixed, and the words it only suggests.

- Routine request: read the message with the corrections and continue.
- Important request (delete, publish, deploy, spend money, send to someone) that contained a fixed or suggested word: write one line "I understand this as ..." and wait for a yes before acting.
- A word that is not in the dictionary but is clearly a dictation error you can resolve from context: use that reading and say it is a guess. Do not guess when the two readings lead to different actions.

## Step 2. Learn

When the user corrects or confirms a word ("I meant GitHub", "yes, that one", "remember this word"):

```bash
python3 "<this skill>/scripts/tu_dien.py" hoc "<heard as>" "<meant>"
python3 "<this skill>/scripts/tu_dien.py" hoc "sq" "skill" --nhap-nhang    # hint only, never auto-fix
```

- Default is auto-fix. Use it for clearly wrong phrases that are not real words.
- Hint only (`--nhap-nhang`) is required for words that are also real words (SQL, SCP) and is applied automatically to anything of 3 characters or fewer. Add `--ep` to force auto-fix of a short word, only when the user asks.
- Learning the same phrase again with a new meaning overwrites it and keeps the old meaning in `ghi_chu`.
- Only save what the user corrected or confirmed. Never save your own guess.
- List entries with `tu_dien.py xem`, remove a wrong one with `tu_dien.py xoa "<heard as>"`.

The dictionary lives in `~/.claude/data/vietnamese-voice-dictionary/dictionary.json`, outside the skill folder, so learned words are never committed or lost on update. Until the first learned word it reads the starter list in `data/dictionary.json`. Set the environment variable `HIEU_GIONG_NOI_DATA` to keep it elsewhere.

## Optional: run it automatically with a hook

A `UserPromptSubmit` hook applies the dictionary to every message and hands the agent the corrected reading as context. It never changes the original message and stays silent on any error or when there is nothing to fix.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command",
        "command": "python3 \"<skill folder>/scripts/hook_userprompt.py\"" } ] }
    ]
  }
}
```

Put it in `~/.claude/settings.json` (all sessions) or a project's `.claude/settings.json`. This is a settings change, so ask the user before enabling it.

## Rules

- Never take an important action based only on a dictionary hit or a guess.
- Do not store names, passwords, keys or private content. Entries are short vocabulary only (60 characters at most).

## Limits

- It only fixes errors it has seen. A word misheard for the first time still needs a question or a guess.
- The starter entries are examples from one speaker's dictation. Check them against your own voice and remove the ones that do not apply.
- Matching is on the exact written form, ignoring case. It does not yet handle one word misheard in many unseen ways.
- Run the tests with `python3 "<this skill>/scripts/test_tu_dien.py"` (12 cases on temporary data).
