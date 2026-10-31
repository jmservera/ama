---
title: Closure audit lane A - cycle 1 Deeper
description: Criterion-level read-only closure evidence for fourteen assigned issues
ms.date: 2026-10-31
---

## Scope and result

Parent: [closure-audit-batch1-research.md](../closure-audit-batch1-research.md).
Machine-readable findings: [closure-audit-a.json](./closure-audit-a.json).

* Pinned repository HEAD: `84035ae9605f7ab42744a3d6e9f620bb65126d99`.
* Assigned issues only: 110, 111, 114, 115, 116, 117, 118, 119, 120, 121,
  122, 125, 126, 128.
* 14 issues, 90 exact checklist criteria, 102 distinct candidate PR snapshots.
* 28 demonstrated engineering/documentary criteria; 62 unproven criteria.
* 15 proposed new engineering ticks; six existing checked criteria are not
  supported as whole criteria by this audit.
* Zero supported closures. All fourteen issues remain OPEN in the snapshots.
* Parent controls every final tick and closure decision. No issue/board edit,
  implementation, test execution, live/cloud request, private dataset read or
  approval was performed.

The snapshot root is
`/home/azureuser/.copilot/session-state/a1bb0cd0-f92d-473e-a842-6a05b8bf7f83/files/closure-audit-inputs/`.
Each issue's full body was checked, including the additional `* [ ]` RAI
sections. Numbering follows every checklist item in body order, not just the
original `- [ ]` section. Exact text, original checked status, complete
candidate numbers, relevant references and criterion evidence are retained in
the JSON.

## Evidence interpretation

Full candidate snapshot bodies/file metadata/check and review records were
loaded for classification. Substantive referencing PR bodies and their complete
changed-file inventories were examined with relevant retained independent
Review outcomes and current source/test assertions. Search matches without
substantive delivery references are not treated as proof. Administrative
backlog references are identified separately.

The two capped inventories in this lane were supplemented from the parent's
paginated files: PR436 has 119 files, PR558 has 184 files. Both supplements were
read, including their full filename/patch records; neither is a new substantive
delivery reference to an assigned issue. Their additional paths are not `src/`
feature implementations. A 100-file initial list was not assumed complete.

All source anchors are on pinned current main. Old `mvp/` paths in PRs
261-281 were followed to the migrated `src/core`, `src/api` and
`src/orchestrator` counterparts. A test filename alone was never a feature
proof: the audit inspected assertions on retained rows, receipt replay,
canaries, denials, aggregation, epochs, history or document counts.

`proven=true` denotes the whole literal engineering/documentary criterion, not
whole-issue acceptance. It never grants actual human/legal authority,
operational release, resident consent, live Azure assurance or screen-reader
acceptance. A software persistence/denial/history requirement can be proven by
reviewed constructed tests; the existence of a field named `approval_ref`
cannot approve anything.

The #114 annual verification criterion is an interpretation-sensitive proposed
engineering tick: the literal requirement asks for verification proved by
test, and PR262's independent review accepts the local code criteria. Current
issue prose and PR403 still call actual annual Azure reliance unproven. Parent
should retain that qualification or decline the proposed tick if the intended
criterion includes deployed Azure reliance. It cannot support closure.

## Criterion outcomes and confidence

| Issue | Demonstrated indexes | Proposed new ticks | Whole issue gap | Confidence |
| --- | --- | --- | --- | --- |
| 110 | 2, 3, 4 | 3 | No actual distinct Hub identities or actual telemetry/credential assurance; live transport remains unverified | High gaps; medium source-only interpretation of 3 |
| 111 | None | None | Standalone exercise comparator not integrated into approved retained-reading analysis/review task; R1-R3 incomplete | High |
| 114 | 1 | 1 | Actual Azure load/latency/cost and witnessed DH-005 restore/deletion reapplication missing | High gaps; medium interpretation of 1 |
| 115 | None | None | Actual approved locked Blob publication and hosted scheduled alert/verification missing | High |
| 116 | 1, 2, 3, 11 | 11 | OD-14/19 approval and complete approved provider-boundary minimization/derivative contract missing | High |
| 117 | 2 | None | Real malware scanner/Defender and Blob tag acceptance absent | High |
| 118 | 2, 3 | None | Dockerfile/kernel hosting constraint, live private edge and Policy/Defender decision absent | High |
| 119 | None | None | Binding selected-provider terms and actual screen-reader test missing | High |
| 120 | 1, 2 | None | Actual staff notice/consultation/administrator ratification missing | High |
| 121 | 10, 12 | 10, 12 | Qualified lawful basis/retention/transfer/rights and complete processing map/derivative controls missing | High gaps; medium documentary proof attribution |
| 122 | 1, 2, 3, 4, 5, 7, 9, 10 | 4, 5, 7, 9, 10 | Actual authorized restart/drill and enforceable old-image exclusion absent | High |
| 125 | None | None | Discovery assistant remains a design hypothesis without readiness/access/comparison proof | High |
| 126 | 6, 7, 9, 11, 12 | 6, 7, 9, 11, 12 | Real protocol/releases/MDE/qualified assessment/AI economics approvals and actual build acceptance missing | High |
| 128 | None | None | Actual AT/user research and complete independently expected/evaluated cohort results missing | High |

### Existing checked discrepancies

These are review findings for the parent, not instructions to modify issues.

* #110 criterion 5: source X.509 selection and sanitization are partial; the
  current sensor synthesis explicitly defers actual source/telemetry secret
  assurance. The original tick must not be read as that live assurance.
* #118 criterion 1: PR347 removed the ENTRYPOINT enforcement guard. Current
  Dockerfiles set UID/GID 10001; read-only/cap-drop are external Docker
  contracts. Container Apps cannot provide the requested hosted enforcement.
* #118 criterion 4: default-off edge/WAF/Private Link definitions and offline
  tests do not prove live private-origin/public-edge acceptance.
* #126 criteria 2-4: source can record releases, pause scopes and prevent a
  Pass/Fail verdict when MDE exceeds target. The recorded fixture decisions,
  `OD-35 demo`, and exercise MDE do not establish actual phase/tranche
  approvals, restart authority or ratified event definitions/MDE.

## Referencing PRs and retained reviewed checks

Check counts below describe the supplied snapshot, not a newly run suite or
fresh exact-HEAD acceptance. Rubric APPROVED records alone are not independent
feature acceptance. Many bodies still say Draft/unmerged at their historical
writing date; the snapshot's merged metadata establishes integration, not
retroactive live acceptance.

| PR | Substantive relationship | Retained assessment and validation boundary | Snapshot checks |
| --- | --- | --- | --- |
| 205 | Administrative RAI body updates for 116/121/122/126/128 | Explicitly not remediation; no application/human/recovery tests | 5 success, 5 skipped |
| 261 | #126 protocol/benefits/release/pause mechanism | Independent conformant engineering review; real OD-18/35/36 decisions absent | 4 success, 1 failure |
| 262 | #114 annual digests, load harness, restore deletion logic | Independent partially conformant local code; 478 tests, 85 opt-in skips historically; Azure proof open | 5 success |
| 267 | #120 reference/notice/independent enabling mechanics | Independent conformant code/shared-store review; 521 tests, 85 skips historically; notice/DPIA actual approval absent | 5 success |
| 268 | #115 remote digests, schedule/alert definition | Independent built-scope conformity; 527 tests, 85 skips historically; lock/live/log contract absent | 5 success |
| 269 | #122 disable/history/change/export mechanisms | Independent synthetic-prototype conformity; 531 tests, 85 skips historically; external head/drill/authority remain open | 5 success |
| 270 | #117 scan-gating/retention/hold | Independent synthetic-scope conformity; 530 tests, 85 skips historically; local scanner not antivirus | 5 success |
| 275 | #116 role inventory/canaries/held notes | Independent original and fix-pass conformant for original three engineering criteria; broader RAI explicitly excluded | 5 success |
| 347 | #118 image/CI/IaC controls | Original full hosted deployment Not accepted; later source correction/CI passes; 61 HIGH/2 CRITICAL unfixed findings retained per full image report | 11 success |
| 395 | #117 bounded offline pending rescan invocation | Original Not accepted, two authorized corrections preserved; later actual local SQL/image checks are not real Defender or hosted schedule | 12 success |
| 398 | #122 epoch/audience-safe export remediation | Original adverse Reviews retained; body records later exact-head bounded independent PASS and 12 checks; actual authority/drill/custody/old-image exclusion open | 12 success |
| 403 | #114 trustworthy bounded loadcheck evidence | Original Not accepted duration finding; one correction with 75 passing tests/16 detected mutants, not Azure load or DH-005 acceptance | 12 success |
| 404 | #115 malformed/missing remote anchor refusal | Original/correction adverse history preserved; final local 27 coupled/46 orchestrator tests, zero skips; actual lock/scheduler/custody open | 12 success |
| 408 | #120 bare-DPIA-flag denial | Independent conformant bounded engineering; actual 23 tests plus 2 HTTP probes pass historically; human notice/DPIA acceptance absent | 12 success |
| 409 | #126 constructed RAI evidence register | Independent conformant engineering, zero original RV findings; actual local SQL 16/16 historical; all 22 register findings remain Open/Unknown | 12 success |
| 411 | #110 durable finite SQL consumer | Original Defects found plus two correction histories retained; corrected local SQLite/SQL Server/image evidence; no live Hub identity or real Azure acceptance | 12 success |
| 422 | #126 finite cost proposal | Independent draft publication only; scoped/expired budget is not phase/measurement approval | 7 success, 10 skipped |
| 426 | #119 provider comparison proposal | Original/recovery/correction Residual work; all vendor/selection/AT limits retained | 11 success, 7 skipped |
| 431 | #122 custody/recovery proposal | Bounded preparation only, no criterion acceptance or witnessed drill | 14 success, 12 skipped |
| 433 | #126 Tokenomics scope amendment | Requirement/backlog proposal only, no denominator/price/budget/benefit acceptance; Windows local-gate failure retained | 1 success |
| 439 | #126 dated cost/minimal demo continuation | Narrow draft-fidelity review, real economics/measurement/approval gates open; no all-in actual forecast assumed | 6 success, 5 skipped, 6 cancelled |
| 458 | #119 temporary OSM demo configuration record | PASS-WITH-FINDINGS, not production provider or screen-reader acceptance; no browser attribution/Referer receipt | 4 success, 5 skipped |
| 508 | #110 bounded SDK consumer/publisher | Original Not accepted and later Conformant correction/refresh/pacing histories retained; local fixtures not actual Hub-to-SQL | 11 success, 7 skipped |

No fresh tests were executed during this audit. All test-run numbers in this
table are previously run retained PR evidence. Independent original negative
outcomes were not replaced by green check counts.

## Complete per-issue candidate exclusions

Every candidate number is retained in JSON `prs`. `referencing_prs` contains
substantive exact references, including explicitly marked scope-only/admin
updates, not mere regex hits. The following complete exclusion sets contain
both unrelated broad-search hits and incidental dependency/history mentions.
An exclusion from `referencing_prs` does not erase an explicitly qualified
indirect source contribution.

| Issue | Excluded candidates |
| --- | --- |
| 110 | 272, 433, 301, 424, 498, 373, 354, 512, 362, 377, 376, 378, 320, 356, 485, 355, 528, 375, 463 |
| 111 | 505, 340, 515, 485, 484, 483, 482, 481, 347, 355, 486, 373, 378, 558 |
| 114 | 472, 496, 546, 404, 397, 402, 384 |
| 115 | 512, 392, 534, 390, 395, 557 |
| 116 | 277, 259, 250, 529, 424, 394, 480 |
| 117 | 343, 342, 548, 391, 410, 372, 392 |
| 118 | 272, 394, 436, 602 |
| 119 | 244, 421, 420, 457, 378, 502, 424, 540, 454 |
| 120 | 292, 281, 270, 235, 325, 355, 395, 555, 503, 433, 418 |
| 121 | 281, 401, 346, 505, 399, 407, 386, 502, 496, 507, 594, 454 |
| 122 | 343, 399, 406, 408, 555, 454, 421, 540, 395, 602 |
| 125 | 291, 401, 409, 389 |
| 126 | 401, 475, 540, 317 |
| 128 | 485, 411, 419, 607, 540 |

### Exact numeric mentions that are not delivery proof

* PR272 mentions #110 as still open/local-mirror reconciliation work. PR320
  and PR485 identify missing consumer integration/compatibility rather than
  deliver #110; PR373 calls #110/#111 context, not ordering/delivery.
* PR498 explicitly leaves #110 consumer/credential/human work separate.
  PR512 says it read #110/#115 dependencies for #146 monitoring work; that
  reading is not delivery of ingestion or locked scheduled ledger verification.
* PR505 explicitly says actual #111/#133 consumer test use remains unmet.
  Its standalone exercise comparator is useful partial evidence, not the
  requested retained-reading analysis/review task.
* PR404 calls #114 a hierarchy parent, not its delivered criterion. PR402
  explicitly says no #114 work changed.
* PR277, PR259 and PR250 leave #116 identity/binding/approval work open rather
  than deliver those requirements.
* PR343 repairs board status and explicitly moves #117/#122 off Done. It
  is not feature evidence and cannot close them.
* PR244's #119 mention is chart/list/accessibility baseline work; all actual
  manual AT records remain Not run. PR420/421's #119 mentions refer to an
  inherited certifi pin correction, not map-provider or AT acceptance.
* PR457 keeps map-provider #119 as an owner decision; seed merging is not
  provider acceptance.
* PR281 explicitly says #120/#121 not assessed. Its constructed chat privacy
  source and draft data-scope boundaries are used only as qualified indirect
  evidence, never actual legal approval.
* PR401 lists #121/#125/#126 as screen-inventory ambiguities. Inventory
  coverage is not implementation/readiness/legal/release acceptance.
* PR399 holds #122/#398; PR406 names held #122 work while preserving historical
  recorder identity; PR408 explicitly excludes #122 source changes. These are
  status/noninterference mentions.
* PR205 is a substantive exact administrative scope update for five assigned
  issues, not delivered remediation. PR433 adds #126 Tokenomics requirements,
  not actual metered benefit/budget-owner acceptance.

### Qualified indirect source evidence

* PR602 does not name the assigned #118/#122 issues in its body. It changes
  existing AI/consumption/task/assistant/store wrappers and adds request,
  financial admission, settlement/quarantine/release and conservative report
  corrections. The full 70-file inventory and 37,012-character body were
  examined for that relationship. Its retained matrix still says applicable
  prices, actual billing/tolerance, OD-51 denominator/quality floor, booked
  destinations and paid held-out batch are unproven. It does not close
  #126's economics/release gates or #121's privacy/derivative gate.
* PR419, available as a #128 search candidate, actually delivers bounded
  operator controls under #221 into the existing continuity files. Its
  source corroborates incident persistence/epoch/restart denial, but it
  explicitly leaves actual OD-35, monitoring thresholds, competent evidence
  and witnessed drill open. It does not deliver the #128 cohort/AT criteria.
* PR421's unapproved cohort manifest supplies draft pair isolation and
  reconciliation tests used to explain #128 gaps. Those tests explicitly
  require AI expectations to remain unlabelled and candidate seeds
  unconfirmed; `test_every_acceptance_criterion_is_not_met` starts at
  `src/agents/tests/test_cohort_manifest_draft.py:309`.
* PR540/607 are progress-dashboard work under #533, not #128 accessibility
  research/cohort acceptance or #126 release decisions. PR607 explicitly
  has no local full-gate/live employee verification acceptance.
* PR555 is paper/presentation work; PR546 is process/closure guidance;
  PR548 is PowerPoint Q&A review. Their broad search matches are unrelated
  to software feature acceptance.
* PR558 is Fabric/capstone/source-reorganization work, not the #111 approved
  analysis/review task. Its full 184-file inventory was not mistaken for a
  truncated sensor delivery.

## Assertion anchors used

The JSON records complete criterion-specific anchors; these examples clarify
why an extant test is evidence rather than a filename.

* `src/core/tests/test_sensor_consumer.py:82`: first admission creates one
  reading; reopened replay returns the same receipt; conflicting content
  cannot add another reading. Lines 192-219 inspect actual fault receipts
  and owned exception timestamps.
* `src/core/tests/test_recovery.py:31`: each year verifies alone/with sealed
  digest. Lines 40/56 detect edits/dropped sealed years; line 121 exercises
  local older-backup erasure reapplication, not witnessed Azure PITR.
* `src/api/tests/test_role_endpoint_inventory.py:78`: every configured role
  plus Mystery runs GET/POST inventories with contractor canaries. Lines
  145/169 inspect actual existing provider/capture wrappers. The read-only
  AST route comparison found zero missing current guard routes.
* `src/api/tests/test_document_controls.py:197`: retention listing preserves
  documents, blocks nonmanager and held deletion, then removes only the
  approved unheld row and verifies the audit. Periods remain synthetic.
* `src/api/tests/test_timecapture.py:101`: invalid DPIA references refuse
  all writes without creating storage. Line 344 retains only the five-person
  activity and suppresses two-person activity with no U0 identifier.
* `src/api/tests/test_continuity_epoch_export.py:1268`: actual constructed
  HTTP manual call, service challenge and hazard operations run during
  suspension; stale proposal review and unsafe progression remain denied.
  Lines 231/533 cover in-flight unknown liability and retained revoked history.
* `src/core/tests/test_governance.py:308`: even all 22 fixture dispositions
  leave every finding Open and acceptance Unknown.
* `src/agents/tests/test_cohort_manifest_draft.py:145`: pair integrity exists,
  but AI expectations are explicitly unlabelled and SD-01 unconfirmed. It
  is not a measured cohort/model/human acceptance report.

## Audit integrity

The artifact validation checked all fourteen objects against the full issue
snapshots: exact checklist text/order and original checked state match for all
90 criteria. Every evidence path exists on the pinned main worktree, every
non-null line is within the referenced file, and every candidate is retained.
The worktree already contained parent-owned untracked tracking files; they
were left untouched. This lane wrote only its two requested artifacts.

Blocking uncertainties are the explicitly documented live/human/AT and
completeness gaps above. They are audit outcomes, not a request to run cloud
checks, make implementation changes, invent approvals or prolong the lane.
