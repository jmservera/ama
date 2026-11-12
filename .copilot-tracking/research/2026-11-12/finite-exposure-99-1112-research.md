---
title: Finite exposure observation guard (issue 99) research
description: Reproduction of a static candidate in exposure_limits.assess, local-only
ms.date: 2026-11-12
---

## Scope and approval

* Task `finite-exposure-99-1112`; branch `fix/demo-finite-exposure-99-1112`; base `d8509ebc4a21bf9de57e11ec687a2988134eb11d`; target main; `Refs #99` only.
* Owner approved "one bounded reproduce-and-fix candidate". This does not reset unknown historical correction balances and authorises no automatic corrections.
* Local-only: no push, issue/PR edit, deployment, provider/model call, spend or private data. Mode manual-style single pass; focused validation tier per owner demo instruction.
* Research disposition: executed (read-only reading, then a runtime reproduction). Planning Readiness: Ready.

## Sources read

* `docs/reference/README.md` (index), `docs/reference/memory.md` (context only), finance #96/#98/#99 pointer in the index, source `src/core/src/zava_forward/core/exposure_limits.py` and tests `src/core/tests/test_exposure_limits.py`. The original case study and addendum were not re-read in full for this narrow candidate; this is a stated limitation.
* The installed `zava-forward-core` editable install pointed at another checkout (`/home/azureuser/source/ama/src/core`). A venv outside the repository (`/tmp/f99/venv`) installed this worktree's `src/core` with pip (`pip install -e src/core ruff mypy`), exit 0, and the import path was confirmed to be this worktree. No `uv`, no `PYTHONPATH` workaround.

## Reproduction (runtime, synthetic fixtures)

Script and raw output: [repro.py](../../evidence/2026-11-12/finite-exposure-99-1112/repro.py) and [repro-before.out](../../evidence/2026-11-12/finite-exposure-99-1112/repro-before.out), exit 0. Fixture: envelope 100 GBP, tolerances capital 10 percent and safety 0 count, approval dated 30 days ago, all synthetic.

| Observation | Status before fix |
| --- | --- |
| committed = -inf, tolerances in range | Within limits, No pause signal |
| tolerances capital and safety = -inf | Within limits, No pause signal |
| all -inf | Within limits, No pause signal |
| committed or tolerance = +inf | Breach, Pause (reports an infinite observed value) |
| committed or tolerance = NaN | Unknown, Pause |

Root cause: `assess` rejects wrong types and NaN (`x != x`) but not infinities; `-inf > maximum` is false, so a nonfinite observation compares as "Within". `_number` already rejects nonfinite approved inputs, and `committed_exposure` already rejects nonfinite commitment amounts, so the gap is limited to the observation passed to `assess` directly.

## Impact boundary

* The finance route builds the observation from `committed_exposure` (it rejects nonfinite amounts, but summing very large finite floats could still overflow to infinity; tolerances are `{}`), so tolerances are Unknown there and no live false all-clear is claimed. The nonfinite-observation defect is demonstrated for observations supplied to `assess` directly; reachability through the finance route was not shown (critique correction CR-02).
* Negative finite observations (for example committed = -5) are also treated as Within. That is a different, unreported behaviour, left unchanged and recorded as a limitation and possible follow-up.

## Evidence of tests

Existing unit tests only covered NaN indirectly through the type check; no infinity case existed. Failing-first run: [test-before.out](../../evidence/2026-11-12/finite-exposure-99-1112/test-before.out), exit 1.
