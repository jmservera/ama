---
title: Issue 212 residual research, home grouping
description: Research for the one unmet acceptance criterion of the deterministic rule engine
ms.date: 2026-11-01
---

Task: 212 / issue-212-home-grouping. Research disposition: executed. Planning Readiness: Ready.

## Findings

* Engine, alerts and API are merged (#328, #331). Criteria 1 to 6, 8 and 9 are ticked and
  evidenced in [test_rule_engine.py](../../../src/core/tests/test_rule_engine.py).
* Criterion 7 is unticked. Closure audit 2026-10-31 names the gap: `rule_engine.py` falls back to
  `home_scope="case_only"` and `home_id=case_id` when a case body has no `home_id`.
* Real case bodies have no `home_id`. They carry `home: {address, town, postcode, area}`
  ([store.py](../../../src/core/src/zava_forward/core/store.py), sqlstore.py case columns).
  Only the test fixtures set `home_id`, so grouping across cases is unproven end to end.
* Ranking by clock and harm, attention publication limit and false-positive classification are
  already implemented and tested (`alerts()`, tests at lines 338 to 504).

## Decision for the slice

* Derive a deterministic home key from the normalised recorded `home.postcode` plus `home.address`
  when `home_id` is absent. Label it `home_scope="address_key"` so it is never presented as a
  registered home identifier. Missing or empty address or postcode keeps `case_only`.
* No model involvement, no new data sources, no resident messaging.

## Unmet boundary (cannot be delivered here)

* A real staff precision and false-positive trial. Criterion 7 stays unticked in the PR, so the PR
  uses `Refs #212`.

## Evidence

* Issue 212 comments dated 2026-10-27 and 2026-10-31; ADR 0005 alert hygiene section.
