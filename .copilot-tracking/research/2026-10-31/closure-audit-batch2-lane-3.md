---
title: Closure evidence audit batch 2 lane 3
description: Read-only criterion audit for fifteen assigned issues at pinned main
ms.date: 2026-10-31
ms.topic: reference
---

## Scope and method

Task `closure-audit-batch2`, lane 3, pinned main
`84035ae9605f7ab42744a3d6e9f620bb65126d99`. Working branch is
`docs/closure-audit-batch2`; existing parent tracking files were untouched.
Assigned issues only: 228, 229, 230, 231, 232, 233, 344, 349, 350, 360,
432, 435, 440, 441 and 462.

Captured complete issue bodies and all 57 unique matched PR JSON objects
(body, file records, review bodies and check rollups) were read as inert data.
References, relevance and surviving source/test/document evidence were assessed,
not titles or merge status alone. `git merge-base --is-ancestor` returned success
for all 57 matched merge commits against the pinned HEAD. No stacked non-main
merge was relied upon; the parent's separate stacked-merge warning remains
applicable to other lanes.

Checkbox line indices are zero-based issue-body lines; JSON `text` preserves the
exact label after the checkbox marker. Existing ticks are preserved, not
recertified. `tick` is the proposed final checkbox value, not permission to mutate
GitHub. Every issue remains open with at least one unproved criterion.

## Results

| Issue | All matched PRs | New documentary/engineering ticks | Closure |
| --- | --- | --- | --- |
| 228 | 496 | None | No |
| 229 | 496 | None | No |
| 230 | 496, 406, 548 | None | No |
| 231 | 496, 529 | None | No |
| 232 | 383, 496, 401, 406, 518 | None | No |
| 233 | 496, 401 | Line 19: hypotheses retained | No |
| 344 | 352 | Line 15: honest Blocked browser-smoke record | No |
| 349 | 437, 352, 394 | None | No |
| 350 | 436, 352, 418 | None | No |
| 360 | 453, 449, 364, 459, 450, 363, 457, 365, 362, 370, 391, 381, 385, 423, 476, 375, 379, 374, 461, 416, 371, 437, 514, 377, 515, 612, 516, 376, 373, 583, 424 | None; three existing ticks retained | No |
| 432 | 602, 612, 433 | Lines 21, 24: dated Unknown price source; capacity-not-cash classification | No |
| 435 | 438, 516, 502 | None | No |
| 440 | 461, 304, 503, 504 | Line 21: bounded architectural assessment; five existing ticks retained | No |
| 441 | 454, 442, 463 | Lines 29, 30, 31: native process, custody/qualified trace, overlap recheck; four existing ticks retained | No |
| 462 | 463, 465, 455, 479, 478, 310 | None; three existing ticks retained | No |

Totals: 15 issues, all open; 100 checkbox criteria; 15 existing ticks preserved;
8 proposed new ticks; 77 criteria remain unchecked; zero closure candidates.

## Exact evidence and limits

### Role designs: 228-233

PR496 directly names each issue's separate child, but the merged parent installs
only a shared host. `src/api/src/zava_forward/api/web/role-screens.js:3,48`
contains the empty module registry and installed-role filtering. Lines 66,
89 and 92 describe unavailable modules, reset and read-only missing-evidence
semantics. Generic shared work/safety tests at
`src/api/tests/test_role_screens.py:74,157-158,191,198,213` are not procurement,
data, programme, technical/quality or housing child-screen acceptance.
The captured parent check rollup includes one FAILURE and 13 SKIPPED checks.
Later review resolves the shared safety omission; that does not integrate
the separate role modules or provide complete Fluent/WCAG/human/AT acceptance.

PR401's authored inventory,
`docs/reference/research/ux/zava-forward-prototype-profile-review.md:44,184,257`,
keeps journeys labelled hypotheses and direct research Not supplied. Line 343
expressly records missing atlas theme-to-state resolution and same-home
walkthrough. Thus issue233 line19 is provable, while its wider pass is not.
The original inventory Review is Complete/Conformant for documentation only,
not human design acceptance. Lines 115 and 134-142 retain Fluent and manual
accessibility limitations.

PR529's case-journey workspace is related to technical/quality journeys but is
not the requested complete queues. PR406 preserves historical recorder identity,
not full programme/housing screen design. PR383 is finance matching and PR518
employee re-apply; neither delivers issue232. PR548 is PowerPoint Q&A navigation,
not issue230 programme navigation, and is rejected as a false positive.

### Public entry and deployed parity: 344, 349, 350, 360

PR352's surviving authored acceptance audit,
`docs/architecture/cutover-evidence-pack.md:1073-1088`, records:

* Real browser sign-in blocked at line 1077.
* Historical public-edge trade-off at line 1078.
* Native API 401 versus browser User-Agent API 302 at line 1079.
* Historical private-SQL management readback at line 1080.
* Authenticated full parity blocked at line 1081.
* Honest Blocked real-user smoke, with no callback/session, authorization or
  consent, at line 1082.

Only the last is newly tickable: the issue explicitly accepts a Blocked
evidence record. Continuing live edge/private-SQL conditions are not newly
ticked, even though the dated document records bounded observations.

PR437 is read-only tenant readiness, not owner provisioning/credentials/staff
binding or real-user session. PR394 is progress-event capture, rejected as a
tenant-readiness match. PR436 is an offline demo feedback checker with a
constructed six-case/five-staff rehearsal and no configured model. It preserves
original non-conformant outcomes and does not prove issue350 deployed parity.
PR418 is retained-priority challenge work for issue220, not deployed restoration.

Issue360 existing source ticks remain supported by PR362/365/370 and surviving
`infra/tests/test_setup_entra.py:315,425,440` and
`infra/tests/test_bicep_policy.py:1050,1055`. The tests cover no-Front-Door
direct path, direct-origin guard/callback preservation and private-service guard
matrices. They do not prove owner-approved migration, live browser/role/SQL/AI
conjunction or authorized retirement after that conjunction.

PR449/450/453 retain live session/readback gaps; PR457/459 are bounded SQL
seed/removal work, not full live acceptance. PR514/515/516 are employee fixes
and configuration with explicit acceptance limits. PR612's latest live record
still blocks employee authenticated journeys/capacity/AI metering. PR416/423/437
are private transport/readiness; PR374/583 belong to credential issue358.
PR461 is a checkpoint; PR371 climate, PR373 sensor faults, PR376 queue reset,
PR377/424 form staging/review packs are contextual or false-positive matches,
not issue360 closure evidence.

### AI consumption and pitch: 432, 435

PR602 survives on main but expressly delivers source-only engineering.
`src/core/src/zava_forward/core/ai_consumption.py:1023-1028` declares incomplete
historical/resident financial joins. Actual owner budgets/alert appointments,
Azure billing/tolerance, denominator/quality floor and held-out authority remain
open at `docs/reference/resources/ai-tokenomics.md:241-249`.

The dated artifact,
`docs/reference/resources/azure-ai-price-source-2026-10-31.json:2-19`, stores
official URL/date/version/hash, unavailable numerical rates and cost Unknown.
`src/core/tests/test_ai_consumption.py:475-489` proves billing is the financial
source and missing/partial evidence stays Unknown. This supports issue432
line21 without claiming an applicable approved numerical price.

The report at `src/core/src/zava_forward/core/ai_consumption.py:1068-1072`
returns capacity classification and cash Unknown. The test
`test_quality_regression_fails_even_when_cheaper_and_capacity_not_cash`,
`src/core/tests/test_ai_consumption.py:651-665`, asserts capacity 4 and cash
Unknown. This supports line24's classification rule, not measured released
time or Finance-booked value.

The pitch drafting insert at
`docs/reference/resources/ai-tokenomics.md:251-267` labels source-only results
and gaps, but lines 255-256 explicitly leave delivered deck/generated notes
unchanged. It cannot tick actual slide/Q&A delivery.

PR602 retains original Defects found Review, scoped publication/continuity
Residual work and failed/unverified full gate. The static skip-parser and
browser B023 roots blocked eight downstream groups. A successful captured
workflow is not financial, human or full integration acceptance. PR612 says
live metering Blocked. PR433 is requirements framing only.

PR438 directly refs435 but is a portable 30-minute presentation/10-minute demo
authoring handoff, not completed PowerPoint workflow or performed 15-minute
Tokenomics rehearsal. It retains four CHANGES_REQUESTED review events.
PR516 is manager briefing and PR502 indoor synthetic bounds, both rejected as
issue435 closure evidence. No mentor/owner confirmation, measured-batch
disposition or complete delivered-deck statement/challenge audit is proved.

### Stabilization: 440

PR461's authored assessment at
`docs/architecture/cutover-evidence-pack.md:2219-2227` covers auth/roles,
proposal/human controls, resident/safety holds, SQL/ledger, import/package
contracts and manual failure paths. Lines 2244-2248 expressly confirm no stable
application defect or necessary refactor, rather than inventing one.
`.github/agents/ama-backlog-delivery-coordinator.agent.md:215-223` requires
behavior-preserving scoped fixes and regression tests for confirmed bugs.
This proves issue440 line21's bounded assessment criterion.

Lines 2240-2248 retain PERF-440's unknown-root validation risk without a new
independently scoped bug/refactor issue, so line23 remains unchecked.
Lines 2269-2278 record chooser discovery only coordinator-attested, transcript
absent, simulated behavior proxy evidence and original Partial/Residual work.
That does not establish complete Major HVE behavior/host validation at line24.
The first checkpoint is explicitly historical at lines 2260-2264.
PR304 is historical source repoint; PR503 leaves chat grounding/stabilization
work open; PR504 explicitly says issue440 stabilization is not delivered there.

### Requirements integration: 441

PR442's actual native phase record,
`.copilot-tracking/rpi-sessions/2026-10-23/resident-portal-requirements-441-phases.json`,
retains ordered continuation and protected primary/sibling boundaries.
The original Review,
`.copilot-tracking/reviews/logs/2026-10-23/resident-portal-requirements-441-review.md:26-51`,
confirms the topic worktree, exact integrated documents and original custody.
The changes record,
`.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441-changes.md:107-110`,
records phase-log correction without rewriting original outcome. These support
line29.

The exact custody JSON is
`.copilot-tracking/research/2026-10-23/resident-portal-requirements-441-input-custody.json`.
The original Review at lines 45-48 and 153-189 verifies original byte/hash
custody, retained identifiers and qualified downstream trace. Surviving
`docs/prds/zava-forward-retrofit-programme-demonstrator.md:1008-1022` retains the
resident BRD/PRD trace to the linked unregistered proposal. This proves line30,
not registration.

Overlap research at
`.copilot-tracking/research/2026-10-23/resident-portal-requirements-441-research.md:207-217`,
original Review lines 373-381 and changes lines 113-120 record shared hunks,
exact sibling heads and fresh pre-publication recheck. This proves line31.

Preserve four existing ticks. In particular, already-ticked registration
wording must not be recertified: PR442 and original Review lines 55-58,308
explicitly retain `id: null`, UNREGISTERED and registration UNMET.
Per-message human review remains normative at
`docs/prds/zava-forward-retrofit-programme-demonstrator.md:966,1051-1052`;
actual requirements-owner disposition is not newly inferred.

PR442/454 provide exact historical passing gate records and focused
checks/baseline diagnostics. Their historical receipts do not alone establish
the final merged/publication-head conjunction after later score/head/base
movement. PR442 capture has no checks. Line37 remains conservatively unchecked;
this lane does not rerun or fabricate a final receipt. PR463 preserves the
unsigned handoff boundary, not requirements approval.

### Synthetic resident showcase: 462

Preserve three existing engineered/evidence-record ticks. PR463's surviving
`src/api/tests/test_resident_demo_api.py:185,278,348,367,376,397` covers allowlist,
generic login, forged session, own-case and expiry. Lines 301,319,508 cover
CSRF/same-origin, secure HttpOnly cookies and generic database failure.
These are not actual owner-held-password live login.

PR465 explicitly records a tightly coupled cap correction whose plan/Review
followed interim deployment and an UNGATED image. PR463 retains early planning
push deviation, original release-preflight Request changes and cost erratum
not independently re-reviewed. Do not retroactively tick prospective process
or financial gate criteria.

PR455 preserves loopback preview, not whole issue444 acceptance. PR478 is
partial deployment with negative checks and no positive login proof.
PR455's captured source review retains the High fixture-identifier finding
`discussion_r4372517587`; its recovered rubric alone is not complete reviewed
dependency resolution.
PR479's original Review is Complete/Not accepted with owner-run positive
login/own-case/sign-out/live-expiry groups Blocked; scoped publication receipt
is not complete final gate. Its URL/identity/owned resources/expiry record is
honest partial evidence, not full-service acceptance. PR310 is staff
building-model work for issue75, rejected as a resident-showcase false positive.

## Validation and handoff

No source edits, git writes, remote mutations, nested agents, private datasets,
secrets, paid inference, Azure changes or heavy tests. Only requested evidence
artifacts were authored. Source/tests were inspected, not rerun. Local validation
is limited to JSON/schema/checkbox reconciliation, citation-path/line checks and
Markdown/whitespace review. Hosted checks are captured history, not fresh lane
validation; full publication gates and synthesis/mutations belong to the parent.

Machine evidence:
`/home/azureuser/.copilot/session-state/463953af-009d-4142-bfe5-deebb9be5868/files/lane-3.json`.
Executed lightweight validation passed: all 100 exact labels/zero-based lines,
15 issue states, exact matched-PR arrays, existing-tick preservation, closure
logic, citation paths/ranges, frontmatter and trailing-whitespace checks.
`git diff --check` passed; it does not inspect untracked parent artifacts.
All 57 ancestor assertions passed. Captures contain 1,794 file records,
445 review records and 449 check records; body/review strings were fully loaded.
The surviving web tree contains only the `registerRoleScreen` function definition
at `src/api/src/zava_forward/api/web/role-screens.js:30`, no installed registrations.
The captured file lists for PR436/438/442 contain exactly 100 entries; this audit
does not assert uncaptured file-list completeness or use that limit to infer
missing acceptance. All retained adverse outcomes/source-only qualifiers remain
material. No issue is recommended for closure or reopening.
