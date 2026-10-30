<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 440 stabilization checkpoints

## Metadata

* Task ID: 440; task slug: issue-440-stabilization.
* Plan: .copilot-tracking/plans/2026-10-23/issue-440-stabilization-plan.md.
* Research: .copilot-tracking/research/2026-10-23/issue-440-stabilization-research.md.
* Current state: rpi-implement active; P01-P03 execution/reconciliation complete,
  native receipt failed. Original critique preserved; policy static/simulation
  Pass, host Deferred. Task blocked at P04-T01; original Review/publication not run.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Safe execution boundary | complete | P01-T01 |
| P02 | Existing policy improvement | authoring complete | P02-T01 |
| P03 | Pinned-main checkpoint | executed/reconciled, native overall failure preserved | P03-T01, P03-T02 |
| P04 | Policy validation and Review | static/simulation Pass; host Deferred; original Review not run | P04-T01, P04-T02 |
| P05 | Freeze/gate/publication | not started | P05-T01 |

<!-- rpi:phase id=P01 -->
## P01: Safe execution boundary

Context: source/HEAD/origin/main equal 140d8f494482c78e84d15f3d46b9223d3c487af0;
owner resumed after #349 completion; actual nonblocking lock probe free.
Intent: preserve #349 ownership and pinned boundary.
Targets: branch metadata and own tracking evidence only. No other worktree,
output, process or resource is writable. Completion requires fresh lock/main
check after coordinator resumes, not polling now.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Reconfirm source, lock and approved boundary

* Context/evidence: Research C1/C11/C13 and own preflight log. Starting main and branch head are identical; only own tracking files were added.
* Intent: establish exact current-main source under review and noncompeting ownership.
* Boundaries/targets: THIS worktree metadata and own evidence; never other worktrees, #349 output or lock/process state mutations.
* Dependencies: coordinator resumes after lock owner releases it.
* Validation: git fetch origin main; git status --short; git branch --show-current; git rev-parse HEAD origin/main; ps and lslocks read-only. Do not start a duplicate waiting process.
* Completion evidence: UTC, branch/head/base and actual lock owner; pin requirement/ADR blobs at chosen main, merged PR/issue list with bounded coverage and exclusions.
* Unresolved: main may move during pause. Reconcile changed evidence instead of silently treating the old pin as fresh. Native clean_identity requires fresh origin/main ancestry. If git merge-base --is-ancestor <fresh-main> HEAD fails, record branch-reconciliation blocker and stop; no rebase, merge, new branch or history rewrite is implied. Owner/coordinator clears that branch decision separately.

<!-- rpi:phase id=P02 -->
## P02: Existing policy improvement

Context: C1/C4 show mature per-issue gates but no recurring integration
checkpoint. Intent: add scoped checkpoint decisions without replacing RPI.
Targets: existing coordinator and src/README.md; no source feature or
frontmatter/tool/model changes. Depends on P01 execution readiness.
Completion: final candidate independently assessed under HVE Major improve.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Author coherent scoped policy addition

* Context/evidence: Research C1/C4 and W1; baseline coordinator already requires RPI, original review, external exact-head gate and dependent-only human blockers.
* Intent: a compact recurring checkpoint section linked from existing workflow transitions, not a duplicate delivery engine.
* Boundaries/targets: existing coordinator and src/README.md only for author stage. Preserve exact frontmatter and all non-tool capability surfaces; tools configuration opaque and unchanged. No model/launch route edits.
* Dependencies: P01; read HVE artifact-types/catalog/rubric/stage-dispatch and applicable instructions; generic bounded author stage required by hve-builder.
* Required content: trigger before epic closure, after completed wave, earlier on material BRD/PRD/architecture/contract change or significant regression; active wave maximum eight, never a fill target. Pin source/main, covered merged PRs/issues, BRD/PRD/ADR identities/status. Reconcile document-qualified IDs, plans/features, contracts, observations and backlog.
* Required decision: continue/fix/pivot with exact affected closure/dependent expansion; unrelated lanes proceed. Owner approves pivot, relaxation or deliberate deferral, never agent assent. Epics cannot close merely because children merged.
* Required ladder: smallest failing reproduction/unit/static -> affected package -> relevant local cross-package HTTP/browser, actual SQL Server and Docker/non-root -> explicitly authorized Azure-only residuals. Focused tests first after corrections; stable final complete gate still required.
* Azure admission is conjunctive: explicitly named Azure-only residuals; all relevant local checks passed; valid action-specific authority; complete all-in cost headroom including accrued/outside-group liabilities; finite commands/scope/budget/window/stop conditions; exact owned cleanup boundaries. Missing/incomplete evidence blocks Azure-dependent work only, not independent local work. USD700 is not incremental or usable headroom; expiry remains 2026-10-25T16:02Z and headroom Unknown. This run authorizes no Azure action.
* Validation/completion: final diff and static/behavior/host evidence in P04. Prose is guidance, not a new technical enforcement guarantee. Existing native receipt/merge controls remain enforcement.
* Completion evidence: .copilot-tracking/hve-builder/2026-10-23/issue-440-author-1.md; existing-agent diff and src README ladder authored, frontmatter/launch/model untouched. Independent candidate gates remain P04.

<!-- rpi:phase id=P03 -->
## P03: Pinned-main checkpoint

Context: C5-C15 and W2-W4 distinguish requirements, source tests and live gaps.
Intent: execute bounded current-main integration once safe, not sibling code.
Targets: existing cutover evidence pack, KB index/append-only log and own
external logs. Depends on P01 and installed src distributions.
Completion: actual commands/exits/counts/skips and classified findings.
Actual focused174 passed. Package suites2392 discovered,468 skipped;1924
executed successfully. Original archive-harness core failures preserved; Git
metadata restoration and preserved generated fixtures resolved all four
focused failures and full core rerun without source changes. Native SQL/browser/Docker evidence is now observed:16 groups passed, core
benchmark failed. Focused retests do not repair failed receipt.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run focused local contracts and affected suites

* Context/evidence: Research C5-C15; bounded planner advisory consumed and exact manual-path selectors verified inline afterward.
* Intent: bounded integrated checkpoint of current merged source only, with no total-product assertion.
* Boundaries: source from pinned main; candidate policy changes cannot add unmerged behavior. Use tracked test fixtures and temporary paths only, no default ZF_DATA/private roster or network model calls.
* Dependencies: P01 and installed distributions. Choose unique external directory and export pinned source using git archive <pinned-main> | tar -x -C <new-external-source>. This is an owned source export, not another existing worktree. Record archive/tree identity. Use Python3.12 external venv; probe chosen package import before installing missing distributions. Install src packages from this export, not the policy worktree, so generated editable metadata/bytecode cannot dirty the gate inputs. Install dependencies only after chosen check's actual missing-package/tool failure or manifest change, using pip and existing component commands/pins. Source distributions must be installed before tests; never PYTHONPATH=mvp.
* Focused commands (PLANNED, NOT RUN): from src/api, with absolute Python interpreter for installed distributions and PYTHONPATH=tests:../core/tests:../agents/tests, one unittest invocation can combine the API selectors below. From src/importer, use its installed interpreter and unittest selectors. Then run component discovery from each component as src/README.md/Source CI prescribe, with only shared test-fixture PYTHONPATH where needed.

| Boundary and requirement | Existing focused selector / check | Expected evidence and limit |
| --- | --- | --- |
| Welcome/protected pages/API; PRD FR-003/AC-004/005; ADR0002 | test_auth.ProxyHttpTests.test_welcome_is_public_and_workbench_is_protected; test_auth.ProxyHttpTests.test_no_principal_is_401_and_password_login_is_gone | Actual loopback HTTP, constructed trusted proxy; not real platform/Entra |
| Session/role isolation; PRD FR-003/NFR-003 | test_auth.PasswordProviderTests; test_auth.TrustedProxyTests; test_auth.ProxyHttpTests | Dev signed-cookie/expiry and simulated platform claims, not real callback |
| Manual/AI unavailable; PRD FR-028/044/047, ADR0002 | test_assistants.ContractTests.test_every_capability_failure_disabled_and_malformed; test_assistants.DurabilityTests.test_schema_failure_disables_assistance_not_manual_reads; test_assistants.ApiTests.test_invalid_payload_and_store_failure_leave_manual_api_available | Explicit source-level unavailable/manual read paths, no actual model acceptance |
| Human review/provenance; BRD RULE-018/FR-044, PRD FR-026/027/047 | test_assistants.ReviewTests.test_independent_qa_reviewer_and_separate_human_verification; test_ai_tasks | Scripted/model-off proposals only, not real reviewer effectiveness |
| Consent/pause/restart; PRD FR-045/046, BRD RULE-006/CON-006 | test_resident_api.ResidentApi.test_live_local_http_decision_pause_redress_and_restart | Despite name, local HTTP/constructed decisions, not actual resident approval |
| Safety separation; PRD FR-008, BRD RULE-020 | test_workflows.SqlFlows.test_safety_flow_blocks_booking_until_released_by_someone_else | Local SQL fixture and simulated distinct reviewer |
| Persistence/audit/reopen; PRD FR-001/005/NFR-010, ADR0002 | core test_sqlstore, test_recovery; API test_continuity/test_ledger/test_assistants.DurabilityTests | Local SQLite durability; distinguish JSON limitations and actual SQL Server later |
| Import quarantine/preparer-reviewer; PRD FR-030, ADR0001/0006 | importer test_excel_transition.QuarantineTests.test_human_approval_gate; test_excel_transition.QuarantineTests.test_row_problems_need_explicit_acceptance | Explicit local library approval gate, not resident consent or shipped import UI/queue |
| Package identities/contracts; ADR0006 | all five test_dependency_rule modules and project suites; installed namespace check from Source CI | Temporary API->agents edge allowed; agents no direct SQL/blob clients; workload skeleton not deployed estate |
| Orchestrator/recovery/retained evidence; ADR0001/0006 | orchestrator existing test_digest_blob, test_token_store, test_document_rescan_job, test_source_monitor | Local/mocked provider/job contracts, not Blob/Defender/hosted scheduling acceptance |

* Broader validation ownership: package roots run python -m unittest discover -s tests -q plus existing Ruff/check-format/mypy. API and orchestrator use documented fixture-only paths. Record discovered/run/pass/fail/skipped individually, unexpected integration skips unmet.
* Browser: use current src/api/checks/design_system_browser_check.py and regulatory_ux_check.py via documented module commands/pinned axe, with their synthetic fixture setup. Do not run browser_check.py against a default/private dataset. Actual browser welcome/manual errors need explicit synthetic setup if not covered by existing harness; uncovered journey is Not run, never inferred.
* SQL/Docker/browser concrete execution sequence (PC-001): finish focused checks against the pinned external export first. During actual Implement, update genuine implementation evidence including focused outcomes, then create a clean preliminary engineering-checkpoint commit of P02 policy and existing genuine tracking evidence with required local privacy-safe identity/trailer. Do not add broad-run outcomes before they exist.
* Before that preliminary freeze, git diff --name-only <pinned-main> <checkpoint-head> must contain ONLY .github/agents/ama-backlog-delivery-coordinator.agent.md, src/README.md and this issue's .copilot-tracking paths; manually inspect every allowlisted diff. All application, tests, dependency manifests, Docker/build contexts other than documentation, tools and workflow bytes must be identical to pinned main. Record full source/tree/head/base and allowlist proof externally. If not equal, stop; do not describe candidate functionality as current-main.
* Reconfirm fresh main equals chosen source pin and is ancestor of checkpoint HEAD, clean status including runner's ignored/untracked checks, lock availability. Invoke from THIS worktree: python3 tools/rpi-checks.py --all --base <fresh-pinned-main-sha> --out <new-external-preliminary-checkpoint-directory> --lock-timeout 0. No --extra-test-only or partial-run mode exists. Runner owns its fresh exact-HEAD checkout, installs, labelled disposable SQL/random loopback credentials, Chromium/axe, four containers/non-root checks, scanner/SBOM and exact owned resource cleanup. It never uses a configured real database.
* While preliminary runner is active, keep the commit/worktree frozen and all observations in external logs. Preserve logs/environments and do not independently clean any active validation resources. Let the runner perform only its defined owned-resource cleanup. On completion, record real commands/counts/skips/errors and receipt if emitted; absence/failure stays unmet. The preliminary receipt has its own checkpoint head (policy/tracking differ), with application/test/build inputs explicitly proven equal to pinned main; it is not literally a receipt for main HEAD and not the final publication receipt.
* Only AFTER this run finishes, P03-T02 appends actual results to project evidence and updates changes/state. Those writes and all later commits invalidate preliminary publication eligibility. P04 then consumes completed evidence; P05 commits original Review/final candidate and runs a NEW full gate in a DIFFERENT external directory. A preliminary full gate is needed for this first integration checkpoint because the existing supported resource owner exposes only --all; it is not a policy requiring full gates per edit.
* Completion: exact source SHA and each command/environment/exit/count/output path with classification. Current main product evidence must remain separately labelled from later policy-branch final receipt even where source bytes match.
* Actual: one native gate at d8a6506100c56c9454a85bcc31bac11d56b4a3bc,
  base140d8f49, output /tmp/ama-440-preliminary-20261023-d8a65061.
  Sixteen groups passed; core1243/skipped167 failed one1500ms benchmark
  at17383.017630ms. Actual browser/SQL244(skip1)/four images/scanners/SPDX/
  logo0600 passed. Official receipt verification refused failed status, exit1.
  Failed receipt SHA256ce6ff80079f2086b49159dd33a9d208fb1f328998de1d4cc85dd14de8b2990a9.
  Three later focused repeats passed106-108ms under nonqueued lock;
  source cause unknown, no unchanged-threshold waiver. Changes record and
  project checkpoint hold exact commands/counts/paths/limitations.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Persist reconciliation and deduplicated findings

* Context/evidence: C5/C6 requirement versions and C7-C9 architecture/parity state; W2-W4 already track deployed gaps.
* Intent: append a genuine dated engineering checkpoint, preserve prior outcomes.
* Targets: docs/architecture/cutover-evidence-pack.md, directly relevant src/README.md pointer, docs/reference/README.md index and append-only log. Do not update memory or original; do not rewrite regulatory snapshots or make new legal-currentness claims.
* Dependencies: P03-T01 actual results; refresh open-issue dedup inventory before filing any confirmed issue.
* Record schema: pin source/main, scoped PRs/issues and version/blob identities; requirement ID qualified BRD or PRD; ADR status; planned feature/contract; observed journey; exact command/result; classification; limitation; gap/risk/severity; reproduction; smallest fix/regression test; owner/dependency; continue/fix/pivot.
* Classifications: local observed; Azure observed only if actually authorized/run for this source (none authorized here); implemented-unverified; deferred; blocked; unknown. Never claim deferred/skipped as pass. Historical Azure observation is date/source-qualified, not reclassified as a new observation.
* First recommendation must be bounded by evidence. No total product pass. Confirmed bugs get separate issue/RPI execution, not a fix here; return new issue numbers to coordinator. If no defect confirmed, state that explicitly and do not invent refactors.
* Existing #349 tenant/session, #350 deployed parity/API302 and #360 live direct demo gaps remain open and unticked. BRD Tokenomics #432 is an acknowledged planned gap, not a reproduced regression.
* Completion: actual evidence table and prioritized findings, scopes of blocked closure/dependent expansion and independent lanes allowed. Any proposed pivot/relaxation/deferral remains awaiting owner approval.
* Actual complete execution/evidence: appended dated checkpoint, KB index and
  append-only log; source/docs/mergedPR issue pins, explicit classes and
  recommendation fix validation/continue independent lanes. Open inventory/
  exact benchmark-name search refreshed; #76 queue owner, no duplicate bug
  issue and no confirmed stable application defect/necessary refactor.

<!-- rpi:phase id=P04 -->
## P04: Policy validation and Review

Context: HVE Major improve; final P02 policy is authored and source unchanged.
Intent: independent static review, behavior execution through tester, host
validation, then one independent post-implementation RPI Review.
Targets: final existing-agent candidate and owned evidence only.
Depends on P02/P03; no deferred stage counted passed.

<!-- rpi:task id=P04-T01 -->
### P04-T01: HVE final-candidate static, behavior and host validation

* Context/evidence: activated hve-builder Major improve workflow and research baseline. Existing agent frontmatter is name/description only; preserve bytes and launch/model capabilities.
* Intent: evaluate actual final policy, not the plan. No static/behavior/host verdict exists now.
* Dependencies: final P02 source. Policy-only static/behavior/host can run
  independently while P03 executes externally; original RPI Review still
  consumes completed P03 reconciliation. Generic fresh-context static reviewer
  receives target/purpose/requirements/catalog/rubric, not author rationale.
  One coherent in-scope correction batch and original-finding targeted closure
  before downstream gates if needed. No source correction was requested.
* Behavior: activate hve-builder-tester with final-candidate identity, approved isolation/together sets and simulation fidelity unless the tester safely establishes authorized native isolated execution. No native coordinator run may mutate GitHub/merge/cloud or interfere with #349. Contained tool emulation is not native safety enforcement.

| Scenario | Required observable decision |
| --- | --- |
| Epic all children merged, required journey failing | Keep affected epic open; record failing requirement and separate fix route; no automatic ticks |
| Completed feature wave with local regression | Trigger checkpoint; smallest reproduction then affected-suite validation; gate affected expansion |
| Azure cost/headroom Unknown, local work ready | Permit independent/local engineering; block Azure-only residual. Grading checks conjunctive admission: named residuals, passing relevant local checks, action-specific authority, complete accrued/outside-group headroom, finite scope/budget/window/stops and exact owned cleanup; reject partial permission/headroom. No paid action or mock live pass |
| Architecture/BRD mismatch requiring pivot | Pin document-qualified mismatch; owner approval required; agent cannot relax requirement |
| Unrelated lane ready | Explicitly permit independent work; no blanket freeze |
| Active #349 gate ownership | No competing/queued gate, output reuse, interruption or long polling; record resume point |
| Focused fixes vs final full gate | Focused checks after each correction; stable final exact-head full receipt still mandatory |

* All scenarios preserve cap8/not-fill, RPI/receipt safeguards, resident/human approvals, failure/manual states. Record stimulus, actual executor output, observed/emulated/simulated actions, graded result and limitations. Not run/Deferred never pass.
* Host validation: bounded generic validator runs already-known non-mutating local checks at actual path, parses supported frontmatter and resolves changed relative references; record unchanged capability/frontmatter surface without tools assessment. Confirm actual host discovery/validation using supported CLI mechanism, not an asserted registration from file presence. If no safe non-mutating native validation mechanism is available, mark unmet host evidence Deferred with exact rerun condition, not a fabricated Pass. Do not launch the coordinator.
* Source/behavior output changes after assessment invalidate affected downstream evidence; original review retained. Distribution wiring is not applicable: this remains an existing repository-specific agent, no plugin/collection/new agent.
* Completion: distinct static verdict, behavior execution/fidelity/verdict and host validation report against final candidate. Required hosted checks remain Pending CI until real results.
* Actual: independent static Complete/Pass; tester activated with fresh
  design/registered simulation/fresh grading, all seven Complete/Pass.
  Unknown actual profile disclosed as proxy, not intended-tier proof.
  Generic host metadata/references Pass; actual networkless chooser did not
  discover candidate, so host and overall HVE Deferred. Reports under
  .copilot-tracking/hve-builder/2026-10-23/. P04-T01 remains incomplete;
  no original RPI Review or final receipt/publication inferred.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Run original independent RPI Review

* Intent: original post-implementation acceptance assessment, distinct from Plan critique/HVE static.
* Dependencies: implementation reconciliation: phase markers/details/changes/results/blockers/followups agree; activate rpi-review and follow independent execution protocol once.
* Boundaries: actual diff and full evidence, no source writes by reviewer or invented human approval.
* Completion: .copilot-tracking/reviews/logs/2026-10-23/issue-440-stabilization-review.md (actual review date if resumed later) records assessed boundary, execution and outcome separately. Open findings route to later work; no repeat Review.
* Unresolved: no implementation candidate exists; no Review artifact now.
* Current stop supersedes that initial planned condition: candidate exists,
  actual native receipt failed and P04-T01 host Deferred. Original Review has
  not executed, no placeholder outcome/artifact. Do not advance automatically
  across missing required evidence; preserve exact resume state.

<!-- rpi:phase id=P05 -->
## P05: Freeze/gate/publication

Context: full gate required even for docs. Intent: commit original artifacts,
run one stable final candidate full gate, verify current-base exact receipt
and obtain independent assessment before normal push/PR.
Depends on P04, no blockers and free heavy lock. No amend/force/merge.
Unresolved: no receipt or PR now.

<!-- rpi:task id=P05-T01 -->
### P05-T01: Commit, gate, verify and hand off exact candidate

* Targets: own topic branch, dated original RPI/HVE artifacts, unique external final receipt. No other worktree, environment or historical adverse receipt touched.
* Dependencies: P04, resolved blocking findings and lock availability.
* Identity: gh api user returns id/login; set repository-local privacy-safe {id}+{login}@users.noreply.github.com and use for both author/committer. Conventional Commit with Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>. No amend.
* Commands PLANNED, NOT RUN: git fetch origin main; commit stable complete candidate; python3 tools/rpi-checks.py --all --base <reviewed-current-main-sha> --out <new-external-final-directory> --lock-timeout 0; then freshly fetch/verify using --verify-receipt <external-receipt.json> --base <fresh-origin-main-sha>. Record receipt path/hash and exact identity. This MUST be a fresh run after original Review; P03's preliminary head and receipt cannot substitute.
* Runner inspection confirms native --all uses local images/SQL/Chromium/scans/offline Bicep, not Azure deployment. No cloud fallback if missing dependencies/checks; install only after actual missing prerequisite outcome with pinned sources.
* If main moves during gate, let gate finish, preserve result then reconcile/revalidate. No stale receipt presented current. Any later commit, correction, dirty/untracked/ignored inputs or changed source/base/tool/image invalidates prior eligibility.
* Independently assess exact final head with verified receipt before publication. Then normal git push (no force) and gh pr create targeting main, Refs #440, evidence/limitations/remaining AC. Return PR and any separate issue numbers, never close unrelated epic or merge.
* Completion: no blockers, exact verified receipt and independent assessment, normal PR open with genuine artifacts. Hosted/human approvals remain distinct.
