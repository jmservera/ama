---
title: Issue 358 final-candidate plan critique
description: Single evidence-grounded assessment of the bounded credential-preservation plan
ms.date: 2026-10-17
---

## Metadata

* Task ID: 358
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/entra-credential-preservation-358-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no further critique requested.

## Inputs and Criterion Boundary

* Caller direction: full surgical RPI delivery on
  test/entra-credential-preservation-358, preserving abaca788 and #370 job/CI
  behavior, existing delegating legacy CLI and #360 ownership of broader
  setup/job readiness.
* Supplied research:
  .copilot-tracking/research/2026-10-17/entra-credential-preservation-358-research.md,
  especially C1-C7, W1-W6, selected reconciliation approach and live-proof limits.
* Direct evidence: infra/scripts/setup-entra.py credential selection,
  reconstruction, wait_for, credential-store recording, Azure error handling
  and setup activation ordering; infra/tests/test_setup_entra.py FakeAzure,
  invoke, expiry, failure-recovery, Key Vault and legacy delegation tests.
  Existing infra runbook, cutover acceptance evidence and workflow gate
  references were consulted for scope and validation consistency.
* Requirements assessed: generated and legacy stored expiry; full, sparse and
  omitted KV inventory rows; exact keyVaultUrl/identity and app-value retention;
  env/auth references; safe errors and activation ordering; genuine
  failing-before and expiry/KV/app-value mutation evidence.
* Locked test boundary: existing infra/tests/test_setup_entra.py only, no
  removals, at most ten ordinary new methods and one mutation method, subtests
  permitted, no generated targets, existing legacy test unchanged.
* Delivery boundary: offline implementation and existing gates, dated evidence,
  honest acceptance audit and topic PR. No Azure/Graph operations, secret/private
  dataset reads, role/network changes, image builds, spend or agents were used
  for this critique. No implementation or tests were executed.
* Live criterion: actual non-production preservation is UNMET. Public schema
  inspection is supplied evidence, not an authorized or executed round-trip.
  This accepted limitation does not block assessing the offline candidate.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner branch/base and #370 preservation | Covered | Current branch matches the requested topic; HEAD is abaca78 and the abaca788 ancestor check succeeds. Candidate excludes job/CI edits. |
| Stored generated/legacy expiry; C2/C3; P01-T01 | Covered | Fixed-clock old/exact-boundary/missing/future matrix across check/dry-run/apply; old credential cleanup remains human-owned. |
| Inventory reconstruction; C4/W6; P01-T01/T02 | Covered | Union by name, known KV metadata over resolved values, config-name-only/full-list reference case, ordinary empty/nonempty values, malformed/duplicate/unrecoverable refusal before password creation. |
| App env/auth reference retention; P01-T01 | Covered | Exact PATCH and persisted state, secretRef and tokenStore are named test oracles; unrelated policy changes are excluded. |
| Verification and safe failure; C5; P01-T01/T02 | Partial | Same-run reference verification is explicit; recovery after a persisted mismatch can bypass it on reuse: PC-001. |
| Write-only app values; C4/C5; P01-T01/T02 | Partial | Correct production rule is stated, but the current fake exposes written values on GET; an explicit redacted-readback success case is absent: PC-002. |
| Baseline and mutation evidence; W1; P01-T01; P02-T01 | Covered | Real baseline assertion failures, independent URL/identity mutations, both expiry paths and app-value-loss mutation; errors cannot count as kills. |
| Test ownership and method budget | Covered | One canonical suite, no removals/generated targets; revisions below fit subtests in the existing method budget. |
| Legacy CLI; C1/C7; P01/P02 | Covered | Existing forwarding/return-code regression is retained without a second implementation or competing suite. |
| Existing validation; P02-T01 | Covered | Focused then required-Bicep full infra gates, scoped lint/type/compile and offline Bicep checks; no live commands required. |
| Documentation and acceptance; C6/W1; P02-T02 | Covered | Existing runbook/evidence plus KB index/append-only log; no memory edit, invented live proof or live checkboxes. |
| #360 sequencing and architecture scope | Covered | Narrow shared preservation functions/tests only; no job, crypto, identity or network redesign. |
| Single review and publication; P03-T01 | Partial | All remaining review findings are automatically deferred, without a correctness/safety outcome gate: PC-003. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the reconstruction approach and ordinary regression matrix are
  credible and appropriately bounded. The candidate needs a precise recovery
  contract for failed preservation verification, an explicit realistic
  write-only-readback oracle and a review-outcome publication gate. These are
  planner-owned corrections, not grounds for new research, cloud access,
  another critique or a broader test suite.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: A persisted preservation failure can bypass verification on rerun

* Related IDs: C2/C5; functional reference-verification and safe-error requirements;
  P01-T01; P01-T02.
* Evidence: infra/scripts/setup-entra.py:1242-1252 returns immediately for a
  matching stored generated or legacy credential; infra/scripts/setup-entra.py:1327-1336
  persists the replacement inventory before verification. The proposed phase
  details require retained-reference checking only on that rebuild path and
  explicitly leave failure recovery unchanged at
  .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md:49-52.
  setup calls auth_patch after secret_reference returns.
* Concern: if the replacement is persisted with the new name but an old
  reference is missing or altered, the new check will correctly fail the first
  invocation. On rerun, the valid generated password and its stored name can
  take the early reuse path without the prior retained-reference expectation.
  A readback transport failure also leaves an unverified handoff. The candidate
  does not define how either outcome is reconciled before reuse/activation.
  This is a code-supported recovery gap, not a claim that Azure has exhibited it.
* Impact: a preservation-specific failure may become a later successful auth
  switch even though the failed preservation obligation was never established.
  A stronger same-run predicate alone cannot close that hole.
* Smallest useful change: define a bounded incomplete-handoff policy in
  P01-T02 and test it in P01-T01. An unverified rebuild must remain distinguishable
  from an ordinarily reusable pair until its retained-reference obligation is
  reconciled, or reuse must fail closed with a sanitized human-reconciliation
  handoff. Preserve normal verified-pair reuse and successful interrupted-run
  recovery. Do not solve this by deleting credentials, storing app values in an
  evidence/checkpoint record, silently rolling back, adding permissions or
  changing #360 jobs.
* Action owner: Planning parent, then implementing parent for the narrow
  preservation/reuse path.
* Exact resolving evidence: revised plan/details name the incomplete-handoff
  state and the pre-auth reuse gate; one existing-budget test with subtests
  persists a new pair while omitting an old name or independently altering its
  KV URL/identity, fails the first verification, then invokes setup again and
  proves no auth switch while unresolved. Include a transport-failure then
  verified-readback recovery subcase and a normal verified rerun control.
  Assertions inspect AUTH_URL writes and retained-reference state, not merely
  a printed error or a new credential count.
* Decision route: Direct planner correction. Existing fail-closed and
  preservation direction resolves the safety choice; no user response or live
  permission is required. Keep the mechanism within the narrow workstream.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The success oracle does not explicitly simulate write-only readback

* Related IDs: C4/C5/W6; functional readback requirement; P01-T01/T02; P02-T01.
* Evidence: infra/tests/test_setup_entra.py:187-197 stores the supplied secret
  rows in self.app and returns that same app on ARM_APP GET. Therefore written
  app-local values remain visible to the fake's subsequent GETs.
  .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md:35-38
  specifies list response shapes and failed readback, while lines 49-50 correctly
  state that app values are write-only but do not require a redacted success
  fixture.
* Concern: an implementation that mistakenly compares readback secret values,
  or the whole secret array, can pass a fake that echoes PATCH values and then
  time out against ordinary metadata-only configuration reads. A negative
  missing-reference test does not prove this positive boundary.
* Impact: offline tests could approve a verification predicate that prevents
  otherwise correct rotation on the real service.
* Smallest useful change: explicitly require a scenario-local ARM GET projection
  that omits every app-local value after PATCH while preserving names and KV
  URL/identity. Keep a separate synthetic stored inventory/PATCH capture for
  app-value assertions. Reuse the existing fake with a local response hook or
  projection; do not introduce another suite or globally rewrite #370 behavior.
* Action owner: Planning parent for P01-T01's oracle, implementing parent for
  the fixture and assertions.
* Exact resolving evidence: plan/details specify a positive rotation case with
  empty and nonempty ordinary app values, metadata-only GET readback and full
  retained KV references; it succeeds and activates auth only after reference
  verification. The captured PATCH and synthetic backing store retain exact
  app values, while the GET result demonstrably lacks them. Include this as a
  subcase within the ten-method budget; recorded passing offline evidence does
  not change the UNMET live criterion.
* Decision route: Direct planner correction; no user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Publication is unconditional on the single review's outcome

* Related IDs: P03-T01; full surgical delivery and failure-safety requirements.
* Evidence:
  .copilot-tracking/plans/2026-10-17/entra-credential-preservation-358-plan.md,
  P03-T01 says to route review findings to later work;
  .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md,
  P03-T01 says to route any remaining finding to follow-up and then push/open
  the PR. Neither distinguishes accepted residual limitations from a newly
  found in-scope correctness or secret-preservation defect.
* Concern: performing exactly one review does not establish a passing review
  outcome. As written, even a review finding that refutes preservation or
  failure-before-activation can be deferred while the delivery is reported ready.
  The caller's accepted live-proof limitation is different from such a defect.
* Impact: the full-loop handoff can promote known-broken offline behavior or
  misstate readiness despite the single review detecting the problem.
* Smallest useful change: retain exactly one review and no repeat critique,
  but gate publication/readiness on its outcome. Only explicitly accepted,
  out-of-scope or nonblocking residuals may be deferred. An unresolved
  in-scope correctness/safety defect must leave delivery unready and be reported
  to the parent; do not mandate an unlimited review/fix loop or automatic
  expansion into #360. Any non-ready PR must be clearly identified as such.
* Action owner: Planning parent for P03-T01 and final delivery reporting.
* Exact resolving evidence: revised P03-T01 defines the accepted-residual versus
  blocking-finding disposition, keeps one review, and requires the eventual
  review artifact and PR readiness statement to agree on outstanding findings.
  The separately UNMET live criterion remains explicitly disclosed either way.
* Decision route: Direct planner correction; no new user decision is required
  to avoid claiming readiness with an unresolved correctness defect.

## Strengths and Residual Risk

* Reconciliation is based on available configuration metadata and synthetic
  list values, not on assuming that schema-optional KV fields are always present.
* Duplicate/malformed inventories and missing app values are rejected rather
  than guessed; empty strings remain legitimate values.
* Exact PATCH, stored state, env/auth references, ordering, return codes and
  sanitized output are stronger oracles than implementation-text assertions.
* Both expiry-selection paths and independent KV-field/app-value mutations are
  named, with runner errors explicitly excluded as evidence of a kill.
* Branch, delegate, #370 and #360 boundaries are coherent. No change to broader
  job readiness or cloud/network/identity authority is justified.
* The accepted residual risk is lack of actual service preservation proof.
  That criterion remains UNMET, not waived, and cannot be fixed by stronger fakes
  or public-schema reading.

## Questions or Blocking Evidence Gaps

* None requiring user input for this offline plan. The parent can resolve all
  three findings directly.
* Future live acceptance requires separate authorization and evidence. Do not
  perform permission discovery or cloud experimentation to resolve this critique.

## Limitations

* This assesses the supplied candidate once, not a future implementation.
  No baseline failures, mutation kills, lint/test passes or live behavior were
  reproduced or claimed.
* W1-W6 were considered as supplied research evidence; external issue/PR/schema
  retrieval was not repeated. The direct local trace supports the findings.
* Only this critique artifact was written. Plan, details, research, source,
  tests, existing review records, knowledge-base files and owner memory were
  not changed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: define the failed-verification rerun contract and its
  behavioral subtests, then incorporate PC-002 and PC-003 directly into the
  final plan/details without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-17/entra-credential-preservation-358-plan.md | Assessed final-candidate plan |
| .copilot-tracking/details/2026-10-17/entra-credential-preservation-358-phase-details.md | Assessed phase details |
| .copilot-tracking/research/2026-10-17/entra-credential-preservation-358-research.md | Supplied evidence and accepted live-proof limit |
| .copilot-tracking/reviews/plans/2026-10-17/entra-credential-preservation-358-plan-critique.md | Complete single critique and resolving-evidence requirements |

## Next Steps

Planning parent: disposition PC-001 through PC-003 directly, finalize the bounded
offline plan and continue only after its readiness gate passes. Do not request
or execute another critique. No user action is required; actual non-production
preservation remains UNMET.
