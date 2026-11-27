---
name: topic-research
description: "Web research for a lesson topic into learning/research.md: sourced claims and learning values. Use for 'topic-research', 'cào data', 'research cho lesson', 'tìm learning values'."
---

# topic-research

Find sourced material for one lesson topic and write it down so the lesson can be built from it. Input: a topic, plus the lesson folder (for example `library/lessons/04-deliver/<slug>/`). Output: `<lesson folder>/learning/research.md`. Do not write the lesson, the outline or the practice sheet; hand off to `build-lesson` for that.

Read first, if they exist: `_system/rules/vi-voice.md` (language), and any existing `learning/` file in the lesson folder (do not repeat what it already holds).

## 1. Frame the question

Write down in one or two lines what the lesson must let a learner do, and what a learner already knows. Pick 3 to 5 search angles: the concept, the tool steps, common mistakes, how it is tested or used in practice, and a counter-view or limit.

## 2. Search

- Run 3 to 5 `WebSearch` queries in one turn, in `standard` mode.
- Switch to `extended` only when a standard result is thin, off-target or possibly outdated, or when the topic is niche.
- Prefer primary sources first: vendor help docs, standards, research papers, the tool's own blog. Then practitioner blogs. Then forums and community posts, which are leads, not evidence.
- Read the page itself (web-fetch agent or direct fetch) for any claim the lesson will rely on. A search snippet alone is not verified.

## 3. Record every claim

Each claim goes in a table row:

| Claim | Source (URL, title, date if known) | Tier | Status |
|---|---|---|---|

- **Tier:** `primary` (vendor docs, standard, paper) · `secondary` (practitioner blog, course) · `lead` (forum, community, vendor marketing).
- **Status:** `đã xác minh` only when the page was read and the claim is on it. `chưa xác minh` for snippet-only. `[to confirm]` when sources disagree or the claim is old.
- Quote numbers and percentages only when a source gives them. Never estimate one.
- If a search says a feature exists but the docs cannot be read, keep the claim and mark it `[to confirm]`.

## 4. Write `learning/research.md`

Front matter: `status: private working notes`, `date`, `topic`. Then, in Vietnamese with English headings where they are terms:

1. **Kiến thức nền**: a table of concepts with one-line meaning and the source.
2. **Giới hạn và lỗi thường gặp**: each as a numbered item with its source. These become "bài tập bắt lỗi" material.
3. **Học liệu gợi ý**: links for the learner, with the tier.
4. **Learning values**: a table with IDs `LV1, LV2...`. Each row: the learning value, what the learner does when they have it, and which section above supports it. Aim for 6 to 9 values; the lesson picks 3 to 4.
5. **Dự thảo thời lượng**: a timing sketch that matches the lesson's session length, marked as a draft.
6. **Câu hỏi mở cho người dạy**: what the lesson cannot decide from research alone (prior knowledge of the group, the case to use, what comes next in the series).
7. **Nguồn**: the full list of URLs used, with tier and date.

## Rules

- Private: this file stays under `learning/`, never under the lesson's public files. Do not add it to any site page.
- No specific AI tool names in the text; use "AI chat tool", "AI coding tool". Tool names that are the topic itself (for example a Figma feature name) are fine.
- No mentee, company or cohort names.
- Never present an invented case or number as data. Label illustrative examples `bản nháp`.
- Keep `[to confirm]` markers. Do not fill them in to make the file look finished.
- Say what was not found. A topic with no good source is a result, and it goes in the file.

## Report back

In a few lines: number of sources, how many claims are verified, the list of learning values, and the open questions. Then stop; the user chooses which learning values to teach.
