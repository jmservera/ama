---
title: Issue 1259 ranking archive path health plan critique
description: One independent read-only critique of the 1259 prospective plan, with dispositions
ms.date: 2026-11-08
---

## Inputs and boundary

* Plan, details and research for 1259 under .copilot-tracking, checked against ranking_publication.py, ranking_publication_runner.py, store.py and the runner tests. No test, install, network or git write was run by the critic.

Critique execution: Complete (independent rubber-duck subagent, single pass). Verdict: Revise.

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | High | A path under a dangling-symlink ancestor makes both stat and lstat return ENOENT and would be reported as absent | Accepted. Details phase 2.3 now walks to the nearest existing ancestor and requires it to stat as a directory; tests add dangling-ancestor and symlink-to-directory control |
| PC-002 | High | exercise=True publish bypasses the archive_unreadable refusal | Resolved as a scoped decision: keep the existing exercise convention (read-only dry run, never writes, exempt as for the PermissionError case); the test asserts written False, nothing created and unknown window with the unreadable problem shown. Not a governance change |
| PC-003 | High | tests.test_* import cannot resolve fixtures | Accepted. Command is PYTHONPATH=tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q for red and green |
| PC-004 | Medium | Store.ranking_publication_status reports overdue True rather than unknown for unreadable | Scoped. Pre-existing for PermissionError; one test asserts a problem rather than healthy; the overdue semantics are a residual follow-up, not widened here |
| PC-005 | Medium | Runner fallback str(e) can contain a path | Accepted. Fixed path-free fallback phrase in _verify (only planned runner change) plus a test |
| PC-006 | Medium | Phase 1.1 claimed a commit before it existed | Accepted. Wording changed; the commit is recorded in state and response |
| PC-007 | Low | Gate command omits stack provenance | Accepted. --stack heads of 1258 and 1259 added to the later gate note |

No repeat critique is planned for this task. Residual risk: the 1258 hunks in ranking_publication.py are unverified until propagation.
