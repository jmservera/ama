---
title: Resident manifest verification correction independent plan critique
description: Single prospective final-candidate assessment for issue 441 correction2
ms.date: 2026-10-24
---

## Metadata

* Task ID: jmservera/ama#441 / resident-portal-requirements-441.
* Critique date: 2026-10-24.
* Plan: .copilot-tracking/plans/2026-10-24/resident-portal-requirements-441-correction2-plan.md.
* Phase details: .copilot-tracking/details/2026-10-24/resident-portal-requirements-441-correction2-phase-details.md.
* Critique execution status: Complete.
* Assessment: One independent pre-implementation final-candidate critique.
* Protocol: Installed rpi-plan-critique skill and its critique template.

## Inputs and Criterion Boundary

The supplied owner direction authorizes assessment and this new artifact only.
It does not authorize implementation, source/test/product/custody/score/state
changes, Git operations, a gate, cloud activity or publication. The later
implementation must preserve the verified bot direct-child history through
the separately authorized fast-forward, not recreate its score bytes.

The following evidence identities are used below. All workspace paths are
plain text, not workspace-root hyperlinks.

* PLAN: .copilot-tracking/plans/2026-10-24/resident-portal-requirements-441-correction2-plan.md.
* DETAILS: .copilot-tracking/details/2026-10-24/resident-portal-requirements-441-correction2-phase-details.md.
* RESEARCH: .copilot-tracking/research/2026-10-24/resident-portal-requirements-441-correction2-research.md.
* PACKAGE: .copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/.
* VALIDATOR: PACKAGE/validate-refinement.py.
* TESTS: PACKAGE/test_validate_refinement.py and PACKAGE/test_validate_integration.py.
* INTEGRATION: PACKAGE/validate-integration.py.
* MAP: PACKAGE/refinement-evidence/source-to-integrated.json.
* ADR-MANIFEST: PACKAGE/refinement-evidence/adr/reconciliation-output-manifest.json.
* PRD-MANIFEST: PACKAGE/refinement-evidence/prd/output-manifest.json.
* ADR-INPUT: PACKAGE/refinement-evidence/adr/reconciliation-input-manifest.json.
* BOUNDARY: PACKAGE/refinement-evidence/adr/capstone-review-boundary.md.
* EVIDENCE-README: PACKAGE/refinement-evidence/README.md.
* Supplied native-session evidence: files/441-correction2-reproduce.py,
  files/441-correction2-reproduction.log and
  files/441-correction2-reproduction-report.json, read from the caller-specified
  session 59f31558-980b-475c-b2e2-3b8d68279ed9. These are external session
  artifacts, not repository paths or committed evidence.

The original case study, relevant addendum context, knowledge-base index and
owner memory were also read. They do not turn this validator correction into
product delivery or requirements acceptance.

The assessment covers the proposed normalization/verification contract,
actual caller regression, selected-source exceptions, test budget, sequencing,
preservation boundaries and stop/handoff controls. It assesses planning
credibility, not implemented correctness, current remote ancestry, quality
approval, acceptance, registration or publication readiness.

## Coverage Assessment

* RESEARCH C1 / AC1: Covered. Existing main skips ADR comparisons because
  string membership is applied to a list of objects. Supplied script, log and
  report demonstrate actual-main acceptance after a reversible in-memory
  source mutation.
* RESEARCH C2-C3 / P01-T02: Covered. ADR-MANIFEST contains ten path objects;
  PRD-MANIFEST contains eighteen path-keyed objects. Explicit normalization of
  both real contracts addresses the observed mismatch without changing
  immutable inventories.
* Functional requirements / P01-T02: Covered. Nonempty inventory,
  entry/path/hash/byte shape, duplicate list paths and explicit contextual
  ValueError are required. Missing fields cannot silently become an empty
  inventory.
* Selected-source hash and size / AC3-AC4: Covered. Production verification
  must compare selected reconstructed source SHA and byte length. Existing
  reverse/forward mapping and fixed pins remain separate checks.
* Exceptions / P01-T02: Covered. Read-only inventory comparison confirms
  exactly the three named absent selections. Exception paths must be compared
  normally if listed; unknown selected omissions fail.
* Actual caller / P01-T03 / AC3: Covered. Regression must use actual main,
  actual pinned ADR inventory and the research mutation. It must first prove
  reversible reconstruction and then assert the contextual manifest failure
  before lint, not a downstream proxy.
* Existing behavior / AC4: Covered. Eight integration methods and two
  refinement methods exist. Retaining all ten and adding at most five methods
  with subtests is adequate for the bounded matrix.
* P01-T01 / AC2: Covered. Critique precedes implementation and bot
  fast-forward. Parent must recheck exact refs, parentage and score-only diff;
  changed refs require stopping, not alternate history operations.
* P01-T03 / AC5: Covered. Both existing validators, focused tests, new-artifact
  lint/links and preservation checks are specified. Archived whitespace
  failures remain explicit rather than repaired or relabelled.
* P02-T01 / AC6-AC7: Covered. One genuine later Review follows reconciled
  implementation evidence. A remaining defect triggers stop/report, not
  another correction/review cycle.
* P02-T02 / AC6: Covered. Narrow commit scope, safe identity/trailer, clean
  postcommit external handoff and no preclaimed commit completion are
  explicit. No gate or publication is authorized here.
* Product and adverse-evidence boundaries: Covered. Historical receipts,
  PRD quality failure, unsigned/deferred status, unrun criteria and score
  residuals are not upgraded by this correction.

## Verdict

* Verdict: Pass.
* Rationale: The plan directly addresses the reproduced actual-caller defect
  with a small task-local correction, explicit fail-closed inventory handling
  and production-path regression evidence. The three exceptions match actual
  selected inventory gaps and are narrowly qualified rather than blanket
  bypasses. Scope, test budget, ordered execution and retry cap are credible.
* Severity counts: Critical 0, High 0, Medium 0, Low 0.

## Findings

The complete actionable PC finding set for this supplied boundary is empty.
No substantive plan revision or unresolved significant/divergent user decision
is identified. No PC identifier is assigned to a cosmetic preference or to a
future implementation check already required by the plan.

## Strengths and Residual Risk

* Evidence is stronger than an isolated membership demonstration: the supplied
  reproduction mutates adr/requirement-map-reconciled.json in memory, retains
  unchanged integrated bytes and passes source_bytes() before actual main
  incorrectly emits PASS. The logged alternative source hash
  efefeea626725b54b165abaf9beb5d1af9c5bb6f6ed79234bc56b525664f4aae
  differs from the manifest hash
  72ba21d6ab350a8544603e327ea1c297a133198e6be36e7d417f40501cc697b8.
* Read-only inspection confirms eighteen selected mapping records. Every
  selected inventoried record's declared source hash and size currently match
  its manifest entry. This metadata comparison is not a fresh execution of
  source reconstruction or either validator.
* The exact absent selected paths are prd/output-manifest.json,
  adr/reconciliation-output-manifest.json and
  adr/capstone-review-boundary.md. The manifests explicitly exclude themselves.
  ADR-MANIFEST covers new reconciled outputs only; ADR-INPUT separately records
  the legacy capstone boundary at 4118 bytes with source hash
  aef30bfac121b652ab4934485365209f6c21b728ccdfb3818dd5a7532f96368d,
  matching MAP. The proposed exception does not falsely authenticate that
  legacy output through the new reconciled-output inventory.
* Duplicate source selections for integrated and inert archived copies are
  legitimate. The plan rejects duplicate inventory list paths, not those
  valid selected mapping records.
* The five-method maximum permits coherent helper subtests for real list/dict
  success, malformed inventories/entries, duplicate paths, hash/size mismatch
  and missing-entry/exception boundaries, plus the actual-main regression.
  It does not require a new framework or broad application suite.
* Residual implementation risk remains until the exact helper and main wiring
  are tested and reviewed. Plan Pass is not a prediction that those checks
  have passed. If a defect remains after the single later Review, the owner
  has already selected stop/report rather than another local retry.
* The f902 receipt and prior 97-file PASS remain historical. Current PRD
  quality remains FAIL / Validate BLOCKED with seven findings; all thirty
  resident criteria remain Not run and routine automation remains OFF.
  The ADR remains id:null/unregistered/deferred, A5/B6 remain OPEN and all
  twelve archived FAILED whitespace diagnostics remain adverse history.

## Questions or Blocking Evidence Gaps

* None for the bounded planning decision. No user response is required.
* Current refs and bot ancestry are deliberately not revalidated by this
  critique because Git operations are prohibited. P01-T01 requires that check
  before the later authorized fast-forward and stops if the supplied state
  has changed.

## Limitations

* No implementation was written, no tests or validators were run, and the
  reproduction was inspected rather than re-executed. Its actual main invokes
  Git and writes a report, outside this critique's authorization.
* The only executable inspection used PYTHONDONTWRITEBYTECODE=1 and python3 -B
  to read inventory JSON, compare selected metadata, count existing methods
  and confirm the critique destination was new. It imported no project
  modules and performed no Git or network operation.
* This is a complete assessment of the supplied bounded candidate, not an
  open-ended audit, a new product quality review, a heavy-gate receipt or an
  independent exact-head publication assessment.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this single Pass disposition, then follow the
  already authorized ordered implementation, focused validation and one
  Review. Do not request a second critique merely to repeat this assessment.
* Decision route: Direct parent continuation under existing owner direction;
  no significant/divergent user decision is outstanding.
* User response required: No.

## Existing Artifact References

Assessed final-candidate plan:
.copilot-tracking/plans/2026-10-24/resident-portal-requirements-441-correction2-plan.md

Assessed execution and test boundaries:
.copilot-tracking/details/2026-10-24/resident-portal-requirements-441-correction2-phase-details.md

Prospective research and supplied reproduction provenance:
.copilot-tracking/research/2026-10-24/resident-portal-requirements-441-correction2-research.md

Current caller containing the reproduced bypass:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/validate-refinement.py

Current reconstruction and tampering regressions:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/test_validate_refinement.py

Eight existing scope/baseline regressions:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/test_validate_integration.py

Selected source and derivative mapping:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/refinement-evidence/source-to-integrated.json

Actual list-shaped reconciled ADR inventory:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/refinement-evidence/adr/reconciliation-output-manifest.json

Actual dictionary-shaped PRD inventory:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/refinement-evidence/prd/output-manifest.json

Legacy capstone source identity:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/refinement-evidence/adr/reconciliation-input-manifest.json

## Next Steps

Return Complete / Pass to the active planning parent. No user action is
required. This critic stops after writing and checking this artifact; no
implementation, peer stage, Git operation or publication is performed.
