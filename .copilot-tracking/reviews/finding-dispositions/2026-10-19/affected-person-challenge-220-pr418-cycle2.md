---
title: PR 418 second bounded finding correction dispositions
description: Current-reader and indexed SQL evidence with explicit remaining web blocker; not a replacement Review
ms.date: 2026-10-19
---

## Boundary and actual review provenance

Same automatic task 220, supplied branch feat/affected-person-challenge-220.
The prerequisite rpi-220-final-bot-gate session and runner had exited before any
source/tracking edit. Clean supplied HEAD was
b4cd1c160f74f906282d238ebfcc2ea49fbb83de. Its historical final-bot all17
receipt passed; it does not certify this correction.

Actual paginated `gh api` reviews and comments are retained unmodified under:
`/home/azureuser/.copilot/session-state/8cfe8558-5e33-4d48-86fa-47f4c74405db/files/issue220-cycle2/`.
`reviews.json` and `comments.json` are the primary payloads, not a paraphrased
review. Source review [5578223974](https://github.com/jmservera/ama/pull/418#pullrequestreview-5578223974)
at 1291355aeef23a387a67dd094c14917ff42c0181 labels four prior comments
resolved, retains SQL scanning and identifies cached-detail authority.
The actual latest completed Copilot review is
[5578292301](https://github.com/jmservera/ama/pull/418#pullrequestreview-5578292301),
22:00:13Z, at b4cd1c1. It labels SQL scanning resolved but identifies cached
detail and off-page duplicate forms. Neither COMMENTED nor a platform resolved
label establishes engineering closure.

The user selected a bounded backend correction and SQL investigation, not
another review or web implementation. All original research, critique,
Review and previous dispositions remain byte-identical. No replacement Review
or independent exact-head acceptance is represented here.

## Bounded verdict and finding dispositions

Selected backend corrections are implemented and focused-validated.
**Not merge-ready:** the latest reported duplicate-form defect remains
unresolved, plus coordinator exact-head, genuine hosted and human acceptance
gates. Stop after this second correction; no automatic third repair loop.

| Finding | Disposition | Evidence and residual boundary |
| --- | --- | --- |
| Cached case-detail authority, reviews 5578223974 and 5578292301 | Corrected in selected scope | `Store.detail` reuses `challenge_references_visible` for BOTH copied challenge collection and generated target catalog. Current registry downgrade/removal removes both while ordinary detail remains. Trusted internal `user=None` stays unchanged. Existing authenticated identity and populated cache are retained in JSON/SQLite/native tests; actual HTTP reuses the same cookie across direct SQL registry changes and an entitled colleague remains a positive control. |
| Prior [4318714876](https://github.com/jmservera/ama/pull/418#discussion_r4318714876), SQL writer full-case JSON scanning | Confirmed remaining performance defect despite latest platform resolved label; corrected within existing derived-column pattern | One integer correction-presence flag and filtered index, no new domain table/service/dependency graph. Actual native60000 baseline scans all rows and calls OPENJSON 60000 times; final SQL seeks one flagged row and calls OPENJSON once. Exact policy/source/proposal matching and current actor/owner/rowversion/race checks remain. Sparse local measurements do not establish dense-load or operational capacity. |
| Native-specific denial-audit persistence gap adjacent to prior 4318715035 | Covered by directly related native regression | Missing release accept/edit each persist exactly one `ai_release_denied` after reopen, retain unchanged proposal and valid ledger. Native failed-save rollback still removes failed accept/edit side effects. |
| Duplicate off-page draft resolution forms, latest review 5578292301 | Unresolved reported web defect; concrete coordinator blocker | Reported reproduction: with 50 challenges leave CH-1 resolution dirty, record the 51st, refresh first page, then Older challenges. Restored draft can exist outside history and duplicate IDs/forms when CH-1 becomes visible. No web source or browser-harness change is authorized in this backend-only directive. Not independently reproduced in this scope; coordinator must select a bounded web fix and 50-to-51 refresh/paging regression before merge. Do not silently dismiss or infer resolution from the generic browser gate. |
| Prior 4318714670/4784/4963/5035 | Prior bounded dispositions retained, no blind dismissal | Actual source review labels all four resolved. Earlier substantive proof and implementation-owned dispositions remain unmodified. This cycle adds case-detail and native denial persistence proof, not a claim of broader auth, UX or audit completeness. |

## Smallest reused persistence mechanism

`CASE_COLS`, `_row`, `_migrate`, seed/save and the existing filtered
`ix_cases_open_hazard` / derived queue indexes are repository prior art.
`priority_correction` is derived from terminal `Correction recorded` records
and stored with the case body in the same rowversion-controlled update.
An open challenge or explanation-only resolution does not set it.
Failed save rolls back both; a reopened store sees only committed flags.

Upgrade reuses the derived-column rebuild, made atomic with column addition
inside the existing serialized writer transaction. Injected rebuild failure
rolls the new column back; the next open retries rather than accepting default
zero. Actual SQLite and native SQL upgrades preserve id/rowversion/seq/body and
recover the existing correction. The small dialect hook uses SQLite ADD COLUMN
versus T-SQL ADD. There is no broad indexing redesign or domain-schema change.
One-time migration still reads existing cases and requires the existing startup
writer lock; large-database migration availability is not benchmarked.

## Native 60,000-case measurements

Primary files: `native60000.json`, `baseline-actual-plan.sqlplan`,
`indexed-actual-plan.sqlplan`, both `*-query.sql`, `native_measure.py` and
`native-measure-console.log` in the evidence directory above.
Generated public DATA case structure plus existing `scale_fixture.homes`,
seed174; exactly 60000 cases, one corrected case, 74566390 UTF-8 body bytes,
1234-1396 bytes each. No private data, configured/live SQL, Azure or IAM.
Actual SQL Server 2022 developer container: 2 CPUs, 3 GiB memory limit, 2 GiB SQL
cap, random loopback port, task-owned label and exact resource cleanup.
The shared `/tmp/ama-rpi-heavy.lock` was held once, never nested.

Three bounded warm-cache query samples per SQL variant, one actual execution
plan each. Competing unrelated writer acquires the SAME production exclusive
application lock, then updates another case's seq to itself. DMV evidence
confirms its application lock WAIT while the measured writer holds GRANT.
No inference call or state mutation is hidden in timing.

| Observation | Original correction-only query | Indexed flag predicate |
| --- | --- | --- |
| Actual case access | Clustered scan: 60000 rows read, 30237 logical reads | Filtered index seek: 1 row/3 reads, clustered lookup: 1 row/1 read |
| Actual OPENJSON executions | 60000 | 1 |
| Returned correction targets | 1 | 1, identical |
| Query plus target decode range | 1.458-1.533 s | 0.792-0.889 ms |
| Measured application-lock interval | 1.491-1.566 s | 33.260-33.821 ms |
| Competing unrelated writer lock-acquire wait | 1.489-1.565 s | 32.083-32.442 ms |

Total lock and competitor wait INCLUDE a deliberate 25ms rendezvous and
connection/DMV overhead; do not label them query-only time. This is one sparse
warm-cache dataset, not full application throughput, an SLA, dense-correction
capacity, cold storage or large narrative evidence. The flag is coarse:
JSON work scales with flagged case/challenge count and can approach full stock
when corrections become dense. A normalized dependency schema would require
separate design/approval, not a third repair iteration in this scope.

## Focused validation and preserved failures

* Final combined JSON/SQLite resident, actual HTTP and existing SQL store tests:
  138 tests, 136 passed, two existing declared skips (SQLite JSON-file rollback
  non-applicability and opt-in local browser).
* Final native: nine selected tests, nine pass, zero skips. Registry downgrade/
  removal, atomic upgrade/retry, correction flag save/rollback, persisted
  release denial, reference rights, accept/edit races, cross-case policy,
  current owner/decision and failed acceptance/edit rollback.
* Configured core/API strict mypy pass for 128/62 source files; changed Python
  Ruff and test formatting pass. No tools, matrix or exemptions changed.
* First failing proof reproduces cached-reader disclosure and the absent
  filtered query plan. Retain failing-first.log; do not reclassify it as passing.
* Initial type/style failures are retained. First native regression nine pass
  preceded a benchmark-fixture KeyError for the public case's missing seed
  defaults; fixed by reusing the actual seeded case structure. Final measurement
  succeeded once; no uncontrolled repeat of the expensive experiment.
* After the atomic migration refinement, native regressions were rerun once on
  final source, without repeating the 60000-case benchmark. Measured query SQL
  is byte-identical to final method constant, verified before freeze.

No web code changes or new browser-conformance claim. The unchanged full17 gate
is pending after commit; it is not a substitute for the unresolved reported
off-page draft defect or independent exact-head assessment. Its receipt,
exact HEAD/base and verification are recorded externally after freeze.
No push, PR mutation, closing reference, rescore, protection change or merge.
Refs #220 only; whole issue remains OPEN.
