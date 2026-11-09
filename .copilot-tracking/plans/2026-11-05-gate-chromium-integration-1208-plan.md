---
title: Gate Chromium integration and native Runner evidence plan (#1208)
description: Plan to merge accepted main and prove the Runner Chromium path natively at the final head
ms.date: 2026-11-05
ms.topic: reference
---

* Phase 1: fetch and merge origin/main (3d7ad2fe) with a merge commit; reconcile conflicts append-only (none predicted).
* Phase 2: author the external harness /tmp/ama-1208-runner-harness.py that drives the real Runner; commit these RPI artifacts so the head is final.
* Phase 3: on the final committed head, run the focused tier: tools.test_rpi_checks, test_ci_affected, test_backlog_sync; Ruff, format and mypy with external caches; then, under a nonqueued heavy lock, the harness (Runner install, Runner.install_chromium, Runner.command resident-summary test, one test, zero skips). Record all evidence externally; make no later commit.

Critique: executed once, self-review. Compatible finding applied: the harness must not use a standalone install command and must keep check_skips fail-closed. No whitelist change, no full gate, no receipt.
Details: [details](../details/2026-11-05-gate-chromium-integration-1208-details.md).
