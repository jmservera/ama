<!-- markdownlint-disable-file -->
# Research: Issue #201 cut-over evidence sync after 1586 (0018)

* Task: `201-post-1586-sync-0018`; branch `docs/demo-201-post-1586-sync-0018`; base `origin/main` `38b13ec9e44e8be47d9817eaf4412b15b0626d4a` (PR 1586 merge), equal to HEAD; tree `962a3a80ed2d666443ae0f0c7ead976d0c8c3ea1`.
* Research disposition: executed. Planning Readiness: Ready.
* Open PR 1584 (#201) appends a "Current-main cut-over local verification (2026-11-13)" section to the end of `docs/architecture/cutover-evidence-pack.md` and adds its own `201-cutover-evidence-current-main-2333-*` files under the 2026-11-13 tracking folders. To avoid a textual conflict, this task inserts its section before the "Post-wave stabilization checkpoint" heading, away from the file end, and uses distinct artifact names and a distinct dated folder.
* Link check: all relative file links and in-page anchors in the pack resolve at this head; no inbound link to the pack from docs or `src/README.md` is broken.
* `mvp/` and `prototype/` have zero tracked files; `src/` holds core, agents, api, orchestrator, importer.
* Local test evidence comes from pip venv `/tmp/venv-201-0018` with editable installs; results are in the pack section and the review artifact.
* Issue #201 open criteria are unchanged: CI equal-coverage proof, deployed healthy src build, dependent epics, private data relocation, owner sign-off. Nothing here ticks them.
