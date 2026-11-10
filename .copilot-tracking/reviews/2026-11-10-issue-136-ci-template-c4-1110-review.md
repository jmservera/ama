---
title: Review for issue-136-ci-template-c4-1110
description: One author-inline review of the template test correction
ms.date: 2026-11-10
---

Executed once, author-inline, no nested agent. Not independent approval.

## Outcome

Conformant for the one coupled test contract, with qualifications.

* The CI failure was a stale raw-text assertion, not a template regression: compiled default is 4, public-simulation enabled is 1. The template is unchanged.
* The replacement asserts the compiled conditional, parameter default False, min replicas reference, and no resident conflation; mutation checks show inversion, cap loss, default ON and a resident name are each caught.
* The target test, the whole resident-demo module, policy and container contract tests, and offline Bicep build and lint pass.

## Qualifications

* ruff check and format still exit 1 on baseline line 133 of the same file (identical at HEAD, not my hunk); mypy exit 1 with 20 baseline errors in this file and 3 known in the policy test, none introduced. Not a strict pass.
* Not run: startup image tests (inputs byte-identical, image reused), full suites, SQL, cloud.
* Retained adverse: edits batched with `implement-start` (witness qualification), earlier duplicate C3 launch, rejected CLI preflight, original hooksPath override, C2 spike.
* No whole-#136, #1288, live, human or production acceptance.

## Routing

No open findings. Optional later work: the baseline ruff and mypy cleanup in these test files.
