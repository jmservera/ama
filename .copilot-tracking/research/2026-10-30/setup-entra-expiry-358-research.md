---
title: Setup Entra expiry and secret preservation research
description: Current-source assessment for issue 358 under offline-only constraints
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

Investigate #358 for the coordinator on the explicitly selected branch
`fix/setup-entra-expiry-358`, base
`9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19`.
Output mode: convergence toward the smallest justified in-scope change.
Requested output: dated Research, Plan/details, Implement and Review evidence,
local validation, local commit only. Research writes are restricted to this
research artifact and the workflow state.

## Research Parameters

Focused posture, selected because the issue names an exact script and regressions.
Initial internal areas: `infra/scripts/setup-entra.py`,
`infra/scripts/initialize-api-auth.py`, `infra/tests/test_setup_entra.py`,
`infra/README.md` and prior issue evidence.
External area: GitHub issue and related PR metadata, read-only.
No Azure, deployment, live sign-in, credential files, secrets or push.
No web edits are anticipated; frontend skills are inapplicable.
Resolved evidence root: `.copilot-tracking/`.

## Extension Registry and Provenance

* Selected repository instructions: `.github/copilot-instructions.md`, global
  match; preserve prior evidence and distinguish offline from live acceptance.
* Selected RPI phase skills; independent critique and Review are required.
* Research specialist skipped: a single connected source trace is best handled
  inline. Web/design/security audit skills skipped: no corresponding scoped work.

## User Participation and Research Decisions

The user explicitly requests the full loop in order and supplies the branch,
base, limits and validation. No interactive clarification is available or needed.
Current issue comments say earlier changes already delivered offline criteria;
this is a claim to verify against current source, not a reason to duplicate work.

## Direction Controls

* Implement exactly issue scope; do not introduce unrelated cleanup.
* Preserve historical outcomes; do not equate synthetic evidence with live
  existing-resource/full-setup acceptance.
* Commit locally using `Refs #358`; no remote writes.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Does current coverage reject expired stored credentials? | depth | Open |
| Q2 | Does reconciliation preserve Key Vault URL/identity and app references? | depth | Open |
| Q3 | Is the delegating legacy main retained after merged conflicts? | straightforward | Open |
| Q4 | What acceptance remains possible under the no-Azure boundary? | straightforward | Open |

## Prior Knowledge Gate

`gh issue view 358 --comments` reports #374 and #417 merged, with remaining
populated existing-app/full-setup acceptance unmet. Related #352 and #356 are
merged. Verify source and existing dated evidence before selecting changes.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Issue/PR metadata locates already-merged offline fixes and bounded synthetic
component evidence. Reflection: prioritize current regression tests and the
remaining acceptance boundary, rather than replay the original issue body.

#### Wave 2: Deeper

Inspected the expiry test, mixed inventory cases, preservation failure/retry
tests, production helper and legacy entry point (C1-C5). Reflection: both
expiry boundaries and both generated/legacy names are already exercised;
no missing test or source fix is demonstrated.

#### Wave 3: Contrarian

Challenged the original mutation weakness: seven existing behavioral mutation
cases include bypassing generated expiry and legacy expiry checks (C3).
Challenged synthetic-as-live equivalence against the original independent
Partial / Residual Review and sanitized synthetic summary (C6-C7). The latter
explicitly excludes full `secret_reference` and original populated-app coverage.
Reflection: repeating mocks or manufacturing a new helper would not supply
the only missing acceptance evidence. Current source needs validation, not
speculative modification.

#### Parent Synthesis and Disposition

Accept already-delivered code/coverage subject to fresh local execution.
Reject adding redundant expiry tests or a replacement preservation abstraction.
Defer the actual populated existing-app/full-setup observation: the user
prohibits Azure and credentials. Another cycle cannot resolve that authority
boundary; stop after this complete focused cycle.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/358, retrieved 2026-10-30 | Comments explicitly retain live acceptance gap after #374/#417. |
| W2 | https://github.com/jmservera/ama/pull/352, retrieved 2026-10-30 | Merged, including the legacy initializer and setup tests. |
| W3 | https://github.com/jmservera/ama/pull/356, retrieved 2026-10-30 | Original setup feature merged. |
| C1 | infra/tests/test_setup_entra.py:1435 | Expired credential rotates without removing the old credential. |
| C2 | infra/tests/test_setup_entra.py:1444 | Frozen 2030 clock covers expired, equal-now, missing and future expiry, generated and legacy names, check/dry-run/write. |
| C3 | infra/tests/test_setup_entra.py:2235 | Seven behavioral mutations must fail assertions, including both expiry guards and lost KV metadata. |
| C4 | infra/scripts/setup-entra.py:1402 | Pure reconciliation preserves KV metadata; :1483 filters expiry; :1582 rebuilds configuration with preserved plus new secrets. |
| C5 | infra/scripts/initialize-api-auth.py:178 | main delegates through runpy to setup-entra.py; callback-only Python API remains. |
| C6 | .copilot-tracking/reviews/logs/2026-10-19/live-keyvault-preservation-358-review.md:38 | Original Review execution Partial and outcome Residual work remain historical, not upgraded. |
| C7 | .copilot-tracking/changes/2026-10-19/live-keyvault-preservation-358-synthetic-summary.json:81 | Synthetic summary explicitly excludes original populated deployed-app/full setup acceptance. |
| C8 | infra/tests/test_setup_entra.py:1508 | Mixed inventories preserve exact KV URL/identity, ordinary/empty values, env reference and token-store binding across five response shapes. |
| C9 | infra/README.md:1876 | Current runbook distinguishes no-write preflight, temporary synthetic exercise and remaining literal gap. |

## Findings Mapped to Questions and Evidence

Q1 answered by C1-C3: required test is already present and mutation-sensitive.
Q2 answered locally by C4/C8; actual originally populated target remains
blocked under W1/C6/C7. Q3 answered by C5/W2: merged lineage retains delegation.
Q4 answered by caller limits and C9: perform offline checks and record the
unmet live criterion, without claiming closure.

## Alternatives and Decision State

Select a dated runbook reassessment plus durable RPI/local validation evidence.
Reject duplicate source/test changes because no current defect is demonstrated.
Reject live execution because it violates explicit caller limits.
No current provider/schema or operational acceptance claim is made.

## Risks and Residual Uncertainty

Fresh local validation is pending. Ruff/mypy and application dependencies are
missing in default Python; use a run-owned pip environment after those
observed missing-module results. The shared heavy lock was held at inspection;
honor the caller's explicit `flock -w 600` instruction for admission.
Live acceptance and human/hosted publication review remain unproven.

## Current Decisions

Preserve previous delivery and original evidence; update only the runbook and
dated tracking artifacts. Run local validation; treat failures as observations,
not authority for unrelated cleanup.

## Planning Readiness

Ready for bounded offline reassessment, not for live acceptance.
Research disposition: executed. Self-check: questions mapped to stable evidence;
all three waves completed inline; no delegated researcher or cloud execution.
