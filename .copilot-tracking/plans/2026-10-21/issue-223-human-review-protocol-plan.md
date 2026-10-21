<!-- markdownlint-disable-file -->

# Implementation Plan: issue-223-human-review-protocol

Task ID: issue-223-human-review-protocol | Date: 2026-10-21 | Branch: docs/human-review-protocol-223 | Base: 993a7b88c03f5240f1e7a4c7c7afa7c064281622

## Executive Summary

Add one clearly labelled PROPOSED, NOT RUN meaningful-human-review protocol section to src/agents/README.md (the existing evaluation protocol placement, next to the #108 accounting and mirroring the #215 comprehension protocol precedent), index it, and append a log entry. It defines seeded critical-error case classes, controls, automation-bias negative controls, retention fields, OQ-017 reviewer authority evidence, denominators, and full-effort comparator definitions. It executes nothing, approves nothing, and ticks no #223 criterion. #108 (open) and #222 (unapproved manifest) stay explicit dependencies.

Research: .copilot-tracking/research/2026-10-21/issue-223-human-review-protocol-research.md

## User Decisions and Requirements

* Owner comment 2026-10-20 on #126 authorises preparation only; no participants or execution.
* Reuse existing protocol/synthesis placement; no new service, harness, evaluator or runtime code.
* Do not touch #222 manifest/fixture/tests, original case study, memory, PRD/ADR.
* Label thresholds, samples, roles, outcomes PROPOSED/UNFILLED/NOT RUN; no invented reviewers, approvals or participant findings; scripted/role-agent evidence is never human-effectiveness benefit.
* Record dependency on #108 (open) rather than claiming it met; #106 closed (partial delivery only).
* Refs #223 only, no closing keywords; exit at frozen local commit without heavy gate, push or PR.

## Goals

* A reviewable protocol that a later approved evaluation can execute without redefinition.

## Scope and Non-Goals

* Scope: src/agents/README.md section, docs/reference/README.md index row, docs/reference/log.md append.
* Non-goals: code, fixtures, thresholds approval, #222 labels/cohorts, participants, model calls, Azure, PRD edits.

## Functional Requirements

* FR-A Seeded case classes: wrong, stale, unsupported, incomplete, valid-citation-wrong, plus correct controls and unflagged critical field.
* FR-B Negative controls: default-acceptance, citation-validity-only and automation-bias (confident wording, accept-first ordering, correct proposals mixed in).
* FR-C Retention: reviewer, source, reason, disposition, effort, version bindings, hashes.
* FR-D OQ-017 evidence: authority, competence, independence, conflicts, all UNFILLED.
* FR-E Denominators and effort: preparation, checking, correction, re-review, coordination, resident, support versus workflow-only and manual/template and parser/rules alternatives.
* FR-F Blocking and outcome rules: pass/fail/insufficient/not run.

## Non-Functional Requirements

* ASCII, no em dashes, `*` lists, relative links, explicit non-claims; consistent with existing README tone.

## Acceptance Criteria

* H3 section "Meaningful human-review protocol (#223; proposed, Not run)" under the AI evaluation harness H2 (anchor meaningful-human-review-protocol-223-proposed-not-run); a table maps each of the five #223 criteria to protocol parts and states none is met.
* Every number is labelled PROPOSED and every role/sample UNFILLED; outcome NOT RUN.
* Decision rules: an always-accept arm and a citation-validity-only arm must be shown to fail; detection counts only with a source-grounded reason scored against a frozen key; false-block rate and zero-miss sample limits stated.
* One Inspect-form index row with Refs-only non-claim; one `query` log entry; earlier entries unchanged.
* Checks: added-line ASCII/no-em-dash grep, anchor check, git diff review, src/agents unit tests unaffected. Local gate and publication are NOT performed and not satisfied.

## Phase Checklist

* [x] P01 Author protocol section
* [x] P02 Index and log
* [x] P03 Focused validation and commit

## Critique Disposition

Critique (executed once, verdict Revise, 9 findings, all direct planner corrections, no user decision): .copilot-tracking/reviews/2026-10-21/issue-223-human-review-protocol-plan-critique.md. The critique file is unaltered.

| Finding | Disposition | Applied as |
|---|---|---|
| PC-001 traceability/acceptance | Accepted | Criterion-to-section map table; checkable acceptance below |
| PC-002 blocking/pass rules | Accepted | Decision rules: always-accept and citation-only baselines must fail; detection needs source-grounded reason against frozen key |
| PC-003 comparator pairing | Accepted | Pairing, order, clock rules; scenarios from unapproved #222 manifest |
| PC-004 automation bias | Accepted | Arms, prevalence, ordering design |
| PC-005 retention/identity | Accepted | Existing fields versus gaps; identity retention UNFILLED owner/privacy decision |
| PC-006 OQ-017 | Accepted | Role separation, per-class competence |
| PC-007 seeded-defect integrity | Accepted | Frozen key, false-block rate, zero-miss sample limits |
| PC-008 placement/validation | Accepted | H3 under harness, anchor, Inspect row, query log, exact tests, gate-not-performed statement |
| PC-009 closing step | Accepted | This table; fetch origin/main before commit; #108 wording in dependency block |

## Follow-Up Items

* Reviewer identity retention versus anonymous codes: owner/privacy decision UNFILLED. #108 open (PR #405 offline accounting only; no criterion ticked). Fetch origin/main before commit.
* Owner approval of thresholds/samples/panel; OQ-017 holders; #108 closure; #222 manifest publication and approval; consent/accessibility/privacy authorisation; separate finite costed plan; Finance validation; actual execution.
