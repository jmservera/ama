---
title: Issue 441 owner disposition packet research
date: 2026-11-02
task_slug: issue-441-owner-disposition
status: complete
---

## Scope

Research disposition: `executed`. Planning Readiness: `Ready`.

Next independently reviewable slice of #441 after merged #442, #454, #686 and #726.
Documentation only. No product, ADR ID, memory or approval change.

## Evidence (all observed 2026-11-02 on origin/main 071e132a8)

1. Integration is merged. BRD v0.21.0 (FR-053 to FR-064, AC-104 to AC-132, OD-52 to OD-55) and PRD carry the resident increment. The pinned draft patches still do not apply to main, so nothing is re-applied. Recorded by #726.
2. Overlaps. No open PR touches `docs/brds`, `docs/prds`, `docs/adrs` or the addendum. Open PRs that touch the shared log or index: #763, #761, #758, #746, #742. A conflict there is a rebase, not a dependency. #426, #424, #439, #722, #690, #704, #698, #640, #692, #648 and #668 are all merged.
3. Re-run of the merged read-only verifier (`.copilot-tracking/changes/2026-11-01/issue-441-recheck/verify-441-recheck.py`) on this head: `overall_ok` true (freshness, custody, registries, policy, formulas, links, adr, log).
4. Hosted checks observed on merge commits (GitHub check-runs API):
   * #442 `df3e9643c`: activation, agent, detection, safe_outputs, record_rubric_score, conclusion and three `changes` runs succeeded; one Dependabot run failed (unrelated automation, not a PR gate).
   * #454 `ffde36315`: activation, pre_activation, rubric_prepare and three `changes` runs succeeded; others skipped.
   * #726 `3466bc933`: activation, pre_activation, rubric_prepare, conclusion succeeded; others skipped. Its PR-head rollup showed `conclusion` FAILURE and `rubric/score` PENDING before merge, so the merge-commit rows are the observed result, not proof of a complete final-head conjunction.
5. Current normative wording (unchanged by this slice):
   * BRD FR-044 (docs/brds/agentic-retrofit-programme-brd.md line 1602): named per-output human review is required except bounded routine resident communication explicitly enabled under RULE-028/FR-061.
   * BRD AC-084: the exception record may identify policy approver/version instead of a reviewer only for communication enabled under RULE-028; it must not fabricate per-message review.
   * BRD RULE-028 (line 1704) and AC-126: exception activates only after OD-53 records authorised approval and a RULE-020 release.
   * BRD OD-53 (line 2171): OPEN. All AI-drafted resident messages stay individually human-approved until activation.
   * PRD lines 110, 966-972 and 1049-1052: per-message review is the current default; the exception is OFF; owner scope direction is not OD-53 activation evidence.
6. Criterion 5 needs an explicit human requirements-owner disposition. No document, merge or check can supply it. The closure audit (2026-10-31) and #726 both say so.
7. ADR: `docs/adrs` holds 0001 to 0006; the proposal stays unregistered with a null ID. The allocator needs a `.adr-config.yml` that does not exist; no bootstrap is supported. Not changed.

## Findings

1. The only unmet criteria are 5 (human gate) and 9 (exact-head evidence). A third full re-verification adds little; the useful new evidence is the observed post-merge hosted result and a one-question owner decision packet.
2. The owner question can be answered in one line: confirm that the wording above makes per-message review normative now with the exception inactive until separate OD-53/RULE-020 approval.

## Follow-ups

1. Requirements owner replies on #441 with the disposition (unblocks criterion 5).
2. If the owner confirms, a later slice records it, ticks criterion 5 and, with an exact-head gate observation on that slice, criterion 9.
3. Register the proposed ADR only after a repository-native allocator path exists (separate decision).
