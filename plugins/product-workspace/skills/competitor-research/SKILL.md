---
name: competitor-research
description: "Run competitor research inside an AI Product Workspace project: pick competitors, build a feature-by-product checklist, capture public product screens (web pages) with headless Chrome, keep a capture log, hand the owner a list of login-only and mobile screens, then tie screens and findings to claims in work/competitor-analysis.md (SWOT, opportunities). Use whenever the user mentions competitors, competitor analysis, competitor screens or screenshots, benchmarking products, feature comparison, 'chụp màn hình đối thủ', 'phân tích đối thủ', work/competitor-screens/, or asks to capture or compare how other products look and work, even if they do not say 'skill'."
license: MIT
---

# Competitor research

Evidence work for a product workspace folder (has `AGENTS.md`, `work/`, `insights/`). Read `AGENTS.md` first: its rules win over this skill. Read `references/lessons.md` before capturing, it holds site quirks learned in earlier runs. Add new lessons there, not here.

## Why this shape
A claim about a competitor is only worth as much as the page behind it. So every screen gets a URL, a date, who captured it and what it proves; anything not seen stays `unknown`. The owner is the one who can log in, pay and hold a phone, so work is split by what each side can do safely.

## Steps

1. **Scope** (ask only what the folder does not answer; use the owner's earlier answers if `work/competitor-screens/index.md` exists). Products, uses (evidence, flow comparison, inspiration, thesis figures?), web and/or mobile, which accounts the owner has, whether people on screens are blurred (owner decides; do not assume).
2. **Checklist.** Create `work/competitor-screens/index.md` (frontmatter `type: "competitor-screens"`, `stage: "Discover"`, `status: "draft"`, `supports: []`; follow `_ai/add-media.md`). Use the table in `references/checklist-template.md`: rows are features, columns are products, cells `☐ W ☐ M` / `✔` / `n/a` / `login`. Name the research questions it serves (AGENTS.md rule 11).
3. **Capture public pages myself.** No login, no account creation, no entered credentials, no bypassing blocks or CAPTCHAs. Method and file naming in `references/capture-method.md`. After each save, open the image and check it shows what you think it shows (cookie banners, blank pages, wrong language, popups hiding content).
4. **Log it.** One row per file in the Capture log: file, feature, product, platform, URL, date, who, what it proves. Then tick the checklist cell. A blocked, hung or 404 page goes under "Not captured, and why" as `unknown`, not as proof the page does not exist.
5. **Owner capture list.** For every row that needs a login or a phone, write what to look for, not what the screen contains (you have not seen it). Include the stop rule: no payment, no booking a real person, hide own email, card and meeting links.
6. **Tie back.** Link screens to the claims they prove in `work/competitor-analysis.md`, mark read level (`stated` on the page, `inferred`, `assumed`, `unknown`), and flag contradictions (a page's own title vs its content, "illustrative" numbers, test-looking demo data). Edit only the sections the owner asked for.
7. **Commit and report.** Check `git status`, commit the folder, run `python3 _ai/build-report.py` (do not hand-edit `index.html`). Report: files saved, what each shows, what was blocked, what the owner must capture, anything you did not verify.

## Rules for every screenshot
- Prices, ratings and counts are what the page said on that date; label sample or illustrative numbers as such.
- Internal evidence by default. Say so in "Source and limits" and do not use captures as thesis figures unless the owner decides to (copyright, personal data).
- Real people on screens: follow the owner's recorded choice. If none is recorded, ask before saving a page that shows personal data (AGENTS.md rule 6).
