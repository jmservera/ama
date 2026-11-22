---
title: "Gate flakes, issue 2190: re-verification on current main"
description: Re-run of the three gate flake fixes merged in #2220 on the current head, with a per-criterion verdict for issue 2190.
ms.date: 2026-11-22
---

Scope: issue #2190 criteria "each reproduced or explained, fixed with a regression test, no check relaxed". Synthetic DEMO, desktop only. No Azure resource was read or changed; the flakes are local gate behaviour. The fixes landed in commit c9350f3a3b (#2220); the reproduction and explanation are in [the 2026-11-21 note](./issue-2190-live-20261121-2026-11-21.md). This note re-verifies them on head 671a17fde3 and changes no source file.

## Re-verification

* Flake 1 (`_region_passed`, `_classes_executed`, `check_skips`): `python3 -m unittest tools.test_rpi_checks` ran 123 tests, OK ([output](./issue-2190-live-20261122-evidence/gate-tests.txt)).
* Flake 3 (218 timeout): `test_rai_release_readiness_api_218` ran 5 tests in 21.3 s, OK, including the budget test ([output](./issue-2190-live-20261122-evidence/api218.txt)).
* Flake 2 (`late_success`): `checks.employee_chat_browser_check` with 14 busy-loop processes on 8 cores passed 6 of 6 runs ([runs](./issue-2190-live-20261122-evidence/chat-check-loaded-runs.txt)); the final line reports the nine controlled late successes passing.

## Per-criterion verdict

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Each flake reproduced or explained | Proven | Reproduction and cause in the 2026-11-21 note (flake 1 on real output, flake 2 once in 15 loaded runs, flake 3 in 9 of 12 loaded runs); not repeated here |
| Fixed with a regression test | Proven for flakes 1 and 3; unproven as a deterministic test for flake 2 | Gate tests and the 218 budget test pass now. Flake 2 is a real-browser timing race; only repeat runs under load (6 of 6 here, 0 of 30 failures after the fix on 2026-11-21) support it |
| No check relaxed | Proven by inspection of c9350f3a3b and passing rejection tests | Failing patterns and snapshot fields are unchanged; a wait before the snapshot and a larger transport timeout were added |

Not run: the complete local gate (`rpi-checks.py --all`), hosted CI for the final head.
