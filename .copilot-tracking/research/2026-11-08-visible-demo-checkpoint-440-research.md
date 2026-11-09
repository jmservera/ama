---
title: Visible-demo integration checkpoint 440 research
ms.date: 2026-11-08
---

## Task identity and scope

* Task: `440-visible-demo-checkpoint`, slug `visible-demo-checkpoint-440`. Bounded continuation of original session `9dfa8bcc-4468-4888-be6a-d543c459c94f`. Earlier checkpoint topics (c96a, correction1) merged as #1281; this record does not reconstruct or backdate them.
* Worktree `/home/azureuser/source/ama-wt/issue-440-visible-checkpoint-1108`, branch `docs/visible-demo-checkpoint-440`, target `main`, clean at start.
* Research written 2026-11-08T19:56Z onward, before any repository implementation edit.
* Objective: one concise dated visible-demo integration checkpoint section in the existing `docs/architecture/cutover-evidence-pack.md`, plus index paragraph and an appended log entry. Docs only. Recurring #440 stabilization work after the #149/#229 UX wave and the owner-authorized employee model observation (#891). Not audit expansion or a benchmark.

## Pinned identities (observed 2026-11-08T19:55Z, read-only fetch)

* Branch base and `origin/main`: `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`, tree `0fddb514670c2e1e112f0eb284fdee9f9846c952`, parent `656cafb1`.
* `git diff --name-only 656cafb1 6354b13f7` and `git diff --name-only 6354b13f7 origin/main`: the first lists only `.github/rubric/scores/latest.json`; the second is empty. Confirmed by actual Git.
* PR 1286 `test(ux): integrate employee AI-state and document-control evidence`: MERGED `28c6ec11cbfc0185a756eb15cd9b324ab0856b94` 2026-11-08T19:38:09Z, head `0362e2626587153f367d1dab49c7d0f52611bcba`, 109 files changed (3,008 insertions), `gh pr checks` reports 19 passing.
* PR 1290 `docs(demo): record observed employee model answer and preserve chronology`: MERGED `656cafb1eca2813469cf0e8e60af3bfb31b619a6` 2026-11-08T19:44:02Z, head `5b6b965715d5192b323145574156bddedcb3e7ae`. It changes only `.copilot-tracking` records (10 paths): the #891 live and C1 research, plan, changes, review and state.
* Earlier #1281 (`e2ecee25`) is the previously merged checkpoint; #1285 recorded the VM demo release and guarded live check; #1284 qualified synthetic chat memory evaluation evidence.
* Open at observation: #440, #149, #229, #891, #157, #159, #81, #1274, #184 (Sensor simulator stage 2: live streaming into Azure IoT Hub), #1288 (`feat(quality)`: show retained sensor values and ground Quality AI review flags), PR 1240 (parent #81, head `6ef6dc36`, base `main`, open). Per-issue child delivery is not inferred from counts.
* `gh pr view 184` and `gh pr view 1288` do not resolve as PRs; both resolve as open issues. Their native candidates (#184 source c80f / tree 3f1d, #1288 C1) are coordinator statements, unmerged and not in main. Not verified here.

## Source movement since the prior checkpoint (actual Git)

* `git diff --name-only 608c98e6 6354b13f7 -- src infra .github/workflows tools` lists only `src/agents/src/zava_forward/agents/chat_eval.py` and `src/core/src/zava_forward/core/doc_controls.py` (plus tests, checks and READMEs under `src/`). The audited chat, assistant, isolation, privacy, thread, AI, registry modules and agents `chat.py`, `server.py` are byte-identical to 608c. The earlier source observations on those modules therefore hold at 6354, as source reading, not new execution.
* `chat_eval.py` (#1284): isolation memory assertions are scoped as component-only diagnostics (`COMPONENT_PROBE_SCOPE`), serving memory only as receipt-declared (`memory_scope`), and "integrated memory poisoning: not covered". This qualifies the earlier F2 observation (eval probe prompt differs from serving prompt); the probe/prompt mismatch itself is unchanged, now disclosed.
* `doc_controls.py` (#1286): refusal wording for legal-hold deletion and retention-trigger refusal now states that nothing was deleted, that retention values are demonstration values, and that a real hold needs the Legal delegate. Wording only; no authority change.
* Unchanged: `ai_registry.demo_activation_honoured` (needs `ZF_CHAT_DEMO_ACTIVATION` exact value and `ZF_DEPLOYMENT_PROFILE=demo`), `chat_admission` in `server.py` lines 48-58, `Assistants.review`, `REGISTRY` of five assistants.
* UI label: `src/api/src/zava_forward/api/web/chat.js` line 131 selects "Summary by rules, no record changed", "Model-generated, not approved. Demo only." or "Workflow-only help, no record changed". The employee browser check `src/api/checks/employee_chat_browser_check.py` line 288 asserts the model label against a controlled provider, not a real one.

## Mandatory reading performed in this iteration

Honest ranges, nothing beyond:

* `docs/case_study_48_original.md`: all 49 lines.
* `docs/reference/memory.md`: all 67 lines (context only, not evidence).
* `docs/case_study_48_addendum.md` (1,987 lines): lines 1-148 (purpose, status, resident proposal, additions) and 1481-1580 (where agents fit, five-capability table, Decision 1 design) read in full; the heading map (all `##`/`###`) listed. Other ranges not read in this task. Earlier sessions recorded other ranges separately.
* `docs/reference/README.md`: lines 1-60 and the c96a/correction paragraph region located by grep; not read end to end.
* Existing pack: heading map, the full c96a section lines 3092-3214 re-read, including Correction 1.
* Issue #440 current body from the coordinator file `issue440-current-2000.json` (data only): criteria 1-6 are ticked; criterion 7 (triage of findings into issues) and criterion 8 (genuine RPI artifacts and independent review in the PR) are unticked. Not changed here.
* PR 1286 and PR 1290 public bodies; `891-5b6b-independent-assessment.json` read as data.
* Component guides were not re-read this task. The component facts used are direct source reads listed above.

## Original brief, document-qualified requirements and approvals

* Original case study (unchanged, 2026-09-10): five agents with autonomy levels Stock Prioritisation L2 recommend; Assessment L3 drafts, retrofit coordinator approves; Grant and Funding L3 drafts, finance submits; Contractor and Resident Coordination L3 acts within resident preferences; Quality Verification L4 autonomous flags; resident consent and the asset director approving investment.
* Addendum (blob `28c1924285eed255e53c1e359e0ad98eedab1d22`, `ms.date` 2026-11-08, proposals not approved requirements): the current five-helper service has a recommendation and evidence-preparation boundary; fuller L3/L4 behaviour is scope or authority gaps (lines 15-26). Deterministic core versus agent value table, lines 1481-1560. AI must not diagnose, decide duty satisfied, release a hold, approve, infer consent, commit capital, accept quality or contradict a resident from sensor absence.
* BRD 0.21.0 draft blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 in-review blob `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0004 blob `9406c2e747ced91e5ba7be4072f9482293c0c38f` accepted by owner 2026-10-15 option C staged (decision issue #158); ADR 0002 Proposed, ADR 0006 Accepted. Draft and in-review documents are not approved. No DPO, Legal, HR, control-owner or RAI approval exists in this evidence.
* BRD and PRD IDs already traced in the prior checkpoint (FR-044, AC-084, RULE-018/022/025/028 and the AI authority rows). They are reused by reference to the existing section, not re-derived; this checkpoint adds only the visible-demo and sensor-exclusion joins below.

## Evidence classification (prepared)

* Local observed (this session): Git identities and diffs above; source reads; PR/issue states. No tests run.
* Local observed historical, source-qualified: PR 1286 candidate fd48 selected API 76 OK, Core 19 OK, Atlas 194 and Data 100 Chromium passed with two axe scans zero violations on Data; raw mypy API 195, Core 269 success; Ruff API 121, Core 216; 212 matching installed production files at fd48. Exact `0362e262` assessment Pass; 19 hosted checks passed on that head; merged tree matched the prepared projection (coordinator reports, PR body). Not new-tree, assistive-technology or whole-issue acceptance.
* Azure observed (historical, coordinator-reported): one generic synthetic employee question to the deployed demo app source `e2ecee2565e86889c6beb43cb32e7c5b54270e01`, revision 0000027: HTTP 200, `azure-openai`, `workflow_only` false, `model_calls` 1, outcome answer; UI disclaimer and model label visible; displayed token count 375. First-party identity attestation reported; identity, token and account values are not copied. Two earlier navigation failures and retrospective original report chronology are adverse qualifications; C1 made zero new calls. Not current-main deployment.
* Implemented-unverified: five-agent substantive case-grounded answers, the employee model path against real case sources, per-call cost/privacy/retention/refusal conjunction (#891 criterion 2 unticked).
* Deferred or blocked: sensor-grounded Quality AI (#1288), live IoT receiver/sender (#184), parent #81 integration, assistive-technology and human usability, named professional approvals.
* Unknown: current-main deployment state; whether later main moves alter the demo.

## Adverse and limiting findings

* One model answer proves one generic answer only. It does not prove five agents, case-grounded Quality inference, full refusal/privacy/retention acceptance or approval.
* Historical fd48 evidence ran on a candidate before ordinary merge and later main moves. Hosted 19 checks are for head 0362; nothing transfers to later heads beyond actual Git diffs.
* The PR 1286 native record named fd48 as the immediate first parent incorrectly; the PR body qualifies this additively. Record that qualification, do not rewrite.
* The recommendation-ordering defect said to be diagnosed in #81 could not be verified: a search of the #81 body and comments for "recommendation", "order", "sort" and "ranking" found no such diagnosis, and a search of open and closed issues for "recommendation ordering" returned nothing. It is therefore not linked and no issue is created.
* No additional defect was confirmed by this research. No reproduction was run.

## Recommendation (proposed)

Bounded CONTINUE: the existing employee demo and the independent source corrections for #184 and #1288 proceed in their own sessions. Sensor-grounded Quality and whole-agent acceptance, and closure of #149, #229, #891, #157, #159, #81 and #440, wait for actual source fixes, integration, separately admitted activation and observed journey evidence. No pivot, deferral, relaxation or approval is granted here.

## Planning readiness

Ready. Research disposition: executed. Next: plan and prospective critique, then commit research and plan before any implementation edit.

## Gates

* Independent exact-head assessment, hosted checks and human or named approvals are coordinator or owner work. Nothing here states approval or publication.
