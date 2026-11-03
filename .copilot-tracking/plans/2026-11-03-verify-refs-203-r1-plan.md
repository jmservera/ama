---
title: Issue 203 round 1 plan
ms.date: 2026-11-03
---

* [x] Add src/core/tests/test_live_doc_links.py (stdlib only, skips when docs absent)
* [x] Run the test, ruff check/format and mypy (cache /tmp/mypy-203)
* [x] Commit artifacts, push, open PR with Refs #203

Details: [details](../details/2026-11-03-verify-refs-203-r1-details.md)

## Critique (executed once)

Verdict: compatible. Exclusions limited to append-only history; helper self-test proves it detects a missing target; no network or git dependency. Applied directly.

Tier: focused. Slice touches no security, infrastructure, SQL or deployment, so no gate is needed by this slice; the coordinator owns any gate.
