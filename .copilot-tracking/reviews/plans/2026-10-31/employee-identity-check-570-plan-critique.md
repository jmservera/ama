---
title: Employee identity runner final candidate plan critique
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: employee-identity-check-570, issue #570.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/employee-identity-check-570-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/employee-identity-check-570-phase-details.md.
* Critique execution status: Complete.
* Assessment: exactly one final candidate critique; no additional reviewers.

## Inputs and Criterion Boundary

* Caller direction: full ordered Research, Plan, Implement, Review loop; privacy-safe maintained src runner; outside-package regression using actual installed local Chromium; supplied API discovery and Ruff checks; actual employee chat, map filters and case navigation; at most two newly authorized sign-ins; no Azure changes.
* Locked change envelope: one new runner, at most one new test module with six focused tests, no test removals, owning API README documentation, historical evidence unchanged.
* Supplied research: .copilot-tracking/research/2026-10-31/employee-identity-check-570-research.md, Q1-Q3, C1-C6 and W1-W3. Read the pointed helper, HTTP tests, README and historical runner code, plus the pointed synthetic employee browser checks.
* Relevant source: src/api/checks/employee_identity_check.py; src/api/tests/test_employee_identity_check.py; src/api/pyproject.toml; src/api/src/zava_forward/api/web/chat.js; src/README.md; tools/rpi-checks.py.
* Read issue #570 and read-only current branch/PR metadata. Branch fix/employee-identity-check-570 is at 5666bd33; no matching open PR was returned. Existing untracked planning/research/state artifacts belong to the caller and were not moved or edited.
* Independent expected object ID is unavailable after the recorded directory denial. Neither an observed session nor display email can resolve this prerequisite. Current authorization is a new maximum-two-attempt budget; the README's historical consumed slots are not reusable.
* Assessment covers design feasibility, requirements, task/dependency sequencing, acceptance evidence, failure handling, privacy, publication and scope. This is not an implementation audit or live acceptance run. It cannot establish historical raw claims, independent account identity, current live model behavior or a passing local gate.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI, dated original evidence | Partial | Research and Plan exist; implementation/review ordering is credible, but final gate inclusion and exact-head handling need PC-009. |
| Q1, C1-C5, cause and immutable authority | Covered | Existing HTTP regressions and historical display-email check support the contract-level cause, not a recovered historical identity. |
| Q2, W2, independent expected identity | Partial | Correct live blocker, but expectation provenance and authorization preflight need PC-002. |
| Q3, bounded sign-ins | Partial | Per-invocation limit is not a two-attempt campaign limit; PC-001. |
| P01-T01, credential safety and output | Partial | Intent is sound; missing concrete file, diagnostic and cleanup contracts, PC-003/PC-004. |
| P01-T01, origin and identity admission | Partial | Shared predicate is appropriate; executable caller fail-closed contract needs PC-005. |
| P01-T01/P01-T02, finite execution | Partial | Bounded intent lacks operation/deadline enforcement, PC-006. |
| P01-T02, live chat/map/case | Partial | No defined success predicates or result reducer; PC-007. |
| P01-T01, one module/six tests/actual Chromium | Partial | Feasible with composition and six grouped contracts; PC-008. |
| P01-T02/P02-T01, discovery/Ruff/gate | Partial | Commands and required new-test execution must be explicit; PC-009. |
| P02-T01, complete local publication gate | Blocked | Current gate opens a prohibited scratch location; PC-010. |
| API-owned README, historical preservation | Partial | Scope names README, but there is no assigned documentation delivery contract; PC-011. |
| No Azure/UI/mapping/roster change | Covered | Appropriate envelope; obtaining an ID does not authorize role grants or directory configuration changes. |

## Verdict

* Verdict: Revise.
* The maintained runner repair is feasible within the locked additions, and BINDING should remain unchanged. However, the candidate does not yet make its two-attempt limit, capture-free behavior, fail-closed caller admission or live success executable and testable.
* Live acceptance remains Blocked pending independent expected identity. Publication also has an evidenced environment/tool conflict. These are separate from the Complete critique execution and must not be converted to successful checks.
* This is the complete actionable finding set for the supplied boundary. The planning parent should resolve it directly and finalize without another critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: A new output filename permits unlimited newly admitted attempts

* Related IDs: Q3, maximum-two-sign-ins requirement, P01-T01.
* Evidence: plan Functional Requirements promise one password submission per invocation and exclusive new output creation. Phase details require a new external output file. Neither defines a shared authorization-scoped counter. The historical Guard in .copilot-tracking/changes/2026-10-30/live-acceptance-1030c/acceptance.py:145-177 is also path-local, not authority for the new campaign.
* Concern: unique output paths prevent replay of that filename, not a third invocation, concurrent invocations, or reuse after an uncertain/crashed submission.
* Impact: the runner can exceed the expressly authorized two attempts while every invocation obeys its own checks.
* Smallest useful change: define one durable externally stored campaign ledger, fixed to this authorization, with two slots maximum and exclusive reservation before sign-in starts. Persist and fsync submission intent before submitting; treat uncertain submission/crash as consumed, fail closed on ledger errors, and prohibit a reset/new campaign under this authorization. A new result file must not create a new budget. Define conservatively which sign-in actions consume a slot.
* Action owner: planning parent, direct implementation correction.
* Exact resolving evidence: revised ledger/state ordering plus focused subtests proving third invocation and concurrent admission are refused, changed output filename does not reset the budget, and persistence failure or a crash after intent cannot replay a submission. Synthetic tests consume no live slots.
* Decision route: direct planner correction; the caller already decided the budget. No user response is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: GUID shape alone does not establish independent authorized identity

* Related IDs: Q2, W2, mandatory expected IDs, P01-T01/P01-T02.
* Evidence: src/api/checks/employee_identity_check.py validates GUID shape and equality; src/api/README.md:19-24 requires owner/identity-administrator verification before sign-in. The candidate mandates CLI IDs but does not specify their independent evidence or authorization-expiry enforcement.
* Concern: any syntactically valid IDs, including values learned from /me, could be supplied. The plan also lists the January authorization expiry without defining a preflight refusal after expiry or an explicit supplied-evidence route instead of more directory reads.
* Impact: a correct equality check could still authenticate the wrong expected person or run outside the authorization window.
* Smallest useful change: require a preflight record of independent tenant/object provenance and its owner/administrator attestation, held privately outside repository/output; retain only provenance-valid/authorization-valid booleans publicly. Bind it to the authorized test account and current campaign. Validate IDs, evidence availability and expiry before browser, slot reservation and credential access. Accept independently supplied evidence as an alternative to read-only lookup; never inspect a session to fill the gap. Stop on denied alternatives rather than altering directory access.
* Action owner: planning parent for the preflight contract; identity administrator/owner for unavailable independent evidence.
* Exact resolving evidence: revised preflight order and invalid/missing/expired-evidence no-browser/no-credential tests; for live eligibility, private independent expected tenant/object verification predating the attempt, with only its sanitized disposition retained.
* Decision route: direct planner correction and external evidence prerequisite, not a request to reconsider strict identity. No new user policy decision is required; supplying missing independent evidence is required for live execution.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Generic secret-safety intent omits the sensitive process failure boundary

* Related IDs: privacy-safe runner, P01-T01, debug preflight.
* Evidence: the historical password runner's public_state in .copilot-tracking/changes/2026-10-30/employee-password-acceptance/employee_acceptance.py:89-113 retains sanitized body/control text; inspect_employee_shell records BrowserError categories, but its top-level and subprocess behavior cannot be inherited as proof. The new plan forbids raw exceptions/DOM but does not define parser, Playwright driver/browser stdout/stderr or cleanup-error handling.
* Concern: credential parsing errors, argparse rejected values, locator/assertion diagnostics, Playwright protocol debugging and child-process startup/cleanup failures can bypass a boolean result writer. Redacting captured text after the fact is not the required no-capture design.
* Impact: secret, identity, URL, case text or response content can escape even when the normal result is sanitized.
* Smallest useful change: specify a positive allowlist of result fields and fixed failure codes; guard all execution/cleanup boundaries and reject diagnostic environment settings before launching/importing sensitive automation. Disable trace/HAR/video/screenshots, raw console/network/pageerror retention and core dumps; control child diagnostic streams without collecting raw secret-bearing output. In-memory routing may inspect offered controls but must export only fixed categories. Define bounded password-only parsing with fixed errors, not inherited DOM redaction.
* Action owner: planning parent.
* Exact resolving evidence: revised failure/output schema plus synthetic canary subtests covering malformed credential input, credential fill/submission failure, driver failure and cleanup failure; assert absence of raw canaries and encoded variants in stdout/stderr and every owned retained file. Tests must not read the authorized credential file.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: External storage and disposal lack a concrete private file contract

* Related IDs: P01-T01, external output, durable intent, disposable scratch.
* Evidence: details say new external output and owned temporary scratch but specify no ownership/permission/symlink/bounds policy. Historical scripts use tempfile and Path reads; those mechanisms do not by themselves constrain locations or permissions.
* Concern: external does not mean private or safe. A linked/non-regular credential source, unsafe ledger parent, broad output mode or browser profile outside the selected owned directory can expose data or break persistence. Cleanup failure must not erase intent or authorize retry.
* Impact: confidentiality and crash-safe attempt accounting can fail without violating the current prose.
* Smallest useful change: name an owner-controlled non-temporary-root scratch/output contract, private directories/files, regular-file/no-symlink checks and bounded credential reads. Open the credential only after all preflights and shortly before the offered password step. Force browser/driver scratch into the owned directory; prohibit saved sessions/downloads. Close resources in finally, delete only this invocation's disposable scratch and preserve the durable ledger/result. Report cleanup failure using a fixed code.
* Action owner: planning parent.
* Exact resolving evidence: documented paths/modes/open flags and ordering; synthetic unsafe-file/parent and cleanup-failure tests; actual local Chromium leaves no session artifacts outside its selected owned scratch. Inspect only synthetic files, not the live credential.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Admission must be a strict executable caller contract, not result truthiness

* Related IDs: C1/C4, P01-T01, expected-account admission.
* Evidence: BINDING returns a boolean object containing both admission and diagnostic flags. Historical binding_probe in .copilot-tracking/changes/2026-10-30/employee-password-acceptance/employee_acceptance.py:144-160 admits any user-like field. Candidate says only shared BINDING can admit but does not specify how the wrapper validates/consumes its returned result.
* Concern: a truthy result object, missing/malformed projection or displayEmailMatches could accidentally authorize downstream checks. Page origin can change during awaited operations, and an admitted session can be lost during later navigation.
* Impact: the new maintained caller can reintroduce the exact identity defect while importing the correct helper.
* Smallest useful change: define a typed probe that invokes the unchanged BINDING on the exact app origin and admits only a well-formed boolean projection with authenticated strictly true. Do not merge diagnostics into admission. Recheck origin before every credential fill and again before submission, before /me evaluation and after navigation; refuse unexpected destinations/challenges, account-switch controls and session loss without another sign-in. Make all downstream entry points require admission and stop/reprobe fail closed after relevant session/navigation changes.
* Action owner: planning parent.
* Exact resolving evidence: real Chromium expected-rosterless and same-email-wrong-ID runs exercise this wrapper; negative/malformed-result/origin/session-loss subtests show chat/map/case callbacks are never invoked, not merely that a helper returns false.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: A deadline check between transitions is not an enforced execution deadline

* Related IDs: bounded sign-in and /me, P01-T01/P01-T02.
* Evidence: BINDING uses a 120000ms AbortSignal for /me. The historical authenticate loop checks 180 seconds between operations but also performs its own waits. The new details say bound transitions without operation budgets or a caller-level timeout for page.evaluate.
* Concern: navigation, routing, selector waits, warm-up, body processing or a hung browser can overrun the intended total duration. Independent per-operation waits can multiply it.
* Impact: unattended credential-bearing automation can hang, and a retry decision becomes ambiguous.
* Smallest useful change: define finite warm-up/sign-in/probe/observation totals and per-operation timeouts capped by remaining monotonic budget. Specify the caller/process watchdog for unresponsive evaluation/browser shutdown while preserving submission intent. Do not shorten or otherwise edit the shared predicate just to achieve the wrapper budget.
* Action owner: planning parent.
* Exact resolving evidence: concrete timeout table and controlled stalls/timeouts proving bounded exit, fixed failure code, no late downstream admission and no resubmission.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-007 -->
### PC-007 [High]: Observations do not yet define live acceptance or overall failure

* Related IDs: issue #570 third criterion, P01-T02, aggregate results.
* Evidence: phase details promise chat sends, keyboard map filters and case navigation. Historical map_check explicitly routes to #/overview and waits for a corresponding map response. src/api/src/zava_forward/api/web/chat.js:100-111 renders workflow-only/unverified responses as assistant messages, so message presence is not actual-model success.
* Concern: the candidate defines neither required actions/minimum counts nor successful response/UI predicates. It does not explain how false observations, empty filter loops or caught stage errors affect exit status.
* Impact: a visible shell, stale assistant message, selected filter without successful fetch, or empty case list could be reported as live verification.
* Smallest useful change: specify a bounded harmless general-work prompt, successful current send and selected-skill response with no alert, separating workflow-only from actual AI evidence. Navigate explicitly to overview; require at least one offered unselected filter, actual completed matching map request and corresponding selection/data state. Navigate through an actual offered case link and require loaded case content with no workspace/API error. Use no synthetic fulfillment in live mode, no arbitrary case ID and no business record mutation. Define passed/failed/blocked/not-run per stage, all required predicates and a strict reducer: any required unproven stage yields nonzero. Missing prerequisites initialize all live stages Blocked without browser/credential access.
* Action owner: planning parent.
* Exact resolving evidence: revised action/success/result matrix; negative subtests for no reply, HTTP failure, no available filter/case and false booleans; eventual sanitized live results proving each required action under independently verified identity. Report actual-model behavior separately rather than silently requiring or claiming it.
* Decision route: direct planner correction. Broader paid-model or record-changing acceptance would require new authority and is not needed to correct this plan.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: The six-test budget needs an explicit feasible fixture and test allocation

* Related IDs: locked one-module/six-test additions, P01-T01, actual local Chromium.
* Evidence: src/api/tests/test_employee_identity_check.py:72 defines EmployeeIdentityTests with seven inherited-discoverable test methods, actual HTTP payload construction and a Node fetch stub. It has no Chromium caller test.
* Concern: subclassing EmployeeIdentityTests to reuse payload would discover its existing seven methods plus new tests. Reusing only its Node evaluator would not prove the maintained browser caller or real browser HTTP transport.
* Impact: a natural implementation violates the locked limit or substitutes helper-only evidence for the required regression.
* Smallest useful change: specify the new test module path and exactly six named focused contracts: preflight, campaign accounting, secret/file/failure safety, caller fail-closed/deadlines, Chromium expected-rosterless, Chromium same-email-wrong-account. Use subtests where closely related. Reuse existing HTTP fixture through composition/setup helpers, not inheritance from its test class; fulfill constructed /me via actual loopback HTTP with exact trusted-proxy fixtures. Exercise the maintained typed probe and downstream gating in Chromium, with no live credentials or external network. Preserve every existing test.
* Action owner: planning parent.
* Exact resolving evidence: revised six-test inventory and fixture strategy; discovery lists only those six new tests; two required Chromium methods execute using an installed binary and real constructed HTTP responses; no skip counts as their execution.
* Decision route: direct planner correction within the agreed envelope.

<!-- rpi:critique id=PC-009 -->
### PC-009 [Medium]: Validation and exact-head publication do not bind the new regression concretely

* Related IDs: P01-T02/P02-T01, API discovery/Ruff/mypy, full ordered RPI/gate.
* Evidence: src/api/pyproject.toml excludes checks/*.py from configured Ruff formatting, so generic ruff format --check . does not format-check the runner. src/README.md:198-202 permits tracked issue-specific --extra-test selectors. The plan states commands generically and does not select the new regression in the full receipt.
* Concern: standalone browser success can be lost at final candidate publication; an opt-in skip or ordinary format command can appear to cover the new runner when it does not. Receipt verification must use the same extra selectors/scope as execution.
* Impact: final exact-head evidence can omit this issue's essential integration or formatting contract.
* Smallest useful change: pin runnable commands and working directories in details: supplied API discovery with PYTHONPATH=../core/tests:../agents/tests, explicit new-module execution, Ruff lint, isolated runner format check compatible with existing line length, and mypy. Name module entry points/import context because checks is outside the installed distribution. Run Research/Plan/Implement/Review in order; preserve the original critique/Review. Resolve follow-ups before committing the final candidate and dated evidence. Add the required new tracked selectors via --extra-test to the complete local gate and receipt verification, retain external results and re-gate after any source/head/base/input change. Require exact-head independent assessment after verification and no approval substitution.
* Action owner: planning parent/publication coordinator.
* Exact resolving evidence: revised literal command/selector list; executed/skipped counts and current head/base recorded; full receipt proves the new required integration executed and verifies with matching selectors immediately before non-force publication. No repeated original critique or Review is needed.
* Decision route: direct planner correction; exact-head independent assessment is already requested.

<!-- rpi:critique id=PC-010 -->
### PC-010 [High]: Current full gate conflicts with this execution environment's storage prohibition

* Related IDs: P02-T01, full local gate, locked additions.
* Evidence: tools/rpi-checks.py:2273-2276 unconditionally opens /tmp/ama-rpi-heavy.lock. The active execution constraint prohibits all file operations in /tmp or temporary directories. Passing an external --out or setting TMPDIR does not redirect that literal lock path.
* Concern: the mandatory existing gate cannot be executed here as written. Changing the gate tool is outside the locked runner/test/README scope; skipping it or fabricating a receipt is expressly disallowed.
* Impact: publication is concretely blocked even if the runner and all targeted checks are correct.
* Smallest useful change: record this specific publication blocker now. Complete eligible implementation/targeted checks without launching the prohibited gate; route approved gate compatibility remediation as separately scoped work, or execution of the unchanged complete gate in an independently authorized compatible environment. Preserve serialization and exact-head/full-scope receipt requirements; no silent lock change, fallback or skip.
* Action owner: planning parent records the blocker; owner/publication coordinator chooses and authorizes the out-of-scope compatible route.
* Exact resolving evidence: approved compatible gate execution/remediation provenance and a current exact-head/current-base full passing verified external receipt. A changed tool or environment requires a fresh full run.
* Decision route: recording/refusing publication is a direct planner correction. A route changing the locked scope or execution environment needs a significant owner decision if no existing approved route is available.

<!-- rpi:critique id=PC-011 -->
### PC-011 [Medium]: README is in scope but not assigned as a verifiable deliverable

* Related IDs: locked README documentation, P01-T01, C5.
* Evidence: plan Scope names README but P01-T01 and phase details describe only the runner/test. src/api/README.md:19-44 still calls the runner future work and records historical consumed attempts.
* Concern: adding the runner without updating its owning contract leaves no supported entry point, external ledger/output instructions or clear separation of historical and current authorization.
* Impact: maintainers may invoke the wrong historical runner, reset a campaign accidentally or read local regression as live acceptance.
* Smallest useful change: explicitly assign the existing #570 README section update to P01-T01: supported module command, independently verified inputs, authorization/budget policy, private paths, diagnostic refusal, return codes, local regression command and honest live/publication blocker dispositions. Preserve dated historical claims and all historical artifacts; add current state instead of rewriting earlier results.
* Action owner: planning parent.
* Exact resolving evidence: revised task delivery checklist and final README diff matching the actual runner CLI/tests, with historical consumed slots and unproven live criteria still distinguishable.
* Decision route: direct planner correction; already authorized documentation.

## Strengths and Residual Risk

* The correct solution is caller integration, not an authorization, Entra mapping, roster or UI change. The shared predicate already rejects wrong tenant/object despite matching email and accepts correctly authorized rosterless identity.
* Cause is identified at the comparison-contract level. The absent historical raw claim and actual historical signed-in account remain Unknown; no new runner can retrospectively recover them.
* Real constructed HTTP/Chromium evidence can establish engineering behavior without live sign-ins or private data. It cannot establish Entra live identity or employee live acceptance.
* Live chat intentionally creates chat/audit activity even though it must not mutate case/home/business records; benign general-work prompts and private-session disposal reduce exposure, not server-side retention. Do not claim zero persistence or full privacy acceptance.
* Blocked identity, operational and publication gates remain separate. Refs #570 is correct while any issue acceptance criterion is unproven.

## Questions or Blocking Evidence Gaps

* Independent expected tenant/object provenance remains missing. The identity administrator/owner must supply it or an authorized read-only source must establish it before live execution. No observed-session expectation or weaker verification is an eligible alternative.
* Current gate storage is incompatible with the active environment. The planning parent must record the blocker and the publication coordinator must establish an approved compatible route before publication.
* No new identity policy, budget increase, Azure change or broader model authority is required to resolve the planner-owned findings.

## Limitations

* Read-only critique: no implementation, browser launch, live sign-in, credential-file access, Azure operation, dependency installation, test execution or gate run.
* Source and supplied research support design concerns, not claims that an unwritten runner already has these bugs. Canary/deadline/concurrency outcomes above are exact required resolving evidence, not observed results.
* Directory denial and health warming are supplied dated W2/W3 evidence, not independently repeated here. Read-only issue and branch metadata were checked.
* Plan, details, research, state and all historical evidence remain unchanged. Only this caller-specified critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: revise P01-T01's authorization-scoped durable two-slot admission contract and allocate its regression within the six-test inventory, then incorporate all remaining findings directly.
* User response required: not for planner-owned corrections. Missing independent evidence blocks live execution; a new out-of-scope gate/environment route requires owner authorization if no approved route exists.

| [.copilot-tracking/plans/2026-10-31/employee-identity-check-570-plan.md](.copilot-tracking/plans/2026-10-31/employee-identity-check-570-plan.md) | Assessed final candidate plan |
| [.copilot-tracking/details/2026-10-31/employee-identity-check-570-phase-details.md](.copilot-tracking/details/2026-10-31/employee-identity-check-570-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-31/employee-identity-check-570-research.md](.copilot-tracking/research/2026-10-31/employee-identity-check-570-research.md) | Supplied bounded evidence |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-plan-critique.md) | Complete one-pass critique; Revise |

## Next Steps

Active planning parent: resolve PC-001 through PC-011 directly, retain this original outcome and finalize without another critique. Continue the ordered loop only after incorporating the executable safety contracts. Do not run live sign-in until independent expected identity is verified; do not publish until the complete compatible gate and exact-head requirements are met. No user action is needed for the direct revisions; the external identity evidence and any newly authorized gate route remain explicitly owned blockers.
