---
title: Issue 144 permit SQL boundary plan critique
description: Authored self-critique of the prospective real-MSSQL permit boundary plan (not independent)
ms.date: 2026-11-11
task_id: issue-144-permit-sql-1111
---

## Status

Authored by the plan's own author. This is not an independent assessment; Root arranges that before implementation. Execution: one critique pass over the final candidate plan. Verdict: proceed to Root admission with the dispositions below.

## Findings and dispositions

* C1 Medium, coordination flake. The block observation polls DMVs and the release depends on database time. Disposition: bounded polls, preconditions that fail the test as invalid setup, no retry, no widened timeout; a failure is reported as observed.
* C2 Medium, the authority-crossing case is not a discriminator for the original defect, because `reserve_in` already reads its own clock after the lock. Disposition: stated in research and plan, kept as an E1 guard, control N1 predicted to pass it; do not present it as proof of the stale-clock defect.
* C3 Medium, the controls need mutated source copies and extra venvs, which cost network `pip` and time. Disposition: explicit admission item D3; running without the mutants (Option U without N1 and N2) is not recommended because the negative control would stay unobserved.
* C4 Low, `MssqlFixture` does not call `sqlguard`. Disposition: the new class calls `require_task_owned_loopback` itself; `test_assistants.py` is untouched.
* C5 Low, helper reuse by assigning `ConsumptionApi` methods couples the module to that class. Disposition: accepted to avoid copying and to leave the existing file unchanged; a future refactor to a shared harness is out of scope.
* C6 Low, the module shares the `zf_test_assistants` database with other `Mssql*` assistant classes which drop tables on `setUp`. Disposition: serial execution in one owned container and never concurrent with other SQL suites.
* C7 Medium, a new module is not selected by hosted CI or `SQL_SELECTORS`. Disposition: recorded as D2; full-tier if wired; the evidence is local and direct only.
* C8 Low, consent, readings and operator-disable cases remain predicate-patched on SQLite. Disposition: labelled SQLite-only, not mirrored, to avoid claiming SQL proof of patched predicates.
* C9 Low, the heavy lock was free only at a past instant and the host had 727 MiB free (8018 MiB available). Disposition: admission is probed at run time by the driver and is Root-controlled.
* C10 Process, no canonical witness chain for this launch. Disposition: recorded in the details and the state; not regraded.

## Rejected advice

None conflicted with confirmed decisions.

## Remaining decisions

D1 to D4 in the plan. Counter: E1/E2 spent, three remain; this launch spent none.
