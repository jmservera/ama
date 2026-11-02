---
title: Issue 441 FR-044/AC-084 owner disposition packet
date: 2026-11-02
status: awaiting requirements-owner decision
---

## Decision needed (one question)

Does the integrated wording below make per-message human review normative now, with any routine resident-message exception inactive until a separate OD-53 and RULE-020 approval?

This is not a request to activate automation, repeat Option B or approve the architecture. Owner: requirements owner (jmservera). Nothing in this packet is a disposition; criterion 5 of #441 stays unmet until the owner replies.

## Current wording on main (evidence, observed 2026-11-02 at 071e132a8)

| Source | Position |
| --- | --- |
| BRD FR-044, `docs/brds/agentic-retrofit-programme-brd.md` line 1602 | Named per-output human review is required, except bounded routine resident communication explicitly enabled under RULE-028/FR-061. |
| BRD AC-084 (same row) | The exception record may name the policy approver/version instead of a reviewer only for communication enabled under RULE-028; it must not fabricate per-message review. |
| BRD RULE-028 and AC-126, line 1704 | Policy gate absent, expired or out of scope means named per-message approval. Activation needs OD-53 approval, scope, expiry, evaluation, monitoring, disable/recovery and a RULE-020 release. |
| BRD OD-53, line 2171 | OPEN. All AI-drafted resident messages stay individually human-approved until explicit activation. |
| PRD lines 110, 966-972, 1049-1052 | Per-message review is the current default; the exception is OFF; owner scope direction is not OD-53 activation evidence. |

## Options

| Option | Reply on #441 | Effect |
| --- | --- | --- |
| A. Confirm | "Confirmed: per-message review is normative now; exception inactive pending OD-53/RULE-020." | A later slice records the disposition and can tick criterion 5. No wording change. |
| B. Change wording | State the wording to change. | A later documentation slice edits BRD/PRD and re-verifies. |
| C. Defer | "Defer." | Criterion 5 stays unmet; #441 stays open. |

No option activates routine automation, selects a provider or approves live release.

## Hosted checks observed on merged heads (criterion 9 evidence, not a closure claim)

| PR | Merge commit | Observed result |
| --- | --- | --- |
| #442 | `df3e9643c` | activation, agent, detection, safe_outputs, record_rubric_score, conclusion and three `changes` runs succeeded. One Dependabot run failed (dependency automation, not a PR gate). |
| #454 | `ffde36315` | activation, pre_activation, rubric_prepare and three `changes` runs succeeded; the rest skipped. |
| #726 | `3466bc933` | activation, pre_activation, rubric_prepare and conclusion succeeded; the rest skipped. The PR-head rollup before merge showed `conclusion` FAILURE and `rubric/score` PENDING. |

These rows show what ran, not an independent exact-head review of the final integrated bytes.

## Verifier re-run

Command: `python3 .copilot-tracking/changes/2026-11-01/issue-441-recheck/verify-441-recheck.py --out .copilot-tracking/changes/2026-11-02/issue-441-owner-disposition/recheck-report.json`, evaluated at head `071e132a8` with a clean tree on 2026-11-02. Report: [recheck-report.json](./recheck-report.json), `overall_ok` true (freshness, custody, registries, policy, formulas, links, adr, log).

## Overlaps and ordering

No open PR touches the BRD, PRD, ADR registry or addendum. Open PRs #763, #761, #758, #746 and #742 touch the shared log or index only; a conflict is a rebase, not a dependency. ADR registration is unchanged: `docs/adrs` holds 0001 to 0006, the proposal ID is null and the allocator prerequisite (`.adr-config.yml`) is absent.

## Still unmet or open

* Criterion 5: owner disposition (this packet).
* Criterion 9: independent exact-head review of the final integrated bytes and a final-head gate conjunction.
* OD-52 to OD-55, BRD Define BLOCKED/quality FAIL, PRD Validate BLOCKED, unregistered ADR: unchanged.
* No live resident acceptance, screen-reader conformance, deployment, spending or final requirements approval is claimed.
