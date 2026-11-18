---
name: landing-page
description: Build or edit Winnie's course landing page (UX Level Up, site/public/landing-vN, static HTML/CSS/JS, Vietnamese). Use when she asks to make, redesign, tweak or review a landing page section, carousel, flip card, popup form or hero, or says "landing", "landing page", "trang đăng ký". Holds her design rules, the interaction patterns that already broke once, and a pre-ship checklist.
---

# Landing page (UX Level Up)

Static page at `site/public/landing-vN/index.html`, no framework. Brand tokens in `site/public/brand/tokens.css` (Manrope; `--ink --indigo --chartreuse --pink --soft --muted --line`). Copy the previous version into a new folder; never overwrite a published one.

## Design rules (she repeated these, do not make her say them again)
- White is the main background. Bold colour only at a few key points; alternate bold band, plain section, 1 column, multi column.
- No tab chips. No light-purple background under text. Little purple text; body text is ink.
- Icons: thin rounded Material Symbols (weight 300, fill 0), centred with the text. No solid check icons.
- Progressive disclosure: keep the first view clean, put secondary detail behind a button, `<details>`, or a popup. But do not hide content that fits (e.g. show all 6 outcomes, short).
- Section label: small uppercase text only, no dash before it. Captions and sub lines: one short line.
- Hero fills the first screen and eases into the content. Dot table of contents on the right.
- Motion on elements (reveal, count-up, draw-in) and always off under `prefers-reduced-motion`.
- Copy: keep her Vietnamese from the previous version; ask or use the `vi-voice` skill before writing new copy. English terms stay English.

## Patterns and the bug each one avoids
- **Horizontal carousel** (`.route`, showcase `.rail`): native `overflow-x:auto` + scroll-snap. Mouse drag in JS must check `pointerType==='mouse'` and reset on `pointercancel`; if touch is handled in JS the page gets stuck. Use unique variable names per carousel (a shared `sx` caused a SyntaxError). Prev/next buttons centred under a progress bar. Never pin a section and drive it by vertical scroll: users scroll sideways and get stuck.
- **Click whole card to open details**: toggle `<details>` on card click, ignore the click right after a drag (`moved` flag) and clicks on the `<summary>`.
- **Hover effects**: wrap in `@media(hover:hover)` so touch devices do not keep a stuck hover.
- **Flip cards**: flip on hover (hover media) and on tap/Enter/`:focus-within`; back side is info only; no flip icon chip.
- **Outlined text**: `-webkit-text-stroke` on a variable font shows overlapping contours. Fill with the background colour, `paint-order:stroke fill`, double the stroke width.
- **Material Symbols**: use only valid names (`local_florist`, not `florist`); hide icon text until the font loads (`.ms-ok` gate) so names never show as words.
- **Popup form** (`<dialog>`): name, email, LinkedIn URL, all required, inline red error. Endpoint is one constant (`REG_ENDPOINT`). If it is empty, show a real "chưa kết nối" error; never fake success. Needs a Google Apps Script / Formspree URL from Winnie.
- **Parallel `.stk` badges / SVG pills**: positions are SVG viewBox units; keep pills clear of the stroke of the stair path.

## Pre-ship checklist (do each, do not claim what you did not run)
1. Serve `site/public` (`python3 -m http.server`; astro may lack node_modules in a worktree). Reload with a new `?v=N`: the browser caches the old page and gave false results before.
2. 375px wide: `document.documentElement.scrollWidth === innerWidth`.
3. Console has no errors (the log can show stale entries from earlier loads; confirm after a fresh load).
4. Every icon renders as an icon, not text.
5. Tap a card, press next, open the lightbox and the popup, submit with a bad URL.
6. Reduced motion: nothing animates, nothing is hidden.
7. Say plainly what was not checked (real touch device, other browsers, hover with a real mouse).

## Ship
Commit to the `claude/...` branch and push. The site deploys only when merged into `main` (GitHub Actions, `.github/workflows/deploy.yml`). `gh` may be missing: give her the compare link `https://github.com/vannguyen2910/ai-design-workflow/compare/main...<branch>?expand=1`. Public URL: `https://vannguyen2910.github.io/ai-design-workflow/landing-vN/`.
