---
title: Issue 146 incident suspension and diagnostic redaction plan
date: 2026-11-14
task_slug: 146-incident-suspend-redaction-0038
---

* [x] Phase 1: widen `diagnostic_logging.SENSITIVE`, add traceback and exception-text redaction, keep `%` argument consumption; share the pattern with `monitoring_coverage`
* [x] Phase 2: add redaction tests (secrets, PII, identifiers, exception strings, operational markers survive)
* [x] Phase 3: add seeded event to breach to owned suspension to no-silent-restart test in `test_operator_suspension.py`
* [x] Phase 4: validate (ruff check/format, mypy, core, agents, api suites incl. scenario manifest)
* [x] Phase 5: review, commit with trailer, clean tree, no push

Details: [details](../../details/2026-11-14/146-incident-suspend-redaction-0038-details.md)
Critique: single pass, no conflicts with confirmed decisions. Applied: avoid changing `continuity.py` (already fail-closed) and keep the change additive.
