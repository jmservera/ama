---
title: Issue 1401 cycle 2 requalification plan
ms.date: 2026-11-11
task_id: 1401-c2-qualification-1111
---

Prospective plan, committed before any cycle 2 verification command. Validation tier: focused (documentation and tracking records plus existing focused tests, lint and type checks, no source change). Basis: no workflow, dependency, SQL schema, security control or deployment edit. Details: [details](../details/2026-11-11-issue1401-c2-qualification-1111-details.md). Research: [research](../research/2026-11-11-issue1401-c2-qualification-1111-research.md).

## Phases

* [ ] Phase 1: commit this research, plan and details before verification.
* [ ] Phase 2: create a fresh unique external evidence directory and run each existing check with exclusive noclobber `.out`, `.err` and `.exit` files, direct exit captured before any tee, import-origin and SHA256 provenance in the same environment.
* [ ] Phase 3: write the C2 changes record, a byte-exact copy of the independent finding if needed, and the explicit C1 process deviation and capture limits.
* [ ] Phase 4: one critique of the final candidate records and one Review, original adverse outcomes preserved.
* [ ] Phase 5: final commit, clean frozen state, handoff, stop for the same independent reviewer.

## Expected results (defined before running)

* Core: `tests.test_aftercare`, `tests.test_aftercare_intake`, `tests.test_aftercare_store` discover 104 tests; 15 opt-in SQL Server skips; 89 executed; outcome OK, exit 0. This is not 104 passes.
* API: `tests.test_aftercare_served`, `tests.test_aftercare_screen` run 21 tests, OK, exit 0.
* `ruff check`, `ruff format --check` and `mypy` on the three owned changed source and test files exit 0 with the repository configuration.
* A failing expected result is recorded raw and stops the cycle without edits, assertion changes or cycle 3.

## Out of scope

Any application, helper, test, schema or validator edit, refactor, #1402 blank-state fix, new issue, SQL, container, browser, image, model, cloud, spend, credential, permission, install or resource cleanup, full gate, rebase, push, PR, issue or board write, heavy SQL rerun, and whole #133/#89 or production acceptance.

## Dispositions fixed in advance

* The 15 actual SQL Server results from C1 (`/tmp/mssql1401.txt`, sha256 in research) are reused only because the source and test file identities are unchanged from 678c458, as a qualified historical C1 result. No new SQL and no new cleanup verification. The original outer script status can hide failure, the direct `mssql_exit=0` is real, and the original container-zero and flock-zero claims remain unverified handoff claims. The manifest is gone and is not recreated. No universal SQL failure-path or cleanup conformity is claimed.
* The original wrapper exit and the collapsed API, lint and type outputs are not reconstructed and are not counted as 0.
