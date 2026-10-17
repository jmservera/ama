<!-- markdownlint-disable-file -->
# Review: hazard-referral-controls-85

## Scope and Evidence

* Task ID: 85.
* Review date: 2026-10-17.
* Review scope: one independent post-implementation assessment of the supplied
  hazard-referral workstream, fix/hazard-referral-controls-85 against b5d4c840.
* Assessed boundary: new hazard.py; hazard methods in workflows.py; additive
  sqlstore.py hook/guard and directly necessary transaction/recovery context;
  canonical hazard tests, API tests and MSSQL adapter; component READMEs and
  existing knowledge synthesis/index/append-only log.
* Research: .copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md
* Plan: .copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/hazard-referral-controls-85-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/hazard-referral-controls-85-changes.md
* Other evidence: original case, bounded addendum/index/memory/sector primer,
  exact PRD FR-015/AC-018/AC-038 and BRD FR-003/RULE-003 anchors, canonical
  current-actor helper, JSON save/audit and SQL transaction/recovery paths,
  supplied permitted sanitized suite logs, independently executed tests and
  the RV-001 fictional probe.
* No finance.py/quality.py implementation, other worktrees, private datasets
  or historical rosters were read. No nested agents, commits, network writes,
  source/plan/state/changes edits or additional review artifacts were made.

## Opening Review State

Assess exact issue criteria and bounded hazard evidence/current-actor correction.
P01/P02 markers and details reconciled to passing targeted/static and actual
task-owned SQL results. P03 Review/publication remains open by design.
Acceptance basis: four original issue criteria, preserved external ownership,
plan identity/atomicity requirements and PC-001/002/003 direct dispositions.
First comparison: canonical hazard.py/workflows/sqlstore scope against
fail-before/final tests and documented evidence boundaries. Read-only source;
only this canonical review record may be written. No initial blocker.

## Execution Status

* Execution status: Complete.
* Review execution evidence: the full supplied boundary and all five canonical
  input artifacts were compared once. Independent tests and the RV-001 probe
  completed. This describes assessment execution, not acceptance of the result.
* Implementation markers P01/P02 remain as supplied; Review did not mutate
  completion claims. P03 publication is intentionally pending and is not a
  missing-source defect.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01 | Current Actors and Trustworthy Evidence | Reconciled with one material defect | Seven mutations use the new scope, identities are retained and SQL revalidates subjects. Post-commit failure is incorrectly treated as uncommitted recovery; RV-001. |
| P02/P02-T01 | Documentation and Integration Evidence; Commands, Results and Failed Attempts | Reconciled with validation coverage limit | Existing JSON/SQLite/HTTP behavior and exact manifest audit pass independently. Parent actual SQL/static/full-suite results are distinctly attributed. Failure tests omit the reproduced post-commit interleaving. |
| P03/P03-T01 | Independent Review/delivery remain | Reconciled | This record supplies the one independent Review; parent owns authorized correction, reconciliation and publication. No publication or independent acceptance is invented. |
| Follow-Up Items | Blockers and Follow-Up Items | Reconciled | External operational ratification and verified-service/live/human evidence remain separate; they do not explain away RV-001. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/hazard.py; src/core/src/zava_forward/core/workflows.py | Reuse canonical registered actor lookup; separately bind destination; retain historical identities; scope failure handling | Every existing hazard mutation enters decision_scope; receive/accept/repair/timing compare persisted receiver identity; release compares normalized email/code/OID against reporter and repair recorder | Canonical JSON/SQLite and API tests passed independently | Identity correction is supported; SQL post-commit recovery is not acceptable, RV-001 |
| P01-T01 | src/core/src/zava_forward/core/sqlstore.py | Add hazard validation inside writer transaction and suppress eager discard while hazard scope owns recovery | Exact diff adds only named import/call and hazard-context guard; existing validators and transaction ordering are retained | Parent full core/API and actual MSSQL reports; independent SQLite failure/authority tests | Additive integration preserved, but hazard wrapper must distinguish commit state |
| P02-T01 | src/core/tests/test_hazard_referral.py; src/api/tests/test_hazard_api.py; src/api/tests/test_mssqlstore.py | Formalize caller/destination/receiver/alias and backend-specific failure evidence using canonical reuse | Nine added core semantic methods, one HTTP method and three MSSQL method bindings; no removals, within 12/3 budget | Independent 41 core/manifest tests and four HTTP tests passed; parent MSSQL 16/one skip reported | Good pre-commit coverage; no post-commit synchronization case, RV-001 |
| P02-T01 | src/core/README.md; src/api/README.md; docs/reference/research/ux/zava-forward-prototype-profile-review.md; docs/reference/README.md; docs/reference/log.md | Document evidence integrity correction and external limits in existing documents | Scoped diff preserves service ownership, provisional authority and JSON partial-outcome limitation; log change is append-only | Direct Markdown/link review and git diff --check passed | Appropriate scope and caveats; SQL failure/exactly-once assurance needs reconciliation with RV-001 |

### Four-criterion meaning assessment

* Create/link only: raise/refer retain human source/awareness and external case
  reference. No external hazard closure, category decision, transport action or
  statutory clock calculation was added. The observation labels are not a
  transfer of service categorisation authority.
* Separate evidence: sent, received and accepted have distinct evidence,
  timestamps and history; acceptance requires receipt. Sender follow-up remains
  until acceptance. Current registered caller and separate eligible destination
  are rechecked inside SQL save's writer transaction. Stored receiver identity
  prevents recycled-code substitution.
* Affected-home hold and accountable release: scope is server-created Home and
  case_id; the recorded accountable role is retained. Repair and acceptance
  evidence precede a distinct eligible person's recorded release decision.
  Normalized historical email/code/OID matching blocks aliases. No time or
  state automatically releases the hold; sibling, consent and building gates
  remain independent. RV-001 concerns erroneous recovery after an otherwise
  valid release has committed, not release without an accountable actor.
* Visible external times: response due/actual and resident-update due/actual
  remain externally supplied, unknown when absent and available in projected
  detail/HTTP lifecycle, including later updates after retrofit restart.
  No new browser claim is necessary or made for unchanged web source.
* These are record-only engineering mechanisms. Actual service receipt,
  professional judgement and release sufficiency are not established by a
  synthetic caller, successful HTTP response or retained role label.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/P02-T01, destination subject | Add separate fresh destination and writer-time validation; bind receiver identity | PC-001; existing current-designated-staff intent, no new user decision required | Functional requirements, acceptance, details and code/tests agree | Critique Revise directly dispositioned | Compatible revision implemented; caller refusal does not substitute for recipient evidence |
| P01-T01/P02-T01, JSON ordering | Save before success/emergency audit; restore known pre-save failure and annotate post-save audit failure | PC-002; supported JSON separate-file behavior, no new persistence subsystem | Plan/details/changes/README and canonical tests distinguish JSON from SQL | Direct compatible revision | Supported by independent passing pre-save and post-save tests |
| P01-T01/P02-T01, SQL pending baseline | Capture prior pending audit before staging, quarantine before recovery and preserve original errors/context | PC-003; eager-discard branch, no changed user direction | Plan/details and supplied failures agree for uncommitted errors | Direct compatible revision; no material scope expansion | Only partially satisfied: new blanket restoration replays a committed baseline, RV-001 |
| P02 validation execution | Correct fixture paths, component selector, HTTP test lock and expand failure subcases | Changes record's failed attempts; no business-decision change | Successful commands separated from failed attempts; final narrower results identified | No fresh planning/critique needed | Evidence is candid; failed imports/selector are not relabelled as passes |

## Critique and Material Revision Assessment

* PC-001 High: explicitly dispositioned and implemented. Separate destination
  validation and transaction-time removal/role/OID/email substitution are
  exercised with the other subject valid; persisted receiver identity is bound.
* PC-002 High: explicitly dispositioned and implemented. JSON pre-replacement
  failure does not emit success audit; post-save audit failure retains durable
  state and adds uncertainty notes/logging. This is not SQL proof by analogy.
* PC-003 Medium: plan disposition is explicit and uncommitted failure branches
  pass; implementation is incomplete at the commit boundary. RV-001 is a new
  implementation defect in that accepted direction, not a new decision gap.
* All three revisions clarify existing intent without significant divergence.
  Plan and details consistently name the corrected requirements before their
  completed implementation evidence. No unaccepted material revision or
  premature dependent-work resumption is evidenced by the supplied artifacts.
* Research's opening "In progress" and changes' early "Next" wording describe
  earlier history; their final readiness/completion/handoff sections reconcile
  current P01/P02 state. They do not prevent a credible comparison.
* Changes' count of two adapter methods is imprecise: the actual adapter binds
  three canonical SQL methods, still within the explicit three-method budget.
  This is not a substantive implementation finding.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Operational responsibility, release authority and timing/escalation ratification | Fictional role mappings and observations cannot establish company delegation, legal interpretation or professional approval | Named Repairs/Safety/Housing owners must ratify policy before operational activation | Open distinct external follow-up; no active-plan defect or invented approval |
| Verified service transport and Azure/model/human acceptance | This authorized task is local engineering; synthetic references are not independently verified delivery/receipt | Integration/platform owners and designated human approvers must run authorized real-service/platform acceptance | Open distinct follow-up, not evidence that RV-001 is deferred |
| Browser/WCAG acceptance | No web source changed and no accessibility acceptance was performed | Existing UX/accessibility acceptance owner retains separate real-user/conformance work | Existing boundary retained; no new UI task or claim |

Unresolved follow-ups remain outside active P01/P02 completion and acceptance.
No plan revision, external legal research or operational ratification is needed
to correct RV-001.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Post-commit SQL synchronization failure replays committed prior audit

* Related scope: P01-T01 SQL failure/pending-baseline contract; P02-T01;
  PC-003. This is local evidence integrity, not an external ratification gate.
* Evidence: src/core/src/zava_forward/core/hazard.py:47,56-65 decision_scope restores
  its pre-operation pending baseline on every exception. However,
  src/core/src/zava_forward/core/sqlstore.py:591-593,620-630 save commits state/audit, clears
  pending/touched and then calls _sync when another writer advanced the global
  sequence. A failure of that post-commit read reaches hazard recovery despite
  the operation already having committed. _discard(pending) then restores audit
  that was included in that successful commit, and outer lock exit appends it
  a second time through _discard at sqlstore.py:632-636 and outer _finish.
* Independent reproduction: installed worktree Python, canonical
  SqlHazardReferral tiny fixture, ready_for_release, two connections to its
  disposable SQLite database; stage one prior_event under the outer lock;
  immediately before the real release save, use the second connection to log
  contact on ZF-2; inject a one-shot OSError in _sync following COMMIT. The
  original OSError returned without outcome notes. Durable reopen showed
  released=True, safety_released once and prior_event twice. The audit hash
  chain remained intact, so hash verification does not detect the semantic
  duplication. Probe exited 0 after asserting those observations and cleaned
  its fictional files. No production source or test was modified.
* Impact: normal concurrent work plus a transient post-commit read failure can
  report failure after releasing the home hold and silently duplicate an
  unrelated already-committed audit entry. This contradicts the exactly-once
  prior-audit requirement and omits explicit persisted-outcome uncertainty.
* Destination: rpi-implement, active parent, authorized bounded correction.
* Smallest useful next action: distinguish failed/uncommitted transactions
  from committed operations whose subsequent synchronization failed. Do not
  replay an already-committed pending baseline; retain the original error and
  explicitly annotate/log the committed or uncertain outcome. Extend the
  canonical failure matrix with this interleaving and durable reopen, retain
  additive shared-hook discipline and all existing refusal/recovery assertions.
  This worker does not implement, close or re-review the finding.

## Defects

* RV-001 High: newly introduced unconditional pending-baseline restoration can
  duplicate committed audit after post-commit SQL synchronization fails.
* Complete severity set: 0 Critical, 1 High, 0 Medium, 0 Low. No other
  substantive implementation defects were identified in the supplied boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 High | rpi-implement | Active automatic parent; use authorized bounded correction to distinguish committed from uncommitted recovery and add the canonical interleaving probe | Defect in accepted local evidence-integrity direction, not a policy or research gap |

Later implementation does not require another Review. Parent self-verification
must not be reported as this independent worker closing the finding.

## Residual Work

* Distinct external operational and real-service/platform/human acceptance
  follow-ups remain open as assessed above. No new active implementation scope
  is created by retaining them.
* The parent still owns P03 artifact reconciliation and authorized
  commit/push/main PR publication. Nothing was published by this worker.

## Blockers and Remaining Work

* Review blockers: none; assessment completed with sufficient evidence.
* Acceptance blocker: RV-001, a reproduced local implementation defect.
* Remaining active work: parent-owned authorized correction/reconciliation,
  then P03 publication; preserve this adverse assessment and its evidence.
* No external evidence or owner clarification is required to act on RV-001.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| From src/core: TMPDIR="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests ../../.venv/bin/python -m unittest test_hazard_referral test_scenario_manifest -q | Independent canonical JSON/SQLite hazard and exact manifest audit | Passed | 41 run, one explicit JSON-only skip, 11.316s. No private data or manifest refresh. |
| From src/api: TMPDIR="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_hazard_api -q | Independent authenticated loopback HTTP lifecycle and revoked-session check | Passed | Four run, no skips, 4.562s. Expected unavailable-law-store logging retained; not statutory-rule acceptance. |
| Installed Python stdin probe, same core environment and canonical SqlHazardReferral setup | Independent RV-001 post-commit synchronization interleaving | Failed control, reproduction passed | Returned original OSError, no notes; reopened hold released, one safety_released, two prior_event entries, intact audit chain. Exit 0 asserts these adverse observations. Fictional files cleaned; no test added. |
| git diff --check | Scoped worktree changes including review | Passed | No whitespace errors. |
| Supplied permitted core-tests.log and api-tests.log summaries | Parent full core/API discovery, not independently rerun | Passed as reported; summary inspected | Core 726/21 skips, 374.295s; API 658/184 skips, 332.451s. Full core preceded final test-only matrix expansion. Existing ephemeral scale generation is disclosed, not private historical-stock evidence. |
| Supplied final-core-targeted.log and final-api-targeted.log | Parent final focused regressions, not independently rerun in full | Passed as reported; summaries inspected | Core 168/20 skips, 45.677s; API 39/no skips, 26.194s. Earlier wrong-selector run remains a failed attempt. |
| Changes record: configured ruff check ., ruff format --check ., mypy in core/API | Parent configured static gates, not independently rerun | Passed as reported | Mypy 112/53 files; final core checks repeated after test expansion. Attribution does not establish RV-001 conformance. |
| Changes record: final task-owned actual loopback SQL Server run; canonical MssqlHazardReferral adapter inspected | Parent actual SQL semantics, authority and pre-commit failure/recovery matrix | Passed as reported; not independently rerun | 16 run, one JSON-only skip, 28.452s. Parent reports separate-connection changes and exact-container cleanup. Review did not inspect excluded session scripts or create a database/container. RV-001 was independently reproduced on SQLite only; actual MSSQL reproduction is not claimed. |
| Web/browser, Azure, actual model, verified external transport, operational/human approval and WCAG | External acceptance | Not run | No changed web source or authority for these activities; neither successful local tests nor parent SQL parity supplies this acceptance. |

### Reproduction mechanics for RV-001

The executed probe reused SqlHazardReferral.setUp and ready_for_release without
editing tests. It held store.lock, staged prior_event, wrapped store.save to
commit a second connection's unrelated ZF-2 contact before calling the original
save, and wrapped store._sync to raise a one-shot OSError only after that
interleaving was armed. Entry synchronization remained unmodified. Thus the
failure occurred in real save's post-COMMIT catch-up path, not in an invented
transaction implementation. Hazard recovery's next _sync succeeded. Outermost
lock exit flushed the restored baseline, creating the duplicate. Durable reopen
and action counts, not in-memory state alone, established the result.

## Outcome

* Outcome: Not accepted.
* Outcome rationale: basic four-criterion mechanisms, actor binding, normalized
  independence and tested uncommitted/JSON failure behavior are supported.
  Nevertheless RV-001 reproduces semantic audit duplication and an unannounced
  committed release behind an error response, violating the current accepted
  SQL failure contract. Passing suites do not cover or negate that defect.
* This verdict is local engineering acceptance only; it does not establish or
  remove any external operational, professional, legal or platform prerequisite.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Active parent, authorized correction of RV-001; preserve adverse record |
| Decision gap or invalid assumption | None | No divergent decision was required or found |
| Material evidence gap | None | Enough local evidence exists to route the reproduced defect without new research |
| Non-blocking residual work | Distinct external follow-ups | Repairs/Safety/Housing ratification; integration/platform/human and existing accessibility acceptance owners |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: independent 41 core/manifest and four HTTP tests passed;
  independent post-commit fault probe failed the intended control. Parent
  broad/static/actual-SQL evidence remains explicitly attributed.
* Blockers: RV-001 blocks acceptance; no blocker prevented review execution.
* This is the one independent assessment. No correction, second assessment or
  independent closure was performed by this worker.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md](.copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md) | Compared research and original defect evidence. |
| [.copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md](.copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md) | Compared current requirements, markers and follow-ups. |
| [.copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md](.copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md) | Compared backend failure matrix and task evidence. |
| [.copilot-tracking/reviews/plans/2026-10-17/hazard-referral-controls-85-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/hazard-referral-controls-85-plan-critique.md) | PC-001/002/003 and direct dispositions assessed. |
| [.copilot-tracking/changes/2026-10-17/hazard-referral-controls-85-changes.md](.copilot-tracking/changes/2026-10-17/hazard-referral-controls-85-changes.md) | Compared completion, failed attempts and parent validation. |
| [src/core/src/zava_forward/core/hazard.py](src/core/src/zava_forward/core/hazard.py) | New actor, persistence and independence scope; RV-001. |
| [src/core/src/zava_forward/core/workflows.py](src/core/src/zava_forward/core/workflows.py) | Assessed hazard-only mutations and existing four-criterion behavior. |
| [src/core/src/zava_forward/core/sqlstore.py](src/core/src/zava_forward/core/sqlstore.py) | Additive hook/guard and commit/recovery context. |
| [src/core/tests/test_hazard_referral.py](src/core/tests/test_hazard_referral.py) | Canonical semantics and reused tiny probe fixture. |
| [src/api/tests/test_hazard_api.py](src/api/tests/test_hazard_api.py) | Authenticated real-loopback evidence. |
| [src/api/tests/test_mssqlstore.py](src/api/tests/test_mssqlstore.py) | Inspected canonical MSSQL adapter. |
| [src/core/README.md](src/core/README.md) | Compared core contract and evidence limits. |
| [src/api/README.md](src/api/README.md) | Compared API contract and evidence limits. |
| [docs/reference/research/ux/zava-forward-prototype-profile-review.md](docs/reference/research/ux/zava-forward-prototype-profile-review.md) | Existing hazard engineering synthesis. |
| [docs/reference/README.md](docs/reference/README.md) | Existing task-routing update. |
| [docs/reference/log.md](docs/reference/log.md) | Append-only knowledge-base entry. |
| [.copilot-tracking/reviews/logs/2026-10-17/hazard-referral-controls-85-review.md](.copilot-tracking/reviews/logs/2026-10-17/hazard-referral-controls-85-review.md) | One completed independent assessment; RV-001 High retained. |

## Next Steps

No user action is required. Return this Complete / Not accepted assessment to
the active automatic parent. The parent should continue through the authorized
rpi-implement correction for RV-001, reconcile its evidence and publication
state, and preserve this independent finding without claiming this worker
implemented, re-reviewed or closed it. External follow-ups remain distinct.
