---
title: Issue 358 live research, second pass (opening)
ms.date: 2026-11-18
---

## Scope

Second pass over #358 after #1931. The earlier note left two gaps: the throwaway
app deletion has no retained output, and criterion 3 (#352 delegating `main()`)
was not re-verified. Authority: demo, resource group `ama`, no rotation, no
production change, no Graph credential change.

## Plan

* Re-read live state of `ca-cutover-test-demo-api` (read-only) and confirm
  `ca-358-throwaway` is absent.
* Re-run `infra/tests/test_setup_entra.py`, and check `initialize-api-auth.py`.
* Record a second research note under `docs/reference/research/`.
