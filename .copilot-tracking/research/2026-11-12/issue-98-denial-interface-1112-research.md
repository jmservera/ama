---
title: Issue 98 field review to held-pack denial path trace
description: One trace of review, deterministic validation and held export freshness on pinned main, with one admitted gap
ms.date: 2026-11-12
---

## Scope and authority

* Task `issue-98-denial-interface-1112`; branch `research/funding-denial-interface-98-1112`; worktree-local; pinned main `cd81888e4a81cf4c712d50b357ca900fd5c8c06b` (fetched at start, equals HEAD).
* Issue #98 (open): criteria 1 and 4 ticked, 2 and 3 unproven. Authority: issue body, comment [6652965181](https://github.com/jmservera/ama/issues/98#issuecomment-6652965181) (rule/pack interface and denial-path engineering may proceed without inventing approved rules; named Finance review stays separate) and the launch comment 6835926959 (do not duplicate 510/888/1083/1093, do not renew corrections). PRD FR-042 and FR-043 (exact stale propagation of pack reviews).
* Research disposition: executed. Local-only; focused validation tier. No approval, rule, template, reviewer identity or Finance decision invented.
* Environment: venv outside the repository, `pip install -e src/core -e src/agents -e src/api ruff mypy`; imported `form_review` path confirmed inside this worktree. No PYTHONPATH, no uv.

## Trace (single path)

1. Field review: `form_review.action(... "review")` in `src/core/src/zava_forward/core/form_review.py` changes only its own field, appends history, bumps `input_version`.
2. Deterministic validation: `_report` marks fields Stale on schema or source drift, emits Fail/Unknown/Conflict issues, hard-codes `approved_rule_validation="Not evaluated"`, `reviewed_ready=False`, `status="Held"`; `_holds` records template-rules, OD-12, OD-15 as Held with owner role and next action; `_approvals` evaluates draft-scoped approval lineage as Held/Current/Review required.
3. Held pack: `form_export.draft_export` returns a digest-covered body (`BODY_KEYS`: schema id/version/digest, template, rule_refs, fields, history, attachments, stale_fields, open_issues) with fixed Held/not reviewed/not submitted.
4. Freshness: `form_export.export_freshness` compares schema digest, `input_version`, per-field rows and current `stale_fields` (delivered by 888, 1083, 1093).

Version and authority binding exist (schema digest, input version, history, hold ledger). Unknown/Held with no approved rule evaluator is deliberate and is not the gap: no approved rule inventory exists (FD-01 to FD-14 under #96/#97).

## Concrete gap (reproduced)

`export_freshness` never compares `open_issues` although they are in the saved digest. Staging a conflicting candidate for an Unknown field after export adds a `Conflict` issue, changes the export `content_sha256`, yet the saved export is reported `Current` with that field listed as unaffected. FR-043 requires exactly the dependent proposals and pack reviews to be marked stale.

Evidence: [probe-before.py](../../evidence/2026-11-12/issue-98-denial-interface-1112/probe-before.py) output (Current, `stale_fields: []`, digest differs); failing-first test `test_changed_open_issue_stales_only_its_field` in `src/core/tests/test_form_export.py`, original output [failing-first.out](../../evidence/2026-11-12/issue-98-denial-interface-1112/failing-first.out) (both stores, `'Current' != 'Stale'`, exit 1). A first invocation error (test module not importable) is retained as [invocation-error-before.out](../../evidence/2026-11-12/issue-98-denial-interface-1112/invocation-error-before.out). Baseline: 67 form tests pass ([baseline-form-tests.out](../../evidence/2026-11-12/issue-98-denial-interface-1112/baseline-form-tests.out)).

## Admission

* Distinct from 510/888/1083/1093: those compare field rows and stale fields; none compares held issues. This is a gap in the freshness comparison of a held pack under criterion 3 and FR-043, not a renewal of a PR correction: this branch has no PR and no spent cycle.
* Smallest fix: compare open issues grouped by field in `export_freshness`.
* Not in scope: a rule evaluator, rule registry, approval status fields, case-scoped holds (OD-12, OD-15 are not evaluated per draft; whether a case-scoped approval should bind drafts is a Finance decision, recorded as a follow-up, not changed).
* Planning Readiness: Ready.

## Follow-ups

1. Approved rule and template inputs (FD-01 to FD-14): human Finance decision; still blocks criteria 2 and 3.
2. Case-scoped hold lineage (`_approvals` skips `draft_id=None`): needs a decision on how a case-wide approval binds drafts.
