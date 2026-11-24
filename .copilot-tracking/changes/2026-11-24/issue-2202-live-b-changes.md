---
title: Issue 2202 live changes b, 2026-11-24
ms.date: 2026-11-24
---

## Changes (Refs #2202; not closing)

* Added `docs/reference/research/issue-2202-live-r2-2026-11-24.md` and its evidence folder (az state, probes, screenshots, tiles, coverage).
* `src/api/src/zava_forward/api/iot_stream.py`: in a bounded window an event after the deadline now ends the window normally; stop requests still raise RUN_STOPPED. One regression test in `src/api/tests/test_iot_stream.py` (fails without the fix, passes with it).
* Index row in `docs/reference/README.md` and entry in `docs/reference/log.md`.
* Validation: `tests.test_iot_stream` and `tests.test_live_control` 111 tests OK; `mypy` in src/api clean; `ruff check` and `ruff format --check` clean. Not run: full local gate and hosted CI (coordinator).
* Azure read-only: nothing created, changed or deleted. `rpi-checks.py --all` not run; tier FULL (src change), gate left to the coordinator.
* Divergence: the source fix and its failing-then-passing test were first tried before this record was written; that edit was reverted and re-applied after the implement-start witness.

## Per-criterion table

See the table in docs/reference/research/issue-2202-live-r2-2026-11-24.md. Summary: proven: revisions Healthy, hardening enforced, agents difference, charts, gauges, consent checkbox, chat routing, 58.9% coverage, receipt. Partly proven: images rolled (commit provenance unreadable, registry firewall). Noted not exercised: rollback (no drills authorised). Unproven: generative answers (owner actions), receiver fix live effect (needs image rollout).
