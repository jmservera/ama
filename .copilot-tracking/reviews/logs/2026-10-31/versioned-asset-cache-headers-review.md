---
title: "RPI Review: versioned asset cache headers"
description: "Independent post-implementation review of versioned asset cache policy."
ms.date: 2026-10-31
---

## Scope and Evidence

* Task ID: 12a8273a-1cfb-42aa-ae85-97f032ffafbd.
* Review date: 2026-10-31.
* Review scope: One independent full-task post-implementation Review.
* Source boundary: Nine tracked changed files against HEAD f1a87593dcad38114c8ddbcc6ea721ae87c8e735; tracked diff SHA256 16242405c4fea4b502a798d7404da33aa34a22fa7ab83b59bf7b14ef42cf932d verified before comparison.
* Canonical artifact set: research, plan, phase details, plan critique, changes and state under the supplied 2026-10-31 versioned-asset-cache-headers paths.
* Plan: .copilot-tracking/plans/2026-10-31/versioned-asset-cache-headers-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/versioned-asset-cache-headers-phase-details.md.
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/versioned-asset-cache-headers-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-31/versioned-asset-cache-headers-changes.md.
* Research: .copilot-tracking/research/2026-10-31/versioned-asset-cache-headers-research.md.
* State: .copilot-tracking/rpi-sessions/2026-10-31/versioned-asset-cache-headers-state.json.
* Original evidence: Read with git show only from origin/chore/ops-redeploy-1031:.copilot-tracking/reviews/logs/2026-10-31/demo-sites-redeploy-1031-review.md. Original RV-001 High identifies missing long-lived headers and routes a distinct cache-policy source workstream; this task addresses that source concern, not the redeployment's acceptance outcome.
* Context: docs/case_study_48_original.md; opening scope of docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md; sector-primer context; src/README.md local gate and shared-lock policy. No business, legal, visual or accessibility acceptance is inferred.
* Validation evidence: Supplied external session cache-validation root, addressed below by evidence labels. External evidence was read only; no generated assets or environments were created by this reviewer.

## Opening Review State

* Interpreted review goal: Assess intended current-version immutable caching without weakening HTML, old-URL compatibility, error, API or authentication policy; reconcile planning and recorded validation.
* Review scope: Complete supplied source task, not commit, publication, hosted checks or live acceptance.
* Evidence readiness: Source identity verified; supplied artifact and validation paths identified, contents awaiting comparison.
* Acceptance basis: Owner requirements, canonical plan/detail markers, critique disposition, recorded implementation and real-browser evidence.
* First comparison boundary: Read canonical artifacts and complete tracked source diff, then inspect existing response paths and supplied validation summaries.
* Active read-only boundaries: Source and evidence remain read-only; write only this canonical Review. No tests, browser, cloud, model operations, agents, commits, source repairs or remote writes.
* Initial blockers: None established; publication prerequisites and acceptance are explicitly outside this Review's authority.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One independent comparison on 2026-10-31 of all nine tracked changes, current surrounding response/snapshot paths, canonical artifacts, original redeploy finding and bounded recorded validation. No validation was rerun. The supplied tracked diff hash remained unchanged after comparison.
* Scope distinction: Review execution is complete; full-plan execution remains Partial until parent-owned P03-T02 local persistence. This record completes P03-T01's assessment without changing parent plan or state.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01; FR1-FR4; AC1-AC2 | Shared query-aware response policy | Reconciled | Frozen Asset retains snapshot version; all three handlers pass raw query; existing success/conditional and guard paths retained. |
| P01-T02; AC3-AC4 | Focused regression matrix, browser assertions and guide | Reconciled | One added focused method; existing handler matrix expanded; bare Leaflet retained; immutable reuse and explicit HTTP validation separated. |
| P02-T01; AC5 | Final requested validation | Reconciled | Recorded final discovery and focused runs pass after bounded assertion/dependency restoration; first adverse run remains preserved. |
| P02-T02 | Pre-Review reconciliation | Reconciled | P01/P02 markers, detail phase index, changes and state agree; current diff identity verified. |
| P03-T01; AC6 | One independent Review | Reconciled at handoff | Parent artifacts correctly leave this task pending while assessment runs; this one record is its completion evidence. |
| P03-T02; AC6 | Local commit | Deliberately remaining | Parent-owned after Review; no commit, clean committed candidate or metadata verification is claimed here. |
| Follow-Up Items | Live acceptance and future publication gate | Reconciled | Distinct outside-scope work; not silently added to source acceptance. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/static_assets.py | Single decoded current v selects exact public, max-age=31536000, immutable | HTML short-circuits first; parse_qs with keep_blank_values=True compares the complete v value list to one snapshot version | Shared direct test and actual-handler matrix recorded passing | Conformant |
| P01-T01 | src/api/src/zava_forward/api/server.py; src/api/src/zava_forward/api/resident_demo/app.py; src/api/src/zava_forward/api/resident_preview/app.py | Preserve request query when obtaining response headers | Employee uses existing url.query for 200/304; residents use urlsplit(self.path).query in their shared GET/HEAD response branch | Three-handler GET/HEAD/304 matrix | Conformant |
| P01-T02 | src/api/tests/test_static_assets.py; src/api/tests/test_ui_support.py | Assert new exact policy without relaxing old freshness or validators | Existing matrix expanded; one new method; existing UI-support assertion alone amended | Focused restored 73 tests; full discovery 1430 tests | Conformant with justified ownership amendment |
| P01-T02 | src/api/checks/asset_cache_browser_check.py | Observe fresh-cache reuse independently of explicit 304 | Normal same-context navigation checks per-rendered-script/style origin counts before APIRequestContext requests; executed release/shared markers wait before count comparison | Employee/resident results and request histories passed | Conformant |
| P01-T02 | src/api/checks/workspace_scripts_browser_check.py | Supplement existing bare Leaflet assertion with rendered versioned URL | Same bytes and ETag, correct immutable header, original recovery assertions retained | Restored workspace log passed | Conformant |
| P01-T02 | src/api/README.md | Describe exact-current boundary, obsolete compatibility and real cache measurement | Guide matches policy and restart/no-hot-reload boundaries | Direct Markdown/diff assessment | Conformant |

### Response, snapshot and compatibility assessment

* Exact equality is on the decoded v value list, not on the entire query string. An unrelated parameter alongside a single current v still qualifies, as deliberately specified. Blank, bare v, stale, duplicate current, current-plus-stale and current-plus-blank values do not. Encoded current version and parameter ordering have direct coverage.
* Frozen Asset bodies and release versions are captured together. Existing deterministic release hashing covers sorted packaged paths and byte hashes; rewritten HTML selects that same release. The new test proves an old snapshot remains release A while a new snapshot serves release B and rejects A's version for immutable policy.
* No historical byte store or stale-URL rejection was introduced. Actual-handler requests to bare/stale/ambiguous URLs assert the same current bytes and ETag as the rendered current URL.
* HTML remains no-store with no ETag and cannot become 304 through Asset.not_modified, even with a current query and wildcard validator. GET and HEAD share policy; HEAD has no body, normal content length is retained and 304 omits Content-Length.
* Employee trusted-proxy admission still precedes static lookup/headers. API authentication, redirects, missing-file and denial responses continue through default no-store SECURITY headers. Resident host, expiry, concurrency/session boundaries and preview unavailable-feature/read-only guards are unchanged and precede asset responses; default HEADERS remain no-store.
* Existing employee and resident no-store denial/API tests are retained. Preview guard behavior is established here by unchanged source ordering and existing-suite evidence, not by inventing a newly added denial matrix.
* All nine tracked changed files are within the accepted boundary. No UI file bytes, chat implementation, dependency manifest or workflow files changed. Tests remain outside the runtime package. No source-level constructor incompatibility was found in the inspected shared construction path.
* Browser cache evidence is actual origin-response counting without Playwright route interception in the cache module. Explicit request-client HTTP 200/304 checks happen after the browser reuse comparison and are not misrepresented as browser cache hits. Workspace routing is recovery/header evidence, not the independent cache-reuse measurement.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 test ownership; P02-T01 | Add only the existing UI-support exact-version header assertion to the named scope | First full discovery exposed 13 subtest failures from the prior no-cache expectation; no product decision changed | Plan Scope, Test Ownership and Change Budget, detail P02-T01, changes amendment and final results agree | Immediately relevant amendment; no material re-planning or repeated critique required | Justified: tightly coupled expectation fix, not weakened acceptance or unrelated test repair |
| P02-T01 dependency availability | Restore three existing distributions in an isolated external venv | Actual azure.eventhub and API distribution-metadata errors; owner permits restoration after missing-dependency failure | Plan Dependencies/amendment, details and changes preserve original failure and exact final command context | Accepted direction and unchanged manifests retained | Justified environment restoration; system package mutation or new tooling is not claimed |
| Critique disposition; P02-T01 lock | Reject PC-001's asserted parent /tmp prohibition and retain shared coordination | Caller explicitly supplies parent-context correction; src/README.md requires shared /tmp/ama-rpi-heavy.lock for heavy validation | Plan disposition, details, changes and state agree | One original Complete / Revise critique preserved; final Ready disposition recorded | Supported within supplied parent execution context; see scope qualification below |

## Critique and Material Revision Assessment

* Exactly one critique is recorded. Its original Complete / Revise verdict and PC-001 Medium remain visible; rejection is a disposition, not a retroactive rewrite to a passing critique.
* PC-001 was context-dependent, not a cache design flaw. Parent-context absence of the alleged prohibition is supplied by the caller, not independently reconstructed from unavailable parent instruction history. Repository shared-lock policy independently corroborates why replacing it with a private lock would be inappropriate.
* This Review has its own prohibition on /tmp operations and executed no lock, tempfile consumers, validation or scratch-file commands. Accepting the supplied earlier parent-context disposition does not waive the reviewer boundary or authorize future forbidden operations.
* Research documents Wider, Deeper and Contrarian execution, C1-C9 and explicit rejection of any-present-v immutability. Plan/detail reconciliation preserves those decisions and the owner's no-store HTML requirement.
* The assertion and dependency amendments do not introduce significant or divergent product decisions. No material revision readiness gap or evidence of dependent source work preceding the recorded Ready disposition was found.
* Original redeploy RV-001 remains historical; the source correction does not alter that Review's Not accepted/live outcome or automatically resolve its separate authentication/governance follow-ups.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Owner-authorized live cache and signed-in acceptance | This task is local source work; deployment/sign-in authorization is excluded | Owner commissions separate deployment and authenticated acceptance with approved access | Open distinct live-acceptance follow-up; not a source defect |
| Complete publication gate, exact-head and hosted/human approval | No push/publication is authorized; candidate commit follows this Review | Parent or later authorized publication owner commits evidence, obtains required complete fresh gate and verifies exact candidate/base before publication | Open distinct publication follow-up; local tests are not a gate receipt |

The plan's live item and changes-record publication item remain outside active implementation acceptance. Original resident generated-prose activation and other prior redeploy gaps are neither repaired nor accepted by this cache task.

## Findings

No substantive current-task implementation defect, decision gap or material evidence gap was found. Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low. No RV-xxx identifiers are fabricated for deliberately pending parent work or already-separated acceptance gates.

## Defects

* None identified within the supplied source/evidence boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | No corrective RPI stage required by this assessment | No substantive source finding |

Later implementation of any independently discovered issue does not require this Review to run again.

## Residual Work

* Distinct live-acceptance follow-up: owner authorization, deployment and signed-in evidence remain unestablished.
* Distinct publication follow-up: complete gate/real SQL/full browser prerequisites, current-base exact-head verification, hosted checks and human approval remain unperformed.
* Existing 320 unittest skips remain disclosed. They are not recast as passed SQL/browser/model/live acceptance or introduced as new active plan tasks.

## Blockers and Remaining Work

* Review blockers: None.
* Remaining active work: P03-T02 local persistence, owned by the parent. Update plan/detail/changes/state with this outcome, resolve approved privacy-safe local identity and persist the exact candidate with Refs-only issue linkage and the required trailer. This reviewer neither performs nor verifies that future commit.
* AC6 is not fully delivered before that local commit. P03 remains Partial at this handoff despite complete source assessment and Review execution.
* Publication, live and human acceptance remain unavailable by deliberate task boundary; no push or issue closure is authorized.

## Validation Evidence

Evidence root E: supplied external session files/cache-validation directory for this task. E labels identify files relative to that root, not repository deliverables. All statuses below describe recorded implementation validation, not commands executed by the reviewer.

| Recorded command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q, from src/api with restored venv PATH and shared flock wrapper | Full API discovery | Passed with disclosed skips | E/api-unit-restored.log summary: 1430 tests in 502.331s, OK (skipped=320). Hash verified. |
| Original same discovery attempt | System environment before restoration | Failed, preserved | E/api-unit.log summary: 1368 tests in 483.107s, failures=13, errors=3, skipped=320. Failure classification is recorded in changes; large failure bodies were not reread. |
| Restored focused selectors named in changes | Cache, related UI-support, missing-import and metadata regressions | Passed | E/focused-restored.log: 73 tests in 21.114s, OK. |
| ruff check | API project | Reported passed | Changes records All checks passed. No separate Ruff log was supplied/read; no rerun or stronger independent execution claim. |
| ruff format --check | API project | Reported passed | Changes records 65 files already formatted. No separate format log was supplied/read. |
| python3 -m checks.asset_cache_browser_check --out supplied external asset-cache-restored directory | Actual employee/resident loopback handlers, Chromium 156.0.8078.4 | Passed | E/asset-cache-restored/results.json and log: same-origin legacy turnover, release-B JS/CSS/shared/vendor execution, immutable reuse, controlled first widget 503 and recovery, explicit ETag 304 and bare/stale policy. Hash verified. |
| python3 -m checks.workspace_scripts_browser_check | Actual employee loopback workspace | Passed | E/workspace-restored.log: running/responsive server, original actual-script recovery and companion settlement paths, bare and rendered versioned Leaflet bytes/ETag/header checks. Hash verified. |
| python3 -m checks.chat_submit_browser_check --out supplied external chat-submit-restored directory | Actual employee/resident local rules plus controlled race cases | Passed | E/chat-submit-restored/results.json and log: responsive server, ordinary Enter/Send real local API replies on both apps, focus and auth/session timing cases. Hash verified. |
| git diff identity comparison | Nine tracked changes | Verified read-only | Base HEAD and supplied SHA256 matched before and after comparison; this untracked Review is not part of that source hash. |
| Complete local publication gate; real SQL; full browser matrix; hosted/human/model/live acceptance | Outside local selected validation | Not run / unestablished | Explicitly excluded or missing prerequisites; no receipt, cloud fallback, fabricated pass or publication authorization. |
| Independent validation in this Review | All executable checks | Not run | Caller prohibits tests, browser, cloud/model operations; assessment uses source and preserved evidence only. |

### Verified evidence hashes

| E-relative evidence | Verified SHA256 |
| --- | --- |
| api-unit-restored.log | 6afbaae612a1c2bed509d3aaa1a39308319885f9690cb77ecc02def95ef9cfeb |
| asset-cache-restored/results.json | 66b7772501982430898fdd12bce2715eac19436e951ceb5d864063d3d7a6c5f0 |
| workspace-restored.log | c6976c85c52dde47e9f9bdc502754a02793f068f7918291958d23c6c0963788b |
| chat-submit-restored/results.json | 90f90dca18ca55fe7074f94a4e68cb116a4a1756a5c4512f5c4a0303b34c5bbf |

Hashes establish identity of the supplied evidence, not a committed-candidate publication receipt or independent reexecution.

## Outcome

* Outcome: Conformant with justified divergence.
* Outcome rationale: The whole supplied source task meets FR1-FR4 and AC1-AC5 within recorded local evidence. The immediately relevant existing-test ownership amendment and isolated dependency restoration are justified, reflected in current artifacts and preserve required behavior. No actionable cache defect was found. AC6 local persistence remains intentionally parent-owned after this one complete Review; publication and live acceptance are not claimed.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction recommended |
| Decision gap or invalid assumption | None | No rpi-plan revision recommended |
| Material evidence gap | None within source scope | No rpi-research return recommended |
| Non-blocking residual work | Distinct live/publication follow-ups | Owner authorizes acceptance and any later publication gates separately |

* Execution status: Complete.
* Outcome: Conformant with justified divergence.
* Validation coverage: Recorded full API discovery, focused regression and three selected browser checks; Ruff passes reported in changes; 320 skips disclosed.
* Blockers: None for Review/source handoff. Local commit remains pending; publication/live acceptance are not established.
* Continuation: Return this one Review to the active parent. No current-task source repair, repeat critique or repeat Review is requested.

## Next Steps

The active parent records this outcome and completes P03-T02 local persistence only. Keep live acceptance and full publication gates as distinct authorized follow-ups. No user action or corrective RPI invocation is required by this Review.
