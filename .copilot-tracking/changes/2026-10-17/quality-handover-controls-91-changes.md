---
title: Quality handover controls issue91 changes
description: Execution, validation and delivery evidence
ms.date: 2026-10-17
---

## Scope and State

Task issue91, quality-handover-controls-91, automatic; full plan P01-P04.
Research executed; Plan Ready after one critique, original Revise verdict
preserved, PC-001/002 resolved directly. Full-plan implementation P01-P03
complete; all markers reconciled. Independent Review executed Complete with
original outcome Not accepted; RV-001/RV-002 Medium. Caller-authorized correction
ONE completed with separate closure evidence, original Review preserved and no
repeated Review. Implementation pushed normally and main PR #387 created.
Automatic session stops at the user's explicit PR terminal.
No implementation delegation. No blocker.

## P01: Controls and Regression Evidence

Research temporary fail-before probes reproduced blank remediation, revoked
actor acceptance and active old handover after replacement in JSON/SQLite.
Existing 50 quality/procurement tests passed. Canonical regression assertions
were added before source changes. Canonical first run: six selected JSON/SQLite
methods produced six failures/four subcase errors: wrong exception for forged
actors, reinspection passing from Submitted, Accepted replacement refused and
old handed-over records surviving replacement. These are retained fail-before
results, not successful validation.

Implemented quality.py only for production backend:
current registered actor via existing stock.decision_scope (including SQL
writer-time validation), retained contributor identities and legacy resolution,
required remediation, Fixed-only reinspection, strict indices and explicit
resident-told boolean. Same-measure Accepted/HANDED replacement retires all
active predecessors into Superseded with prior_acceptance/history/lineage.
No active decision transfers to new evidence. Unknown legacy contributors
refuse acceptance; old evidence/history/aftercare remain. No risk categories,
professional delegation or finance/payment authority introduced.

SQL uses existing rowversions, quarantine-before-recovery and actor checks,
with the quality wrapper restoring a legitimate pre-existing pending audit
prefix after the shared decision scope discards failed work. JSON caught
failures restore state/own ledger tail, including after actual writes, and
explicitly report unknown durable outcome if restoration itself fails.

## Amendments and Divergences

* Immediately relevant test update: existing resident_decisions regression now
  expects unknown-scope replacement to refuse before mutation rather than create
  an unusable unbound replacement. Positive scoped workflow/withdrawal tests
  remain; no skip/validator was weakened.
* P01-P03 initially required no finance.py, dataset.py, app.js, server.py,
  manifest, SQL schema or shared SQL helper edit. P04 then added only the
  two-line quality-specific server.py HTTP outcome handler. The existing MSSQL
  replay inherits new tests; no aliases/copies.
* Parallel #95 overlap is component README/KB append/index integration plus that
  declared server.py exception handler, sequenced after the core outcome contract.
  No grants/finance dispatch changed. Original upstream log prefix/all routes
  retained; no reads of another worktree or private datasets.

## P02: Dependent Surface

web-design-guidelines activated and current upstream command.md fetched in full
before edits, 2026-10-17; fetched again in full before changed-file review.
Read the entire changed ops.js and assessed all fetched rule categories.
Quality remediation now has an explicit label, inline status/error/focus,
preserved inputs and busy native action controls. Replacement has native
confirmation/cancel and explicit historical rendering, with no old action.
Owner-selected Fluent/content/WCAG foundations retained; no redesign.

### Web-guidelines findings (existing out-of-scope gaps)

## src/api/src/zava_forward/api/web/ops.js

src/api/src/zava_forward/api/web/ops.js:27 - existing defect/owner fields lack name/autocomplete.
src/api/src/zava_forward/api/web/ops.js:82 - existing evidence submission fields lack name/autocomplete.
src/api/src/zava_forward/api/web/ops.js:105 - existing save-evidence flow lacks busy progress and field-local server-error focus.
src/api/src/zava_forward/api/web/ops.js:197 - existing work-order note/bindings controls lack name/autocomplete.
src/api/src/zava_forward/api/web/ops.js:21 - no existing unsaved-edit navigation warning; broader workbench follow-up.

These do not alter the exact backend acceptance controls; complete Web Interface
Guidelines/WCAG conformance is not claimed. Repository plain ASCII/sentence-case
content convention takes precedence over generic typography/title-case advice.

Component READMEs, existing programme journey continuation, index route and
append-only KB log updated. No new knowledge-base page or case-study change.

## P03: Validation

All final counts below are actual; overlapping reruns are not added together.

| Execution | Actual outcome |
| --- | --- |
| Existing quality/provider baseline | 50 run, 50 pass |
| Combined final current-actor/quality/resident/stock/finance/SQL-store/API/provider/assistant/workflow selection | 357 run, 308 pass, 49 existing opt-in skips |
| Actual isolated local SQL Server, latest tests | 36 run, 36 pass, zero skip |
| Actual real-app Chromium changed quality journey | Pass; return, blank remediation error/focus/input preservation, keyboard correction, independent reinspection, resident handover, replacement cancellation/confirmation, retired history/no old action, fresh acceptance/handover, 320/390/1280px reflow, reduced motion, labelled controls, no page errors |
| Configured core Ruff / format / mypy | Pass; 58 format-managed files, 111 mypy source files |
| Configured API Ruff / format / mypy | Pass; 21 format-managed files, 53 mypy source files |
| Node ops.js syntax / git diff whitespace | Pass |

Combined command from repository root, installed editable local venv:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_quality_procurement test_resident_decisions test_stock_reconciliation \
  test_finance_signoffs test_finance_match_controls.JsonFinanceChecks \
  test_finance_match_controls.SqlFinanceChecks test_sqlstore test_role_matrix \
  test_procurement_api test_resident_api test_stock_reconciliation_api \
  test_finance_match_api test_assistants test_assistants_dispatch test_workflows -v
```

Actual SQL selected `test_mssqlstore.MssqlProcurement`, ZF_TEST_MSSQL=1,
using a process-generated unlogged secret, dynamic loopback port, owned
`ama-quality91-9d85e42da3b8` container and `quality91_ba224519232649fd95e2cb037c02648c`
database. Actual SELECT 1 readiness succeeded, tests passed, exact owned
container removed in finally. An earlier harness attempt hit missing `tests`
module; adding `src/api` to the fixture path fixed it. Failed-attempt container
was also removed, not reused. No existing database was touched.

Actual SQL tests include all JSON-independent Flows plus SQL-only actor-change
inside transaction, stale replacement writer, actual case/audit writes followed
by refusal and healthy/early/persistent recovery faults. Legitimate prefix,
original exception, clean cache/audit and reopened state asserted.

The 49 combined skips are one explicitly isolated Azure SQL acceptance test,
one existing opt-in stock browser test (separate quality browser ran), and 47
existing opt-in assistant SQL Server tests. The separate actual SQL execution
targets quality/provider persistence, not those 47 assistant tests. Full core/API
discovery, cloud acceptance, paid model calls, screen-reader and human tests
were not run; no shared persistence-helper change justified broader discovery.
Configured migration exemptions in pyproject remain: quality.py and inherited
untyped test files are linted under existing rules but excluded from formatting/
strict typing. No new exemption added.

Session-only execution receipts (not committed/private data):
`quality91-final-tests.log`, `quality91-sql-final.log`,
`quality91-browser.log`, `quality91-browser.png`,
`quality91-sql.py` and `quality91-browser.py` under
`/home/azureuser/.copilot/session-state/723ca656-7a1a-411a-a9dd-f55919a9a289/files/`.
Source tests and the evidence summary are persistent PR artifacts.

## Original Review Handoff and Current Disposition

A1/A2/A3 have actual fictional local implementation evidence. A4 gates executed
with skips and operational limits explicit. Plan/details/checklists reconcile;
P01-P03 had no active source task or known blocker at handoff. Independent Review
subsequently executed Complete / Not accepted and identified RV-001/RV-002.
P04 implements those findings under caller authorization; see separate closure
evidence below. No Review rerun or regraded Pass.

## Authorized Correction ONE

Independent Review reproduced two implementation defects, not missing human
approval: RV-001 historical legacy FIXED recorders omitted from staff resolution;
RV-002 confirmed COMMIT followed by refresh failure requeues an already committed
legitimate prefix and reports ordinary failure.

Both corrected within existing quality scope. Canonical fail-before run:
JsonFlows.test_quality_legacy_repeated_recorders and
SqlFlows.test_quality_sql_postcommit_refresh produced five errors (one legacy,
four committed-refresh subcases), reproducing the independent findings before
production correction.

RV-001: historical FIXED recorder names now enter staff resolution before the
unknown-identity guard. The canonical new shared method removes only legacy
participants, retains different earlier/latest recorders, asserts earlier
recorder/alias denial specifically for independence, and independently accepts
with Pam. Existing genuinely unresolved legacy identities still refuse.

RV-002: own committed snapshot advancement is detected inside the quality
action exception boundary, before shared recovery can reload a winning writer.
Committed prefixes are not restored; QualityOutcomeError preserves/logs the
original read error and explicitly directs reload/history inspection. The
two-line server.py handler returns HTTP 503, outcome=committed. No success-shaped
fallback or ordinary rollback claim. Shared #95 overlap is declared above;
no grants/finance dispatch, app.js/dataset/manifest or SQL helper change.

Canonical SQL test uses a real second store committing an unrelated case write
between entry and the real save, then a fault after real COMMIT. Transient and
persistent refresh failure, with/without legitimate prior audit prefix, assert
exactly one decision/prefix, clean pending/touched, preserved cause and
reopened Accepted state/valid ledger. HTTP test executes actual COMMIT/read
failure and verifies 503/reload/readback. The first handler placement was
incorrectly within GET; the HTTP test exposed a disconnected POST, and moving
the handler to POST corrected it before final validation.

| Final execution | Actual outcome |
| --- | --- |
| Four exact JSON/SQLite/HTTP correction selectors | 4 pass |
| Same combined command recorded under P03, after production correction | 361 run, 312 pass, same 49 existing skips |
| Final quality, QualityMatrix, content standard, design system, endpoint inventory | 101 pass; overlaps combined count |
| Final actual local SQL Server MssqlProcurement | 38 pass, zero skip |
| Final actual Chromium full journey plus committed-refresh HTTP 503 notice/reload | Pass, zero page errors |
| Core/API configured Ruff, format, mypy; node syntax; git whitespace | Pass; existing exemptions unchanged |

Final SQL receipt: SELECT 1 readiness, unique loopback container
ama-quality91-5dbc50a0fc5a, database
quality91_9e67163bfe9e4e359f62378133a76f45; exact owned container removed.
No secret persisted. Session-only receipts: quality91-correction-targeted.log,
quality91-correction-tests.log, quality91-final-correction-check.log,
quality91-sql-correction.log and quality91-browser-correction.log. Counts overlap;
do not sum reruns. The existing 49 skips and external limits under P03 remain.

The original independent Review prefix is unchanged; pre-addendum SHA-256:
28e92d3b759320a29f52a4468c303c778af7f2d0a8a293ce9ed2d8bf04dd62cc.
Review execution remains Complete and original outcome remains Not accepted.
This implementation-owner closure evidence resolves RV-001/RV-002 locally,
not an independent Pass. P01-P04 complete; no open implementation finding,
repeated critique/Review or human/tool blocker. Delivery remains normal
commit/push/main PR with Refs #91, no merge or issue closure.

## Acceptance Limits

All people/data fictional; no private datasets/rosters, Azure, paid AI, new
infrastructure, live orders, financial commitments or actual professional
approval. Seeded role does not establish competence. Local SQL is not Azure
acceptance; browser is not human/WCAG acceptance.

## Delivery

PR https://github.com/jmservera/ama/pull/387 targets main from
fix/quality-handover-controls-91. Source commit ca8b950d was committed with
fresh authenticated id/login-derived local noreply author/committer identity
and required Copilot trailer, then pushed normally. Final delivery metadata
uses a separate normal commit on the same branch, not an amendment.

The PR includes Refs #91, actual ordered phase/artifact evidence, original
Review Not accepted and distinct correction closure, exact tests/skips and
the minimal shared #95 handler boundary. Owner/coordinator checks/rubric and
integration decision remain separate. No merge, rebase, force-push or issue
closure performed. User explicitly directed stopping at clean pushed PR;
no unrelated follow-up is started. Full current head is available from git/PR
without a self-referential commit hash in this artifact.

Resume session: 723ca656-7a1a-411a-a9dd-f55919a9a289.
