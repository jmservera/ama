---
title: "Issue 86 formal-complaints adapter: review-correction plan"
description: Ordered plan, validation tier and review plan for correcting three Medium contract findings, written before any source edit
ms.date: 2026-11-07
issue: jmservera/ama#86
rpi_phase: plan
task_slug: issue86-formal-complaints-review-corrections
parent_task_slug: issue-86-formal-complaints-adapter
---

Scope: jmservera/ama#86 only, `Refs #86`. Research: `.copilot-tracking/research/2026-11-07/issue-86-formal-complaints-review-corrections-research.md`. Details: `.copilot-tracking/details/2026-11-07/issue-86-formal-complaints-review-corrections-details.md`. Critique: `.copilot-tracking/challenges/2026-11-07/issue-86-formal-complaints-review-corrections-critique.md` (one independent pass, before implementation).

## Objective

Correct the three Medium findings of the independent exact-head functional assessment (`approve_with_comments`, preserved, not a blocking verdict) in the adapter boundary only: bind each send to the exact reservation it committed, record an exception or malformed reply as unconfirmed receipt (never non-receipt) with explicit reconciliation, and require the named independent reviewer's persisted identity continuity including for managers. The shipped receiver stays unconfigured. No real receiver, destination, transport, resident or human approval, legal interpretation, dispatch, #144 permit/worker/consumption change, web change or unrelated interface work.

## Validation tier and rationale

FULL for publication. The change touches adapter receipt persistence, an access boundary (who may forward an independent review) and records exercised against SQL-backed stores. This planning stage runs nothing and admits no gate: #1248 holds the sole nonqueued browser slot. The planning commit and the later source commits change the head, so the FULL r5 receipt for `3445238e` does not cover the corrected candidate. A fresh FULL, independent exact-head assessment, hosted CI and human approvals remain pending and are not claimed.

## Phases

* [x] 1. Research (executed), committed with this plan before any source edit.
* [x] 2. Plan, details and one independent critique (verdict Revise: four Significant, one Minor, all accepted and applied to the plan and details) with dispositions; planning-only commit returned for coordinator inspection. No source or test file is changed in this stage.
* [ ] 3. Implement (only after a later explicit admission): red tests first, then source, in the order below.
* [ ] 4. Focused validation (no heavy service): affected core tests, strict mypy, configured Ruff check and format, own-source import origin.
* [ ] 5. Changes record and separate author Review; routed findings become later work. FULL stays a coordinator handoff.

## Implementation order (all in `src/core`, existing files and patterns)

1. Tests first (RED), added to `JsonResidentDecisions` so the SQL subclass inherits them:
   * Attempt binding: deterministic seam between reservation commit and lookup (critique 2; Event-controlled, timed, released in `finally`). A competing attempt 2 is committed in that gap; assert RED against current code, then that A's outcome lands on attempt 1, attempt 2 stays Pending and A's envelope carries `attempt` 1. A second test: request closed or version changed in the same gap means the receiver is not called and the attempt records a definite `Failed` (not sent) outcome (point-in-time guard only).
   * In-flight: `retry_unresolved` on an attempt this Store instance is sending is refused with a reconcile-later message (the reservation, lookup and registration run under one lock hold, critique 1); after the send finishes the normal Pending rules apply. Per Store instance only, with the limit tested.
   * Ambiguity: a synthetic receiver that records the envelope then raises; a malformed-reply receiver; assert status `Unconfirmed`, reason does not say "not received", receipt fields absent, local request unchanged, identity preserved; ordinary retry refused, `retry_unresolved` accepted and reuses `idempotency_key` with attempt 2; a receiver raising `NotSent` yields `Failed` with ordinary retry still allowed; `Unconfigured` unchanged.
   * Identity: a manager sharing the named reviewer's email with a changed `oid` or `code` is refused and nothing is sent; the genuine reviewer still succeeds; the same manager may still forward a Complaint route (unrelated manager right preserved); an Independent review whose `redress_identity` is missing or Unknown fails closed; existing hold-access and independent-reviewer-exclusion tests stay green.
2. `complaints_route.py`: add `NotSent`, status `Unconfirmed`, replace `FAILURE_REASON` with definite and unconfirmed texts, keep annotations strict.
3. `resident_decisions.py`: reservation identifier, exact-attempt lookup and snapshot guard under one lock, in-flight registry, `Unconfirmed` retry gate, `_send` classification, named-reviewer identity helper.
4. `README.md` (core): formal-route section states the three statuses honestly and the reconciliation rule.
5. Re-run the tests: RED reasons recorded, then green.

## Boundaries and non-goals

* No receiver activation or configuration beyond `unconfigured`; `receiver_from_env` is unchanged.
* No migration or rewrite of persisted records; no web or panels change (verified none renders formal-route status).
* No claim that the in-flight registry prevents cross-process duplicates; receiver-side dedupe, real receiver, web control, two-process proof and whole-issue operational acceptance stay unimplemented and unticked.
* Preserve the R4 adverse receipt, the r5 passed receipt and every original review untouched.

## Review plan

* Author Review after implementation, separate from the independent exact-head assessment, assessing the diff against the three findings, the unchanged-behaviour list above and the validation actually run.
* Record, never fabricate: which tests ran, which SQL-backed variants were skipped without a service, and that FULL, independent, hosted and human gates are pending.
* Do not tick acceptance or review boxes.

## Exit evidence for the later stages

Red-then-green output for the new tests, strict mypy file count, Ruff and format results, import-origin lines, final head/tree, and an ignored-inclusive empty status.

## Amendment 1 (before source edit): legacy `Failed` compatibility

Added after the 8e3ab67 plan commit; no second critique is run for the same objective. Research Amendment 1 gives the reasoning.

* Add RED-first tests: a persisted legacy `Failed` attempt (no `not_sent` marker, old reason text) is refused an ordinary retry with the reconcile message, accepted with `retry_unresolved`, and still refused after a reopened store (JSON reload; SQL variant inherited and skipped without service). A new `NotSent` or snapshot-guard failure carries `not_sent: true` and retries ordinarily.
* Implementation: unresolved set is `Pending`, `Unconfirmed`, and `Failed` without `not_sent: true`. No migration, no rewrite, old reasons kept.
* Validation tier stays FULL for publication; this stage runs only no-service focused checks.
