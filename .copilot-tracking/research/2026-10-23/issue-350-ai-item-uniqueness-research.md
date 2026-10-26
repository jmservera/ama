<!-- markdownlint-disable-file -->
---
title: Issue 350 second correction research
description: Focused offline AI item uniqueness contract investigation
ms.date: 2026-10-23
---

## Research Brief

Investigate duplicate case IDs in `tools/check-demo-feedback.py` against
`priority_items()` and existing offline helpers. Audience: correction implementer
and coordinator. Output mode: convergence, preparing a bounded implementation.
Research is read-only except this evidence and required workflow state.

## Research Parameters

* Posture: focused, selected from the caller's named defect and bounded scope.
* Evidence root: this worktree's `.copilot-tracking/`.
* Initial internal areas: checker, focused tests, runtime contract, component
  commands, previous correction evidence, complete-gate interface.
* External research: none; GitHub read-only metadata is allowed for branch and
  identity verification, not checker execution.
* Criteria: identify exact uniqueness semantics, red/green test path and gate
  requirements without widening offline acceptance.

## Extension Registry and Provenance

* Repository instructions: selected for package layout, privacy-safe identity,
  history preservation, dated evidence and complete gate.
* RPI research/plan/implement/review skills: selected sequentially.
* Research specialists: skipped; one tightly coupled local trace is sufficient.
* Web/design/security assessment skills: not applicable to this backend-only fix.

## User Participation and Direction Controls

The caller explicitly requests the full ordered RPI loop and stop after local
validation. No intake question is necessary. Preserve PR #436 and remote branch;
no push, rewrite, rebase, merge, new PR, PR-body edit or issue-criteria update.
The requested loop is authorized directly, not an inferred mode switch.
Do not add membership/source validation, limits, networking, credentials, writes
or activation to the checker; do not claim deployed, SQL or AI acceptance.
Run exactly one complete gate at committed head against
`140d8f494482c78e84d15f3d46b9223d3c487af0`, with lock timeout 86400.

## Research Questions and Prior Knowledge Gate

* Q1: What exact duplicate-ID rule does runtime enforce?
* Q2: Which existing helpers and package-layout command exercise offline evidence?
* Q3: How can evidence, commit and one complete gate preserve history/lineage?

Starting evidence: supplied reproduction and prior correction at
`a01b36f86e36092cbe4d90a1b9db87a95a34531d`, to be verified from files.
Initial inspection confirms clean worktree, requested branch, exact starting
commit and OPEN PR #436. Prior artifacts will remain unchanged.
Cross-session recent metadata lookup returned no matching rows; canonical local
artifacts and current code are the evidence, not unverified recollection.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline investigation located the existing structural predicate, runtime
validator and focused AiEvidence helpers. Prior correction evidence confirms
70 tests and an external installed-package venv. No independent lane merits
delegation. Reflection: duplicate rejection is absent from the checker;
runtime rejects equal IDs before membership/citation handling. Prior evidence
does not itself establish this correction's red/green result.

#### Wave 2: Deeper

Prioritize exact equality semantics, malformed-input safety and documented
commands. `priority_items` uses set cardinality without normalization. The
checker first validates nonempty string IDs, allowing a safe set comparison
only after its existing predicate succeeds. Actual installed-package baseline:
70 tests pass. Existing helpers reproduce duplicate checker PASS while runtime
returns `(None, 0, "duplicate or unknown case id")`. Reflection: component status
must be asserted directly because overall remains blocked on valid fixtures.
The documented runner does not discover this tools suite; focused execution is
required separately. Existing external venv is usable; no install needed.

#### Wave 3: Contrarian

Challenge whether reuse of the full validator is safer, and whether case or
whitespace normalization belongs in uniqueness. Full-validator reuse would add
excluded membership/source verification and count limits. Runtime compares raw
IDs, not stripped/case-folded values; verify distinct variants next. Existing
malformed-field matrices already exercise unhashable IDs, so set conversion
must remain behind structural validation.
Actual probes: distinct `ZF-1`/`ZF-2` and case variants both yield two runtime
items; a padded ID is not rejected as a duplicate but can be dropped later by
citation resolution (one item retained). Reflection: do not infer normalization
from downstream citation behavior. Raw equality alone is the correction.

#### Parent Synthesis and Re-entry

Accept C1-C5: the supplied gap is reproduced and a shape-guarded set comparison
is sufficient. Reject full-validator reuse and ID normalization: both widen
scope. Defer semantic membership, citation truth and deployed acceptance by
caller constraint. Another cycle is unnecessary: all bounded questions are
answered, contrary probes introduce no material uniqueness uncertainty.

## Evidence Log and Findings

| ID | Finding | Location | Tool / confidence |
| --- | --- | --- | --- |
| C1 | Checker validates item shape but not uniqueness | `tools/check-demo-feedback.py:461-479` | Read and executed helper reproduction / High |
| C2 | Runtime uses raw set cardinality before source membership | `src/core/src/zava_forward/core/ai_tasks.py:134-154` | Read and local equality probes / High |
| C3 | Existing helpers and two-item runtime positive cover component and blocked/not-run boundaries | `tools/test_check_demo_feedback.py:118-177`, `:580-674` | Read and baseline 70-test run / High |
| C4 | Install namespace packages; committed clean head and external receipt required | `src/README.md:29-109` | Read / High |
| C5 | One --all obtains shared lock and automatically verifies; --lock-timeout supported | `tools/rpi-checks.py:1675-1744` | Read / High |

Q1 answered by C1/C2: exact duplicate IDs must fail. Q2 answered by C3/C4:
reuse `AiEvidence`, `ai_record`, `bundle`, `report_for` and installed-package
venv; run `python -B -m unittest tools.test_check_demo_feedback -q` from root.
Q3 answered by C4/C5 and initial Git inspection: preserve previous artifacts,
commit original Review first, run one unique external complete gate, then
explicit official verifier and hash; do not publish.

External Evidence: none.

## Alternatives and Decision State

Selected recommendation: an `elif` after the existing structural predicate,
comparing the set of validated string IDs to item count, appending an explicit
duplicate-ID problem through the existing FAIL mechanism (C1/C2). Add
adjacent/nonadjacent duplicate regressions and retain distinct runtime-shaped
IDs and every offline residual boundary (C3). Confidence: High.

Rejected: call `priority_items` in checker (adds membership/citations/limits);
normalize IDs (changes raw identity); silently deduplicate (would accept invalid
evidence). No new dependency, helper abstraction or checker IO is needed.

## Current Decisions, Risks and Further Research

* Confirmed / user: uniqueness only, complete ordered loop, one fixed-base gate,
  no publication or remote/history mutation.
* Confirmed / evidence C1-C3: shape-guarded raw set comparison; focused tests
  assert `ai_evidence`, not only aggregate status.
* Publication blocker: divergent PR ancestry; coordinator owns resolution.
* Residual: real SQL, AI, deployed, independent coordinator and human acceptance
  remain unestablished. Gate local SQL fixtures are not deployed acceptance.
* No unresolved implementation decision. Further semantic research is excluded;
  lineage investigation is deferred until coordinator action (C4 and caller).

## Planning Readiness

Ready (C1-C5). Research disposition: executed, Complete. All three waves ran
inline; no worker or external research claimed. Research remained source
read-only; only new evidence/state files were written. Planning may proceed
under the explicitly authorized parent full-loop request. Lineage blocks
publication, not this bounded local correction or gate.

## Sources

No external sources used.

## Artifact Self-Check

Brief, posture, controls, provenance, prior knowledge, ordered waves/reflections,
parent dispositions, question-to-evidence mapping, alternatives, decisions,
risks, readiness and continuation checked. No material gap or speculative
customer claim; no secrets recorded. Local probes and baseline are actual
execution, not a documentation-only self-check.
