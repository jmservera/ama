---
title: Issue 114 loadcheck correction ONE receipt
description: Separate implementation receipt for original Review RV-001, not a second Review
ms.date: 2026-10-18
---

## Authority and Boundary

Caller explicitly preauthorized same-branch original-finding corrections, maximum two source cycles.
This is correction ONE for RV-001 only, not another original Review or corrected-head acceptance.
Original Review remains Not accepted and unchanged:
`.copilot-tracking/reviews/logs/2026-10-18/issue-114-loadcheck-evidence-review.md`,
SHA-256 6510bcd1d1055621b7fb37f73f7ef84426ec5160b65ef1e8bef7bd424017befe.
Candidate e63426148b5bac564ffef4195a9ba3b1b873d068 remains the assessed candidate.

## Intended Correction

`math.isfinite(10**400)` raises OverflowError; CLI currently reaches mocked factory before that
failure. Use direct ordered comparison against the largest supported finite float, without
converting oversized integers. Apply equivalent CLI check before file/store access. This is
representability validation, not an arbitrary runtime duration cap.
Add direct and actual-main oversized positive/negative subcases to existing methods; no new
test method, source target, config or dependency.

## Execution Status

Complete as local implementation evidence. One source correction cycle used of maximum two.
No second Review executed. Independent corrected-head acceptance remains coordinator-owned.

## Delivered Correction

Replaced math.isfinite conversion with `not 0 < seconds <= sys.float_info.max` in direct run
validation and the equivalent CLI preflight. Oversized Python integers compare safely without
conversion. The existing bool rejection remains. Negative/zero/nonfinite values stay invalid.
Representable maximum float and integer equivalent are accepted by direct run under a mocked
expired deadline, proving this is not an invented practical workload-duration cap.

Added oversized positive/negative direct and actual-main subcases in the existing 16 methods.
CLI invalid tests now have a valid minimal synthetic seed/staff and homes=1, so a missing guard
cannot be confused with seed cloning failure; subtest assertions stay inside their subtest.
The invalid direct store uses Mock(spec=[]), making any pre-validation cases access fail.

## Failing-First and Local Validation

`V` is the task-local loadcheck-venv from the primary changes record; `R` is repository root.
All Python correction probes/tests use env -i PATH=/usr/bin:/bin with
TMPDIR=$R/.copilot-tracking/.issue-114-tmp; actual-main probes additionally clear os.environ.

| Command/check | Result |
| --- | --- |
| V/bin/python -m unittest discover -s src/core/tests -p test_loadcheck.py -q, initial added subcases before source change | Expected red, 4 errors. Direct oversized signs raise OverflowError; initial CLI fixture used default homes with missing resident, producing KeyError plus assertion-context fallout. Fixture refined before production correction. |
| Same test command after valid fixture/subtest refinement, displayed through tail -18 | Expected red, 3 errors: direct two signs plus positive CLI OverflowError. Display pipeline exit 0 did not mean runner passed; recorded runner output says FAILED(errors=3). |
| Inline exact original RV-001 repro before production correction | Direct OverflowError; actual main positive 10**400 gives OverflowError after exactly one mocked factory call. No backend initialized. |
| cd src/core; V/bin/ruff format tests/test_loadcheck.py; V/bin/ruff check .; V/bin/ruff format --check .; V/bin/mypy; V/bin/python -m unittest discover -s tests -p test_loadcheck.py -q | Passed; format unchanged, 71 files formatted, 124 files type-clean, 16 tests in 0.066s. |
| After maximum-representable duration subcases: cd src/core; V/bin/ruff check .; V/bin/ruff format --check .; V/bin/mypy; cd tests; V/bin/python -m unittest test_loadcheck test_sqlreads test_sqlstore test_taskqueues test_sqlqueues test_queue_benchmark -q | Passed on exact final source/tests; 75 tests in 89.078s, no skips, Ruff/format/mypy green. |
| V/bin/python session-files/loadcheck_probes.py, in-memory source only | Fixed 16 green; original base 29 failure/22 error subtest outcomes, 10 worker escapes captured; neutral-clock healthy reports exactly equal; all 16 mutants detected. |
| Newly added API oversized-guard mutant | Detected: 3 error subtest outcomes in existing invalid-input tests. |
| Newly added CLI oversized-guard mutant | Detected: 1 error subtest outcome in existing pre-store CLI test. |
| Inline exact corrected API/CLI repro for positive and negative 10**400 | Direct ValueError with static duration message; CLI argparse exit 2, zero factory calls, and nonexistent synthetic input path never read. |
| sha256sum original critique/Review; git diff --check; rmdir .copilot-tracking/.issue-114-tmp | Passed; original hashes unchanged, exact scratch removed. |

The 16-mutant run retains the original 14 behavior challenges, updates zero-duration mutation
to the new comparison syntax, and adds separate API/CLI oversized-guard removals.
This is correction verification, not another original Review or operational acceptance.

## Identity After Correction

| File | SHA-256 |
| --- | --- |
| loadcheck.py | a6bd8d0c4e3ae31484c6248934647b08251af688bf1f3db93a260a9d81fb9858 |
| test_loadcheck.py | db30c48bbd9151eee3bb72af4e50dbca8ba8fbaeb2d87a7083fa6c52fdd7affd |

Correction commit will be identified by the subsequent publication receipt and PR.

## Identity Before Correction

| File | SHA-256 |
| --- | --- |
| loadcheck.py | 7cd7a506e439f0814320cfb7b22e6a3f94b47a18ba255f8eb45dec7e5f581dfb |
| test_loadcheck.py | b45296f3a9eec3478fb3c68987b85b68a538a22ffad6793c5bfa50ebd01100d2 |

## Original Finding Disposition

RV-001 locally addressed with failing-first reproduction and exact corrected interface checks.
No new plan decision, critique or Review. Original Not accepted verdict remains unchanged.
All live Azure load/cost, annual ledger, DH-005 and human acceptance gates remain unmet.
