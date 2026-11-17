---
title: Plan - prove rule provenance AC (#82)
ms.date: 2026-11-14
---

* Add `RuleProvenanceExposureTests` to `src/core/tests/test_gates.py`: every gate result carries a registered rule with all four fields; no unregistered `GateRule`; blank reviewer/version/source refused.
* No source change needed: implementation already satisfies the AC; the reviewer remains the honest unreviewed marker.
* Validate with unittest, mypy, ruff check, ruff format --check.
* Critique (single pass): the change must not claim professional review; PR uses `Closes #82` only if all four ACs are proven by tests, with the unreviewed-marker caveat stated.
