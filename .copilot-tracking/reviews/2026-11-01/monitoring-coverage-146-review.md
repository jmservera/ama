---
title: Monitoring coverage 146 review (2026-11-01)
ms.date: 2026-11-01
---

## Execution and outcome

Review executed once, self-review of the diff plus focused validation (new tests, ruff check, ruff format --check, mypy, infra workbook test). Outcome: conformant for the slice; whole issue not proven.

## Findings

* No defects open in the slice. Sanitiser is allowlist-based; indicator evaluation has no green state; constructed thresholds are offline-only.
* Residual (routed to later work): no poison-queue or AI-limit producer, no deployed signal/appointments, no source-side redaction wired into platform logs, no cost/usage feed, no automatic incident/suspension wiring, no Azure drill. Hosted CI is the evidence for the wider suite.

## Acceptance criteria

Not ticked: all four infrastructure criteria and RAI/tokenomics rows stay partly unproven. Hence `Refs #146`.

## PR #674 review follow-up

Four Copilot threads were valid and fixed (constructed provenance on blocked results, `OverflowError` on huge integer limits, field-level value schemas in the sanitiser, `rai-harm` in the explicit-gap test). The sanitiser now rejects free-text values instead of trusting allowlisted keys. The `activation` CI failure is a GitHub API quota stop in the AIC cache restore step, not a code failure. A second round fixed five more valid threads: string length is bounded before the sensitive-value regex, timestamps are parsed and impossible dates dropped, unknown register statuses are reported, and `offline_only` provenance survives sanitisation (with regressions). The complete local publication gate (`tools/rpi-checks.py --all` with an external receipt) was not run for this candidate; that is an explicit publication blocker, and hosted CI plus focused checks are not a substitute. The outcome of this review is unchanged, and the findings do not trigger a second Review.
