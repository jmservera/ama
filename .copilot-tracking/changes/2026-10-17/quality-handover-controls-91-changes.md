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

## Authorized latest-main integration (2026-10-17)

Coordinator explicitly authorized rebasing this run-owned topic after correction
publication onto freshly fetched latest origin/main, including merged #95.
Clean starting topic/remote/PR head:
d322235641487ff2c4dea1e4339c99f973b7f75d.
Old base b5d4c8402692758bd929a7ff9bf1832770738346.
Fetched integration base 2b24456863c0a8f39d47a73e22daeff3875cc825,
verified PR #386 merged at that exact commit; includes PR #385
1fc7325b93ea845b9cb2e827efbea624f7d20d30.

Rebase completed; candidate c0f67838383007c3f4a95ba0aa957378e2db0ba5.
Four conflicts were documentation-only: core/API README insertion points retain
the full upstream #95 section followed by #91; KB index retains both rows and
every upstream route; KB log retains exact full upstream byte prefix followed
by both #91 entries. No ours/theirs replacement, shared recovery edit or new
grant/finance correction. Source/test patch bytes over all src/tools/infra/mvp
non-Markdown files are identical old-base/old-head versus new-base/candidate:
SHA-256 a7eb041bf6ef894d67f6009a4c66074f0fe56250ade7439e268dcd3dae5038f7.

Upstream finance.py/grants.py/store.py, neutral app.js, dataset fixture,
scenario manifest and original case study verified byte-identical to integration
base. Dataset untouched, so upstream exact hash retained without authority
promotion or recomputation from a different fixture. Current persisted legacy
preparer lookup remains inside grant AND finance transaction validation;
scoped designation, shared _finance_operation and funding history retained.
Issue91's published correction ONE and original single Review remain unchanged.

Although conflicts are docs-only and the own production/test patch is identical,
the runtime now includes substantive upstream shared finance/Store/fixture
changes. A focused combined JSON/SQLite/HTTP and actual isolated local MSSQL
replay will verify grant/finance/stock/procurement/hazard/quality interaction,
rather than calling earlier pre-integration results fresh parity. No full
RPI/Review repetition, browser/UI edit, cloud action or unrelated expansion.
Integration validation completed on production/test candidate
c0f67838383007c3f4a95ba0aa957378e2db0ba5. Historical counts above remain
historical; the fresh integration results are:

| Fresh combined-tree execution | Result |
| --- | --- |
| Quality/provider, grant JSON/SQLite, finance matching/sign-offs, stock/hazard/building, role matrix and grant/procurement HTTP | 206 run, 205 pass, one existing opt-in grant browser skip |
| Actual local MSSQL quality/provider, stock, grant and finance matching | 83 run, 83 pass, zero skip |
| Configured core Ruff/format/mypy | Pass: 59 format-managed files, 112 source files |
| Configured API Ruff/format/mypy | Pass: 22 format-managed files, 54 source files |
| Four conflicted docs' relative file links/marker checks and git diff whitespace | Pass |
| Own whole production/test patch SHA-256 byte parity old/new bases | Pass; digest above |
| Exact upstream log prefix, all upstream index routes, original case and #95 shared-source/fixture/manifest bytes | Pass |
| Original single Review with closure addendum and original critique byte parity | Pass |

Fresh local command, same installed local venv, no dependency restore needed:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_quality_procurement test_grant_lifecycle_controls.JsonGrantChecks \
  test_grant_lifecycle_controls.SqlGrantChecks \
  test_finance_match_controls.JsonFinanceChecks \
  test_finance_match_controls.SqlFinanceChecks test_stock_reconciliation \
  test_finance_signoffs test_role_matrix test_grant_lifecycle_api \
  test_procurement_api -q
```

Actual SQL selected test_mssqlstore.MssqlProcurement (includes quality),
test_mssqlstore.MssqlStockDecisions,
test_grant_lifecycle_controls.MssqlGrantChecks and
test_finance_match_controls.MssqlFinanceChecks. Enabled only their explicit
local test flags against a freshly created unique loopback container, dynamic
port and process-generated unlogged secret. Actual SELECT 1 readiness passed.
Owned container ama-quality91-7509b019ec5b and database
quality91_21b884127be448218985a0f970880ac3; exact container removed in finally.
Grant/finance tests created/dropped only their own UUID databases.
Session-only fresh receipts: quality91-integration-local.log and
quality91-integration-sql.log. The canonical tests explicitly cover issue91's
real COMMIT followed by transient/persistent refresh fault with/without prior
pending prefix, clean subsequent lock exit/reopen and exactly-once audit, legacy
earlier-fixer resolution, and upstream issue95's transaction-time legacy
preparer code/OID rebinding denial for both grant AND finance with no false
audit. No duplicate issue95 implementation.

No browser rerun on this integration: no UI conflict or source delta to the
own patch, and upstream neutral UI retained verbatim. The one skip is the
existing opt-in grant browser; previous quality/95 browser receipts remain
historical, not fresh. No full suite, Azure, paid AI, human authority, WCAG or
independent Pass claimed. Original law-store-unavailable diagnostics remain
explicit in fictional HTTP fixtures.

Fresh fetch immediately after validation still resolved origin/main to
2b24456863c0a8f39d47a73e22daeff3875cc825. Publication uses the specifically
authorized expected-old-remote lease d322235641487ff2c4dea1e4339c99f973b7f75d
only for refs/heads/fix/quality-handover-controls-91. A separate integration
evidence commit contains Markdown/state metadata only; final full head is
reported by PR/git, avoiding a self-referential commit hash. No main write,
merge, issue closure, external approval inference or other's dirty work used.

## Authorized merged-hazard integration (2026-10-17)

Later coordinator authorization names freshly fetched/verified main
1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c, merged PR388/#85.
Clean prior reviewed/published topic head
210b89df0d287675cb8ac5148dd9d198d37dd9c1 on prior base
2b24456863c0a8f39d47a73e22daeff3875cc825. Rebase candidate:
a17eebb30fc8be75f4cfaf6ba7f12791f9823077.

Only docs/reference/log.md conflicted; retained exact complete upstream byte
prefix followed by all quality entries. Component sections/index auto-merged,
all upstream routes retained. No source conflict or SQL marker/harness rewrite.
Whole own production/test patch remains byte-identical over src/tools/infra/mvp
non-Markdown paths, SHA-256
a7eb041bf6ef894d67f6009a4c66074f0fe56250ade7439e268dcd3dae5038f7.

Inspected merged hazard.decision_scope, hazard.validate_sql/mark_committed and
SqlStore.save: hazard validation remains alongside stock, finance and procurement
writer validation. hazard.mark_committed executes immediately AFTER actual
COMMIT, BEFORE committed-snapshot bookkeeping and optional _sync. It marks only
the active hazard operation's persisted context. Existing hazard context is
preserved/restored, committed failures report explicit persisted/reconcile notes
and discard without restoring the committed prefix. Quality keeps its separate
own committed-snapshot detection before shared stock recovery, explicit
QualityOutcomeError/HTTP committed-reload guidance and no committed-prefix
requeue. Neither caller's marker/context is reset early or repurposed.

Verified SQL store, hazard, workflows, MSSQL harness, grants/finance/store,
neutral app.js, fixture/manifest and original case byte-equal to latest base;
both original quality Review/closure and critique byte-equal to prior head.
No global helper redesign, duplicated #85/#95 correction or external authority
inference. Prior results remain historical, not fresh hazard integration parity.
Fresh combined local and actual task-owned MSSQL validation follows; no browser
or full Review rerun. External review reference supplied by coordinator:
42ce6748; this run reports exact source fingerprints for final-head comparison
and does not claim its independent outcome.

First combined local run: 243 run, one error and two existing skips.
The inherited hazard race's quality-accept branch copied a building fixture
whose Synthetic recorder/SYN-RECORDER is deliberately absent from current
staff. Issue91 correctly refuses that unresolved legacy identity before save,
so the test never reached its intended interleaved emergency-at-commit probe.
This is a tightly coupled fixture precondition mismatch, not authorization to
weaken quality unknown-identity refusal. Adjust only that test's copied Submitted
record to identify existing fictional Sam as recorder; independent Pam and the
original expected GateError/no-mutation/audit assertions remain. No dataset or
building fixture/manifest change. Initial full patch parity is historical before
this precise test-only integration correction; production bytes stay unchanged.

The corrected race and both canonical post-COMMIT prefix tests passed in a
three-method focused replay; combined local replay then passed 243 run with
two existing skips. Actual initial merged-hazard MSSQL replay passed 99 run/
98 pass/one existing JSON-only skip. No production change was needed.
Added a direct assertion in the existing quality post-COMMIT regression that
the next healthy locked save leaves exact audit and persisted case unchanged,
matching the existing hazard test's next-save assertion. Final local/MSSQL
replay follows for both precise test-only integration changes.

### Final merged-hazard integration evidence

Tested source/test candidate:
48b90f42fe8170f3f17956e3a194a0c93b33eee2, based on rebased candidate
a17eebb30fc8be75f4cfaf6ba7f12791f9823077 and exact main
1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c.
Only source/test delta after the byte-identical initial rebase is the two
precise regression changes above; no production code change.

| Fresh final merged-hazard candidate execution | Result |
| --- | --- |
| Combined quality/hazard/grant/finance/stock/provider/current-actor/legacy/HTTP selection | 243 run, 241 pass, two existing skips |
| Actual task-owned local MSSQL affected transaction paths | 99 run, 98 pass, one existing JSON-only skip |
| Earlier focused SQLite hazard interleave and both committed-prefix selectors | Three pass; overlaps combined count |
| Configured core Ruff/format/mypy | Pass; 60 format-managed files, 113 source files |
| Configured API Ruff/format/mypy | Pass; 22 format-managed files, 54 source files |
| Production patch old/new bases byte parity | Pass; SHA-256 e932bad340014d11677937d8122e5bf0c3c1cfc4a3e1b90f31fd1ce31f3b1362 |
| Final whole own production/test patch fingerprint, including two test changes | SHA-256 850368c99aacece702c8533fc6db944a81bc358b2dbf799a006e644524d2c4f3 |
| Upstream KB prefix/routes, hazard hooks/marker/harness, grants/finance/stock/provider sources, fixture/manifest/original case and original Reviews | Retained; no authority promotion |

Fresh final local command:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_quality_procurement test_hazard_referral \
  test_grant_lifecycle_controls.JsonGrantChecks \
  test_grant_lifecycle_controls.SqlGrantChecks \
  test_finance_match_controls.JsonFinanceChecks \
  test_finance_match_controls.SqlFinanceChecks test_stock_reconciliation \
  test_finance_signoffs test_role_matrix test_grant_lifecycle_api \
  test_procurement_api test_hazard_api -q
```

Actual final MSSQL selected test_mssqlstore.MssqlProcurement,
test_mssqlstore.MssqlStockDecisions, test_mssqlstore.MssqlHazardReferral,
test_grant_lifecycle_controls.MssqlGrantChecks and
test_finance_match_controls.MssqlFinanceChecks. The inherited hazard SQL
method contains transient/persistent post-COMMIT synchronization failures with
legitimate prior audit, original-error identity/committed note, exact counts,
valid ledger and next healthy save. The quality method covers transient/
persistent actual post-COMMIT read failure with/without prior audit, explicit
committed outcome/cause, exactly-once ledger, clean lock exit/reopen and now
direct next-healthy-save audit/state equality. Both callers' pre-commit
rollback/prior-pending/current-identity checks and legacy fixer/rebinding tests
remain exercised. SQLite additionally exercises the repaired fixture's
interleaved emergency across all nine guarded transitions.

The two local skips are the existing JSON-only separate-file hazard audit
ordering case inherited by SQLite, plus existing opt-in grant browser. The
single MSSQL skip is that same JSON-only case inherited by MSSQL, not a skipped
post-COMMIT/authority transaction test. No skip/validator was added or weakened.
No browser rerun or independent Pass; earlier/browser evidence remains
historical, with no human/Azure/WCAG inference.

Fresh final SQL readiness: SELECT 1 succeeded, unique loopback dynamic port,
process-generated unlogged secret, owned container ama-quality91-b68d9a8810be,
database quality91_aa13e78a169f406ab2a64b27334a65c6. Exact owned container removed
in finally; grant/finance UUID databases cleaned by their existing fixtures.
Session-only receipts: quality91-hazard-integration-local.log (first failing
fixture run), quality91-hazard-integration-targeted.log,
quality91-hazard-integration-local-final.log,
quality91-hazard-integration-sql.log (earlier overlap), and
quality91-hazard-integration-sql-final.log. Counts overlap, do not sum.

Source SHA-256 fingerprints for coordinator external review 42ce6748:

| Path | SHA-256 |
| --- | --- |
| src/core/src/zava_forward/core/quality.py | de1373cdc116a2193b723bff3c97892b233932960e9c6f2210571c21c117b9fd |
| src/core/src/zava_forward/core/sqlstore.py | 2788fb7a6d8b83864303177dd0f4b7159096fbb1d8924e9733304fe7b00c4832 |
| src/core/src/zava_forward/core/hazard.py | 10e1f929b5a0628fe23105144c275f5b250ac338b388c285612925b931e4de62 |
| src/core/src/zava_forward/core/workflows.py | 1d815030342641829a00ee0e5cb939022512da757d5af0a234626491c46275fa |
| src/api/src/zava_forward/api/server.py | 348d5f50dd9580b3bbb24cc13a1dc4ec3e427e6ec45579d42680e17fe5888e0e |
| src/api/tests/test_mssqlstore.py | d8dccf1ee8ddafa0e2fa49e48189929e97e0fed8f58458d4e6f8549794b8afae |
| src/core/tests/test_quality_procurement.py | 2149af05b7c37fce157081f4d96dbe83accd3cb7008e07f2af6e6acae9a13e6f |
| src/core/tests/test_hazard_referral.py | c1fc4c10a5fb8534355bb4651d2ce31b7f70e1c059948a361dcaf08a78663af9 |

Fresh fetch after tests still resolves main to
1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c. Final evidence commit is Markdown/
state metadata only after tested candidate; final full head is reported by PR/git.
Authorized publication uses ONLY own topic with exact expected-remote lease
210b89df0d287675cb8ac5148dd9d198d37dd9c1. No main write, merge, issue closure,
cloud action or independent Review rerun. Original adverse Reviews unchanged.

## Authorized correction TWO: downstream quality assistant

Coordinator reports exact-210b89df external Review Revise / Medium: assistant
capture and len(records)!=1 predicate count Superseded history as current, and
proposal review also traverses historical contributors. Correction TWO explicitly
authorized after completed post388 publication at 4c9597b1. Original single RPI
Review and correction ONE unchanged; no new full Review/self-Pass.

P05-T01 activated before edits. Prior-art search found no shared current-record
selector; quality.py defines explicit SUPERSEDED, one active record per measure
and evidence_version with legacy default 1. Reuse a small state-based selector,
not maximum-version picking that could hide malformed active duplicates.
Keep every active candidate for discrepancy detection; only accepted/handed
current evidence can avoid state discrepancy. Include evidence_version in closed
snapshot allowlist so same-content replacement still invalidates proposals.
No persistence, hazard marker, finance/grant/stock/provider hook or UI edit.

### P05-T01 fail-before and implementation

Two new existing-file canonical ContractTests methods executed before source
changes: test_quality_replacement_uses_only_current_evidence_and_version and
test_quality_current_discrepancies_do_not_rely_on_retired_acceptance.
Result: two run, ten failing assertions/subcases. Actual domain replacement
retained Superseded+Accepted but snapshot included both; old evidence leaked into
captured source and historical-only evidence could satisfy missing current work.
Session-only receipt quality91-correction2-before.log.

Added quality.active_records as the shared state-contract selector, excluding
only explicit Superseded records, never arbitrarily choosing highest version.
Assistant capture, per-measure predicate and current contributor checks use it.
Snapshot's existing scalar allowlist additionally captures evidence_version;
legacy absent version remains null/unknown, not invented authority. Current
state must be Accepted/Handed over to avoid a state discrepancy. Missing/unknown
measures, missing current work, extra unknown-measure records, duplicate-active
records and missing/conflicting current checklist evidence remain discrepant.
Rule description updated; existing rule_hash/source_signature mechanism
invalidates prior proposals without a global registry/service change.

Tests execute actual PM submission/QA acceptance then replacement by QA with
independent PM acceptance. Only current version 2 appears in captured sources; no
false discrepancy, old ready proposal becomes stale and cannot verify, new
proposal has a different source signature/id. Original recorder can independently
review the new proposal; current recorder cannot. Historical evidence changes
do not change current signature, current version changes do. Proposal-only review
does not mutate any domain/quality state. Direct predicate tests also filter
historical snapshots defensively, preserve accepted/handed success, all pending/
defect/unknown states, duplicates, wrong/missing measures, empty sources and
current evidence gaps. Existing valid-case fixture now actually uses Accepted
with explicit version 1, not Submitted posing as already accepted evidence.
No private data or billable AI used; existing deterministic provider double only.

Final test-strengthening uses an otherwise authorized current QA recorder and
requires the explicit Someone independent refusal, not a role-based denial.
Its first rerun correctly hit optimistic ConflictError because the test reused
the proposal revision from before PM verification; retaining the returned
verification revision fixed that harness mistake without any production change.
This intermediate result is preserved in quality91-correction2-review-cas.log;
the subsequent complete focused rerun passed as recorded below.

### P05-T01 final actual validation

| Execution | Actual result |
| --- | --- |
| Five exact assistant/current-version/scanner and hosted hazard regression selectors | Five pass |
| Final assistant/dispatch + quality + hazard + QualityMatrix HTTP selection | 206 run, 156 pass, 50 skips |
| Exact full src/core CI discovery | 788 run, 751 pass, 37 existing skips |
| Core/API configured Ruff, format, mypy | Pass; 60/22 format-managed files and 113/54 mypy source files |
| Diff whitespace and retained shared-source/fixture/Review byte checks | Pass |

Final focused command:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_assistants test_assistants_dispatch test_quality_procurement \
  test_hazard_referral test_role_matrix.QualityMatrix -q
```

Exact full core command taken from .github/workflows/src-ci.yml:

```bash
cd src/core
../../.venv/bin/python -m unittest discover -s tests -v
```

The full discovery includes the exact prior hosted failure
test_hazard_referral.SqlHazardReferral.test_interleaved_emergency_hold_blocks_every_guarded_commit,
all nine interleaved transitions, now passes with the prior test-only registered
recorder precondition. No permission guard relaxed; original assertions intact.
It also includes both post-COMMIT/recovery families and all core quality/
resident/stock/provider/grant/finance tests. No CI rerun shortcut or fabricated
pass. Full-core 60,000-case scale checks use generated synthetic data only.

Focused skips: 49 opt-in assistant MSSQL variants (includes two inherited new
canonical methods), plus one inherited JSON-only hazard audit-order case on SQL.
Full-core skips: 19 opt-in isolated finance MSSQL, 16 opt-in grant MSSQL, one
JSON-only audit-order test inherited by SQL, one explicit isolated Azure SQL
acceptance. Existing opt-in decorators/skip conditions unchanged; no new skip
or validation exemption. No new real MSSQL replay for this consumer-only fix:
no SQL/schema/transaction/recovery implementation changed. Prior actual 99-case
integration replay remains historical, not new assistant SQL parity.
No new browser/UI, cloud/paid AI, real-human/WCAG or independent acceptance.

Session-only receipts: quality91-correction2-before.log,
quality91-correction2-targeted.log, quality91-correction2-focused-final.log,
quality91-correction2-core-ci.log. Counts overlap; do not sum.

Final correction source SHA-256:

| Path | SHA-256 |
| --- | --- |
| src/core/src/zava_forward/core/assistants.py | fefb93c5b63149c8d2dda0723d8822e7533913f9d2f666a2bab71df265f0add9 |
| src/core/src/zava_forward/core/quality.py | 3f4982ebd09ce122670acd9738c970c9c051b47e11a8bc5fb31c134d082ffc89 |
| src/api/tests/test_assistants.py | 55d96da83e9b50d5af2644f2f2eb6a6141328b9c19eef10dadc8d8544fb9606b |

P05-T01 completed with no local unresolved correction finding. Original single
RPI Review, its original adverse verdict and correction ONE are byte-unchanged.
Coordinator exact-210b89df external Review Revise/Medium is retained as reported;
this is separate implementation-owner correction TWO closure, not a new Review
or independent Pass. External final artifact/head gate remains coordinator-owned.
Base stays 1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c, starting published head
4c9597b1991b9ed521c951f0d9f7a8487ebba96f; normal correction commit/push only.
No recovery hooks, sqlstore/hazard/workflows, finance/grants/stock/procurement,
MSSQL harness, dataset/manifest or original case change. No merge/issue closure.
