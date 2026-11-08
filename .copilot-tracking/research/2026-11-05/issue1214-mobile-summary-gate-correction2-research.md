---
title: Issue 1214 correction cycle 2 research
description: Prerequisite and scope evidence for the rebased maintained-runner execution
ms.date: 2026-11-05
ms.topic: reference
---

## Brief

Correction cycle 2 of task issue1214-mobile-summary-gate (not a new task). Posture: focused. Original research, plan, critique, review and correction 1 records are preserved unchanged. Output mode: convergence on how to produce exact-final-head evidence with the maintained runner.

## Findings

* W1 PR #1217 state MERGED at 2026-11-05T12:33:10Z, merge commit 180dcf3e28d976169186ad38790471bec4b13934 (gh pr view 1217, retrieved 2026-11-05). origin/main fetched and pinned at that SHA; it moved from c6d5a8f3c (merge of #1217 only, tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md, docs/reference/log.md and #1215 tracking).
* C1 src/README.md:90-93 (new on main): the runner writes a bytecode-policy `.pth` into the API environment before discovery, which addresses the separate source-bytecode problem. No re-diagnosis with old tooling was done.
* C2 Local branch rebased cleanly onto 180dcf3e2: head 9584a7e1f; source diff vs main is only src/api/src/zava_forward/api/web/style.css (one line, `.top nav{row-gap:.125rem}` in the 600px block). Rebase rewrote commit IDs of the four prior commits; the pre-rebase head 5a4d3b208 is retained as the historical identity of correction 1 and is reachable via reflog only locally.
* C3 Dry selection for the diff (importing changed_groups, no execution): preflight, project-api, namespace, static, browser, image-api, logo-0600. Same as correction 1; no reassessment change. Coordinator authorised local image build, logo stress and Trivy/SPDX for this continuation only.
* C4 Heavy lock /tmp/ama-rpi-heavy.lock: no holder at start (fuser empty). Admission is the runner's own `--lock-timeout 0`.
* C5 Correction 1 evidence (72 units, 407 browser assertions) was at predecessor 3ee3b53e5; the later tracking-only commit invalidated exact-final-head claims. Pre-rebase evidence is now historical for the rebased tree and tool.
* Context reading disclosure: README index and memory were skimmed by size/headings; the 157KB case-study addendum was not read in full because the work is a CSS gate recovery with no case-study text change. Skipped deliberately, not silently.
* Guidelines: full upstream source retrieved successfully on 2026-11-05 (single 20000-character fetch, complete through Output Format).

## Decision and readiness

Run the maintained `--changed` runner on the final frozen head, verify partial scope, report. Planning Readiness: Ready. Research disposition: executed (focused).
