<!-- markdownlint-disable-file -->
---
title: Issue 349 main c8d16059 integration changes
description: Execution record for the bounded integration
ms.date: 2026-10-26
---

## Executed

* Remote e95c0f51 (bot, rubric score only, 73 for b765120a) was adopted by
  git merge --ff-only; no local divergence.
* Plan committed before merging; critique was Approve.
* Normal merge d362a361 of main c8d16059 (#455 resident preview, refs #444).
  One conflict, .github/rubric/scores/latest.json, resolved to main's
  baseline (zero diff versus c8d16059). The bot score for b765120a stays in
  history via the first parent. No rebase, force, push or PR edit.
* docs/reference/log.md merged automatically: zero lines removed versus the
  first parent, so both append-only sets are intact.
* No change to the tenant preflight, its test, the manifest or auth role maps.
  Merge delta versus the first parent is main's 53 files only.

## Checks (small, existing environment)

* 35 focused tenant-preflight tests passed.
* git diff --check versus main reports nothing outside byte-preserved
  historical patch archives, which were not edited.
* No heavy gate, browser, Docker, install, cloud, Graph or SQL action.

## Status

Receipt 7374c1fc is historical after this head and base movement. This is a
bounded local integration, not whole-issue acceptance; owner-reported login and
Entra-authoritative roles are not re-verified; the 2026-10-24 diagnosis stays
dated; #349 criteria remain unticked. A fresh whole gate is for the coordinator.
