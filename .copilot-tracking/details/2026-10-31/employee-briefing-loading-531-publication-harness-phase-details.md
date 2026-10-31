---
title: Issue 531 publication harness correction details
description: Exact resolving evidence for static output and browser callback failures
ms.date: 2026-10-31
---

## P01: Harness repair

P01-T01: Capture stdout only around the two synthetic Runner.command fixture
calls in test_chat_panel_discovery_skip_is_exact_and_integration_fails_closed.
Assert expected fixture output in capture if useful; keep its retained rows and
failure assertions. Add a single regression running that test in a nested suite,
capture stdout/stderr, then pass combined real suite output to unchanged
gate.check_skips(group="static"); assert one executed test and zero skips.
No real command output is hidden in production.

Fix nine exact B023 sites in case_journey_browser_check.py by binding pending,
loads, reads, change, held and snapshot through keyword-only callback defaults.
Use proper typed keyword-only defaults on named callbacks. No loop body,
request matcher, mock response or test assertion removed. Follow required isolated
100-column formatter for this one directly repaired file; retain the diff evidence.

P01-T02: Run unittest discover -s tools -p test_rpi_checks.py -v and unchanged
skip parser on actual combined transcript; isolated Ruff/format for both changed
files and strict tools mypy plus API harness mypy. No lock for these light checks.
Run case-journey pinned-axe browser under flock -w1800 -E75; one capacity retry.
Use mandatory external scratch and owned-server -B wrapper pattern, extended
only to choose the existing case-journey module. Retain original loading results.
All axe reports/incompletes retained. Actual browser failure requires correction,
not success-shaped retries. No SQL/private data/Azure environment inherited.

P01-T03: One fresh independent reviewer, canonical rpi-review, only original
Review artifact writable. Assess complete new correction source/evidence and
preserved failed receipt, no nested agent or fixes. Route residual findings.

## P02: Publication

Resolve privacy-safe identity/trailer, commit implementation and original evidence.
Fetch current main, merge if drifted under existing authorization and preservation
rules. No workflow/hash edit independently. New full --all gate at exact HEAD,
--jobs 3 --lock-timeout 1800 and new external output; retry once on capacity only.
No failed-receipt resume across source changes. Verify fresh current base and
independent exact-head assessment before non-force push and main PR Refs #531.
Final completion state/receipt/PR accounting external to avoid self-invalidating
post-gate commits. Original specialist/live/contrast follow-ups remain separate.
