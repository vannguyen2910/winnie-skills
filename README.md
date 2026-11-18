# winnie-skills

Single source of truth for my skills. Installed at user scope, so every repo can use them.

| Plugin | Skills |
|---|---|
| vietnamese-writing | vi-voice, style-guide-vi, grammar-checker-vi, translationese-cleaner-vi, humanizer-vi, vietnamese-copy-polish, vietnamese-transcript-cleaner, vietnamese-voice-dictionary |
| teaching | teaching-slide-deck, notes-audit, landing-page, review, mentoring-training, training-course-designer, course-restructure |
| product-workspace | product-workspace |
| tools | viet-font-kit |

Rules: reusable skill -> here. Skill tied to one repo -> that repo's `.claude/skills/`.
Edit here, then `claude plugin marketplace update winnie-skills` (local path: edits are live after restart).
Add machine: `claude plugin marketplace add <path-or-github-repo>` then `claude plugin install <name>@winnie-skills --scope user`.
