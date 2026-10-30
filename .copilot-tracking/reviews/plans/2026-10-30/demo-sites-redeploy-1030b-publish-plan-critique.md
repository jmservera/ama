---
title: Final-candidate critique of authorised demo publishing continuation
ms.date: 2026-10-30
---

## Metadata

* Task ID: f07c3f9e-9452-44e9-95f3-7dff928ba9eb
* Task: demo-sites-redeploy-1030b-publish
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-publish-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one final-candidate assessment of this child.
* Severity counts: Critical 0; High 2; Medium 1; Low 0.

## Inputs and Criterion Boundary

The primary inputs are the supplied child research, plan and phase details,
and the caller's current decisions. Supporting supplied evidence includes
.copilot-tracking/changes/2026-10-30/demo-sites-redeploy-admitted-changes.md,
.copilot-tracking/reviews/logs/2026-10-30/demo-sites-redeploy-1030b-review.md,
src/api/README.md, and the admitted publish.py, sql_init.py, rollout.py and
ops.py at the caller-specified retained executor location. The decoder's import
structure and current parent executor constants/file names were inspected
without reading private backup contents. Repository context documents were
read as required; they do not supply additional operational authority.

Read-only Git inspection confirmed branch chore/ops-redeploy-1030b and local
origin/main a72cb268e11f2fc744d299b2b72bdcb1e05b5d6f. Existing untracked child
planning artifacts were left untouched. No fetch or remote state check was
performed by this critique.

Current decisions supersede the earlier blocked publishing boundary: the owner
selected continuation of RV-001, permits a short ACR public window with VM
egress /32 and exact private restoration on failure, and selected az acr build
as fallback. Existing redeploy authority through November 15 and the accepted
USD337.19/700 admission are not reopened. No additional RBAC, endpoint, other
public-network exception, secret, .env, private dataset read or resource-group
deletion is authorised. AI remains off under the separate generated-prose
activation prerequisites. Eight Manual jobs, four minima zero, old manifests,
auth, protected configuration and revision history must remain protected.

This assessment covers AC1-AC8, P01-P03, dependencies, failure paths,
provenance, restoration and truthful local-only closeout. It assesses whether
the proposed procedure can produce the required operational evidence; it does
not certify a deployment. No cloud, build, browser or model operation was run.
Earlier critique and Review outcomes were read as historical evidence, not
re-executed or reissued.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Research C1-C5 and current owner decisions | Covered | Corrected admitted procedures and current authority are distinguished from earlier failures and independent AI gates. |
| P01-T01 / AC1 | Covered | Exact source/archive/config/OCI-label revalidation is required before reuse; retained ops constants must be adapted as the details already direct. |
| P01-T01 / AC2 | Partial | Registry-chain and old-manifest checks are concrete; cleanup interruption handling and the alternate builder evidence path require PC-002 and PC-003. |
| P02-T01 / AC3 | Covered | Final ledger-aware worker, pinned corrected view, narrow-principal verification, aggregate JSON validation, single execution, post-COMMIT hash binding and full job restoration are specified. |
| P02-T02 / AC4 | Partial | Exact-target acceptance is strong, but the retained executor does not implement the stated timeout/recovery contract; PC-001. |
| P03-T01 / AC5 | Covered | Long warming, anonymous asset/source checks, denials, real fresh-context Playwright and no model submission are explicit. Actual results remain implementation obligations. |
| AC6 | Covered | Full eight-job definition comparison, Manual triggers and four app minima zero are explicit. |
| AC7 | Covered | AI stays off; names-only inventory and remaining activation decisions remain separate from redeploy authority. |
| P03-T02 / AC8 | Covered | One child Review, preserved historical outcomes, privacy-safe local commit, Refs/trailer and no push/publication claim are explicit. |
| Failure dependencies and alternate execution | Partial | SQL and rollout depend on registry/restoration proof; the retained rollout exception paths and fallback proof contract need the corrections below. |
| Source/test scope | Covered | No application source changes, no test removals and maximum test additions zero; actual operational evidence replaces no required remote proof. |

## Verdict

* Verdict: Revise
* Rationale: Authority is sufficiently resolved for the intended publishing
  route, and the acceptance boundary is appropriately constrained. Three
  planner-owned execution gaps remain between the promised safety/evidence
  contract and the retained executors or unspecified fallback. They can be
  corrected without a new owner decision or application/test changes.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The retained rollout does not implement the promised bounded warm-up and failure reconciliation

* Related IDs: P02-T02, AC4, non-functional requirements.
* Evidence: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-publish-phase-details.md:41-48
  promises 180-second health attempts within 900 seconds and verified recovery.
  The supplied admitted rollout.py has a 600-second convergence deadline,
  limits health requests to 30 seconds, and retries only RuntimeError containing
  `exit 28;`. The supplied ops.py translates subprocess timeouts to exit 124.
  rollout.py finish catches only StartupFailure; ordinary timeout, transport,
  assertion and verification exceptions escape that handler. The forward
  template PATCH also occurs before finish enters its recovery handling.
* Concern: Copying and invoking the retained script after only source/root
  adaptation does not produce the plan's stated behavior. A cold timeout 124
  can abandon an already-created target, and an ambiguous accepted PATCH or
  later verification exception can leave changed live state without an
  explicit reconciliation disposition.
* Impact: The task can stop with an unverified forward revision still active,
  or initiate recovery earlier than the expressly selected cold-start budget.
  Neither constitutes the promised delivery or verified restoration.
* Smallest useful change: Specify the external executor adaptations before its
  first invocation: 900-second convergence, up to 180 seconds per health
  attempt clipped to remaining time, and read-only same-target retry for both
  timeout forms. Define reconciliation from the persisted intent for an
  uncertain PATCH result or non-StartupFailure exception. Recover only after
  classifying target state and checking protected/auth drift; stop and report
  unresolved ambiguity if safe recovery cannot be established. Never repeat
  the forward PATCH merely because its response was lost. Keep the original
  retained executor unchanged and hash the adapted execution copy.
* Action owner: Planning parent; implementation owner applies the bounded
  external executor adaptation before rollout.
* Exact resolving evidence: Revised P02-T02 details naming these branches,
  plus the adapted executor hash and a static branch inspection showing the
  intended deadlines, exit28/124 handling, persisted-intent reconciliation and
  verified recovery/error disposition. Actual execution must subsequently
  retain its target/readiness/recovery receipts; no synthetic result may stand
  in for those receipts.
* Decision route: Direct planner correction. No user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: A single cleanup error can terminate restoration while ACR remains public

* Related IDs: P01-T01, AC2, restoration-on-failure requirement.
* Evidence: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-publish-phase-details.md:22-24
  requires public-close-first/finally and exact restoration. In the supplied
  publish.py, the first cleanup az call disables public access. If that call
  raises or times out, the rest of network-rule/policy restoration and readback
  is skipped; only credential removal and signal-handler restoration remain.
  SIGINT/SIGTERM continue to raise during cleanup. The 600-second cleanup
  deadline is measured from the initial opening timer, not cleanup entry.
* Concern: finally guarantees that restoration is attempted, not that a failed
  or ambiguous close is reconciled. One transient command failure or a second
  handled signal can leave the public window open without a bounded retry and
  explicit restoration-failure handoff. The plan does not expose this gap or
  reconcile the deadline semantics.
* Impact: The owner's deliberately short public exception can outlive the
  forward operation. Successful credential deletion cannot prove the registry
  is private or its owned policy deltas have been removed.
* Smallest useful change: Add a bounded restoration state machine to the
  external execution copy: defer repeat handled termination signals during
  cleanup; read back an ambiguous close and retry the idempotent public-disable
  operation while within the cleanup budget; after confirmed closure restore
  only owned rules/policies with existing drift guards and exact final
  comparison. Define whether 600 seconds bounds total elapsed time or cleanup
  time and enforce that choice consistently. If control-plane unavailability
  prevents confirmation, persist a sanitized explicit restoration-failed
  disposition, stop all forward work and immediately notify the parent for
  closure/escalation. Do not promise guaranteed restoration under arbitrary
  control-plane failure.
* Action owner: Planning parent and operational implementation owner.
* Exact resolving evidence: Revised P01-T01 cleanup/failure instructions and
  adapted publisher hash/static inspection covering close-timeout readback,
  bounded retry, repeat-signal handling, deadline semantics and unresolved
  closure reporting. During implementation, require actual publicDisabled
  readback followed by full stable ACR equality before declaring AC2 met.
* Decision route: Direct planner correction within the already-authorised
  exception. No broader network permission or new user decision is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The selected remote-build fallback has no equivalent provenance or admission recipe

* Related IDs: P01-T01, AC1, AC2, research synthesis fallback.
* Evidence: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-publish-phase-details.md:25-26
  says to assess az acr build if unavailable, but specifies no source/context,
  Dockerfile, labels, tags, build receipt or failure path. The supplied
  publish.py instead requires a remote config digest equal to each retained
  local build's config digest and an inspected local RepoDigest for the pushed
  tag.
* Concern: An independent remote build need not reproduce the local config
  digest even from identical source. The direct-push proof cannot simply be
  reused for that different artifact, and a VM-only firewall does not itself
  prove a hosted build can publish under existing ACR restrictions. Neither
  feasibility nor equivalent evidence is established by authorisation alone.
* Impact: The fallback is not implementation-ready. It could either fail
  unnecessarily on a local-config equality assertion or produce images without
  the source/config chain required for rollout. Opening broader access to make
  it work would exceed the supplied boundary.
* Smallest useful change: Add a conditional fallback substep after confirmed
  exact restoration of the first attempt. Specify use of only the pinned
  tracked-source archive and src image context, the two pinned Dockerfiles and
  revision labels, unique tags, existing identity/network/cost constraints,
  bounded build status handling, old-manifest preservation, and exact cleanup.
  Distinguish retained-local-build proof from newly built remote artifact
  proof; derive rollout digests only from verified remote manifest/platform/
  config/label chains bound to the exact submitted source and build receipt.
  If the fallback cannot operate with existing permissions/network policies,
  stop and report blocked rather than create infrastructure, broaden access
  or infer permission.
* Action owner: Planning parent; implementation owner performs any subsequently
  authorised operational checks.
* Exact resolving evidence: Revised P01-T01 fallback recipe and explicit
  AC1/AC2 evidence mapping for the alternate artifact, including source archive
  hash, exact build submission and terminal receipt, remote chain verification,
  preservation/restoration gates and a fail-closed unavailable disposition.
  No live fallback build is required to resolve the planning omission.
* Decision route: Direct planner correction. A new owner decision is needed
  only later if feasibility requires something outside current authority;
  that expansion is not recommended or authorised here.

## Strengths and Residual Risk

* The main source pin, existing build reuse and remote manifest/config checks
  avoid equating a tag or old healthy endpoint with delivered current source.
* Ledger-generated columns and valid projected sensor arrays are explicitly
  checked; historical failed SQL hypotheses are not reused as the final worker.
  Preserve the required sql_diagnose.py decoder dependency when copying the
  admitted SQL executor, without executing its diagnostic entry point.
* Baseline/app/auth/history/job comparisons, immutable image references,
  counts-only SQL evidence and exact-target traffic/readiness checks address
  the important preservation and false-success risks.
* The accepted cost/authority envelope and temporary VM-only ACR exception
  remain accepted residual risks, not reasons to repeat the old blocker.
* AI-off is correct. Missing generated-prose activation authority/accounting/
  managed-identity prerequisites and owner-held authenticated/model acceptance
  do not need to be resolved to redeploy with AI disabled.
* Local evidence commits do not imply issue closure, full publication-gate
  success, remote Git publication, accessibility acceptance or clean consoles.

## Questions or Blocking Evidence Gaps

No unresolved owner choice blocks planner correction of this candidate. Actual
registry availability, live resource drift, SQL outcome and new revision
readiness remain implementation gates rather than facts established here.
If neither authorised publishing route is feasible without expanded authority,
the implementation must stop and return that specific evidence to the parent.

## Limitations

Only the supplied planning boundary and directly supplied supporting evidence
were assessed. Retained scripts were read, not imported or executed. Private
backup contents, credentials, .env files and datasets were not read or printed.
No cloud/build/browser operation or application test was performed. Historical
receipts are not fresh remote evidence. This artifact neither repeats the
parent assessment nor changes its original findings or outcomes.

## Recommended Next Action

* Highest-impact finding: PC-002, preventing an unconfirmed public ACR state
  after cleanup failure.
* Action owner: Planning parent.
* Smallest next action: Incorporate PC-001 through PC-003 into the child plan
  and phase details, then bind the necessary external executor adaptations to
  hashes before implementation.
* User response required: No.
* Assessment disposition: This complete finding set is returned once. The
  planning parent owns direct revision/finalisation without another critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/demo-sites-redeploy-1030b-publish-research.md](.copilot-tracking/research/2026-10-30/demo-sites-redeploy-1030b-publish-research.md) | Supplied continuation research |
| [.copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan.md](.copilot-tracking/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan.md) | Assessed child plan |
| [.copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-publish-phase-details.md](.copilot-tracking/details/2026-10-30/demo-sites-redeploy-1030b-publish-phase-details.md) | Assessed execution details |
| [.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-1030b-publish-plan-critique.md) | This single final-candidate critique |

## Next Steps

The active planning parent should directly revise and finalise the child
candidate against PC-001 through PC-003, without a second critique. No user
action is required. This critique stops here; it authorises no execution,
source change, commit or push.
