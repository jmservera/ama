---
title: Research, demo home parent seeded with ready #74 only
description: Evidence and admission decision for the demo parent branch feat/demo-home-parent-0555
ms.date: 2026-11-13
---

Task `demo-home-parent-0555`. Refs #74. Disposition: executed, read-only inspection of git objects and the input's tracking records. Planning Readiness: Ready.

## Scope and base

* Branch `feat/demo-home-parent-0555`, exclusive worktree `demo-parent-seed-0555`, base `origin/main` `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626`.
* Admitted input: `6c86e1dc0e0db09ac01c7e4d54aae6ca4528aac9` (ready #74 packaging, final review and state). Ancestry verified: `f50c5c7fd` (source) then `078965085` (evidence pack) then `6c86e1dc0`, directly above the base.
* Not admitted: the #184 minute-integration candidate `e904`. The owner reports its actual state as partly new format FAIL and SQL unrun, so it is not ready. The #184 candidate object exists locally (`e904ba4c0`, per the critique) but was not admitted; its readiness is owner-reported. It does not appear in this parent's delta, and the home-scope input does not depend on it. The parent must not claim minute-v2 content.

## What the input is

* Source `f50c5c7fd`: three files (`src/api/README.md`, `src/api/checks/home_case_browser_check.py`, `src/api/src/zava_forward/api/web/app.js`). The home case view shows each shared building record's recorded `case_ids` and `package_ids` as listed IDs, Unknown (null) or None (empty). No eligibility, rules, API, filter or approval change; a disclaimer says scopes do not establish eligibility, approval or coverage.
* Evidence pack `078965085` and `6c86e1dc0`: 18 tracking files only (four byte-copied assessment and validation records, research, plan, clarification, critique, changes, handoff, review, state records).

## Evidence limits to carry unchanged

* Recorded results apply to source `f50c5c7fd` (the browser addendum records execution at `8b98f72a3` with source unchanged; the initial check results have no independent Review): node check, Ruff check and format, mypy, six existing API tests exit 0; one bounded browser run, 24 PASS markers, 0 FAIL. The markers are not 24 independent tests.
* Not proved: axe (SKIPPED), a valid base-red (unverified), hosted CI, human accessibility testing, WCAG conformance, owner confirmation of the G5 display or label. Optional G5 is not literal #74 criterion 2; compound criterion 2 stays open.
* The original source independent Review passed. The pack Review covers `078965085` copies and new records; `6c86e1dc0` added the review and modified the packaging plan and state; those final changes were not read by the earlier Review. The source budget for #74 history stays UNKNOWN; the initial addition is not a review correction.
* The plan's API-test-addition checkbox is qualified in the changes record, not rewritten in the original.

## Decision

Merge `6c86e1dc0` with a no-fast-forward merge so source and pack history is preserved. Add only parent RPI tracking records. Admit no functional edit. Future children target this parent only when ready or declared.
