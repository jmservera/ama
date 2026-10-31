---
title: Closure audit batch 2 lane 4
description: Read-only checkbox evidence dispositions for fifteen assigned issues at exact main
ms.date: 2026-10-31
ms.topic: reference
---

## Scope and method

Audited only #466, #470, #520, #521, #530, #531, #533, #550, #551,
#552, #563, #570, #571, #572 and #608. All snapshot issues are OPEN.
The exact repository HEAD is
`84035ae9605f7ab42744a3d6e9f620bb65126d99`, on the parent's
`docs/closure-audit-batch2` branch. Pre-existing parent tracking files were
left untouched.

Input authority is the supplied complete `issue-N.json` and `pr-N.json`
snapshots in the session `files/audit-input/` directory. Full records were
loaded, including each issue body and matched PR body, file list, all review
records and all `statusCheckRollup` records. Exact `#N` references were
distinguished from search noise. Review summaries/findings and original
committed changes/Review records were compared with surviving main source
and named assertions, not substituted with merge status or rubric approval.
PR file lists are changed-path inventories, not a claim every changed source
file underwent a fresh full code review.

The machine-readable result is session
`files/lane-4.json`. Each row preserves the original zero-based
`body.splitlines()` index and exact checkbox line. Existing ticks remain
unchanged; `tick` describes only a recommended new tick. No issue, PR,
source, git ref/index/configuration or remote state was changed.

Focused documentation/evidence tier only. No heavy tests, browser launch,
SQL, Azure, model calls, dependency installation or receipt generation ran.
Recorded historical tests are attributed to their merged evidence, not
claimed freshly executed. Read-only `git diff --check`, JSON schema/checklist
identity checks and merge ancestry checks were performed. Hosted CI is
reported separately below; this audit is not a full local publication gate
or independent exact-head release assessment.

## Dispositions

### Fresh-main revalidation before parent mutation

Revalidated narrowly on 2026-10-31 against `origin/main`
`9ecb159bd843411c2e17dc2785ab59f5e837040f`, using read-only
`git diff 84035ae9605f7ab42744a3d6e9f620bb65126d99..origin/main`
and `git show origin/main:<path>`. The working branch remains at the
original audited `84035ae9605f7ab42744a3d6e9f620bb65126d99`;
no rebase, source/JSON edit, test execution or remote mutation occurred.
Earlier path:line citations remain historical baseline-qualified.

Only three runtime/documentation files changed: `src/api/README.md`
(13 inserted lines), `src/api/src/zava_forward/api/resident_demo/chat.py`
(59 additions, 5 deletions) and `src/api/tests/test_resident_chat_api.py`
(160 inserted lines). Other changed files are tracking/rubric evidence.
All other relied-on lane-4 runtime, browser, tool and infrastructure files
are unchanged. Static AST comparison confirms all 34 existing resident-chat
test/helper functions are unchanged, with three new test methods.

| Evidence | Fresh-main source/assertion comparison | Disposition |
| --- | --- | --- |
| #520 own-case documents | Existing `test_documents_own_case_typed_routing_and_no_cross_case_data` at `src/api/tests/test_resident_chat_api.py:916-950` still requires Survey Missing, upload route, every warning/error, sources, no approval/submission, cross-case denial and revocation. `test_typed_documents_keep_mandatory_facts_in_every_ai_state:995-1055` and `test_document_revocation_during_inference_returns_no_facts:1057-1075` retain AI-off/success/failure/unrestricted-prose and revocation guards. New `test_natural_own_record_questions_reuse_grounded_answers_with_ai_off:478-505` asserts unchanged own-record answers/sources, no other resident and no actions for newly recognized questions. | Existing document recommendation and preserved ticks remain supported within original synthetic/source scope. No actual-model/live/AT acceptance is newly inferred. |
| #550/#563 repair fallback and negative permission guard | `test_explicit_consent_precedes_personal_lookup_or_model_for_every_shape:359-378` still denies missing/false/string permission before lookup or any provider/advisor call. `test_repair_questions_use_explicit_disabled_fallback_not_home_summary:412-431` retains rat-question cause uncertainty, housing-officer route, AI-disabled label and no home-summary/address leakage. `chat.py:286-375` retains the exact existing safety/exclusion/specialist/repair ordering; `:391-411` retains repair help and distinction between record-use permission and works consent. | Accepted negative data-flow, label and honest-fallback evidence is not weakened. #550 resident-consent and #563 consented actual-model/live conjunctions remain excluded/unmet; no actual consent is newly ticked. |
| #571 recognized prompts and obsolete refusal | Unchanged browser assertions at `src/api/checks/resident_assistant_browser_check.py:333-386` retain complete recognized document/form questions and obsolete `documents help`/`forms help` no-fact/no-AI refusal. Existing `test_obsolete_browser_prompts_stay_host_owned_refusals:961-973` is unchanged. New `test_natural_questions_preserve_refusal_and_specialist_boundaries:507-524` covers mixed/appended/third-party instructions and priority routes; `test_unknown_refusal_gives_four_supported_examples_and_human_help:526-540` retains refusal/no-action/help assertions. | All three prior narrow prompt/check recommendations survive; historical local pass evidence is not claimed freshly executed at this SHA. |
| Other lane-4 accepted criteria and closure evidence | All other relied-on runtime/browser/tool files are unchanged. `_record_question` only adds a finite whole-question natural-record fallback; `answer` only replaces the unsupported-topic example wording, retaining explicit refusal, no authority and housing-officer help at `chat.py:423-431`. | No affected evidence weakened and no previously accepted tick must be deferred because of this main advance. Original adverse-review, release, live, human/legal, AT and resident qualifications remain. |
| API README claims used by other lanes (#184/#199/#201/#214) | Read-only line-sequence comparison confirms EVERY baseline README line survives unchanged and in order. The sole insertion at fresh-main `src/api/README.md:1188-1199` documents finite own-record wording, complete-intent matching, continued refusal and no AI activation/deployment or approved resident copy. Adjacent `:1175-1186,1201-1230` retains permission, no client selectors, document facts/source controls, works-consent unknowns and safety limits. | Additive only; no contradiction to the unchanged migration/deployment/API README claims cited by the other lanes. This is delta consistency checking, not reopening those lanes' broader audits. |

The parent's latest checkbox-only closure rule supersedes the earlier
broader retain-open narrative for #520/#551: once their explicit checkboxes
are fully preserved/proven/ticked, the parent may close them while retaining
unlisted live/human qualifications without asserting those fulfilled.
The #466 owner-confirmation proposal remains rejected under the explicit
approval exclusion. This revalidation changes no machine criterion decision
or existing tick and grants no human/resident approval.

| Issue | Original ticks | New recommendations | Remaining checkbox gap | Closure recommendation |
| --- | --- | --- | --- | --- |
| #466 | 4 | 2 | None within recorded scope/decision rows | Retain open: explicit manual/live/publication qualifications |
| #470 | 4 | 0 | Like-for-like full before/after benchmark | Retain open |
| #520 | 6 | 1 | None within bounded synthetic source/existing rows | Retain open: explicit live/AT/publication qualifications |
| #521 | 0 | 2 | Consistency across remaining browser cutoff; confirmed live apply | Retain open |
| #530 | 7 | 0 | Local unit/browser/actual SQL conjunction and live employee evidence | Retain open |
| #531 | 6 | 0 | Live employee verification | Retain open |
| #533 | 4 | 1 | No gap in five explicit local/source criteria | Narrow source-scope closure candidate |
| #550 | 0 | 8 | Resident-consent criterion not newly ticked | Retain open |
| #551 | 0 | 4 | No gap in four local criteria; explicit owner live acceptance remains | Retain open |
| #552 | 0 | 5 | Combined Fluent/WCAG baseline acceptance unresolved | Retain open |
| #563 | 0 | 3 | Actually consented relevant generated answer and authenticated live proof | Retain open |
| #570 | 0 | 2 | Live employee chat/map/case conjunction | Retain open |
| #571 | 0 | 3 | No gap in three local prompt/check criteria | Narrow source-scope closure candidate |
| #572 | 0 | 3 | Fresh complete verified exact-head browser/MSSQL gate | Retain open |
| #608 | 0 | 2 | Accepted full supported-path browser/SQL evidence without skips | Retain open |

Totals: 15 issues, 79 checkbox rows, 31 existing ticks preserved,
36 new bounded recommendations and two narrow closure candidates.
The parent owns final decisions and mutations. #533/#571 candidates do not
mean complete release, live-user, human, legal or accessibility acceptance.
Their PRs' incomplete release/live gates remain recorded and may justify
retaining the issues open under a broader parent acceptance decision.

## Exact-reference and integration inventory

The JSON `prs` arrays retain ALL captured `merged_prs` numbers for each
issue, in the original issue-snapshot order, including rejected search
results. Inclusion is a complete inspection inventory, not accepted
delivery evidence. Exact references, relevance and main integration remain
separate qualifications. Rejected matches:

| Issue | Rejected search results | Reason |
| --- | --- | --- |
| #466 | #335 #334 #529 #515 #418 | No exact body reference to #466 |
| #470 | #253 | No exact body reference to #470 |
| #521 | #267 #266 #340 #342 | No exact body reference to #521 |
| #530 | #270 | No exact body reference to #530 |
| #531 | #269 | No exact body reference to #531 |
| #533 | #418 | No exact body reference to #533 |
| #550 | #377 | No exact body reference to #550 |
| #551 | #297 #298 #377 | No exact body reference to #551 |
| #552 | #477 | No exact body reference to #552 |
| #563 | #562 #362 #376 #375 | #562 references #550/#551/#552 only; other results have no exact #563 body reference |
| #572 | #558 | Visual publication precursor, no exact #572 body reference |

### Reconciliation correction: complete rejected-record inspection

On the parent's inventory correction, every omitted record below was read
in full from `files/audit-input/pr-N.json`: complete PR body, EVERY changed
file entry, EVERY review body/state/commit and EVERY captured check record.
Large bodies and reviews were reread in bounded chunks where combined
outputs truncated; only decorative severity-picture markup was removed
from review rendering, not review prose or findings. Empty review/check
arrays are recorded as empty, never inferred approvals. #562 was already
fully inspected in the original #550/#551/#552 acceptance trace; its
rejection here is specific to #563.

This corrects the machine inventory, not criterion outcomes. All 79
criterion rows, exact text/indices, existing flags, proposed ticks,
evidence, notes, states and closure qualifiers remain unchanged. The
additional inspections supply no missing complete clause that warrants
another tick. No rejected merge SHA is used to establish main delivery.

| Rejected PR | Assigned issue matches | Complete inspection (files/reviews/checks) | Scope and retained qualification |
| --- | --- | --- | --- |
| #253 | #470 | 11 / 0 / 5 | Law-store SQL/Blob adapters for #210, not gate speed. Body retains unrun local MSSQL and fake Blob limitations; captured MVP/image/MSSQL checks SUCCESS are historical, not live WORM/role proof. |
| #266 | #521 | 9 / 0 / 5 | Portable SQL metadata upsert, not January authority renewal. Actual 85-test local SQL run and successful captured CI do not prove the renewal/application clauses. |
| #267 | #521 | 19 / 0 / 5 | Staff-time DPIA/notice/audited-enabling controls, not resident January authority. Real approvals and browser acceptance remain absent despite historical CI SUCCESS. |
| #269 | #531 | 16 / 0 / 5 | Persisted AI suspension/version/export for #122, not briefing loading. Witnessed/live continuity drills and human authority remain unproved; captured CI SUCCESS is bounded. |
| #270 | #530 | 18 / 0 / 5 | Document malware/retention/legal-hold controls for #117, not bounded employee skills chat. Synthetic/fake transport is not real DPO/legal approval; captured CI SUCCESS does not remove that qualification. |
| #297 | #551 | 92 / 0 / 11 | Core-hub M2 migration for #199, not expanded-map filters. Full rename inventory inspected, including `src/core/src/zava_forward/core/chatthreads.py`; local Docker/SQL unavailable and rename checks had seven missing-package errors. Captured source/MVP/image/MSSQL CI SUCCESS does not establish #551 acceptance. |
| #298 | #551 | 44 / 0 / 11 | Synthetic-tool/eval M3 migration for #199, not compact-map interaction. Full moved-file inventory inspected, including `src/core/tests/test_synthetic_output_dir.py`; private data transfer remained owner action, local Docker/SQL unrun and seven rename-check errors retained. Captured CI SUCCESS is historical. |
| #334 | #466 | 10 / 0 / 11 | Rule-engine source gating/cross-episode throttle tests for #329, not own-home sensor UI. Source-only runtime boundary and one opt-in skip retained; captured source/MVP/MSSQL checks SUCCESS do not prove resident/live acceptance. |
| #335 | #466 | 13 / 0 / 11 | Source-monitor retry since last successful observation for #332, not sensor gauges. Core/orchestrator regressions and captured source/MVP/MSSQL SUCCESS do not grant approvals or resident acceptance. |
| #340 | #521 | 19 / 0 / 11 | Indexed task-queue membership for #327, not renewal. SQLite scale/query timing evidence and captured source/MVP/MSSQL SUCCESS cannot prove January authority or live SQL application. |
| #342 | #521 | 23 / 1 / 1 | Private infrastructure deployment for #200/#201, not renewal. Positive authorized HTTP/staff initialization remained blocked and owner checklist untouched; captured rubric-only SUCCESS is not deployment acceptance. |
| #362 | #563 | 32 / 0 / 9 | Direct demo/Entra setup for #360, not resident generated-answer acceptance. Compiled/offline/fake CLI evidence and source/validation SUCCESS retain live auth/AI omissions. |
| #375 | #563 | 23 / 0 / 9 | Laptop-safe restricted migration staging for #360, not resident AI relevance. Independent Revise, four restricted 403 responses and unmet welcome/auth/SQL/AI boundaries remain; captured source/validation SUCCESS is not acceptance. |
| #376 | #563 | 19 / 0 / 12 | Queue signals/reset scope for #77, not resident AI. Native/local browser proof is not human/live acceptance; captured source/MVP/image/MSSQL SUCCESS cannot supply actual generated relevance. |
| #377 | #550 #551 | 22 / 0 / 12 | Unapproved form-schema/candidate staging for #97, not shared chat/map. No actual approved template, UI/AI/submission or legal acceptance; original Residual work retained despite historical source/MVP/image/MSSQL SUCCESS. |
| #418 | #466 #533 | 33 / 18 / 1 | Retained-priority challenge/correction for #220, not sensor or progress-dashboard delivery. `src/api/checks/challenge_browser_check.py` inventory and all review rounds inspected. Original Revise and Partial/Not accepted remain; later reviews still require human/current-head verification. Limited scoped browser/SQL proof does not establish AT/legal/resident acceptance. Captured rubric-only SUCCESS is not full final-head CI. |
| #477 | #552 | 14 / 8 / 9 | Industry-led paper and published-data figures, not case-view icons/tab interaction. `docs/capstone/thought-leadership/everything-but-the-software/main.tex` and figure/tool inventories inspected. Reviews retain human transcription/PDF verification, Tectonic exit-code and assessment-digest provenance concerns. Eight captured rubric jobs SUCCESS coexist with `rubric/score` PENDING. |
| #515 | #466 | 13 / 8 / 1 | Minimal employee model/Bicep prerequisite, not resident sensors. `infra/tests/test_bicep_policy.py` reviewed inventory and all review rounds inspected. No employee activation/inference, scoped preflight FAILED and no full gate; distinct-version test gap and inaccurate environment table remained in reviews. Captured rubric-only SUCCESS does not change those limits. |
| #529 | #466 | 97 / 47 / 18 | Evidence-based employee case journey for #526, not resident gauges. `src/api/tests/test_case_journey.py` and full browser/tool inventory inspected. Original Complete/Defects found retained alongside later repairs, rubric CHANGES_REQUESTED rounds, final hidden regulatory-alert reflow/text coverage qualification, local-only providers and absent human/live/AT acceptance. Captured source/MSSQL SUCCESS and skipped rubric stages do not remove these limits. |
| #558 | #572 | 100 / 29 / 1 | Fabric/capstone integration history, not a fresh #572 full-gate receipt. All inventory including `.github/workflows/src-ci.yml` inspected. Body does report historical real chat-panel browser dispatch, consistent with already accepted owning-PR proof, but final reviews retain blocked current-main exact-head gate, absent native Windows/PowerPoint and human accessibility acceptance. Original failed scoring/changes findings and later bounded corrections remain; captured rubric SUCCESS does not supply the missing full gate. |
| #562 | #563 | 10 / 4 / 0, already read | Live chat UX evidence for #550/#551/#552, not proof of relevant generated AI answers for #563. Real resident honest-inability fallback is not consented model relevance; no captured checks and employee acceptance limitations remain. Its evidence already informs the original acceptance qualifications elsewhere. |

Read-only `git merge-base --is-ancestor <mergeCommit> <exact-main>` confirmed
all relied-on main integrations. #471, #472 and #473 are the exceptions:
their stacked-topic merge SHAs are not main ancestors. Parent #474
`2fbb42f0ed80b84429fc7962eda1e04e3265e15e` is a main ancestor, explicitly
integrates those three children, and its file inventory carries their sensor,
account and assistant source/tests and original evidence. Equivalent source
and tests still exist on audited main. Child merge status alone is not used.

Key successor main merges:

| PR | Main-ancestor merge commit | Evidence role |
| --- | --- | --- |
| #475 | `4bd06495651e58e9957ace590880006eedb8047a` | Gate selection/scope/parallel correction, not full benchmark |
| #525 | `9bfed51863b05a25e9939d82504c576524688e14` | Resident chat, own-case/agenda/source guards |
| #541 | `77c87e0d76b827544fde9b2f2ce7dfbd9d879232` | Employee bounded skills/chat |
| #553 | `4a9d5cceafaa0a7f37d6b8d920e9f7932985ab0e` | Expanded original header filters |
| #554 | `ecbb5a80470292c885764c28d6833c0e5ef63dfa` | Compact journey/icons/popover/tabs |
| #556 | `356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7` | Shared widget and keyboard/thread contracts |
| #568 | `252a498e2001193b0142b4f4ac031096dd6cc2b7` | Enter/Send refresh-state regression |
| #573 | `a0670b58a171255284b005ad281b26fd50ea89c7` | Resident prompt/check reconciliation |
| #574 | `5634f9a077d175a931c15e3400114665d8c071ee` | Immutable identity runner predicate |
| #589 | `18602ae7103ceee89fa4c87ca312b04a57ca0dba` | Document-language/source contracts |
| #590 | `f168d0799624e7f8e943fde6ef6fb08a17db151d` | January authority source and conditional plan |
| #591 | `d986c4c4a1010b6a5c7ba6b00d2c452c4db8f089` | Actual exact-ID/header/narrow map evidence |
| #592 | `9b13cef9e9ea8034e2ab65ff796eed65d2edb166` | Actual desktop/narrow/keyboard/touch case evidence |
| #593 | `ec2d784255c3377ab39e5d2d1b5140e76c8e7f36` | Scripted generated routes and resizable/dockable widget |
| #600 | `e64c6e6c9da407682de59b926944424f94f50671` | Real selected chat-panel execution, exact gate contract |
| #601 | `f11d29e41cd40c1be2b81b111f6189340df84bdd` | Employee identity/action/map regression and mandatory browser inventory |
| #603 | `5198a1ff4bdf416249b64d5f4d832e88f3f7040b` | Authored current scope/model decision and qualified sensor/chat evidence |
| #604 | `28fbe6b6111c5aae4fc2c4f55f8ffca2876ab589` | Loading/briefing evidence and review correction |
| #606 | `3ffea4dd497b0eba4c6ec3df4750c2ccfba8a138` | Gate fixture/skip validation correction |
| #607 | `87bf629c630314f5be086697e322e1b0ec22277d` | Stock-scale source/tests and separately verified actual evidence |
| #609 | `9c67a399c62eb42f99ac46e1861b55526552c112` | Resident browser fixture/skip isolation correction |
| #612 | `b11f5a668ceb98ea81131c10b93d2ff564789041` | Partial live observations, original failed gates |
| #610 | `84035ae9605f7ab42744a3d6e9f620bb65126d99` | Exact audited HEAD, early socket-path admission |

## Clause-level evidence

### #466: recorded decisions, not activation or accessibility approval

PR #603 authors current scope/priority at
`docs/architecture/resident-assistant-prototype.md:7-13` and
`src/api/README.md:1415-1436`. The owner scope direction is already recorded:
own-home gauges/history, advisory assistant with AI, IoT priority, synthetic
data and deployment AI off. Recommending reconciliation of that decision
does not supply new human/legal/AT acceptance.

The model/cap/credential row is an authored decision criterion:
`docs/architecture/resident-assistant-prototype.md:30-37,46-49,66-87`
records regional Standard `gpt-4.1-mini` 2025-04-14, permanent USD20
inference ceiling inside USD30 and managed identity only. Existing tariff
expiry/default-off/accounting guards remain unchanged.

Existing engineering ticks are preserved. Parent #474 integrates the
non-main-ancestor #472/#473 evidence. Current surviving
`src/core/tests/test_resident_sensors.py`,
`checks.resident_sensors_browser_check`,
`src/api/tests/test_resident_chat_api.py:284-314,756-915` and
`src/api/checks/resident_assistant_browser_check.py:314-391`
retain synthetic values, text/table, document/form facts, cross-case/refusal
and revocation contracts.
`resident-sensor-gauges-466-changes.md:77-114` under the current
31 October changes directory records local engineering checks and 42 axe
incomplete results. #603 explicitly retains unavailable complete publication
receipt, manual accessibility and actual-model/live acceptance. #478 Partial/
Not accepted and #479 Not accepted remain historical, not upgraded.

### #470: partial-tier timing is not a full benchmark

#475's full PR body explicitly labels historical full 23-26-minute timing,
changed-tooling-only 60.856 seconds and unmeasured parallel full execution.
#584 preserves missing comparable serial/parallel full runs.
Do not tick zero-based row 15.

Preserved ticks have surviving
`tools/test_rpi_checks.py:test_changed_selection_mapping_and_closure`,
`test_real_partial_fixture_requires_matching_selection_and_evidence`,
`test_parallel_scheduler_overlaps_independent_groups_and_blocks_dependents`,
`test_partial_scope_is_rejected_by_default_before_live_probes:1669`,
`test_worker_limit_respects_cpu_memory_and_invalid_jobs:1802` and
`test_worker_limit_intersects_nested_cgroups_and_ancestors:1883`.
Original #475 Not accepted Review and later corrections are distinct.

### #520: every document-language clause now has own-record support

#525 originally qualified unavailable document data and did not accept this
criterion. #589 is later evidence, not a rewritten #525 outcome.
`src/api/tests/test_resident_chat_api.py:756-790` tests:

* Survey Missing and a recorded secure upload instruction.
* Unreadable page warning, address mismatch error and unfinished scan.
* Own request/document reference, no other-case content.
* Not a decision, cannot upload/send, no approval claim.

`test_typed_documents_keep_mandatory_facts_in_every_ai_state:835-895`
retains facts/citations under off/success/failure/unrestricted-prose output,
denies forged other-case access and keeps private requests out of prompts.
`test_document_revocation_during_inference_returns_no_facts:897-915`
withholds late revoked replies.
`src/core/src/zava_forward/core/resident_documents.py:108-181` authors the
plain-wording scan warnings, request provision, unknowns and approval limits.
`src/api/checks/resident_assistant_browser_check.py:333-378` requires every
document fact in local Chromium and narrow/enlarged-text reflow.

Existing ticks stay unchanged. #525's agenda is synthetic callbacks, not
operational works appointments or works consent. #542 startup rollback,
#543 sufficient local SQL-view cause versus unconfirmed Azure cause,
#545 unauthenticated deployment and #593 unrun final browser/live/AT checks
remain explicit. #534 is RAI evidence, not a chat implementation.

### #521: source plan and arithmetic, unresolved consistency/live operation

`src/core/tests/test_resident_showcase.py:91-100` tests old November/
December cutoffs admitted during January and exclusive new cap refusal.
`src/core/tests/test_resident_showcase_sql.py:200-219,644-707` tests policy
rendering, migration/rights/reapply and rollback. However, #590's final
review flags a still-old shared browser cutoff:
`src/api/checks/resident_demo_browser_check.py:37` and
`src/api/tests/test_resident_demo_check.py:90-106`.
No new tick for the all-code/SQL/helper/docs/tests consistency conjunction.

`infra/README.md:4114-4148` records assumption-labelled USD46/56 against
the original cutoff and overlapping January-only USD15.50/25.50, unchanged
USD700 cap and zero new resources/roles. No actual headroom/funding claim.
`infra/README.md:4069-4112` authors conditional credential/SQL renewal steps.
The original independent
`resident-authority-extension-521-review.md:187-230` in the 30 October
Review directory explicitly passes technical plan assessment, while retaining
separate exact-version/owner operational review. These are two source-only
documentation recommendations, not newly granted human/legal approval.

`infra/README.md:4150-4158` and #590/#545 retain exact live apply Pending.
No rotation, resident consent, live SQL renewal or result verification is
inferred from authored instructions or local tests.

### #530 and #531: preserve existing source ticks, no live completion

#541 supplies five bounded skills and general help.
`src/api/tests/test_chat_panel.py:90,123,165,175,275,330,345,358`
respectively tests cited labelled output, foreign-citation abstention,
workflow fallback, role/case recheck, all five/general, thread owner/scope,
reference-not-content audit and privacy enforcement.
#579 leaves actual local SQL/full API/browser execution unrun after lock
timeout; hosted MSSQL is not a local SQL result.
Do not tick #530's zero-based row 28 conjunction.

#538/#581/#604 supply static shell/panel/status/retry, simulated cold start,
HAX briefing distinctions/sources and unchanged reason/approval behavior.
`src/api/README.md:418` onward links the authored HAX/loading note;
`checks.loading_briefing_browser_check` is the maintained browser assertion
surface, with review dispatch preservation also tested at
`src/api/tests/test_case_journey.py:1595`.
Original citation/parser/startup and focus findings remain historical;
#604 records subsequent corrections without rewriting them.

#612's employee health observation is not employee UI verification:
independent directory attestation denied, zero employee sign-ins,
chat/map/case and first-time tabs/assets blocked. No new #531 live tick,
and no inferred screen-reader/voice acceptance for either issue.

### #533: local/source closure candidate, not deployed progress acceptance

#540 implements dashboard/archive; #582 strengthens checks; #607 carries
stock-scale fixture correction plus distinct verified execution evidence.
`src/api/tests/test_progress_dashboard.py:966` tests zero/one/exact/
last/beyond paging; `:1044` tests existing 60,000-home fixture progress and
filtered boundaries for JSON and inherited SQLite.
`src/api/checks/progress_browser_check.py:58` requires six table alternatives.
The scale browser compares six actual table/meter/API series, 45,000 archive
cases, combined-filter cohort, exact final five IDs, reload/URL and empty
boundaries.

`employee-progress-dashboard-533-correction-changes.md:65-83`
in the 31 October changes directory records two executed zero-skip scale
units, 1432-test API pass with 320 explicitly disclosed discovery skips,
actual local small/scale Chromium pass and 13 zero-violation axe reports.
`:112-127` preserves original Not accepted source and Blocked evidence-access
Reviews and links the separate evidence Review Complete/Conformant that
verified raw pass markers/hashes/skips. That is not relabelling adverse
history or inferring SQL Server/live execution.

All five explicit checklist criteria are now local/source supported.
The candidate `close` recommendation is narrow. #607's absent complete
exact-head receipt and live dashboard/archive acceptance remain separate;
the parent may retain the issue open for these broader gates.

### #550: shared thread/control/semantics, not resident consent acceptance

#556 shared widget and #568 refresh-state correction survive at:

* `src/api/src/zava_forward/api/web/chat-widget.js:3-60,109-180`.
* `src/api/src/zava_forward/api/web/chat.js:42-57,67,88-104`.
* `src/api/src/zava_forward/api/resident_demo/web/assistant.js:193-205`.
* `src/api/checks/chat_widget_browser_check.py:386-564`.

The browser assertions verify newline/no-request versus Enter send,
composition refusal, repeated Send, popup persistence, collapsed sources/
small AI label, disabled Attach/Voice with accessible reason, scrolling log
and fixed composer, retained draft/thread across closing, external focus and
nonmodal traversal. `:500-564` verifies delayed loading hidden at 199ms,
visible at 200ms, errors, keyboard/focus, reduced-motion animation refusal
and pinned axe. This is preservation of screen-reader semantics, not
screen-reader acceptance.

#568 reports failing-before regression now passing for 12 employee Enter/
Send refresh combinations. #562/#567 actual resident runs establish the
explicit honest-inability/housing-officer alternative, not actual generated
relevance. `src/api/tests/test_resident_chat_api.py:316-335` retains repair
routing and refusal of a mere home summary.

The caller forbids new resident-consent ticks, so row 16 stays unticked.
The negative technical data-use guard is documented at
`test_resident_chat_api.py:263-282`; it grants no real resident/works consent.
#565/#567 failed employee acceptance and #612 zero employee sign-ins remain.

### #551: all local rows, owner live acceptance remains an explicit gate

#553 moves original filter nodes, not duplicated independent state.
`src/api/tests/test_map_fullscreen.py:test_expanded_filters_reuse_and_restore_original_controls`
and `test_compact_filters_wrap_scroll_and_preserve_map_space` assert
original-node restore, aria-pressed/text selection, wrapping/scroll/map space.
#591 extends actual
`checks.map_fullscreen_browser_check.check_expanded_filters:84` with exact
API/rendered home IDs, Enter marker/open-home links, all six flag round trips,
header alternate/expanded restore and empty funding/support.

`employee-map-filters-551-changes.md:37-64,80-90` in the 30 October changes
directory records actual browser pass, 320/390/1280 plus short 390x568 and
enlarged text, full 1379-test API pass, 14 axe states zero violations with
14 contrast incompletes. No actual AT or whole-WCAG acceptance.
#553 explicitly requires owner live-site acceptance before closure;
#565/#567/#612 fail/block employee acceptance. Retain open despite four
local checkbox recommendations.

### #552: exact deck assets and actual rendered interaction, baseline gap

#554/#592 and `src/api/tests/test_case_journey.py:1289-1310` verify six
package-included icon files against exact PPTX media SHA256.
`:1312-1359` asserts short summary, complete safe detail, native button/
popover, missing-owner/action human route and no executable injected content.

`employee-single-case-view-552-changes.md:59-95` in the 30 October changes
directory records completed actual Chromium 156/Playwright 1.64 evidence,
1280/390/320 screenshots, ordinary 66.39px versus blocked 110.39px step
heights, bounded ceilings, complete keyboard/touch disclosure and enlarged
text. Tab/panel shared surface, adjacency, non-scrolling tab ancestry and
unchanged tab bounds with positive panel scrolling are asserted. Do not
confuse positive scrolling with reaching the panel end.

Five technical rows are supported. The combined Fluent/WCAG row stays open:
original independent Review Residual work RV-002 retains three scrolled
Resident contrast incompletes requiring named human assessment; RV-003
retains inherited UX debt. See changes `:105-119`.
No whole Fluent/WCAG, AT, live-owner or publication acceptance inferred.

### #563: model guards/labels/fallback are not live generated relevance

#564/#593 source/scripted evidence proves own-case prompt/routing and
label rendering, not actual-model relevance for an actually consented user.
`src/api/tests/test_resident_chat_api.py:263-282` asserts no fetch or any
provider/advisor call for missing/false/string permission across every
assistant/agenda shape. This is a negative data-flow test, not a newly
granted resident consent decision.
`:316-335,815-895` checks disabled/unavailable reasons, housing-officer
route and suggestion labels; shared widget `:146-163` preserves thin label/
collapsed sources.

#576 live enable attempt timed out, rolled back and read back off.
#585 telemetry B1 investigation is unresolved, not a successful AI repair.
#567/#569 resident off-state fallback was observed. #612 makes no question/
model/consent request. No new relevant-generated/live-proof tick.

### #570: sufficient runner cause and regression, live conjunction blocked

#574/#601 identify the display-email expected-identity predicate rejecting
valid rosterless Entra identities. The mapping/runner uses immutable tenant/
object/provider/role/view-only authority, not roster/display-email binding.
`src/api/tests/test_employee_identity_check.py:113-149` allows correct
rosterless identity with blank/alias display email; `:151-162` rejects a
different identity despite same display email; `:164-215` validates strict
expected IDs and source/provider/role/view-only schema.

#601 adds three maintained Chromium rosterless/wrong-account/map regressions
and later source-CI/local-gate requirements with zero-skip execution validation:
`src/api/tests/test_employee_acceptance_check.py:test_chromium_rosterless`,
`test_chromium_wrong_account`, `test_chromium_map_contract` and
`tools/test_rpi_checks.py:63-189`.
Preserve original cluster roundoff, already-open chat, hazard-filter
invariant and command-inventory findings, not merge-only dismissal.
#596 does not prove signed-in acceptance; #612 independent attestation is
denied and zero employee sign-ins means no live chat/map/case tick.

### #571: local prompt/check reconciliation closure candidate

#573/#609 keep complete recognized document/form questions and explicit
refusal of obsolete incomplete prompts.
`src/api/checks/resident_assistant_browser_check.py:333-391` retains
positive Survey/provision/warning/error/source/no-approval/cross-case
checks, then adds obsolete-prompt refusal/housing-officer/no-document-leak
checks. `src/api/tests/test_resident_chat_api.py:792-813` retains form
no-submission and protected obsolete-prompt behavior.

`resident-survey-check-571-changes.md:22-34,48-77` in the 31 October changes
directory records real red mismatch and recognized green result, full local
browser pass with 32 axe scans, focused three HTTP passes and 1430-test API
pass with 320 disclosed skips. Original lock/dependency failures and incomplete
axe findings remain. `tools/test_rpi_checks.py:250-295` retains single-copy
synthetic skip output and uncontaminated outer-suite accounting; the original
incorrect-two count finding is preserved and surviving assertion is one.

All three explicit source/local criteria are supported. `close` is only a
narrow reconciliation recommendation. #609's incomplete exact-head receipt/
live resident verification remains separate, not reported successful.

### #572: exact selected execution wired, no valid complete receipt

#575/#600/#606 retain exact selector at
`tools/rpi-checks.py:94-100,733-744,1689` and opt-in
`src/api/tests/test_chat_panel.py:563-564`.
#600 records actual local selected Chromium execution plus 39 tooling
regressions, preserving earlier unrun/adverse evidence.

`tools/test_rpi_checks.py:190-248` checks exact required command/browser
dispatch/opt-in. `:250-295` admits only exact general-discovery test/reason,
rejects unexpected/dependency/integration/browser skips and prevents outer
suite contamination. `:297-406` rejects missing flag/selector/execution and
requires exact runtime success evidence; `:407` onward recomputes receipt
skip evidence. #595 allowlist expansion is not the sole solution.

Do not tick the explicit full-gate conjunction: #600/#606 have no fresh
verified complete receipt. #612's long-path full gate blocks SQL and later
short-path full receipt fails after source/base movement. Hosted/selected-case
passes do not upgrade that receipt. Original #572 adverse receipt remains.

### #608: exact-main early refusal, full supported-path acceptance unproved

#610 equals audited HEAD.
`tools/rpi-checks.py:161-175` computes Linux 107-byte socket budget,
58-byte filesystem-encoded resolved output and actionable early refusal.
`tools/test_rpi_checks.py:602-626` actually binds AF_UNIX at 107 bytes,
rejects 108 and checks Unicode byte counting.
`:628-692` covers all/changed/resume long-path refusal before probes/lock/
Runner/output/receipt writes.
`:694-736` preserves resolved aliases, external/new output, no rejected
scratch, browser-free long paths and owned permissions.
`:738-764` preserves resume tools/source/receipt tampering refusal.
`:766` onward adds gate-owned TMPDIR fixture regression after the original
high fixture-boundary review finding. #610 reports 54 focused tests and
lint/format; a low critique-link finding remains, not relabelled clean.

Two technical recommendations only. #610 original Review Residual work
RV-001 explicitly leaves full browser/SQL unexecuted. #612 says an earlier
short-path run executed every group but the receipt failed because HEAD/
origin-main changed, and a later isolated exact-head run is still pending.
No accepted zero-skip complete supported-path evidence was supplied.

## Complete matched PR review and CI qualification ledger

The following summarizes all exact-reference PR snapshots used above.
`source+MSSQL` means the snapshot actually lists those successful hosted jobs;
it does not mean a fresh local full gate. Rubric-only success is not executable
coverage. Empty checks mean no supplied check evidence, not failure or pass.
Every original adverse finding remains distinct from successor evidence.

| PRs | Review/body qualification | Supplied checks |
| --- | --- | --- |
| #471 #472 #473 | Stacked, not main ancestors; #472 Not accepted SQL-padding and #473 focus/reservation defects; parent #474 integration required | Source jobs and MSSQL success |
| #474 | Parent source integration; missing parent gate, sensor SQL integration and assistant focus/reservation/logout concerns | Rubric only |
| #475 | Original Not accepted; later selection/resource corrections; full benchmark still unmeasured | Rubric only |
| #478 #479 | Partial/Not accepted deployment; unavailable positive authenticated/model proof and credential/SQL dependencies | #478 rubric; #479 rubric only |
| #525 | Original Partial/Residual work; cross-tab, proposal expiry, hazard and focus/draft findings; source-only synthetic callbacks, AT/scan incompletes | Source jobs/MSSQL success; rubric phases partly skipped |
| #534 | Exact-reference RAI documentation; stale narrative/privacy and relative-link findings, not runtime correction | Rubric pipeline, agent/detection/result phases skipped |
| #538 | Startup/async helper, citation attribution, focus/busy and loading defects; later corrections do not rewrite originals | Source jobs/MSSQL success; rubric phases partly skipped |
| #540 | Lifecycle/null history, reset/paging/accessibility and quadratic scan findings; latest complete local evidence unavailable at that time | Source jobs/MSSQL success; rubric phases partly skipped |
| #541 | Skills/role/audit source; late-answer/access-denial/length/nested-scroll defects, actual SQL/live acceptance missing | Source jobs/MSSQL success; rubric phases partly skipped |
| #542 | Resident activation failed and rolled back; no authenticated acceptance | None |
| #543 | Local missing documents_json sufficient cause, not Azure-cause proof; full publication gate missing | Source jobs/MSSQL success |
| #545 | Authorized docs-only deployment; January renewal and authenticated acceptance parked | None |
| #553 | Repeated-request false-pass/link concerns and short-landscape/live-owner acceptance gaps | Source jobs/MSSQL success |
| #554 | Icon package/selector defects and original unverified rendering RV-001; later local evidence is separate | Source jobs/MSSQL success |
| #556 | Shared widget; toggle/stacking/hover/scroll-follow defects, later #568 correction; AT/live not accepted | Source jobs/MSSQL success |
| #561 | Deploy/health evidence only; private operational evidence unavailable, no authenticated acceptance | Source jobs/MSSQL success |
| #562 | Resident-only actual Enter/Send/disabled controls/honest inability; rules only, employee not reached; runner overwrite/privacy/summary-marker findings | None |
| #564 | Scripted generation; mixed-intent/protected-question routing concerns; actual-model/live/AT unproved | Rubric only |
| #565 | Employee sign-in transition partial before verified identity; Not accepted | None |
| #566 | Redeploy, health/assets/anonymous constraints; AI activation off, broken evidence links | None |
| #567 | Resident fallback; employee identity mismatch; Not accepted; original publication prerequisite wording/link issues | None |
| #568 | Actual 12-combination Enter/Send regression; broad resident check baseline RV-003 retained | Rubric only |
| #569 | Redeploy includes #568, AI remains off; link findings | None |
| #573 | Prompt/check reconciliation, local units/browser/axe; live/AT not claimed; link findings | Rubric only |
| #574 | Identity predicate sufficient local cause; no live retry; link findings | Rubric only |
| #575 | Exact browser wiring; initial real selected/full evidence missing; one Copilot error review is not approval | Source jobs/MSSQL success |
| #576 | AI activation cost preflight failure, later enabled check timeout, verified rollback to off | None |
| #579 | Cross-store source tests; actual SQL/full API/browser unrun; evidence link findings | Rubric only |
| #580 | Evidence-only AI qualification; gate lock timeout/no receipt, links | Rubric only |
| #581 | Strengthened loading browser evidence; link findings | Rubric only |
| #582 | Progress browser/paging evidence; link findings | Source jobs/MSSQL success |
| #584 | Full comparable benchmark and final receipt absent; link findings | Rubric only |
| #585 | AI telemetry B1 remains unresolved; wrong log schema and broken links | None |
| #586 | Source decision qualification/evidence, acceptance unproved; link findings | Rubric only |
| #589 | Own-record document/routing work; failed full gate/no current eligible receipt | Rubric only |
| #590 | January source review; final old browser fixture cutoff and earlier view-batch findings; live owner confirmation pending | Rubric only |
| #591 | Actual local exact-home/header/narrow filter verification; link findings | Rubric only |
| #592 | Actual local case rendered evidence; human contrast/AT and full gate remain; link findings | Rubric only |
| #593 | Source/scripted generated routes and dock/resize; final browser/axe/live-model unrun at PR boundary | Source jobs/MSSQL success |
| #595 | Exact discovery skips, unexpected integration skips fail; evidence links | Source jobs/MSSQL success |
| #596 | Healthy redeploy/anonymous dock; Not accepted whole request, live employee and versioned cache/undock gaps | None |
| #600 | Actual exact Chromium case plus 39 tooling regressions; full receipt missing, links | Rubric only |
| #601 | Identity/action/map/CI/gate tests; initial roundoff/chat/filter/inventory defects; attested live user and full receipt unavailable | Rubric only |
| #603 | Authored scope/model decisions, sensor/chat local evidence; three gate failures before checks, manual/live acceptance open | Source jobs/MSSQL success |
| #604 | Loading/briefing current evidence; later link/CLI correction, owner CI publication exception, no full local or live acceptance | Rubric only |
| #606 | Gate baseline/skip fixture correction; no complete exact-head receipt, links | Rubric only |
| #607 | Original scale fixture defect, corrected source and independently verified local pass evidence; full/live acceptance still missing | Rubric only |
| #609 | Browser prompt fixture and synthetic skip isolation; original two-count defect, corrected current one-count contract; full/live unproved | Rubric only |
| #610 | Early path refusal and 54 focused tests; original high fixture defect resolved, low critique links remain; actual full browser/SQL unproved | Rubric only |
| #612 | Partial live resident geometry/assets, employee attestation denied; source/base-drift failed full receipts; driver aggregation/capacity/allowlist/check-continuity findings | Rubric pipeline, several later phases skipped |

## Validation and limits

Machine result validation checked all fifteen exact issue numbers/states,
79 original index/text pairs, correct existing checked flags, no proposed
new tick on an already checked row and no closure recommendation with an
unchecked/unproved row. All named implementation surfaces were read directly;
the initially guessed employee script name was corrected to existing
`src/api/src/zava_forward/api/web/chat.js` before final delivery.

This lane supplies evidence recommendations, not fresh UI/WCAG review,
regulatory currentness, source remediation, actual hosted-gate approval,
deployment, resident consent, human/legal sign-off or a valid full receipt.
Raw external historical logs were not reopened by this lane; their named
assertions/results and independently verified evidence are attributed to
committed records. No sensitive data, claims, credentials or private dataset
was accessed or reproduced. The parent decides final checkbox/closure actions.
