---
title: Plan for issue 619 acceptance protocol
ms.date: 2026-11-02
---

* [x] Add `docs/reference/research/ux/production-ux-acceptance-protocol.md`
* [x] Add `src/api/tests/test_production_ux_acceptance_protocol.py`
* [x] Link from the WCAG baseline, `docs/reference/README.md`, append `docs/reference/log.md`
* [x] Focused gate `python3 tools/rpi-checks.py --changed`

Critique (single pass, executed): verdict proceed. Risk found and applied: the test must not let an agent fill a row without tester and date; done. PR must use Refs, not Closes, because human criteria are unproven.
