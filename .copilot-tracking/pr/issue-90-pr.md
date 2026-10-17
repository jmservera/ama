---
title: "fix(core): enforce evidenced provider capacity and controlled orders"
ms.date: 2026-10-17
---

## Summary

Closed actual control gaps in the existing migrated procurement, work-order
and case-advance paths. Retained the delivered API/screens, existing SQL
transaction helpers, named human instruction authority, resident commitments,
safety/building gates, #78 provenance and #97 forms.

## Changes

* Bound positive committed capacity to original clean uploaded bytes/hash,
  source version/date, current review, delivery dates, covered homes and
  `home-work-order` units. Offered, legacy and unknown capacity cannot
  authorize work; recorded losses expose deficits instead of fictitious
  availability.
* Required current named managers with explicit trusted contract/supplier/
  scope/action delegation. No self-granting endpoint or production authority
  seed was added. Existing allocation progression works at exact quota;
  alternate case advancement requires an evidenced booked order.
* Added immutable version/issuer/authority/state/appointment snapshots for
  every order change. Preserved contractor own-order reads and denied their
  package reads and all writes. Marked template/AI/review drafts explicitly
  not instructions without adding a send/award path.
* Reused SQL checked-document/writer locks, adding commit-time source,
  identity, delegation and procurement dependency checks. Added surgical
  existing-screen source inputs and local fictional regressions.

## Exact-Criterion Evidence

| #90 criterion | Executed engineering acceptance |
| --- | --- |
| No schedule/confirmation beyond evidenced committed capacity, not offered | Offered 9 / committed 1 admits one allocation and denies a second; unknown/legacy/source/version/hash/unit/date/scope/delegation failures deny; existing at-quota booking succeeds; advance bypass and deterministic SQL last-unit/source/authority races are blocked |
| Every work-order change has version + issuer | Issue, every appointment outcome, reissue, completion, correction and withdrawal retain sequential immutable snapshots; HTTP eight-version lifecycle and failed-write/rollback/reopen checks pass |
| System draft never instruction | Template note, persisted AI marker, review effect and UI copy remain explicit; draft acceptance never mutates procurement |
| Contractor read-only own orders | Two supplier identities, forged/foreign identity checks, package-read denial and every write-route denial pass; both contractor browser screens show only own orders |

## Original Validation (Before Coordinator Correction ONE)

* Failing-first: original 21 procurement tests passed while four new root
  regressions failed eight times across JSON/SQLite before production edits.
* Exact domain/HTTP/roles: **63 passed**.
* Combined API-cwd preservation: **278 run, 277 passed, one existing skip**.
  Separate core-cwd building/procurement/resident/hazard: **114 run,
  113 passed, one existing skip**. These counts overlap; do not sum them.
* Actual local SQL Server 2022, standard existing harness:
  **29 passed** for MssqlProcurement/MssqlProcurementApi, including inherited
  domain/HTTP/race behavior. Only a newly task-owned loopback container was
  used; container and ephemeral credential were removed afterward.
* Local browser: source input, inline refusal/focus, keyboard save,
  issue/book at quota and new version, two contractor views/write denials,
  320/390/1280 reflow and reduced motion passed. External requests were
  blocked; zero page errors.
* Configured changed-path lint/format/types, both changed JS syntax checks
  and diff hygiene passed. Existing migration format/type exemptions were
  unchanged. An explicit-path format invocation bypassed old exclusions;
  the configured force-exclude replay passed and is documented.
* One independent post-implementation Review: **Complete / Conformant**,
  no substantive findings. One earlier plan critique returned Revise;
  PC-001..005 were applied before implementation.

## Dated RPI Evidence

All phase artifacts are committed under the same stable task identity/date.

| Artifact | Path |
| --- | --- |
| Research | [.copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md) |
| Manager research instrument | [.copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md) |
| Plan | [.copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md) |
| Details and execution | [.copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md) |
| One critique/dispositions | [.copilot-tracking/reviews/plans/2026-10-17/provider-capacity-controls-90-plan-critique.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/reviews/plans/2026-10-17/provider-capacity-controls-90-plan-critique.md) |
| Changes/criterion acceptance/phase execution | [.copilot-tracking/changes/2026-10-17/provider-capacity-controls-90-changes.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/changes/2026-10-17/provider-capacity-controls-90-changes.md) |
| One independent Review | [.copilot-tracking/reviews/logs/2026-10-17/provider-capacity-controls-90-review.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/reviews/logs/2026-10-17/provider-capacity-controls-90-review.md) |
| Durable state | [.copilot-tracking/rpi-sessions/2026-10-17/provider-capacity-controls-90-state.json](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/rpi-sessions/2026-10-17/provider-capacity-controls-90-state.json) |

## Scope and Readiness

This is local fictional engineering acceptance, not real company authority,
supplier commitment/signature verification, operational approval, live AI/
Azure SQL, financial commitment or full PRD/WCAG acceptance. Actual trusted
delegation remains the human contract authority owner's prerequisite;
deployment/UX owners must commission hosted/human/screen-reader acceptance.
JSON remains single-process with separate snapshot/ledger crash limitations.
No private dataset, paid AI, live provider order, award or payment was used.

The requested branch started from then-latest main adedf1f. Upstream advanced
one initializer/shared-KB commit to bab4bf3 during delivery. The initial
publication preserved the then-explicit no-merge/no-rebase direction.
The subsequent coordinator-authorized integration is recorded below.

PR #384 was created successfully through the REST API after the GraphQL
quota was exhausted. The original dirty/conflict readback was historical.
On 2026-10-17 the coordinator expressly authorized topic-only integration
onto freshly fetched main bab4bf3a2ac9ec030d78d27063d1390f800c5c7c.
`git rebase origin/main` produced integrated head
db83d4260e4f3d29fa80ce08624155ee4f59ecce before its evidence-only commit.
Only the append-only KB log conflicted. Exact byte checks proved the complete
upstream prefix plus the unchanged issue-90 entry, both README routing-row
sets, all twelve other upstream files exactly main, and byte-identical src
production/test/browser/documentation patches and original Review.
`git range-diff`, main ancestry and diff hygiene passed. No substantive
production conflict occurred, so no full-suite duplication or #84/#94
production-path rerun was warranted.

The final evidence commit records commands/base/integrated head and preserves
the original independent Review's historical Complete/Conformant result.
Topic-only publication uses an explicit force-with-lease expecting old
remote 6e4dbe18d111673b41049830eb68bf81f89051c8, never unconditional force.
External coordinator exact-head gating and hosted CI/rubric remain pending;
the original Review is not a fabricated new gate. No main rewrite, merge or
issue closure was performed.

* [x] Ordered Research -> Plan -> Implement -> Review and local evidence completed.
* [x] Exactly four issue criteria assessed; existing #78/#97 behavior retained.
* [ ] Hosted CI, including rubric scoring, completed successfully.
* [ ] Owner/coordinator accepted delivery and authorized issue closure.

## Related Issues

Refs #90. Parent #89 is hierarchy only, not an explicit dependency.
No issue closure or merge was requested or performed.

## Correction ONE: Coordinator Revise and Hosted CI (2026-10-17)

The external coordinator Review of integrated head 527a537 returned **Revise**
for a Medium defect: package creation accepted an empty immutable contract
version although consequential operations require it. This section supersedes
any implication that the original local Conformant Review closes the changed
source. That original Review is retained byte-for-byte as historical evidence;
external correction closure and hosted reruns remain pending.

| Finding | Correction disposition |
| --- | --- |
| Empty/missing/whitespace contract version creates unusable package | Required trimmed nonempty version before domain mutation; API no longer supplies an empty default. Existing UI shows adjacent inline error with invalid/description semantics, focuses the version and retains entered fields; no new editor or authority grant |
| Hosted core inventory/manifest tests report stale dataset.py source hash | Refreshed exactly the one fixture SHA-256 using the existing manifest contract; validator unchanged; eleven profiles/nine workflows and all unavailable/provisional/proposed/no-approval labels identical |
| Hosted API/MVP CI/validation safety-flow positives lack evidenced booking | Supplied fictional commitment/source, trusted delegation and booked work order after independent safety release; every original blocked-advance/raiser/receiver/release assertion retained, no skips or weakened guard |

New omitted/empty/whitespace domain/HTTP regressions failed first (12
subcase failures across JSON/SQLite), while both exact existing safety
selectors and manifest integrity reproduced the reported failures.
After correction, focused procurement/API/workflow/role/MVP **107 passed**,
existing manifest/inventory **8/11 passed**, then the actual failing
component CI discovery commands passed:

* Core: `cd src/core && ../../.venv/bin/python -m unittest discover -s tests -v`:
  **651 run, 650 passed, one existing isolated-Azure-SQL opt-in skip**.
* API, shared by src-api, MVP CI and MVP validation:
  `cd src/api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -v`:
  **613 run, 471 passed, 142 existing opt-in skips** (141 SQL Server,
  one rendered opt-in).
* Separately actual new task-local SQL Server 2022:
  MssqlProcurement/MssqlProcurementApi **31 passed**, no skips,
  including corrected creation. Container and ephemeral credential removed.
* Separately local browser **passed** blank/whitespace inline refusal,
  version-field focus and input preservation, valid keyboard package
  creation, existing source/capacity/quota/version/contractor journeys,
  320/390/1280 reflow/reduced motion, zero page errors and external requests blocked.
* Full configured core/API lint/format/types, isolated strict changed
  browser-harness lint/format, JS syntax, migrated-package compileall and
  diff checks **passed**. Existing migration exemptions unchanged.

Counts overlap and must not be summed. No tests were removed, new skips
added, manifest validator weakened or professional authority fabricated.
Fresh web guidelines were retrieved before changes and refreshed for
changed-region review; native Fluent-backed behavior retained without
redesign or full WCAG claims. The original dated changes/plan/details/state
record these dispositions separately from the untouched original Review.

Normal commit/push on the same issue-90 topic only; no rebase, force push,
merge or issue closure in this cycle. No real authority, human, AI or Azure
acceptance is claimed. **Coordinator independent external closure remains
required; no new Pass is asserted.** Refs #90.

## Authorized Integration After #382 (2026-10-17)

This section supersedes the earlier correction-only no-rebase direction:
the coordinator explicitly authorized rebase of only this owned topic after
correction publication. Fresh main/base is
`bbbc9243505b606550327c64bf5429243f457f2e`; old expected remote is
`5244f99db0a5b53f761b6c3a7bc5f1d9c4e829c1`. Rebase completed at
`7cf8df7b5ed67055dc6d40a95c554598b448c28e`; final integrated source is
`e2314a7c2ea0d6588b696030d153f29f74208dd7`, followed by the evidence-only
publication commit. The exact final PR head is appended on REST publication.

Shared SQL conflicts retained **both** stock and procurement commit hooks
and **all** stock/procurement SQL test classes. Canonical upstream discard is
unchanged: pending cleanup and committed cache/watermark protection precede
fallible reads. Procurement/advance now own their recovery alongside stock,
preserve the original exception (including cancellation), and log/add explicit
uncertainty on failed reload. Checked-document reload stages complete
reads/decodes before publishing snapshots. No duplicate discard helper,
stock signoff removal or unmerged finance branch import.

Failing-first recovery tests reproduced masked errors and lost committed
snapshots; cancellation extension also failed before correction. Final
twelve combinations check operation/advance, pre-save/transaction/cancellation,
one-shot/persistent SELECT failures, exact original exception identity,
logs/notes, empty pending/touched state, retained committed data, fail-closed
reads, no later audit/mutation flush and a legitimate versioned retry.

| Final affected-path validation | Result |
| --- | --- |
| Core finance signoffs/matching, stock, procurement, SQL store, provenance, bulk/forms | 194 passed, no skips |
| API stock/procurement/workflows/roles/MVP/bulk/forms | 73 run, 72 passed, one existing opt-in skip |
| Actual disposable local SQL Server 2022: MssqlStockDecisions, MssqlFinanceSignoffs, MssqlProcurement, MssqlProcurementApi, MssqlStoreTests, MssqlImproveTests | 74 passed, no skips |
| Shared SQL portability | 3 passed |
| Full configured core/API Ruff/format/mypy and diff hygiene | Passed |

Counts overlap. Existing finance budget/matching/independent approval and
technical signoff tests were replayed using the standard SQL adapter, not
invented #94 controls absent from this main. Task-owned SQL responsiveness
verified before tests; exact container and ephemeral credential removed.
No full component suite was duplicated; the combined SQL replay was
repeated only after the final cancellation ownership change.

Exact preservation assertions passed: upstream KB prefix plus unchanged own
entries; both routing intents including upstream initializer/stock rows and
own capacity row; twelve non-overlapping upstream files; canonical discard;
upstream stock/signoffs/finance and tests; original Review/critique;
corrected fixture/hash and UI bytes. No web changes in this integration,
so no redundant browser run or new visual/accessibility claim.

Changes/plan/details/state preserve the full integration decisions and
commands. Publication uses only the explicit expected-remote lease on
`feat/provider-capacity-controls-90`, never unconditional force or main.
**Original independent Review remains historical; external coordinator
exact-head closure and hosted checks remain pending.** No merge or issue
closure. Refs #90.

## Final Latest-Main Integration: Merged #84 and #94

**This supersedes the preceding bbbc-only final-base/results.** Before any
push, main advanced to merged finance #94. From a clean run-owned evidence
commit, the same authorized topic-only latest-main rebase continued.
Final base is `d400eb8d1d0d6567445b0fc11803260eab897a65`;
validated source head is `7c8965cf9ebc64cd235669444c443bc33a000302`,
followed only by final docs/evidence. Exact publication head is appended
below by REST update. Explicit expected old remote remains `5244f99`.

All **stock, finance and procurement** commit validators are retained.
Canonical `_discard(pending=())` and protected lock exit are unchanged from
latest main. Finance's internal known-refusal error logging and caller's
prior-pending audit restoration are preserved, alongside stock/procurement
scope recovery and staged checked-document snapshot publication. Additive
KB/index/component-doc conflicts preserve both intents; all original stock
signoffs, procurement capacity/source/provenance and human approval guards
remain. No duplicate helper, test deletion or professional authority invented.

| Final latest-main affected-path validation | Result |
| --- | --- |
| Core merged finance-match JSON/SQL classes, finance signoffs, stock, procurement, store/provenance/bulk/forms | 224 passed, no skips |
| API finance-match/stock/procurement/workflows/roles/MVP/bulk/forms and portable SQL | 77 run, 76 passed, one existing opt-in skip; includes portability3 |
| Actual disposable local SQL Server: prior six suites plus existing `test_finance_match_controls.MssqlFinanceChecks` with `ZF_FINANCE_MSSQL=1` | 93 passed, no skips, including all 19 merged finance matching/recovery cases |
| Configured core/API lint, format, mypy, diff and exact preservation | Passed |

Counts overlap; no redundant full component suites. Latest-main source
changed, so targeted combined SQL was necessarily rerun. Task-owned local
SQL responsiveness was verified; container and ephemeral credential removed.
Exact assertions preserve upstream KB prefix plus own entries, all upstream
and own routing rows, 28 non-overlapping upstream files, canonical discard/
lock exit, stock/finance/signoff sources and tests/config, original
Review/critique, corrected dataset/manifest and unchanged UI. No new
browser/human/WCAG/Azure acceptance is claimed.

Source and evidence commit identities are privacy-safe with required
attribution. Only the owned topic is published using the explicit expected
remote lease; no unconditional force/main rewrite, merge or issue closure.
**Independent coordinator exact-head closure and hosted checks remain
pending; original Conformant Review is historical, not a new Pass.**
Refs #90.
