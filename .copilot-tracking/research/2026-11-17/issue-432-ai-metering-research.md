---
title: Issue 432 AI metering inventory research
ms.date: 2026-11-17
---

## Scope

Issue #432, tier FOCUSED, docs plus small tests, no Core store changes, demo-first.
Base eb51af5c9. Research disposition: executed. Planning Readiness: Ready.

## Opening state

* Issue comments record 7 of 9 criteria proven on main (1 to 4, 6, 7, 9). Open: 5 (Azure billing
  reconciliation against real cost records) and 8 (owner-authorised live measured batch).
* [docs/reference/resources/ai-tokenomics.md](../../../docs/reference/resources/ai-tokenomics.md) has a 2026-10-31
  source-only matrix and a "Gaps" table that predates merged work (it still says no price table, no denominator).

## Findings (filled during measurement)

See the measurement section appended below.

## Measurement (2026-11-17)

* Baseline: `cd src/core && python3 -m unittest discover -s tests -p "test_ai_consumption*.py" -q` ran 47 tests, OK
  (the dotted-module form fails on `from dataset import DATA` because `dataset.py` sits in `tests/`; a path artefact, not a defect).
  The installed `zava_forward.core` resolves to the main checkout, not this worktree; `ai_consumption.py` is
  identical at base and main HEAD, so the result applies. Recorded as a qualification.
* Code inventory (main, eb51af5c9): `core/ai_consumption.py` (`Consumption.price/authorize/reserve/complete/billing/report`,
  `batch_spread`, `report_period`); `core/assistants.py` (provider-envelope usage validation, settle on completion);
  `agents/chat.py` (per-call usage kept on `ModelUnavailable`); `agents/heldout_batch.py` and `heldout_aoai.py`
  (finite capped measured-batch runner, fail-closed); `api/resident_demo/aoai.py` and `assistant.py`
  (resident currency reservation, usage recorded as None when invalid); `api/server.py` consumption report route.
* Stale statements: the issue body's "Existing delivery" paragraph and the `ai-tokenomics.md` "Gaps" table
  (no price table, no denominator, no quality floor) predate the merged reporting, price, authority and
  held-out-runner work; the 2026-10-31 matrix lists the held-out batch as mechanism-only although
  `heldout_batch.py` now exists (merged #1559, #1566 per issue comments).
* Open criteria with no source-only fix possible: 5 (needs Azure cost records and Finance validation) and
  8 (needs an owner-authorised live batch). Neither can be proven in this scope.

## Planning Readiness: Ready

Smallest next step for the issue: owner supplies a spend authority and the batch runner is run once live,
then an exact-period Azure Cost Management export is passed to `Consumption.billing` to prove criterion 5.
