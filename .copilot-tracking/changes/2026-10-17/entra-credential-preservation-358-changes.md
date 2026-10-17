---
title: Issue 358 implementation evidence
description: Failing-before, mutation and acceptance record
ms.date: 2026-10-17
---

## Metadata and Execution Status

Task ID: 358. Slug: entra-credential-preservation-358.
Declared scope: full plan, with P01/P02 implementation followed by parent-owned
P03 Review/publication. Status: full plan complete, issue acceptance partial.
Completed markers: P01/P01-T01/P01-T02, P02/P02-T01/P02-T02, P03/P03-T01.
No remaining active marker. Live preservation remains UNMET as recorded below.
Plan: .copilot-tracking/plans/2026-10-17/entra-credential-preservation-358-plan.md.
Details: .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md.
Approved source boundary: setup-entra.py preservation/reuse, existing setup tests,
runbook/evidence/index/append-only log. No cloud/Graph/SQL, private data or secrets.

## Starting Validation

Own Python 3.12 venv created under the session workspace. Original setup suite
passes: 95 tests. No src package installation required for this targeted probe.
Research/Plan/single-critique evidence committed as c64d925.

## Failing-Before Evidence (P01-T01)

After correcting two test-fixture issues (legacy store tag alignment and making
the readback transport failure one-shot so lock cleanup can run), the unchanged
source ran 100 setup tests with 15 assertion failures and zero runner errors:
three persisted-reference failures, three sparse/omitted-KV preservation failures,
and nine unsafe-inventory failures. The new expiry matrix and existing legacy
delegate passed baseline; these are guard regressions, not claimed source bugs.
Raw wholly fictional output retained in session files/358-failing-before.txt.

Full-suite prerequisite probe failed on missing zava_forward and PyYAML in the
fresh venv. Installed editable core/agents/api/orchestrator, pinned PyYAML and
hashed API requirements in that venv only, per the infra guide.

## Implementation-Time Plan and Detail Updates

Single critique corrections are part of the approved candidate, not a second
critique: pending reference-only fingerprint, metadata-only GET success oracle,
and review-outcome publication gate. No user direction changed.

## Preservation Implementation (P01-T02)

Validated named inventories, reconciled known KV metadata with list app values,
rejected conflicts/incomplete references/unrecoverable values before password
creation, and added a reference-only handoff digest atomically with the rebuild.
Readback ignores ordinary write-only values, compares names/KV metadata, then
clears the tag. A failed/unknown readback leaves the tag to block unverified reuse;
a matching rerun recovers without another password. Existing expiry logic and
legacy CLI are unchanged. All 100 ordinary setup tests pass after the fix.
Seven mutations execute in the existing suite, without source-file edits.

## Validation Record (P02-T01)

| Check | Scope and command | Outcome |
| --- | --- | --- |
| Original baseline | Own-venv unittest discovery, test_setup_entra.py | 95 passed |
| Red regressions | Unchanged setup source with five new behavioral methods | 100 ran, 15 assertion failures, zero errors |
| Targeted green | Own-venv setup discovery, including mutation method | 101 passed |
| Legacy helper | Own-venv test_initialize_api_auth.py discovery | 17 passed; existing delegation test also passes within setup suite |
| Full infra | REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q | Final 313 passed, no skips/errors |
| Bicep | az bicep build --stdout and lint for all infra/*.bicep and infra/modules/*.bicep | Passed offline with Bicep 0.48.1 |
| Changed Python | Ruff E9,F63,F7,F82,F401 on setup/test/legacy; mypy --follow-imports=silent --ignore-missing-imports setup and legacy | Passed; existing nonformatted setup style retained, no whole-file reformat |
| Existing CI infra lint | Exact E,F,I,B,UP checks and format checks for Bicep/deploy/pipeline/staff tooling/tests | Passed, eight files already formatted |
| Python/CLI | py_compile setup/test/legacy; legacy --help | Passed |
| Whitespace/docs | git diff --check and relative link/heading review | Passed |

### Killed Mutations

Each mutation compiles an isolated function with original globals and runs the
actual behavioral test against FakeAzure. The suite requires assertion failures
and explicitly rejects test-runner errors. Seven killed mutations:

* Expiry comparison replaced with True.
* Legacy stored-name expiry guard searches all credentials instead of valid ones.
* Dropped keyVaultUrl independently.
* Dropped identity independently.
* Replaced nonempty ordinary app value with empty string.
* Bypassed the pending-handoff pre-reuse check.
* Incorrectly required write-only ordinary values in metadata readback.

Initial mutation-harness indentation errors were corrected before counting
kills; those errors are not acceptance evidence. The final seven execute and
fail behavioral assertions, with no runner errors.

## Documentation and Acceptance (P02-T02)

Updated existing infra runbook and cutover evidence, KB index and append-only
log. No new KB page or owner memory edit. Exact unmet live criterion and #360
shared-file sequencing are explicit. No live resources, secret values, dataset,
Graph, SQL, image build, spend, role or network operation was used.

## Pre-Review Reconciliation

Plan P01/P02 and every subordinate task checked; phase details agree. P03-T01
remains for the one Review and publication. Changed source is only narrow
preservation/recovery; existing expiry logic, delegate, crypto/identity/network
guards, staff jobs and CI remain unchanged. Validation and follow-ups current.
Review Ready for offline scope; live acceptance explicitly UNMET.

## Blockers and Follow-Up Items

Actual authorized non-production preservation round-trip: UNMET. This task's
no-write/no-secret-read constraints prohibit setup/check live execution. #360
owns broader setup/job readiness. No cloud permission discovery is necessary.

## Review and Publication (P03-T01)

One Review executed: Complete / Residual work, no in-scope implementation defect
found; RV-001 live preservation and RV-002 #360 sequencing routed to distinct
owner/coordinator follow-ups. Review artifact:
.copilot-tracking/reviews/logs/2026-10-17/entra-credential-preservation-358-review.md.
Implementation 40e6835be682e1aeffab8ca78a10184889e5e3b4; Review commit 544f0ce.
Topic pushed; PR https://github.com/jmservera/ama/pull/374 opened against main,
explicitly Refs #358, not closing the issue or ticking live criteria.
No source/test/docs changes after Review; final plan/details/state/changes
publication reconciliation only. Hosted checks are not claimed passed.

Owner explicitly requested stop after push/PR. Automatic session stopped; no
follow-up selection, child loop, merge, force push, Azure operation or new spend.
Ranked next-owner work remains actual authorized live proof first, #360
coordination second. All phase artifacts are dated and committed.

## Explicit Phase Log

* 2026-10-17 Implement opened after Plan Ready and one critique disposition.
* 2026-10-17 Original setup baseline: 95 passed in own venv; P01-T01 started.
* 2026-10-17 P01-T01 complete: 15 behavioral assertion failures against unchanged source.
* 2026-10-17 P01-T02/P01 complete: 100 setup tests pass; P02 validation started.
* 2026-10-17 P02 complete: seven killed mutations, final 313 infra tests pass, existing offline gates pass, docs and current plan reconciled.
* 2026-10-17 Implement handoff: Ready for one Review; live acceptance remains UNMET.
* 2026-10-17 P03/full loop complete: one Review Complete / Residual work; PR #374 published; final evidence reconciliation, then stop per owner.
