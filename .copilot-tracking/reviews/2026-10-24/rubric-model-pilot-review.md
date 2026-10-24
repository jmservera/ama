<!-- markdownlint-disable-file -->
---
title: Rubric Model Pilot Review
description: Local request fulfillment, checks and follow-up boundaries
ms.date: 2026-10-24
---

## Review Metadata

Plan: .copilot-tracking/plans/2026-10-24/rubric-model-pilot-plan.md.
Reviewer: orchestrator local self-review, not independent assessment.
Iteration: one pilot cycle, exactly one inference invocation per model.

## Request Fulfillment

* Approved USD 10 one-run-per-model report-only comparison: Complete.
* Same frozen prompt and evidence, hidden baseline: Complete and checked.
* Model identity, credits, time, validity and full grade comparison: Complete.
* Equivalent scores cheaper and faster: Not demonstrated. Luna changed four
  grades and was slower; Haiku omitted summary. Sonnet is not ground truth.
* Production/remote scoring changes: None. Documentation only outside tracking.

## Local Validation

* analyze completed successfully using frozen production adapter and gate.
* All three exact prompt identities and registered source hashes verified.
* Deck extraction reproduced byte-for-byte from the frozen source PPTX.
* Requested/served model IDs match; accounting status complete; read tool
  whitelist and zero reported file writes confirmed.
* Reported equivalent total USD 0.38631076 is below USD 10; no retry/fallback.
* git diff --check passed; scoring scripts, scores and workflows unchanged.
* ai-tokenomics.md editor diagnostics clean. Index/log have pre-existing
  unrelated Markdown diagnostics; no new ones appear in the changed sections.
* Full local publication gate, independent quality adjudication, hosted MCP
  runtime comparison and invoice reconciliation: Not run; not claimed.

## Evidence and Findings

Machine-readable comparison:
.copilot-tracking/sandbox/2026-10-24/rubric-model-pilot/comparison.json.

Sonnet 61/100, 121.746 seconds, USD 0.240189 equivalent. Haiku invalid,
113.765 seconds, USD 0.11417745 equivalent. Luna 59/100, 155.894 seconds,
USD 0.03194431 equivalent. D1-D3 forced to zero; both accepted calibration
cards are Incomplete. Sonnet/Luna differ on A4, A7, B1, C2. Haiku final
response used prose/fences and omitted required summary; no manual repair.

Raw final JSON is not hosted tool-call transport. Haiku's omitted summary
could be rejected/corrected before append in that runtime. One sample cannot
estimate variance or show stable speed. Source is frozen commit 4ed85ba,
not the owner's subsequently modified live PPTX.

## Discover

1. Test native structured submission with explicit budget before judging
   production output reliability or changing the scorer.
2. Run repeated held-out and threshold-adjacent comparisons with independent
   evidence adjudication; compare full vectors, not total or gate pass alone.
3. Resolve trusted-base deck support separately before hosted rescoring.

## Status

Complete as a bounded local pilot. Retain Sonnet. No publication, model switch,
human acceptance or unexecuted gate is inferred.

## Native MCP Extension Review

Owner approval explicitly added one native invocation each for Haiku/Luna
within the original USD 10. Complete in one extension cycle; no extra Sonnet
run, assessment retry, fallback or live publication. Existing test harness and
exact pinned runtime used without modifications. Seven runtime regressions
pass. Earlier all-skipped attempt was a wrong archive path, corrected before
inference and not counted as validation.

Raw evidence:
.copilot-tracking/sandbox/2026-10-24/rubric-model-pilot/native/comparison.json.
Haiku: one call/append, strict gate valid, 64/100, 111.07 seconds, USD
0.10206125 equivalent. Luna: one call/append, strict gate valid, 56/100,
107.97 seconds, USD 0.01870419 equivalent. Both remain Incomplete. Nine grade
differences; Haiku A5 rationale 303 characters is a retained prompt violation.
Neither needed correction, so model correction behavior was not observed.

Combined equivalent cost USD 0.50707620. Confirmed runtime/input hashes,
actual prompt identity, requested/served model identity, complete accounting,
allowed native/read tools and zero reported file edits. Local append files
are intended writes; no GitHub credentials were passed to the MCP child.
No full hosted workflow, native Sonnet control, repeated quality adjudication,
invoice reconciliation or publication gate is claimed. Concurrent owner live
registry/deck changes are outside this experiment.

Recommendation unchanged: keep Sonnet pinned. Next work should establish
independent criterion-level references and repeated native-path/threshold
comparisons, and separately consider enforcing the rationale-length limit
before append. Do not rank accuracy by total awarded score.
