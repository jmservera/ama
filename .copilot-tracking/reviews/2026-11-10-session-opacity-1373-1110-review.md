---
title: Issue 1373 resident session opacity test-oracle review
ms.date: 2026-11-10
task_id: 1373-session-opacity-1110
---

## Execution and outcome

Review executed once on 2026-11-10 after implement-done, by the implementing agent (no nested agents). It is not an independent exact-head assessment; the Root's independent review before publication remains required. Outcome: accepted with no blocking finding. Assessed boundary: working tree over HEAD `9e71736bc09984b07d77c122747483548b580c7d`, one modified file `src/core/tests/test_resident_showcase.py`, plus the RPI records.

## Checks performed

* Diff read in full: only the imports, the helper, the rewritten opacity method and the new regression changed; neighbouring tamper, expiry, restart/key rotation, logout/revocation and CSRF tests are untouched.
* Production source unchanged: `git diff --name-only 9e71736bc -- src` lists only the test file.
* No `_mac`/`verify` mock, run-time search, retry, skip, entropy or alphabet change. Only the module's `secrets` name is replaced inside a `with` block in the regression.
* Token hygiene: a scan of the committed records and the test file for the fixture handle and MAC fragments found nothing; raw logs stay outside the repository.
* Mutation sanity (scratch script, no repository edit): a handle containing the case id fails both new tests (2); a handle not bound to the case fails both (2); a verifier that accepts any MAC fails the regression (1); the baseline passes (0). The tests therefore detect the properties they claim.
* Re-ran results recorded in the changes record: SessionTests 10 OK, resident showcase module 41 OK, Core discovery 2,865 OK (skipped 347, unchanged), Ruff check and format, configured mypy clean, 200 repeat runs of SessionTests clean.

## Findings

| Finding | Severity | Routing |
| --- | --- | --- |
| The `token[:-2] + "xx"` tamper case in `test_tamper_expiry_and_garbage_denied` is vacuous only if a genuine MAC ends in `xx` | Low | Out of scope for this one repair; later user-selected work only; not fixed here |
| Hosted required Core CI, full Core and other projects not run locally in this tier | Info | Required later on the exact published head and after the parent 1371 refresh |
| Same-agent review | Info | Root independent exact-head review before publication |

No authentication bypass was found or introduced, and no security acceptance is claimed. No post-review extension of the repair allowance is created; the Low finding is a distinct follow-up.
