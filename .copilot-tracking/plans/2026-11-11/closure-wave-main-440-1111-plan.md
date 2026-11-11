---
title: Closure-wave integrated-main checkpoint plan (Refs #440)
description: One bounded observation and documentation checkpoint of 1428, 1426, 1423 and 1430 on main 8aedb56b; plan only until Root admits
ms.date: 2026-11-11
---

## Objective

Observe existing focused selectors once on actual main `8aedb56b5909903abd6c6f84777b49f237c1cbb0` and, only after Root's admission, append ONE dated checkpoint to `docs/architecture/cutover-evidence-pack.md` and an append-only entry to `docs/reference/log.md` (index pointer only if needed) with actual results, a continue, fix or proposed-pivot recommendation, affected gates and independent lanes. No source, test, workflow or manifest edit. Not a Quality campaign, not a full gate, not acceptance.

## Validation tier (basis recorded)

Focused tier: documentation-only change plus existing targeted local tests. No workflow, gate-tool, dependency-manifest, Dockerfile, infrastructure, SQL, deployment or security-control edit; the one `pip` step installs into a private venv under `/tmp`, not a manifest. Doubt resolves upward: a source failure or a gate-semantics finding is reported to Root as full-tier material, not fixed here. The documentation commit still needs independent exact-head review, human approval and applicable hosted CI, none of which is claimed.

## Phases

* [x] Phase 0, plan-only launch: research, readiness, plan, details, one independent critique, state, local commit. No test or probe ran.
* [ ] Phase 1, preflight (after admission): assert cwd, branch, HEAD, tree and clean status; confirm `origin/main` unchanged or record the movement; create the raw directory outside the repo; verify the pinned axe asset sha256; create the private venv with editable installs and prove module origins under this worktree; confirm `~/.zava-forward` and `ZF_DATA` state before; check memory and that the lock is free.
* [ ] Phase 2, non-browser selectors: core, importer, API selectors from the details table, one run each, raw exit, run, skip and failure counts.
* [ ] Phase 3, browser selectors, sequential, each lock acquired once by nonqueued admission: handoff guidance browser under one external `flock -n`; handoff download UI and the capacity check unwrapped because each self-locks.
* [ ] Phase 4, record: ONE pack section and ONE log entry from the raw logs; requirement trace by document; recommendation; process record. Link and diff review only.
* [ ] Phase 5, native review, strict tracking, commit, handoff to Root. No push, PR, issue or board write.

## Stop rules

* Busy lock, missing Chromium, Playwright, Node, axe asset or venv: `blocked`, recorded raw, not pass; no queue, retry loop, kill or service install. One repeat after Root says the resource is free.
* Any failure: preserve the first raw failure, stop that surface, continue only independent selectors already admitted, map to the existing owners 80, 1419, 1360, 144 and 440, no new ticket, no source fix, no new test, no budget draw (80 C5 spent, no C6; 1360 and 144 E1 and E2 spent, three remain each).
* Unexpected skip in a browser selector, an executed count of zero, a missing nonzero expected count, or a module origin outside this worktree: not a pass.
* No test is rerun to improve a result; a rerun after a failure needs Root's direction.
* The #132 combined inventory and QA candidate is not imported, run or duplicated; record the remaining gap and resume point only.

## Boundaries

* Local observed on constructed synthetic fixtures, owned temporary SQLite or JSON stores and loopback servers only. No SQL Server, Docker, cloud, model, live, private data or new service.
* No consent, Legal, identity, QA, live, deployed or accessibility acceptance is inferred. Earlier adverse and process records stay unaltered; any correction is an additive dated note.
