---
title: Employee password acceptance plan critique
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: employee-password-acceptance-2026-10-30.
* Parent task: authenticated-live-acceptance.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/employee-password-acceptance-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/employee-password-acceptance-phase-details.md.
* Critique execution status: Complete.
* Original verdict: Revise. This is the one independent final-candidate critique, not a second assessment or a revision of the prior task's critique.

## Inputs and Criterion Boundary

* Read the supplied new research, plan and phase details, and the prior original Review only. The skill template was read for the output contract; Git status, branch and upstream were inspected read-only.
* Caller direction controls the assessment: employee-only acceptance for #550/#551/#552 at the named Azure Container Apps URL; supported Entra alternatives/cancellation only; credential access solely inside automation from ~/.ama-test-user, including trimmed first-line handling; no disclosure, video or HAR; exact sanitized offered text and termination if no password route exists.
* No Azure resource, policy, role, roster or private-data changes; no resident retry, push, issue closure, product changes or old-runner execution. Local Refs-only persistence remains authorized.
* Dependencies considered: prior RV-001 missing authenticated proof, RV-002 executed-byte provenance, RV-003 fail-open capture, RV-004 employee route uncertainty, and RV-005 separate resident access.
* Acceptance boundary: AC-01..04; P01-T01/T02 and P02-T01/T02; the prior Review's complete 9/4/6 compound criterion inventory. Employee success cannot prove resident/shared-use obligations or full Fluent/WCAG acceptance.
* The supplied documents do not contain the literal named application URL or test identity. Their correctness cannot be inferred from the phrase "named employee URL." This critique does not retrieve them from another artifact.
* Existing untracked child artifacts are parent-owned. They were not staged, moved, amended or discarded. Only this critique is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| User scope; research C1/C2/W1-W3 | Covered | Separate employee-only child; originals preserved; no diagnosis or repair authority inferred. |
| P01-T01; AC-03 credential routing | Partial | HTTPS/provider guard is required, but exact app/provider binding and configured inputs are absent; PC-001. |
| P01-T01; first-line parsing and redaction | Partial | Formats and constructed tests are named without deterministic ambiguity/failure rules or a concrete adversarial test boundary; PC-002. |
| P01-T02; AC-01 alternatives and stop | Partial | Supported controls and one password submit are explicit, but finite alternatives, timeouts and post-submit failure termination need definition; PC-003. |
| P01-T02; AC-03 synthetic-only capture | Partial | No pre-auth screenshots and masking are good controls; synthetic authorization and safe extraction/crop eligibility are not operationally defined; PC-004. |
| AC-02; P02-T01; 550-01..09, 551-01..04, 552-01..06 | Covered | All compound decisions required; unobserved subparts remain unmet, resident exclusions retained, source-only 551-04 distinguishable. |
| RV-002; AC-03 provenance | Covered with limitation | Exact executed-script/runtime and uniquely named hashed outputs required. Implementation must establish these at execution, not retroactively label current bytes. |
| AC-04; P02-T02 local gate | Partial | Commit/fetch/external gate, missing prerequisites and no-push boundaries exist; exact command, receipt/base checks and invalidation sequence need correction; PC-005. |
| Validation ownership and additions | Covered | No removals; at most one tracking runner and one offline test module; one manifest, sanitized observations and conditional crops. |
| Independent critique/Review | Covered | One critique before implementation, one bounded original Review afterward, no live login or credential reading by either reviewer. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 3; Medium 2; Low 0.
* Rationale: The bounded investigation and honest acceptance decisions are credible, but security-sensitive implementation choices remain implicit. Resolve the five direct planner corrections below before implementation. Missing live evidence is an expected possible outcome, not a reason to broaden authorization.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Authentication is not bound to exact approved targets

* Related IDs: P01-T01, P01-T02, AC-01, AC-03; plan Functional Requirements.
* Evidence: .copilot-tracking/plans/2026-10-30/employee-password-acceptance-plan.md says "named employee URL," "supplied test identity" and "HTTPS provider allowlist." .copilot-tracking/details/2026-10-30/employee-password-acceptance-phase-details.md says "allowed provider field" and "employee callback" without exact target definitions. The supplied research and prior Review do not supply the literal application URL.
* Concern: The runner lacks an explicit source of the approved application origin, employee identity, exact Entra provider hosts and expected return origin. The credential source ~/.ama-test-user appears in the caller requirements but is not bound in the plan/details. An arbitrary HTTPS login-looking page or unrelated authenticated app must not qualify.
* Impact: Credential entry or authenticated evidence could be directed to an unintended target, and otherwise valid observations would not prove acceptance at the named deployment.
* Smallest useful change: Bind the runner to the previously authorized literal application URL and identity using the parent's authoritative user context, and to ~/.ama-test-user without exposing contents. Specify exact HTTPS host/origin comparisons, rejection of lookalikes/userinfo/unexpected ports, and origin validation immediately before username/password entry and after callback. Bind /api/me to that same app origin. Do not invent missing constants or broaden the allowlist on a redirect.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details contain the nonsecret approved app target and exact provider/callback allowlist, or an unambiguous authoritative configuration reference; identity remains non-output runtime input. The one offline module includes accepted target and rejected lookalike/unexpected-origin cases.
* Decision route: Direct planner correction using already supplied owner direction. If authoritative target/identity cannot be recovered, stop execution and report that evidence gap; this critique does not authorize choosing a replacement.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Parser and sanitizer behavior is not sufficiently specified to test failure safety

* Related IDs: P01-T01, AC-03; research C2; plan Validation Ownership.
* Evidence: .copilot-tracking/details/2026-10-30/employee-password-acceptance-phase-details.md permits "JSON/keyed/plain first line," prefers an "unambiguous candidate," and requests scrubbing the exact credential, identity and URLs. The plan names parser/redaction tests but gives no ambiguity, malformed-format or persistence-failure contract.
* Concern: A malformed structured file could silently fall back to treating syntax as a password; multiple keys/lines could select a different candidate; keyed parsing could split password punctuation. Exact-value replacement alone does not define handling of URL-encoded identity/claims, account displays or unsafe exceptions. The no-password stop path must remain safe even if the credential has not been read.
* Impact: A wrong password attempt or secret/identity retention can occur despite passing trivial parser and replacement tests.
* Smallest useful change: Define deterministic format precedence and accepted keys/types, trimmed-first-line behavior including ignored trailing lines, empty/ambiguous/malformed structured-input rejection, and no retry with alternate candidates. Define text sanitization before any persistence, preserving nonsecret wording/line order with explicit replacement markers. Do not extract input values or raw exceptions. If text cannot be safely sanitized, retain only a categorized capture failure and mark the exact-text obligation unmet rather than persisting raw text.
* Action owner: Planning parent.
* Exact resolving evidence: A concrete parser/sanitizer contract in P01-T01 and planned constructed tests for whitespace/CRLF, trailing lines, punctuation, supported structured values, malformed/ambiguous/empty inputs, identity/URL variants, exception paths and zero unsafe output. Tests use sentinels only and never read ~/.ama-test-user.
* Decision route: Direct planner correction. No new credential format or user decision is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The supported-route investigation has no finite transition and failure budget

* Related IDs: P01-T02, AC-01; caller stop condition.
* Evidence: .copilot-tracking/details/2026-10-30/employee-password-acceptance-phase-details.md says "after ordinary alternatives" and "after each supported transition," permits Escape for a native passkey prompt, and limits password submission to once.
* Concern: No visited-state/repetition limit, transition budget or timeout bounds "ordinary alternatives." Post-submit rejection, MFA/passkey re-entry, unexpected redirect and unverified callback/binding also lack an explicit terminal outcome. Generic exception handling could accidentally continue into observation or another authentication attempt.
* Impact: A nominally bounded attempt can cycle through prompts, retry authentication or continue live work after its authority/evidence boundary is exhausted.
* Smallest useful change: Define a small finite state/transition budget with timeouts, permitted visible alternatives and one visit per repeated state. Treat unsupported routes, exhausted alternatives/timeouts and authentication failure as terminal; capture safely available exact offered text and sanitized controls once, then close context/browser. Distinguish no password route, password rejected, callback/binding unconfirmed and UI unavailable. Never navigate to other app pages after the no-route outcome.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T02 states terminal outcomes and finite budgets; the offline module exercises cyclic/no-route, timeout, rejection and successful-return branches, proving no second password submission or post-stop live action.
* Decision route: Direct planner correction, implementing the existing stop requirement.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Successful authentication alone does not authorize retaining record text or pixels

* Related IDs: P01-T02, AC-03; prior RV-003; plan Functional and Non-Functional Requirements.
* Evidence: .copilot-tracking/plans/2026-10-30/employee-password-acceptance-plan.md permits only "authorized synthetic employee UI" and says to mask inputs/account chrome/private fields if screenshots are needed. Phase details proceed from boolean authentication/binding to chat/map/case observation without defining how synthetic scope is established.
* Concern: Authentication and binding booleans prove neither synthetic-record provenance nor safe capture eligibility. Masking named private fields does not cover unexpected record text, chat responses, tooltips or labels. A screenshot mask also does not sanitize prior whole-panel inner_text extraction.
* Impact: This child could recreate the prior fail-open capture risk after a successful login, retaining private text/pixels while describing them as synthetic.
* Smallest useful change: Require an affirmative authorized-synthetic dataset/case boundary before record-bearing chat/map/case interaction or capture, based on the parent's existing authorized context or safe supported UI evidence, never bulk/private-data inspection. If it cannot be established, stop those observations and mark them unmet. Extract allowlisted controls/booleans/geometry only; prohibit whole authenticated panel/page text dumps. Make screenshots conditional on a specifically scoped, safe crop with explicit masking, with no raw intermediate image. Omit capture when safe scope cannot be guaranteed.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T02 defines synthetic eligibility, safe extraction/crop allowlists and fail-closed outcomes. The offline module covers authenticated-but-unverified/private content, unexpected text and crop failure, demonstrating that no text/image output is persisted on those paths.
* Decision route: Direct planner correction preserving the user's no-private-data boundary. Missing synthetic authorization remains a blocked observation, not permission to change datasets or obtain broader access.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Gate instructions do not define exact-head receipt verification and invalidation

* Related IDs: P02-T02, AC-04; research C3.
* Evidence: .copilot-tracking/details/2026-10-30/employee-password-acceptance-phase-details.md requests a complete external gate and a "verified exact-head receipt" but provides neither gate/verification invocation nor the sequence for a changed fetched base, later artifact write or dirty input. Research records a previous non-ancestor base.
* Concern: A reported attempt is correctly allowed to fail, but a successful result could be incorrectly attributed to the final candidate if Review/disposition/state or source inputs change after execution, or if receipt verification uses a stale main base.
* Impact: Local persistence may be mistaken for a validated candidate despite an invalid receipt. A stale/non-ancestor base cannot be silently repaired under the current no-lineage-change authority.
* Smallest useful change: State the sequence explicitly: finalize original Review/dispositions and task evidence; make the authorized local commit; fetch main and record the reviewed SHA; run python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory>; verify with --verify-receipt <receipt.json> --base <current-origin-main-sha> against the same candidate and inputs. Use only owned approved external paths, not forbidden temporary locations. Record non-ancestor, admission/lock or missing prerequisite failures without repair, queueing, skips or cloud fallback. Any later commit, dirty/untracked/ignored input or relevant source/base/tool/image change invalidates a pass; do not amend merely to include the external receipt.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T02 includes command forms, base/head and clean-input checks, invalidation handling and no-push closeout. Final reporting distinguishes attempted/blocked/failed from verified success and identifies the external receipt without adding it to the validated commit.
* Decision route: Direct planner correction. No publication or lineage repair decision is requested.

## Strengths and Residual Risk

* The plan preserves adverse originals, forbids resident retries and avoids importing the old fail-open runner. This directly respects prior RV-003.
* No password route, failed authentication and unknown roster are not converted into product defects or policy diagnoses.
* Exact executed bytes/runtime and unique output hashes address RV-002 prospectively; they do not repair historical provenance. Bind hashes to the run before subsequent script edits and hash only sanitized retained outputs.
* All nineteen compound criteria are reconciled individually. An employee sub-observation cannot prove a compound employee/resident/shared-use criterion; inherited 551-04 remains source coverage, not a new successful test execution or deployment-parity result.
* Unobserved screen-reader, genuine touch, density baseline, shared rendered-component use and provenance remain unmet. An AI label must be observed on actual content, not inferred from source or a rules-only response.
* Tracking-only ownership, one runner/one offline test module maximum, no removals and no product test expansion are appropriate. The full gate does not grant authorization for additional live credential attempts.
* The live route may still fail after corrections. No owner statement about MFA exclusion or ProgrammeManager role guarantees an offered password path.

## Questions or Blocking Evidence Gaps

* No divergent user decision is identified. The planning parent must bind existing authoritative target/identity and synthetic-scope context; absent evidence blocks the corresponding execution rather than permitting invention or expanded access.
* The unavailable literal application URL prevents this critique from validating that value. It does not prevent assessing the supplied plan's safety and acceptance contracts.

## Limitations

* No credential file was read. No live authentication, browser, network call, Azure operation, dependency installation, test execution, secret scanning or gate execution was performed.
* The prior Review supplies the criterion inventory; issue bodies, implementation/source files, old automation and historical evidence were not independently reopened.
* This is a plan credibility assessment, not an implementation/security audit or a fresh UI/accessibility/conformance review. Passing future offline tests would not itself establish live acceptance.
* Parent-owned untracked files were observed but not changed. The write boundary is this critique only.

## Recommended Next Action

* Highest-impact finding: PC-001, exact target and credential-routing binding.
* Action owner: Planning parent.
* Smallest next action: Dispose PC-001..005 with compatible plan/detail corrections before implementing the single runner and offline module. Preserve this original Revise verdict and route no second critique.
* User response required: No. Use existing authoritative direction; if an input is unavailable, report the specific execution blocker without guessing.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/employee-password-acceptance-research.md](.copilot-tracking/research/2026-10-30/employee-password-acceptance-research.md) | Supplied child research |
| [.copilot-tracking/plans/2026-10-30/employee-password-acceptance-plan.md](.copilot-tracking/plans/2026-10-30/employee-password-acceptance-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/employee-password-acceptance-phase-details.md](.copilot-tracking/details/2026-10-30/employee-password-acceptance-phase-details.md) | Assessed phase details |
| [.copilot-tracking/reviews/logs/2026-10-30/authenticated-live-acceptance-review.md](.copilot-tracking/reviews/logs/2026-10-30/authenticated-live-acceptance-review.md) | Prior original adverse Review and criterion inventory |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-password-acceptance-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-password-acceptance-plan-critique.md) | This original complete critique |

## Next Steps

Return Complete / Revise to the active planning parent. Apply and record the five direct corrections, preserving this original finding set and verdict; finalize without another critique. No user action is required. Do not start live work before disposition, read credentials during critique, delegate, push or expand the approved scope.
