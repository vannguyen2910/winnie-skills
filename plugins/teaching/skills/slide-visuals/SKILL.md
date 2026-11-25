---
name: slide-visuals
description: Produce the visuals for a slide outline - schematic diagrams through the diagram-design skill, real screenshots from a Figma file the user owns, or outside images only with permission - save them in the lesson's assets/, link each one from its slide in the outline, and log every image's source and licence in assets/SOURCES.md. Use when Winnie says "slide-visuals", "làm hình cho slide", "vẽ sơ đồ cho outline", or an outline has DIAGRAM, COMPARE or IMAGE slides without a visual.
---

# slide-visuals

Make the pictures a slide outline needs, and keep a source log for each one. Input: path to a `*-slide-outline.md`. Output: files in the lesson's `assets/`, a `- Hình:` line on each slide that uses one, and `assets/SOURCES.md`. Do not change slide text, layout or speaker notes; that belongs to the outline owner.

## 1. Find the slides that need a visual

List the slides whose layout is `DIAGRAM`, `COMPARE`, `IMAGE`, or whose Visual hint names a picture. For each one, note the Visual hint and the register:

- `SCHEMATIC`: a mechanism, flow, state or comparison. Draw it.
- `REAL`: a real screen, a real photo or a real artifact. Use a screenshot of the user's own file, or ask.
- Text-only slides (`STATEMENT`, `NUMBERED`, `PROCESS`, `MILESTONE`) need no image. Skip them.

Never mix the two registers on one slide (`_system/rules/slide-deck-rules.md`, Visual language).

## 2. Schematic slides: use diagram-design

Load the `diagram-design:diagram-design` skill before drawing. Hand-drawn SVG outside that skill breaks the repo's diagram rule.

- Choose the visual type from the skill's table. Name the type and the size preset in one line before drawing.
- Write one file per slide: `assets/<lesson-slug>-<topic>.html`, self-contained.
- Run the skill's `self_check.py` on each file. Fix before linking.
- Export to `.svg` or `.png` only when the user asks. The export is manual.
- If the project has a brand token file, ask once which skin to use. The default skin is a valid choice; say so.

## 3. Real-screen slides: a Figma file the user owns

- Ask for the file link, or for permission to create a demo file in the user's Figma. Do not guess a file key.
- Use the Figma connector's screenshot tool on the named frame. Save as `assets/<lesson-slug>-<topic>.png`.
- Log the file as `chụp từ file của tôi` in SOURCES.md.

## 4. Outside images: only with permission

Do not download an image from a web page on your own initiative. Before any download, state to the user the source URL, the filename, the approximate size, and the licence you found. Wait for a clear yes. Then:

- Check the licence page. Accept only a licence that allows reuse in teaching materials (for example CC BY, CC0, or the source's own educational terms).
- Save into `assets/` and log it.
- If the licence is unclear, do not use the image. Describe the screen in a schematic instead.

## 5. Link and log

- In the outline, add under the slide's header: `- Hình: \`../assets/<file>\`` (relative path). If the slide already has a `Visual hint`, the link goes just above it.
- Append one row to `assets/SOURCES.md`:

| File | Slide | Loại | Nguồn | Bản quyền | Ngày |
|---|---|---|---|---|---|

`Loại` is one of `tự vẽ (diagram-design)`, `chụp từ file của tôi`, `ảnh bên ngoài (đã được phép)`.

## Rules

- Visuals never carry names of mentees, companies or real people unless the user has cleared it.
- Images are not text. Keep any label inside an image in the lesson's language and do not add tool brand names.
- If a slide has no visual yet, leave its Visual hint in place; do not delete it.
- Report which slides got a visual, which are waiting on the user (a Figma link, a licence check), and which files still need `self_check`.
