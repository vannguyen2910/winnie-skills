---
name: product-workspace
description: "AI Product Workspace projects (AGENTS.md + insights/): new project, insights, opportunities, decisions, evidence, report. Use for 'tạo dự án mới', 'rút insight', 'ghi quyết định', 'tạo lại báo cáo'."
license: MIT
---

# Product workspace

The procedures, scripts and templates for a project folder now live **in the workspace itself**, in its `toolkit/` folder. This skill only points to them: do not look for copies here.

1. **Find the project.** It is the nearest folder, from where you stand upwards, that has `AGENTS.md` next to `insights/` or `work/`. Read that `AGENTS.md` first (folder map, where each file goes, hard rules). Do not read `_personal/` or `work/sources/_raw-private/`.
2. **Find the workspace.** It is the folder that holds the projects and a `toolkit/` folder. Its own `AGENTS.md` says how to create a new project: `python3 toolkit/tools/new-project.py "<Project name>"` from the workspace root.
3. **Pick the skill.** `toolkit/skills/README.md` lists them. Each skill is a folder: `toolkit/skills/<name>/SKILL.md` is the step card, with `templates/` and `examples/` next to it.
4. **Run the scripts** from `toolkit/tools/` (`new-item.py`, `build-report.py`, `serve-hub.py`, `flow-from-mermaid.py`), from inside the project folder or with `--project`. `new-item.py --help` lists every flag.
5. **After you change files,** rebuild the report with `build-report.py` and say what you created and what is still missing. Never edit `index.html` by hand.

The rules that always apply are in the project's `AGENTS.md`: propose first, use only what is in the files, anonymise before using real data, keep AI drafts apart from checked text, and never mark a decision `accepted` unless the owner said so.

If there is no workspace with a `toolkit/` folder, say so and ask the owner where it is. The toolkit is the source: it is edited in the workspace repository, and there is no other copy to sync.
