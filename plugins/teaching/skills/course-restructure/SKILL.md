---
name: course-restructure
description: "Reorganize a course or multi-file content set: merge, split, move, renumber lessons and keep paired files in sync. Use for 'restructure this', 'tái cấu trúc khoá học', 'chuyển bài này'."
---

# Course / Curriculum Restructure

A routine for reorganizing a body of course or curriculum content that lives across many files — sections, lessons, slide outlines, scripts, worksheets — where some of those files are paired and must be edited together, and where a master document (an outline, syllabus, or table of contents) needs to stay accurate.

The core risk in this kind of work isn't technical, it's editorial: silently inventing content the user never gave you (their teaching methodology, a case study, a process they haven't described), or quietly dropping content that used to exist somewhere and now has no home. This skill exists to structure the work so neither of those things happens by accident.

## Why this is a distinct workflow

Restructuring isn't the same job as writing new content or editing one file. Three things make it its own thing:

1. **The plan has to be locked before any file moves**, because once you start moving content around, undoing a wrong call is expensive — you're untangling merges, not reverting one edit.
2. **Files are often paired.** A lesson file might have a matching slide-outline file, a script, a worksheet. If the project has a rule that says "when one changes, update the other" (check for a `CLAUDE.md`, a style guide, or the user just telling you), that rule has to hold for every single move, not just the first one.
3. **Not all new content is yours to write.** Some of what's needed to fill a new section is fact you can look up (how a tool works, a public methodology) and some of it is the user's own IP (their 5-step process, their case study, their framework). Confusing the two means you either waste a research pass on something you should have asked about, or you invent something in the user's voice that they never said.

## The workflow

### Phase 1 — Brainstorm the structure (no files touched yet)

Before editing anything, understand what currently exists. Read the current folder/file layout and skim the key content files — you can't evaluate a proposed restructure, or spot what it leaves homeless, without knowing what's actually there today.

When the user proposes a new structure, don't just agree and start moving files. Compare it against the current one out loud and surface the real tradeoffs:

- **Content with no home.** If section X is disappearing, where does everything currently in it go? Get an explicit answer for every piece, not just the headline items.
- **Terminology or framing changes.** If the user asks to rename a concept or drop a term (jargon that doesn't read naturally, a label that's confusing), note every file that uses the old term — you'll need to sweep for it later.
- **Ordering and numbering ambiguity.** Does a new unnumbered/optional section still need a place in the file-listing order? Does content get duplicated across two parallel tracks, or shared once?
- **Scope creep in "new" sections.** If the user is adding an entirely new section (a new tool, a new topic), that's usually the part of the restructure that needs real content authoring later, not just file-shuffling — flag that early so it doesn't sneak up during execution.

Keep this conversational. Ask direct questions when a decision is genuinely the user's to make (not something you can infer from their existing content or conventions) — don't silently guess on things like numbering schemes, naming, or where dissolved content should land. It's fine for this to take several exchanges; a wrong structural assumption caught here is nearly free, caught after execution it isn't.

### Phase 2 — Turn the locked structure into a migration checklist

Once the structure is agreed, write out a concrete, file-level checklist before touching anything. For each unit of change, name the actual files involved:

- **Moves**: "Lesson X (currently in File A) → becomes Lesson Y in File B."
- **Merges**: "File A's Lesson 2 + File C's Lesson 1 → combined into one lesson in File D, keep both practice sections but merge into a single closing exercise."
- **Dissolves**: "File E is being retired — confirm every piece of its content has a destination before deleting it."
- **New content**: "Section F is net-new — no source material exists yet." Call this out distinctly from moves/merges, because it's the part that needs Phase 3's research-vs-ask judgment call, not just file surgery.
- **Downstream housekeeping**: any master outline, landing page copy, or index that describes the current structure and will need updating once the move is done.

Surface any decisions still open (naming, numbering, whether a new section needs its own version of something an old section had) as explicit questions, and get them resolved before proceeding. Then get an explicit go-ahead to execute — a restructure touches a lot of files at once, so this is exactly the kind of multi-step, hard-to-undo work worth a clear "yes, go" rather than assuming approval from a general "sounds good."

### Phase 3 — Execute

Set up a task list with one task per major item in the checklist (one per section move/merge/new-write), so a long multi-phase job doesn't lose track of itself partway through. Work through it in dependency order — usually: absorb/move existing content first (lowest risk, content already exists), then trim/rename the sections that gave content away, then write net-new sections last (highest risk, needs the most judgment).

For each item:

**Read the full source content before editing it.** Don't paraphrase from a skim — if you're moving or merging content, the goal is usually to preserve it faithfully, not rewrite it. A quick read of headers will miss the details you need to migrate correctly (a checklist buried in prose, a numbered list that needs to stay numbered, a specific example the author chose deliberately).

**Check for project conventions before you start editing, and hold them for the whole job.** Look for a `CLAUDE.md`, a style guide, or anything the user has told you about how this content is supposed to be written or kept in sync. The most common one is a pairing rule — e.g. "lesson file and slide outline must always be updated together" — if that exists, it applies to every single file you touch, not just the first pair. Also check for voice/tone rules (how formal, which words are banned, what terminology stays untranslated) and apply them to anything you write fresh, not just what you're copying over verbatim.

**Migrate before you polish.** When content is moving, copy it faithfully first, then make the minimal edits actually required by the move itself — renumbering, updated cross-references, a rephrased transition sentence. Resist the urge to also improve the prose while you're in there; that's a separate ask, and it makes it harder for the user to spot-check that nothing was lost in the move.

**Split "new content" into two very different cases, and handle them differently:**
- *Externally verifiable facts* (how a piece of software works, a documented process, current best practice) — research it before writing, don't rely on possibly-stale memory. Ground the new section in what you found, and cite sources if the platform's citation rules require it.
- *The user's own methodology, case studies, or judgment calls* (their teaching framework, an anecdote from their work, a process only they've defined) — do not invent this. Stop, write the rest of the checklist, and flag this specific piece back to the user as something you need from them before you can draft it. Inventing a plausible-sounding version in their voice is worse than leaving a visible gap, because a gap gets caught and a fabrication might not.

**Handle the filesystem mechanics directly**: renames are usually a plain move/rename operation; deletions occasionally get blocked by sync/permission layers (cloud-synced folders, some workspace setups) — if a delete fails with a permission error, look for and use whatever access-request mechanism the environment provides rather than reporting the deletion as impossible.

**Sweep for stale cross-references once content has moved.** Search the entire content tree (not just the files you edited) for old section names, old numbers, old terminology you were asked to retire. Anything referencing a section by its previous name or number, or citing a lesson that got renumbered, needs fixing — these references live in places you won't think to check (an intro slide in one section referencing "coming up later," a worksheet pointing back to "the lesson you did earlier").

**Update the master document last.** Any outline, syllabus, table of contents, or landing-page description of the course structure should be rewritten to match reality only once the actual content files are settled — otherwise you're describing a structure you haven't finished building yet.

### Phase 4 — Report back clearly

Summarize what changed, organized by what moved where — not a chronological blow-by-blow of every tool call. Then, distinctly and not buried at the end of a long paragraph, call out:

- Anything you deliberately left undone because it needs the user's input (the methodology/case-study gap from Phase 3), and exactly what you need from them to finish it.
- Anything now stale as a side effect of the restructure but out of scope to fix right now (marketing copy, a pricing page, anything downstream that describes the old structure but has its own open decisions blocking a rewrite) — name it so it doesn't get forgotten, don't silently leave it broken.

## Things that go wrong if you skip a phase

- **Skip Phase 1, go straight to executing:** you'll build the wrong structure confidently, and the user has to catch it after the expensive part is done.
- **Skip Phase 2, execute straight from the conversation:** you'll lose track of some piece of content that had no explicit destination, and it just quietly disappears.
- **Skip the "read full source before editing" step:** merges and moves lose details — a caveat, a specific number, an example the author chose on purpose.
- **Skip checking for a sync rule, or apply it inconsistently:** you end up with one pair of files in sync and three pairs silently drifted apart, which is worse than never having the rule in the first place because it's not obvious anything's wrong.
- **Skip the research-vs-ask split and just write everything:** you'll produce fluent, plausible content for the parts that were actually the user's unique expertise, and they may not catch that it's not what they'd have said, until a student does.
- **Skip the final cross-reference sweep:** the files you directly touched are consistent, but the rest of the content tree still talks about the old structure.
