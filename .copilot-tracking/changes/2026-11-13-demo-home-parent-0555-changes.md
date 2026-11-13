---
title: Changes and holds, demo home parent seeded with ready #74
description: Mechanical integration record, exclusions, holds and remaining publication gates
ms.date: 2026-11-13
---

Refs #74, not closing. Local only; no push, PR, issue or checkbox change.

## Integration

* Base `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626`. Merge commit `1f3e24449` (`--no-ff`) of `6c86e1dc0e0db09ac01c7e4d54aae6ca4528aac9`; first parent is the base. History of `f50c5c7fd`, `078965085` and `6c86e1dc0` is preserved.
* Merge tree `a09d9ae96aa5fe88ccfd420e7a00a51b15ac9f68` equals the `6c86e1dc0` tree. Source blobs equal `6c86e1dc0` and `f50c5c7fd`: `src/api/README.md` `1b9fb02d3`, `src/api/checks/home_case_browser_check.py` `57db4756f`, `src/api/src/zava_forward/api/web/app.js` `2fdf48045`.
* Differences from main: those three modified files plus 18 added `.copilot-tracking` files (input records). Nothing else changed. No functional code or source correction was admitted; no input file edited. Original adverse and independent records, including the original source Review, are preserved.
* Parent tracking added after the merge: this record, research, plan, critique, then the review and state records added after the independent Review returned (not themselves reviewed).

## Exclusion and holds

* Excluded: #184 `e904`. Owner-reported actual state: partly new format FAIL and SQL unrun, so not ready. It does not block this independent input. The parent does not contain minute-v2.
* Hold: no #184 content enters until its format failure and SQL are resolved and it is declared ready; then admit it as a separate integration with its own validation.
* Future children target this parent only when ready or declared, never as speculative main PRs.

## Evidence limits (unchanged from the input)

* Recorded on source `f50c5c7fd`: six existing API tests, node check, Ruff check and format, mypy exit 0; one bounded browser run, 24 PASS markers, 0 FAIL. Not 24 independent tests. Axe SKIPPED, base-red unverified, human AT, WCAG and outcomes unproved. Optional G5 is not literal #74 criterion 2. The false API-test-addition plan checkbox is qualified in the input changes record, not rewritten. Source budget for #74 history is UNKNOWN; the initial addition is not a review correction.
* Review coverage: original source Review passed; pack Review at `078965085` covers copies and new records; `6c86e1dc0` added review and state and modified the packaging plan, not read by that Review. Overall new head assessment is not claimed beyond the independent Review in [the review](../reviews/2026-11-13-demo-home-parent-0555-review.md).

## Remaining publication gates (none performed)

* Fetch main; recompute provenance on the exact head; re-run focused validation (node check, Ruff check and format, mypy, six API tests, one bounded browser run, axe if pinned file available) on the exact parent head.
* Independent exact-committed-head review, owner and human approvals, AT and WCAG evidence, applicable hosted CI, then PR with `Refs #74`. Full gate if combined with infrastructure, SQL or security-sensitive work. This integration does not authorize publication.
