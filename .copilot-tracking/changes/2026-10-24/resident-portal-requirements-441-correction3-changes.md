---
title: Resident validator tool-failure correction changes
description: Actual prospective implementation after independent plan critique
ms.date: 2026-10-24
---

## Implementation Opening

Task jmservera/ama#441, native59f31558. Scope P01then P02as owner explicitly
ordered, no automatic-mode inference. Research executed Complete/Ready; Plan
and details complete, independent final-candidate critique Complete / Pass,
zero findings, before bot integration/source edits. First ready P01-T01guard
and normal ff, then minimal source/test batch, focused checks and implementation
commit before one actual committed-candidate Review. No gate/publication.
Exact UTC phase events also retained prospectively in native session evidence.
No source or bot-history edit has occurred at this opening.

## P01-T01 - Bot Preservation

2026-10-24T08:18:09Z, fresh exact main/topic/local parent/path guard passed,
no tracked/index or unexpected/ignored changes, only five owned RPI files.
git merge --ff-only origin/docs/resident-portal-requirements-441 succeeded.
Actual score-only16+/16-botb06ca0b4 ancestry retained, SHA256
78b5f15a2b808364387e800bf772f0c44aa521970bb65aa9ad5a7686ee28671a.
No manual score change. No source correction before this checkpoint.

## P01-T02 - Shared Lint Contract

Source/test batch2026-10-24T08:18:42Z, strictly after critique and botff.
Changed only existing lint() in validate-integration.py and four new methods
in test_validate_integration.py. All15earlier methods retained; no unrelated
refactor. Return triple/text/location-normalized Counter unchanged.
Before normalization accepts only0/empty output or1/nonempty all-genuine
stdin:positive-line[:positive-column] MDnnn/aliases description on stderr.
Unexpected output/status or stdout with1raises contextual RuntimeError
including selected CLI/status/output. Missing node OSError still propagates.
No error filtering/catch/default/existence-only check or config change.
Refinement imports this exact helper; no second fix or source change there.

Implemented source SHA256:
1645296581eafafc3c745264e60f4be7d52cfb6c5b8679a3f854316bf991c75c.
Tests SHA256:
0ffed9c0834d1e2e138af2605e2b4e3a2696ec4c4c56003dacd8613e335ddc66.

## P01-T03 - Focused Evidence

Commands below set PYTHONDONTWRITEBYTECODE=1. P denotes the existing
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441
package; CLI is correction1's existing external markdownlint0.45.0;
OUT is this native session's files directory. Exact absolute argv and output
hashes belong to the external final handoff, not portable working links here.

```bash
python3 -m unittest discover -s "$P" -p 'test_validate*.py' -v
python3 "$P/validate-integration.py" \
  --markdownlint-cli "$CLI" --out "$OUT/441-correction3-integration-report.json"
python3 "$P/validate-refinement.py" \
  --markdownlint-cli "$CLI" --out "$OUT/441-correction3-refinement-report.json"
```

* All19tests PASS exit0, includes actual missingCLI public helper and actual
  main raises at lint/no report. Expected fatal Git stderr in older negative
  reference tests is asserted, not a hidden suite failure.
* Contract fixtures exercise genuine0and1with/without columns, duplicate
  counts/shifted-line equivalence, mixed config/diagnostic, missing module
  stack, empty1, noisy0, genuine-on0, unexpected2/4/signal and stdout-on1.
  Portable tests do not depend on external private CLI location.
* Both real validators exit0,22original hashes and18refinement mappings.
  Original actual Markdown comparison lines/exits/counters and link fields
  equal correction2report exactly. No proxy-only claimed preservation.
* Actual main before source edit with absent CLI exited0and wrote
 441-correction3-bad-cli-accepted.json, retained as false-positive adverse
  evidence only. Same absentCLI actual main now exits1at explicit RuntimeError
  markdownlint failed, MODULE_NOT_FOUND; new output report does not exist.
* External real-cli-after script confirms actual clean0, genuine MD0121
  without column and MD034/MD0591with column still accepted. Actual missing
  config plus MD012 code1and malformed config stack1both rejected explicitly.
  Initial research two-space hardbreak fixture was actually clean; honest
  failed diagnostic-fixture attempt retained, not silently substituted.
* New five Markdown artifacts lint/link PASS with existing helper/config and
  real CLI. No new diagnostic suppression or long-table workaround needed.
* git diff of docs, all source/refinement evidence/mappings, score and prior
  refinement validator/tests against bot entry exit0. No source archive,
  protected original/memory, append-only log or product byte changed.
* Correction-only git diff --check exit0. Full-branch main diff check
  FAILED exit2,52archival diagnostics including12refinement, exact text
  byte-identical to bot entry. No raw byte rewrite, passing all-branch claim,
  skip or waiver. Full failed log retained externally.

## External Evidence Hashes

* 441-correction3-reproduction.log:
  c53ef0a3abab62caf54bbd97e95483222897b256cfe3553eda2201a7e4134e99.
* 441-correction3-contract-probe.log:
  2b6a513e75b307c8e2c7a6f7de5d5276b67d81e34e87ee9fe245fd010c78f695.
* 441-correction3-main-before.log:
  2b48da1d7adaec4978d6d8196523202503f36da8e091eb754e82ad7a1d4d9991.
* 441-correction3-main-after.log:
  c6f756563a9008bf981ab9e71574cef03132297dbfbf29abd8b14b975e953d51.
* 441-correction3-regressions.log:
  ac85d7546f35f37c341cccbf82e230336b7124337bbabee8989101e2eb5c8969.
* 441-correction3-integration-report.json:
  6ce739e27e7235b626640c6a3dd1824a8c8517c3397d202530ea99400a4458d3.
* 441-correction3-refinement-report.json:
  6dd403c6fd47b8edc712d7821ce9c3636b93afff202f28883abdba3d5aac37d3.
* 441-correction3-real-cli-after.log:
  aab0af83864d56d80c7d906bcbcb74755730b0de3db5991b87784f3742eccb50.

## Reconciliation and Remaining Work

P01 Complete. No material divergence or unresolved implementation decision.
Plan checklist/details/changes agree. P02implementation commit and single
Review remain pending; this original pre-Review evidence does not preclaim
commit success/approval. Wrapper will commit Review-only evidence afterward,
with exact assessed implementation identity and final clean handoff externally.
No source amendments or repeated Review after that assessment.

All seven current PRD FAIL/ValidateBLOCKED/FinalizeNOT_EVALUATED findings,
singularity1<2,30ACNotrun,automationOFF,OD52-55/OQ28-31,NFRprecedence,
unsigned/live gates and id:null proposed/unregistered/deferred ADR unchanged.
A5/B6 remain OPEN per owner; bot changed citations externally, no closure
claimed. Prior ADR-list finding4365410759 resolved per hosted owner evidence,
no replay. Correction3addresses only4365610794. Historical gatefc7b2596
and protected resident/cost environments untouched, no cleanup/gate replay.
Coordinator owns later exact-candidate gate and retained independent assessment.
No push/PR edit/merge/close/ACticks/cloud/tenant/billing/private/model/scorer call.
