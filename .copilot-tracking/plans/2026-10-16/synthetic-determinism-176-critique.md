---
title: Issue 176 final-candidate plan critique
description: One bounded assessment of offline fabric provenance and acceptance delivery
ms.date: 2026-10-16
---

## Metadata

* Task ID: #176, synthetic-determinism-176.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/synthetic-determinism-176-plan.md.
* Phase details: .copilot-tracking/details/2026-10-16/synthetic-determinism-176-phase-details.md.
* Research: .copilot-tracking/research/2026-10-16/synthetic-determinism-176-research.md.
* Critique execution status: Complete.
* Assessment count: one final-candidate critique; no further critique requested.

## Inputs and Criterion Boundary

The controlling brief requests end-to-end offline delivery, with explicit unmet
acceptance rather than invented satisfaction. Executable edits belong only in
src/ or infra/. The locked implementation is the existing stock_fabric CLI
and its existing test file, with no removals, new production/test files,
dependencies, or more than two added test methods. Related documentation
and delivery artifacts remain in scope.

No mvp/prototype edits, Azure calls, private datasets, properwarm.json,
.env/.vscode/setup-entra changes, issue mutation, or implementation execution
are authorized by this critique. Existing support regressions may be read
and later executed through the selected core tests; that does not authorize
editing support executables or presenting them as a recovered stock generator.

Evidence read:

* The supplied plan, phase details and research, including C1-C7.
* src/core/src/zava_forward/core/synthetic/stock_fabric.py.
* src/core/src/zava_forward/core/synthetic/provenance.py.
* src/core/tests/test_stock_fabric.py.
* src/core/tests/test_synthetic_determinism.py, relevant byte-level regressions.
* src/core/tests/test_sensor_stock.py, register-backed repeatability coverage.
* src/core/tests/test_generated_dataset.py, fixture-backed builder coverage.
* src/core/pyproject.toml and relevant src/core/README.md validation guidance.
* docs/reference/research/retrofit-synthetic-data/README.md, determinism,
  manifest history, refresh proposal and owner-open-items sections.
* Required project context in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md; only relevant context was used for conclusions.

The assessment covers the supplied three issue criteria, not independently
retrieved issue text. AC1 remains unmet for the original OSM-backed stock
register. AC2 must distinguish newly generated receipts from historical
outputs. AC3 must distinguish the documented proposed policy from actual
human approval and live-reset authority. None is a reason to replace the
missing original generator with a fictional substitute.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Offline delivery and executable scope | Covered | Existing fabric CLI/test only; prohibited resources are unnecessary. |
| C1, C2, C7; AC1 | Covered within declared boundary | Existing fixture and sensor regressions establish conditional byte repeatability, not original register reproduction. |
| C6; original OSM stock gap | Covered | Research and existing synthetic-data README explicitly preserve the absent generator and missing pinned inputs/runtime. No substitute is proposed. |
| C3; P01-T01 exact consumed-input provenance | Partial | Read-once hashing and logical keys are specified, but newline-preserving CSV parsing needs an explicit compatibility oracle; PC-002. |
| P01-T01 strict optional date | Covered in design | Existing provenance.parse_as_of rejects noncanonical calendar-date spelling; omission stays null/unknown and never consults the clock. |
| P01-T02; locked test budget | Partial | Existing tests can host the required coverage without more methods, but mutation and compatibility assertions need sharpening; PC-002. |
| C4; nonempty output refusal | Covered | Existing prepare_output rejects nonempty/direct-symlink destinations, and planned tests expand byte-preservation evidence. |
| P02-T01 validation | Covered as a planned activity | Four named core modules, scoped ruff/mypy and fictional CLI smoke; no execution evidence exists yet. |
| P02-T02; AC2 | Covered | Current receipt fields, historical omissions and unchanged historical outputs are explicitly separated. |
| P02-T02; AC3 and human authority | Covered within declared boundary | Policy remains proposed; owner approval and live-reset authority are not inferred from a refusal test. |
| P02-T03 review and delivery dependency | Partial | Review is scheduled, but disposition language can defer in-scope release-blocking findings without a publication gate; PC-001. |
| Documentation, audit and PR relationship | Covered | Existing related READMEs, reference index, append-only log and Refs #176 PR; no issue checkbox edits or merge. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The scope and acceptance honesty are credible. Two direct,
  bounded planner corrections are needed: make implementation review a real
  delivery gate and make byte-input compatibility/sensitivity evidence
  specific enough to detect a regression introduced by the read-once change.
  Neither requires a divergent user decision, scope expansion, extra test
  methods, dependencies, or another plan-critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Review findings have no explicit blocking disposition before delivery

* Related IDs: P02-T01, P02-T03; end-to-end working delivery requirement.
* Evidence: .copilot-tracking/details/2026-10-16/synthetic-determinism-176-phase-details.md:38-42
  says to record review findings and route later work without another
  implementation/review loop, then commit and publish. The corresponding
  plan task at
  .copilot-tracking/plans/2026-10-16/synthetic-determinism-176-plan.md:71
  combines review, commit and publication without a finding-disposition gate.
* Concern: The text does not distinguish already accepted issue-level gaps
  from newly discovered defects in this change. A correctness, provenance,
  privacy or destructive-write defect could be routed to later work while
  delivery still proceeds as completed.
* Impact: A single review would produce an artifact but not protect the
  promised working offline improvement. The missing original generator and
  unapproved policy are acceptable disclosed gaps; a newly introduced defect
  is not automatically an accepted gap.
* Smallest useful change: Amend P02-T03 to require explicit disposition of
  every review finding before successful delivery. Fix in-scope blocking
  defects within the existing change budget and rerun affected checks,
  without scheduling another independent review or plan critique. If a
  blocker cannot be resolved within scope, mark implementation/delivery
  blocked rather than claiming success; any published draft must explicitly
  retain that blocked status. Only genuinely unrelated follow-ups may be
  deferred without blocking this improvement.
* Action owner: Planning parent, then implementation owner for execution.
* Exact resolving evidence: Revised P02-T03 names the review-disposition
  gate and blocked-delivery branch. At execution, the review/changes record
  maps each finding to its resolution and targeted validation result, or
  an explicit unresolved blocker. The PR completion claim agrees with
  that record and separately preserves the pre-existing AC1/AC3 gaps.
* Decision route: Direct planner correction. No user response is required
  for this gate; an actually necessary scope expansion would be a separate
  divergent decision, not permission to bypass the gate.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Input-reading compatibility and raw-byte sensitivity lack decisive test oracles

* Related IDs: C3; P01-T01, P01-T02; exact consumed-byte hashes, unchanged
  payloads and label-only date requirements.
* Evidence: src/core/src/zava_forward/core/synthetic/stock_fabric.py:340-341
  currently passes an utf-8-sig stream opened with newline="" to
  csv.DictReader. The existing CLI regression in
  src/core/tests/test_stock_fabric.py uses an ordinary ASCII register and
  checks repeatability/output hashes, not BOM or quoted-newline input
  semantics. Phase details:9-20 specifies decoding and general changed-input
  coverage, but does not identify how newline semantics will be preserved
  or which differences must affect metadata rather than payloads.
* Concern: Replacing the stream with decoded bytes can accidentally use
  splitlines or newline normalization. Quoted embedded newlines are valid
  CSV, and the current home-ID validation permits internal newlines; changing
  them can change the seeded draw and identifier bytes. Separately, a test
  that changes parsed records and merely checks that the snapshot differs
  would not prove hashes cover the original bytes, nor that register and
  optional case digests are independent. A date-change inequality alone
  would not prove the date remains only a metadata label.
* Impact: Tests could pass while the new provenance path changes previously
  accepted CSV semantics, hashes a normalized representation instead of the
  consumed bytes, or incorrectly changes payloads on a date-label change.
* Smallest useful change: Specify a newline-preserving text stream over the
  single captured register byte buffer, retaining utf-8-sig decoding and
  existing case utf-8 behavior. Extend the existing CLI test or the already
  budgeted two methods with subtests for:
  * BOM and quoted CRLF input, compared with the existing newline="" parser
    semantics and unchanged fabric/linked payload expectations.
  * Exact SHA-256 of the supplied register and case bytes, with each input
    varied independently. Include a semantically equivalent byte change
    such as CSV BOM/line endings or JSON whitespace, so its digest changes
    while generated payload bytes remain equal.
  * Absent cases, with an explicitly defined absent-input representation
    rather than a fabricated case digest.
  * Date-only changes, asserting the declared as_of changes while every
    non-summary payload remains byte-identical; omission remains null.
  Keep the read-once invariant and verify it by inspection or an in-process
  read spy within the same test-method budget.
* Action owner: Planning parent for the detailed oracle contract;
  implementation owner for the parser and assertions.
* Exact resolving evidence: Revised P01-T01/P01-T02 records the stream
  semantics, absent-case representation and independent byte/date mutation
  oracles. At execution, the existing test file contains those assertions
  with at most two added methods, no removed golden assertions and no new
  files/dependencies; the recorded scoped test run passes.
* Decision route: Direct planner correction. These are preservation and
  provenance requirements already selected by the user, not a new generator
  or a divergent feature decision.

## Strengths and Residual Risk

* The plan refuses to treat missing original stock-generator code as
  discoverable through more fixture testing. Recovered code, pinned OSM
  inputs and runtime remain follow-up prerequisites for original-register
  reproduction, not acceptance earned by this change.
* Keeping fabric(), fabric_rows(), summary() and stock-fabric-v1 stable
  minimizes risk. The CLI summary's source revision will legitimately
  change when its source changes; that is distinct from changing seeded
  fabric row values or the algorithm version.
* Exact input digests support replay verification but do not archive inputs,
  pin arbitrary Python runtimes or authorize access to private sources.
  Replay needs the same input bytes, source dependencies, runtime and seed.
* Existing linked-case behavior retains source case content in the private
  output artifact. The new provenance fields must add only logical input
  names and digests, not paths/content; no fictional or private generated
  output should be committed or uploaded as delivery evidence.
* The documented refusal guard is not atomic concurrent publication,
  rollback on write failure or authority to reset a live database. Those
  existing limitations need not expand this provenance-only task.
* Local tests and smoke remain prospective. Their fixture/output locations
  must satisfy execution-environment controls and the existing CLI
  prohibition on checkout destinations; neither guard should be weakened
  for convenience. Unavailable validation must be reported, not assumed.
* Owner adoption of the refresh proposal and replacement of historical
  manifests remain separate human decisions. Current user direction
  already authorizes disclosing these gaps while delivering the bounded
  improvement; no new policy question is required by this critique.

## Questions or Blocking Evidence Gaps

No decision-critical evidence gap prevents assessing this bounded plan.
The original generator and owner policy approval remain explicitly unmet
issue acceptance, not a Blocked critique or a request to invent substitutes.
The two findings above require direct planner revision, not human answers.

## Limitations

No tests, linters, smoke commands, cloud operations, issue changes, source
edits, commits or publication were performed. This is a plan credibility
assessment, not implementation verification or accessibility, legal,
operational or deployment approval. Issue wording and historical source
availability were assessed from supplied research and cited local evidence;
no independent remote retrieval or open-ended history search was performed.
Existing untracked planning inputs were left untouched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the review-disposition gate to P02-T03 and the
  compatibility/raw-byte test oracles to P01-T01/P01-T02; record both direct
  dispositions and finalize the plan without another critique.
* User response required: No.
* Stop: This critique is complete. Only this critique artifact was written;
  no implementation or peer-stage invocation follows from this assessment.

## Next Steps

The active planning parent should apply the two direct corrections and
finalize its planning handoff. No user action, additional critique, issue
mutation or implementation execution is required from this critique.
