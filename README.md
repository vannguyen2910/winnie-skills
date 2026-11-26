# winnie-skills

Single source of truth for my skills. Installed at user scope, so every repo can use them.

| Plugin | Skills |
|---|---|
| vietnamese-writing | vi-voice, style-guide-vi, grammar-checker-vi, translationese-cleaner-vi, humanizer-vi, vietnamese-copy-polish, vietnamese-transcript-cleaner, vietnamese-voice-dictionary |
| teaching | teaching-slide-deck, notes-audit, landing-page, review, mentoring-training, training-course-designer, course-restructure, topic-research, slide-visuals |
| product-workspace | product-workspace, competitor-research, stakeholder-map, pestel-analysis, survey, interview, user-voice-synthesis |
| tools | viet-font-kit |

Rules: reusable skill -> here. Skill tied to one repo -> that repo's `.claude/skills/`.
Edit here, then `claude plugin marketplace update winnie-skills` (local path: edits are live after restart).
Add machine: `claude plugin marketplace add <path-or-github-repo>` then `claude plugin install <name>@winnie-skills --scope user`.

Five skills of product-workspace (stakeholder-map, pestel-analysis, survey, interview, user-voice-synthesis) are also shipped inside the course workspace-template. After editing them, run `scripts/sync-to-toolkit.sh` (`--check` to see drift).

Not included on purpose: `customer-journey-map` (CC BY-NC-SA 4.0 upstream, no commercial use without permission).
