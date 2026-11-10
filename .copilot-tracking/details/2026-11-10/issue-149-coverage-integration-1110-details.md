---
title: Issue 149 coverage parent integration details
description: Exact commands and acceptance details for the focused DEMO-tier integration
ms.date: 2026-11-10
---

## Common environment

Owned venv `/tmp/i149-1110/venv` (Python 3.12.3; ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0; editable `src/core`, `src/agents`, `src/api[dev]` of this worktree; `src/importer` added editable only for its unit suite). `PYTHONDONTWRITEBYTECODE=1`. Working directory `src/api` unless stated. Raw logs under `/tmp/i149-1110/logs/` with `M*` labels for post-merge runs (baseline `B*` unchanged). Browser work only under `flock -n /tmp/ama-rpi-heavy.lock` (never queued; actual holder checked first with `fuser`; a busy exit is recorded as blocked and distinct from a check failure).

## P1 merge

1. `git status --short` empty (tracking artifacts of this task excluded); `git fetch origin`; `git rev-parse origin/main` equals `d52f20a5198de7269f39daf794911545aee01ced`.
2. `git merge --no-ff origin/main -m "<message>"` with trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
3. Verify: parents (first `ae4b20007`, second `d52f20a51`), tree equals `a9b51381c57eb233e8aae2371a3b8456e23147ab`, `git diff --check`, no `<<<<<<<` markers, both histories' entries present in `docs/reference/log.md` and `README.md` once, `git diff HEAD^1 --stat` limited to main's delta, `git diff HEAD^2 --stat` limited to the parent's delta.
4. Conflicts, if any: resolve by keeping both sides; stop for Root if the resolution needs a semantic choice.

## P2 checks

* Q1 Importer editable install into the venv; manifest check: `git diff --name-only` of both sides against the scenario manifest registered sources (read `src/core/tests` manifest module) to decide whether scenario or needs-manifest tests apply.
* Q2 API unit: `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest -v test_atlas_tensions_checker test_handoff_read_guidance test_handoff_api test_role_screens test_role_screens_conformance test_programme_screen test_workspace_paging test_role_endpoint_inventory test_workbench test_exception_register test_exception_register_screen test_finance_grants_screens test_form_held_download_api test_form_staging_api`.
* Q3 handoff browser: same selector `test_handoff_read_guidance` with `ZF_BROWSER_TESTS=1` under `flock -n`.
* Q4 Core from `src/core`: `python -m unittest -v test_import_refusals` (the only Core test the main delta changed; no Core test references the exception register). Importer from `src/importer`: `python3 -m unittest discover -s tests -v` (README command). Core `test_resident_showcase` is not selected, so the PR 1371 collision is neither hit nor waived.
* Q5 `ruff check .`, `ruff format --check .`, `mypy` (no selectors) in `src/api`; ruff and mypy per README for Core and importer on the changed Python files only if their projects configure them (mirror CI selectors, no new command).
* Q6 Browser under one nonqueued admission via `/tmp/i149-1110/run-browser.sh M1` (role screens default, 230, 231, 231q, 231p, 231qp; atlas; paging) and `held_form_download_browser_check`. `ZF_AXE_JS=/tmp/axe-4.10.3.min.js`; axe classification per check.
* Q7 Web review: read `app.js` #153 hunk and `role-screens.js` #96 hunk against the fetched guideline rules; report `file:line` findings; no edits.
* Q8 Read `handoff-1362-version-diagnostic-1110.md` (present, read) and the issue 149 record; no resolution claimed.

## P3 record

Section title `Parent 149 coverage integration checkpoint (2026-11-10, Refs #149 #440 #153 #156 #230 #231 #233 #96)` appended after the last section. Subsections: identities and scope, merge delta and conflicts, observed commands (baseline and combined), requirement trace (document-qualified), classification, findings and owners, gates, recommendation. Index: one paragraph after the discovery CLI paragraph in `docs/reference/README.md`; log: one appended entry, both linking the pack.

## Acceptance

All Q commands exit 0 with recorded counts and skips; the merge tree identity matches; no source or workflow file edited by hand; the two commits carry the identity and trailer; the tree is clean after the commit; witness verify exit recorded.
