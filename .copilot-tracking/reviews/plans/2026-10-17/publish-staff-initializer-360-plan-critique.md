<!-- markdownlint-disable-file -->
# RPI Plan Critique: Publish staff initializer #360

## Metadata

* Task ID: 360
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/publish-staff-initializer-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/publish-staff-initializer-360-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one final-candidate critique; no implementation or cloud operations performed.

## Inputs and Criterion Boundary

* Caller requirements: Full ordered RPI with committed artifacts; normal Docker only; conditional publication and image-only pin through a validated existing private path. No new services, spend, roles, network changes, Tasks/import/pools/VMs, unrelated uploads, secret payloads, private SQL/data, Graph, restart or job execution. Zero new tests, no removals or production changes.
* Supplied plan, phase details and research: .copilot-tracking/plans/2026-10-17/publish-staff-initializer-360-plan.md; .copilot-tracking/details/2026-10-17/publish-staff-initializer-360-phase-details.md; .copilot-tracking/research/2026-10-17/publish-staff-initializer-360-research.md.
* Relevant cited source inspected: infra/cutover-proof.Dockerfile; infra/.dockerignore; infra/README.md:1642-1692,1781-1835; infra/tests/test_container_contract.py; infra/tests/test_staff_azure.py; infra/tests/test_private_cutover_proof.py; infra/tests/test_initialize_workbench_staff.py. Relevant import/main boundaries of the six COPY assets were inspected without executing them.
* Repository context: docs/case_study_48_original.md; relevant context from docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md. Branch inspection confirmed chore/publish-staff-initializer-360 at b15f2f0. Existing untracked planning artifacts were left untouched.
* Decision and dependency boundary: Failed private reachability prevents authenticated registry requests, retained-base pull/build, image smoke, push and pin. P01 supplies offline results and no-write preservation evidence; P02 updates factual documentation, reconciles records and hands off to one independent Review and ordinary topic-branch publication.
* Acceptance boundary: Assess the credibility and safety of that bounded blocked-outcome plan, not successful image delivery, runtime acceptance or #360 d/e completion. Supplied live observations are accepted as dated evidence, not independently repeated.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and actual artifacts | Covered | Research, plan, changes and Review paths are identified; parent owns commit/push/main PR and remote-head verification. |
| Q1, C1-C3, P01-T01 | Partial | Exact infra context, six COPY assets, inherited nonroot behavior, source hashes and source-only caveats are explicit. Existing tests need a safe scratch-path precondition: PC-001. |
| Q2, W2-W4, P01-T02 | Covered | Public 403 is distinguished from authenticated authorization; exact login/data IP probes fail. No permitted private route is demonstrated. |
| Q3, C4, W1, P01-T02 | Covered | No new validated digest means no pin. Manual trigger, original initialize args, identity, registry and complete read-visible configuration remain preserved. |
| Publication and image acceptance | Covered | No substitute base; retained immutable API is not local. Real image import/help, push, digest, pin and pin idempotency remain Not run. |
| No services/spend/IAM/network/workload changes | Covered | Both phases prohibit scope expansion and keep job execution, private data and secret payloads out of scope. |
| Before/after preservation | Covered | In-memory comparison of complete read-visible identity/configuration/template, sanitized output only; comparison is limited to this no-write window. |
| P02-T01, documentation and evidence sufficiency | Covered | Explicitly correct stale Docker wording, preserve historical logs, distinguish IAM activation, record current route failure and leave d/e UNMET. |
| Change budget and validation | Partial | Existing focused modules and zero new tests/removals/code changes are appropriate; scratch placement must be operationalized before running them. |
| Final review and stop boundary | Covered | One post-implementation Review and explicit final stop; any unresolved adverse verdict must remain visible, not become an acceptance claim. |

## Verdict

* Verdict: Revise
* Rationale: The blocked-publication strategy is supported by the supplied evidence and appropriately constrained. One direct execution-safety correction is needed before the existing tests run. No new research cycle, second critique or owner decision is required.
* Severity summary: Critical 0; High 0; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Bind existing test scratch files to an allowed project-local path

* Related IDs: P01-T01; plan Test Ownership and Change Budget; phase-details P01-T01.
* Evidence: infra/tests/test_private_cutover_proof.py uses tempfile.TemporaryDirectory() for fixture persistence; infra/tests/test_initialize_workbench_staff.py also uses tempfile.TemporaryDirectory() for roster fixtures; infra/tests/test_staff_azure.py imports tempfile. The plan permits local temporary files only in session files, but neither candidate artifact specifies an enforced temporary-directory setting for the test process. The active execution constraint requires created files to be project-relative and forbids /tmp, /var/tmp and mktemp.
* Concern: Default Python temporary-directory selection can create files outside the allowed project path. An abstract promise about scratch placement does not ensure the existing unittest runner and its imported tests obey that boundary. A session-files location outside the worktree also does not satisfy the project-relative constraint.
* Impact: The first focused validation can violate the file-operation boundary even though all fixtures are synthetic and all cloud operations remain blocked. This is a runner precondition, not a reason to modify tests or weaken coverage.
* Smallest useful change: In P01-T01, require an explicitly named project-relative scratch directory, resolve its allowed absolute path, and set TMPDIR for the entire fresh Python test process before tempfile is imported. Verify tempfile.gettempdir() resolves to that directory in the same configured runner. Keep fixture payloads uncommitted; remove only that task-owned directory by exact path after the runner exits, including failure handling. Reconcile the plan's session-files-only wording with the active project-relative requirement.
* Action owner: Planning parent; implementation parent executes the corrected runner precondition.
* Exact resolving evidence: Revised plan/details specify the directory, environment binding, preflight assertion and exact-path cleanup. The eventual sanitized changes receipt records the checked scratch location, focused module results and cleanup outcome without fixture payloads. Zero new tests, removals or production changes remain required.
* Decision route: Direct planner correction under existing instructions; no significant or divergent user decision.

## Strengths and Residual Risk

* The plan does not mistake Docker 29.9.0 availability for registry connectivity. Public HTTP403 is not represented as AcrPush denial, and private connection timeouts do not establish authenticated push permission or successful TLS negotiation.
* The private endpoint NIC and DNS agreement supports probing the supplied addresses, not a claim that the host has a working approved private route. Normal TLS and explicit no-proxy probes avoid treating an intermediary response as private-path success.
* Source imports/help and packaging tests are expressly proxies for source contracts only. They cannot prove imports, dependencies, user identity or CLI behavior inside the unavailable retained-base image.
* The original Manual initialize argument is an execution hazard, explicitly contained by prohibiting job start and forbidding argument changes that would manufacture acceptance.
* A no-write before/after comparison is sufficient for this task's preservation claim, but not historic equivalence, secret-payload equality, image-pin idempotency or functional initialization.
* The caller has accepted stopping at a concrete route blocker. Future private publication remains a separate gated continuation using existing authorized facilities; this plan does not authorize route repair.

## Questions or Blocking Evidence Gaps

* No user question is required. The known private-route failure blocks image delivery but does not block the proposed offline/evidence work after PC-001 is corrected.
* Current publisher push authority, new image digest, real image smoke and genuine staff/browser/SQL/AI acceptance remain unproven. They must stay unproven in the handoff, not be inferred from tests or management-plane reads.

## Limitations

* No tests, imports, help commands, Docker operations, authenticated registry operations or Azure reads were executed during this critique. Live endpoint/configuration findings are the caller's supplied observations corroborated by the research narrative, not a new independent receipt.
* No open-ended research, additional publisher inventory or external-source refresh was performed. The historical ACR Tasks example in infra/README.md is not an instruction to run it in this task.
* Assessment covers the supplied final candidate once. Raw secret values, private data and image contents were neither requested nor inspected.
* Only this critique artifact was authored. Existing plan, details, research and state remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct the test scratch-path precondition and matching plan wording, record the disposition, then continue the ordered bounded implementation and single Review without another critique.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/publish-staff-initializer-360-plan.md](.copilot-tracking/plans/2026-10-17/publish-staff-initializer-360-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-17/publish-staff-initializer-360-phase-details.md](.copilot-tracking/details/2026-10-17/publish-staff-initializer-360-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-17/publish-staff-initializer-360-research.md](.copilot-tracking/research/2026-10-17/publish-staff-initializer-360-research.md) | Supplied source and live-evidence synthesis |
| [.copilot-tracking/reviews/plans/2026-10-17/publish-staff-initializer-360-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/publish-staff-initializer-360-plan-critique.md) | Complete single critique and actionable finding set |

## Next Steps

The active planning parent resolves PC-001 directly and records its disposition, then continues the authorized ordered RPI sequence. No second critique, cloud mutation or user response is required by this critique. Image publication and pin remain blocked until the existing private-path gate is genuinely satisfied.
