---
title: Issue 350 feedback correction4 plan critique
description: Single preimplementation final-candidate assessment of strict JSON type correction
ms.date: 2026-10-22
execution_status: Complete
verdict: Revise
---

## Metadata

* Task ID: issue-350-demo-feedback-correction4.
* Critique date: 2026-10-22.
* Critique execution status: Complete.
* Timing: preimplementation. HEAD is
  05b5b7d2b754ae0e7134df8db1a867861726a821; the read-only source diff for
  tools/check-demo-feedback.py and tools/test_check_demo_feedback.py was empty.
  The supplied correction4 plan, details, research and state were untracked.
* This is exactly one final-candidate critique, with one complete actionable
  PC finding set. No implementation, tests, lint, caches, gate, network,
  credential, Azure, tenant or live-data operations were performed.

## Inputs and Criterion Boundary

* Plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction4-plan.md.
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction4-phase-details.md.
* Research: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction4-research.md.
* Relevant evidence read: tools/check-demo-feedback.py, account/map checks and
  report aggregation; tools/test_check_demo_feedback.py, runtime-built fixtures,
  JSON serialization helper and focused contract tests;
  src/api/src/zava_forward/api/server.py, tile configuration and /api/me;
  src/api/src/zava_forward/api/auth.py, account providers; and
  tools/rpi-checks.py, clean_identity and gate entry/preflight.
* Required contract: account name/email/provider strings, preserving the
  existing nonempty provider and deployed trusted-proxy restrictions; map
  tiles null-or-string and attribution string. No additional restrictions
  on contents, no coercion, no changes to other checker behavior.
* Required tests: every wrong JSON type for every affected field for both
  staff and contractor, valid null tiles and empty contractor email.
* Publication direction: exactly one unchanged full gate against
  b4d467cad84535ed106cffa1ae9aa303db7bfed2, then commit only after successful
  gate and receipt verification. No early commit, hidden inputs, altered gate,
  fabricated receipt, old-HEAD substitution, push or PR update is authorized.
* Scope excludes new runtime restrictions, live acceptance and remediation of
  prior adverse outcomes. The original issue acceptance remains unmet.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR1, FR2; C1, C2, C5; P01-T01 | Covered | Local string checks for name/email and unchanged provider checks match the supplied boundary. |
| FR3; C1, C3; P01-T01 | Covered | Runtime production tiles can be null with empty attribution; planned guards preserve these values. |
| FR4; P01-T01, P01-T02 | Partial | Explicit failures are planned; regression oracles need the precision in PC-002. |
| Wrong JSON types, both roles; P01-T02 | Covered | Null, arrays, objects, booleans, integers and floats are enumerated, with null excluded only for tiles. |
| Valid strings and null; P01-T02 | Partial | Null tiles and empty contractor email are explicit; PC-002 closes positive-value and status-oracle ambiguity. |
| Cache-free validation; P02-T01 | Partial | Bytecode/cache controls are specified, but scratch paths conflict with the execution boundary: PC-001. |
| Exact-base gate and receipt; C4, B1, P02-T02 | Covered, blocked for publication | clean_identity rejects the actual uncommitted candidate before checks/output creation; the plan correctly prohibits workaround and commit on failure. |
| One Review, no publication/acceptance claims; P03-T01 | Covered | Prior outcomes are preserved and residual work is routed without another correction loop. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* The implementation design is narrowly correct. Revise the prohibited
  validation paths and make the regression oracle explicit before execution.
  The independently acknowledged B1 publication blocker is real and is not
  cured by either planner correction.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned validation uses prohibited scratch locations

* Related IDs: P02-T01, P02-T02, validation lock, B1.
* Evidence: The plan specifies /tmp/fh350-venv and a new /tmp gate output;
  the details repeat the environment path and require external logs.
  tools/test_check_demo_feedback.py:167-171 uses an unqualified
  tempfile.TemporaryDirectory for every report fixture, with further
  unqualified temporary directories in the same module. No explicit safe
  scratch routing is specified. The active execution instructions prohibit
  /tmp, /var/tmp and temporary-directory file operations and require new
  files to be workspace-relative. tools/rpi-checks.py:1709-1720 independently
  requires a new output directory outside the checkout.
* Concern: The validation recipe is not executable within the active file
  boundary. Cache suppression does not redirect fixture JSON writes, and the
  external gate-output requirement cannot silently override that boundary.
* Impact: Following the recipe would violate the execution constraints before
  producing trustworthy validation evidence.
* Smallest useful change: Remove the prohibited location instructions. Specify
  only an execution-permitted interpreter and fixture/log strategy; do not
  assume default tempfile routing is permitted. Record incompatible scratch or
  external-output prerequisites as blockers rather than creating forbidden
  files. Preserve the owner's single-gate mandate and record if even the
  attempt cannot legally be made; do not substitute a gate run or output path.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T01/P02-T02 and validation lock contain
  no prohibited file operations, identify how all fixture/log writes obey the
  active boundary, and explicitly retain any unresolved gate-output constraint
  alongside B1 without claiming gate execution or success.
* Decision route: Direct planner correction to obey existing instructions and
  record blockers. No user response is needed for that correction; any later
  permission change belongs to the owner, not the implementer.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make the field-specific regression oracle explicit

* Related IDs: FR3, FR4, P01-T02, valid-boundary acceptance criteria.
* Evidence: P01-T02 explicitly names null tiles, empty attribution and empty
  account name/email, then says "arbitrary strings" without assigning them to
  each field. It does not explicitly name empty-string tiles or require
  me_contract PASS for each positive mutation. The stated positive assertions
  are overall blocked, acceptance not-accepted and case_write_reload blocked.
  tools/check-demo-feedback.py:527-535 aggregates any BLOCKED result to blocked;
  tools/check-demo-feedback.py:558-560 fixes acceptance to not-accepted.
  Thus those aggregate assertions alone do not establish the positive field
  contract. Negative tests require FAIL, but do not explicitly check the
  promised diagnostic.
* Concern: Tests could omit a legitimate empty-string tiles value, or classify
  a positive mutation as BLOCKED while still satisfying the listed aggregate
  assertions. FAIL-only negative assertions can also miss an unrelated failure
  masking the field under test.
* Impact: The test plan can fail to prove the narrow no-content-restriction
  contract and explicit type-failure requirement despite apparently passing.
* Smallest useful change: Specify per-field positive subtests for both roles:
  empty and nonempty strings for name, email, tiles and attribution; null tiles;
  and nonempty provider behavior under the existing origin restrictions.
  Keep the explicit empty contractor email case. Require me_contract PASS for
  each positive mutation alongside the existing aggregate limitations. For
  every wrong-type mutation require me_contract FAIL with a nonempty
  account/map diagnostic identifying the relevant contract; preserve the
  existing generic provider diagnostic rather than requiring a provider rewrite.
  No string-content policy or new test framework is needed.
* Action owner: Planning parent; primary implementer owns the resulting tests.
* Exact resolving evidence: Revised P01-T02 specifies that matrix and its
  per-check oracles within the existing subtest/test-method budget. Later
  corrected-source evidence must show those assertions pass, but no such
  execution is claimed in this preimplementation critique.
* Decision route: Direct planner correction; no significant or divergent
  decision and no user response required.

## Strengths and Residual Risk

* The provider guard already rejects non-string and empty values; preserving
  it avoids unnecessary contract or trusted-proxy changes.
* Runtime evidence supports null tiles and empty attribution, and proxy account
  fallback supports empty email. Blanket nonempty, URL, email-format or other
  contents restrictions are correctly excluded.
* The invalid-value matrix covers all wrong JSON types for both roles,
  including both booleans and empty/populated collections.
* B1 remains a publication blocker, not a new authorization question for this
  critique: tools/rpi-checks.py:149-175 requires clean committed HEAD, while the
  owner forbids committing before successful gate/receipt. The actual untracked
  correction4 artifacts already prevent that preflight from passing.
* Exactly one attempted gate is not the same as a successful full gate. Any
  preflight refusal must be recorded as such, with no receipt verification if
  no candidate receipt exists, and no commit, push or PR update.

## Questions or Blocking Evidence Gaps

* No additional domain research is needed for the narrow correction.
* Publication remains blocked by B1 and, until corrected or explicitly recorded,
  the file-operation incompatibility in PC-001. Neither authorizes changing
  the owner sequence or running an old committed candidate.

## Limitations

* This is plan/source inspection, not corrected-source validation or a
  postimplementation Review. No source edits for correction4 were present.
* Prior test counts, historical receipts and prior review outcomes were not
  treated as correction4 evidence. The supplied authorization was not fetched.
* Only the requested critique artifact was written; supplied planning sources
  remain unchanged. No tests, gate commands or external actions were run.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Resolve both planner-owned findings directly, retain
  B1 and any still-incompatible file-operation prerequisites as blockers, and
  do not commission another critique.
* User response required: No for the plan corrections. Publication cannot
  proceed under the unchanged conflicting constraints.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction4-plan.md](.copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction4-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction4-phase-details.md](.copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction4-phase-details.md) | Assessed implementation and validation details. |
| [.copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction4-research.md](.copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction4-research.md) | Supplied runtime and gate evidence synthesis. |
| [.copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-correction4-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-correction4-plan-critique.md) | Complete single-pass critique and actionable findings. |

## Next Steps

Planning parent revises directly for PC-001 and PC-002 without another critique.
No user action is required for those revisions. Preserve the publication
blockers, original unmet acceptance, no-early-commit direction and prohibition
on push/PR updates. This critique stops here.
