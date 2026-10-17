---
title: Initializer ACR CLI plan critique
description: Independent final-candidate assessment for task 360
ms.date: 2026-10-17
---

## Metadata

* Task ID: 360 / initializer-acr-cli-360
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/initializer-acr-cli-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/initializer-acr-cli-360-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: Actually attempt the existing hosted az acr build route,
  preceded by the retained-base local attempt. Do not infer present capability
  from historical dbb success or VM private-endpoint failure. Preserve the
  seven-file infra context and pinned retained API base. Permit an image-only
  job pin only after actual local image smoke and exact source/digest proof.
* Prohibitions: No infrastructure, pool, network, public-access, bypass or IAM
  changes; no job execution, live SQL/data/Graph operations or API restart.
  Existing four test modules own regressions; removals none, maximum additions
  zero absent a concrete root-defect amendment.
* Planning inputs: The research, plan and phase-details paths supplied by the
  caller, including research C1-C5/W1-W4, all P01/P02 tasks and acceptance
  criteria 1-4.
* Source evidence inspected: infra/cutover-proof.Dockerfile, infra/.dockerignore,
  infra/README.md:1839-1940, infra/tests/test_container_contract.py:1-130,
  infra/tests/test_private_cutover_proof.py:1-140,
  infra/scripts/private-cutover-proof.py:1-100,
  src/api/Dockerfile and src/check-container.py. Focused inspection also covered
  initializer/worker CLI main guards in infra/scripts/.
* Repository context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md:1-90, docs/reference/README.md:1-100 and
  docs/reference/memory.md:1-100. Candidate worktree HEAD is bab4bf3 on
  fix/initializer-acr-cli-360; supplied planning artifacts were already untracked.
* Dependencies and decisions: Local access can block without preventing the
  authorized hosted experiment. Hosted publication alone cannot authorize a pin.
  CLI/ARM update semantics and complete read-visible preservation must be
  established before any conditional update. Human/live acceptance remains
  outside this task.
* Boundary: Planning credibility and safety gates, not execution or acceptance.
  No external research, Azure calls, Docker execution, tests, production actions
  or edits to any supplied input were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner scope and exclusions | Covered | Both planning artifacts preserve the explicit prohibitions; no permission expansion is proposed. |
| C1-C2; seven-file context | Covered | Dockerfile copies five Python scripts and the registration manifest; infra/.dockerignore explicitly allows these six payload files plus the Dockerfile. Native upload allowlist verification is planned. |
| C3-C5; retained base/security | Covered | P01-T01 names the exact retained API digest. No arbitrary cached substitute is allowed. Source API Dockerfile retains pinned upstream base, upgrades and UID/GID 10001. |
| W2-W4; P01-T02; criterion 2 | Covered | Actual az acr build with infra context, relative Dockerfile, unique tag and finite service/client bounds is required, including upload-versus-agent failure reporting. Historical dbb is explicitly not present proof. |
| P01-T01; criterion 1 | Covered | Local retained-base attempt precedes hosted build; imports/help override the entrypoint, fixture smoke stays local and failures are recorded without source-only acceptance. |
| P01-T02/P01-T03; criterion 3 | Partial | PC-001: exact hosted digest, uploaded source and locally smoked image are not explicitly joined by a single mandatory acceptance record. |
| P01-T03; configuration preservation | Covered | Fresh full-response comparison, preservation of complete container/template/configuration/identity, update-contract inspection, drift stop and independent readback are required. No job start is permitted. |
| P02-T01; locked tests | Covered | Exactly the four named existing modules; no removals or new methods absent concrete root-defect amendment. Historical 83 tests are not claimed as a current run. |
| P02-T01; documentation/privacy | Covered | Dated supersession preserves historical observations; KB routing/log updates and sanitized evidence avoid retaining credentials, environment values or raw archives. |
| P02-T02; independent Review | Covered | One later independent full-task Review; bounded root-defect corrections do not authorize repeated Review or invented acceptance. |
| P02-T03; criterion 4 | Covered | Normal topic push/main PR, Refs #360, exact head check, privacy-safe identity and no merge/issue closure. Criteria d/e remain UNMET. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 0; Low 0.
* Rationale: The empirical hosted experiment is credible and appropriately
  bounded. One planner correction must make the conditional pin's exact
  tested-artifact/source identity gate executable rather than implicit.
  This does not block an evidence-only outcome or require broader authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Bind hosted-digest acceptance to the exact locally smoked image and uploaded source

* Related IDs: C1-C2, P01-T01, P01-T02, P01-T03, acceptance criterion 3 and
  the owner's exact source/digest proof requirement.
* Evidence: The plan requires exact digest/source provenance in its summary,
  but criterion 3 separately asks for an output digest and local image gates.
  In phase details, P01-T01 compares copied hashes on the initial local build;
  P01-T02 verifies the upload allowlist/source SHA256 and then says to attempt
  safe actual image pull/validation after hosted success. P01-T03 does not
  explicitly require a matching immutable digest across those separate records.
  infra/cutover-proof.Dockerfile copies six payload files and inherits the
  retained API base; its independently built local image is not automatically
  the same artifact as the hosted output.
* Concern: The candidate does not expressly forbid accepting smoke from the
  initial local build, or a mutable-tag pull, as runtime proof for a different
  hosted digest. Nor does it explicitly require the hosted image's copied
  payload hashes to match the exact seven-file upload manifest. The overall
  intent is correct; the decision-critical linkage remains unspecified.
* Impact: A successful local build and a successful hosted build could each
  pass their separate checks without proving that the precise digest selected
  for the job contains and executes the reviewed source. This could incorrectly
  open the only authorized cloud-mutation gate.
* Smallest useful change: Amend P01-T02/P01-T03 and criterion 3 to require a
  single identity gate: record the exact submitted seven-file path/hash manifest,
  source commit and retained API digest; pull the successful hosted output by
  repository@sha256, verify its local RepoDigest/image identity, compare all six
  copied payload hashes with that submitted manifest, and perform the P01-T01
  UID/import/help/localhost health/protected-denial checks on that same
  digest-addressed image. Pin only that exact digest. Smoke of a separately
  built local image, tag-only identity, missing proof or any mismatch must leave
  the job unchanged. Do not add tests or substitute a new base.
* Action owner: Planning parent.
* Exact resolving evidence: Revised criterion 3 and P01-T02/P01-T03 explicitly
  require the same hosted digest for pull, local smoke/hash proof and conditional
  pin, with a submitted-context manifest and fail-closed outcome. During later
  execution, a sanitized receipt must join run ID, submitted manifest hash,
  source commit, retained base, hosted repository/digest, locally inspected image
  identity, six payload-hash comparisons and actual smoke results; an inaccessible
  image or missing linkage must instead record no pin and unchanged-job evidence.
  Planning resolution requires the amended gate, not cloud execution now.
* Decision route: Direct planner correction. Existing owner direction already
  requires this proof; no significant/divergent user decision is needed.

## Strengths and Residual Risk

* Actual hosted execution, not networking extrapolation, is the selected
  experiment. A local access failure does not erase the authorized hosted step.
* The preserved retained base and narrow native context avoid insecure
  substitutions and unrelated source uploads.
* Source imports and historical successful runs are correctly separated from
  current image runtime evidence.
* Current private-access uncertainty is explicitly accepted as a possible
  evidence-only result, not grounds for network or IAM changes.
* Read-visible configuration comparison cannot attest secret-payload equality;
  research explicitly discloses this limitation and the plan does not authorize
  a secret-payload test.
* No concrete source defect is established by this critique. Existing test
  ownership, no removals and zero-addition ceiling remain unchanged.

## Questions or Blocking Evidence Gaps

* No owner question. Current build/upload/agent/pull capability is intentionally
  unresolved until the later authorized experiment, not a missing prerequisite
  for assessing this plan.
* The update-contract inspection remains a legitimate conditional dependency:
  if preservation cannot be established, the plan already requires no update.

## Limitations

* Azure/CLI/runtime claims in research are supplied evidence, not independently
  rerun results. Historical dbb success is not current build or runtime proof.
* This assessment does not certify secrets, live configuration, deployed
  functionality, tenant acceptance or #360 d/e.
* Exactly one complete finding set is returned for the supplied boundary.
  No further critique pass is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Directly amend the conditional identity gate in the
  existing plan/details, record the disposition, and finalize without another
  critique. Only then proceed under the existing ordered RPI authorization.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/initializer-acr-cli-360-research.md](.copilot-tracking/research/2026-10-17/initializer-acr-cli-360-research.md) | Supplied research and scope decisions |
| [.copilot-tracking/plans/2026-10-17/initializer-acr-cli-360-plan.md](.copilot-tracking/plans/2026-10-17/initializer-acr-cli-360-plan.md) | Candidate plan requiring direct gate correction |
| [.copilot-tracking/details/2026-10-17/initializer-acr-cli-360-phase-details.md](.copilot-tracking/details/2026-10-17/initializer-acr-cli-360-phase-details.md) | Candidate execution gates |
| [.copilot-tracking/reviews/plans/2026-10-17/initializer-acr-cli-360-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/initializer-acr-cli-360-plan-critique.md) | This completed independent critique |

## Next Steps

Planning parent resolves PC-001 directly and finalizes the candidate without
another critique. No user action is required. This critique stops here; it
performs no implementation, cloud action or peer-stage invocation.
