<!-- markdownlint-disable-file -->
# Review: Grant lifecycle controls #95

## Scope and Evidence

* Task ID: 95; Review date: 2026-10-17; assessment count: one.
* Branch: fix/grant-lifecycle-controls-95; HEAD/base d400eb8d, merged #383. Fresh gh inspection found no existing PR for this branch. All implementation changes are still uncommitted.
* Fresh source of acceptance: gh issue view 95 --json title,body,url, retrieved during this Review. Issue title: Grant opportunity, award, claim and cash states. Its two criteria are "No dashboard presents the opportunity amount as an award or cash" and "Only designated human financial authority submits, certifies or records receipt". The issue reports existing delivery with source and a second approver; those mechanisms were inspected, not presumed absent.
* Assessed boundary: final tracked implementation/documentation/configuration changes and both untracked test modules, relative to d400eb8d; complete current research/plan/details/critique/changes/state evidence.
* Plan: .copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md.
* Details: .copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-17/grant-lifecycle-controls-95-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-17/grant-lifecycle-controls-95-changes.md.
* Research: .copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md.
* State: .copilot-tracking/rpi-sessions/2026-10-17/grant-lifecycle-controls-95-state.json, read only.
* Requirement interpretation: current BRD FR-023/024 and RULE-009/010 are the grant requirements; the issue's BRD FR-019 pointer now concerns capacity. PRD FR-019/042 and AC-022/050 contain additional pack/version/export acceptance, explicitly outside this issue and not established here.
* Other sources: unchanged original case/addendum, KB index/memory; core/API guides and finance journey synthesis; grants.py, finance.py, store.py and existing SQL/auth/projection/rendering paths; supplied validation history. No private dataset or staff roster was opened.

## Opening Review State

* Interpreted review goal: independently assess existing and locally implemented grant lifecycle controls against freshly retrieved issue #95.
* Review scope: one full post-implementation Review of tracked and untracked source/tests and the complete grant-lifecycle-controls-95 artifact set, dated 2026-10-17.
* Evidence readiness: expected research, plan, details, critique, changes and state artifacts exist; comparison and independent checks are pending.
* Acceptance basis: no dashboard presents opportunity as award/cash; only designated human financial authority submits, certifies or records receipt. Opportunity/application/award/claimable/claim submission/cash remain distinct evidence, with GBP 40 million unverified.
* First comparison boundary: reconcile current plan and critique dispositions with final source and tests relative to d400eb8 (merged #383).
* Active read-only boundaries: write only this review record; do not change source, tests, plan, research, details, critique, changes or state. No delegation, private data, Azure/model calls, authority administration or real commitments.
* Initial blockers: none established.

## Execution Status

* Execution status: Complete.
* The complete supplied implementation boundary and all current artifacts were compared. Independent focused checks, actual local Chromium and a separate adversarial SQL identity probe ran. Completion means the Review executed, not that implementation is accepted.
* Persistent write ownership: this record only. Test-runtime scratch stayed inside the worktree and was removed; no test/source/artifact correction, commit, container, authority administration or second Review was performed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Failing-first probes; new core/API tests; isolated success-fixture adaptation | Reconciled | Both untracked modules were read and executed. No inherited finance test inflation: grant mixin/setup-only reuse is visible. Existing suites miss RV-001. |
| P01-T02 | Shared operation extraction; exact designation; grant/funding event provenance | Partial acceptance | Source exists and normal/refusal paths execute, but changing legacy identity handling regresses transaction-time independence; RV-001. |
| P01-T03 | Guides/KB, focused/full/SQL/browser/quality/migration evidence | Reconciled execution | Supplied broad evidence is distinguished from independent reruns below. The source digest repair is narrowly verified. |
| P01 / handoff | All implementation markers complete; independent Review next | Reconciled | Work ran; its pre-Review readiness claim is not acceptance. This Review now supplies an adverse outcome without mutating parent state. |
| Follow-Up Items | Full pack/export/version workflow and real delegation remain excluded | Reconciled | Separate owners/actions below; neither is silently added to active scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/tests/test_grant_lifecycle_controls.py; src/api/tests/test_grant_lifecycle_api.py | Isolated fictional identities, designation/state/currency/history/rollback/API/browser checks | Final untracked files inspected, JSON/SQLite/API/browser executed | Independent focused run passed; separate RV-001 probe exposes missing coverage | Meaningful tests, not proof of every claimed invariant |
| P01-T02 | src/core/src/zava_forward/core/grants.py | Existing ordered grants retained; exact state/case/scheme human exercise designation, per-event GBP/source/identity and legacy re-proposal | Actual state-machine and persisted-history assertions | Passed normal/denial/state/currency cases | Substantially delivered; shared legacy independence defect applies |
| P01-T02 | src/core/src/zava_forward/core/finance.py | Existing #94 lock/save/rollback boundary extracted; writer validation extended | Existing SQL writer hooks still present; no schema/payment executor added | Existing finance tests passed; fresh alias probe fails required control | RV-001, High |
| P01-T02 | src/core/src/zava_forward/core/store.py | funding_step resolves current staff and requires separate approve/submit/confirm evidence/designation history | Application and grant/provider-finance objects remain separate | Reopen/history/refusal/rollback checks passed | Delivered within narrow application-record scope |
| P01-T03 / PC-001 | src/api/src/zava_forward/api/web/app.js | Neutral application confirmation copy and visible evidence field | Real local Chromium exercised missing evidence and successful confirmation while grant remained Opportunity | Passed | No award/cash inferred by changed panel |
| P01-T03 | src/core/tests/dataset.py; src/core/tests/test_finance_signoffs.py; docs/reference/research/retrofit-synthetic-data/scenario-manifest.json | Only local success-fixture authority/evidence; refreshed actual public source digest | DATA assignment AST equals base; manifest differs solely by fixture SHA-256; actual hash matches | Eight manifest tests plus independent structural checks passed | No changed availability, approval or coverage claims |
| P01-T03 | src/core/README.md; src/api/README.md; docs/reference/research/ux/customer-journeys/finance.md; docs/reference/README.md; docs/reference/log.md; component pyproject.toml files | Contracts, scope limits, traceability and test typing exceptions | Diff inspected; KB log retains exact old prefix; original/addendum/memory unchanged | Diff whitespace and changed backend/test Ruff passed | Documentation readiness is qualified by RV-001; no unrelated feature change found |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/T02, PC-002/003/004/005/006 | Exact trusted designation, fresh UTC checks, application history, legacy re-proposal and path-owned tests | Research fail-before probes and compatible critique findings; no divergent decision required | Current plan, details and changes agree on schema, scope, transaction checks and recovery | One critique's original Revise remains visible; direct dispositions recorded | Direction is compatible; RV-001 is an implementation defect, not missing authorization for a new direction |
| P01-T03, PC-001 | Narrow UI copy/input plus real browser evidence replaced original research's no-web-change expectation | Critique found existing award wording; caller requires no opportunity promotion | Final plan/details/changes explicitly own changed panel and browser checks | Direct compatible disposition, not a redesign or expanded PRD acceptance | Justified |
| P01-T03 | Actual source digest refreshed after public test-fixture adaptation | Initial full core discovery failed two stale source-hash checks | Changes retains initial failure, eight manifest passes and clean full rerun; plan/details acknowledge repair | Tightly coupled integrity correction; no altered dataset coverage or material new decision | Justified and independently checked |
| P01-T03 | Browser route/cleanup and missing local migration package attempts corrected before successful runs | Reported harness/dependency failures | Changes distinguishes those failures from successful runs | No second critique or hidden scope expansion | Reported history retained; not independently replayed |

## Critique and Material Revision Assessment

* Original critique outcome remains Revise; this Review neither rewrites it nor treats disposition labels as implementation proof.
* PC-001: applied in neutral confirmation copy and per-event evidence input; mixed Opportunity/Confirmed case independently passed actual Chromium.
* PC-002: exact trusted dictionary, subject binding, permission action/state/case/route, effective interval and production refusal are implemented; role remains an additional gate. Request data cannot grant designation; no production seed/backfill or authority-grant endpoint was found.
* PC-003: require_authority uses fresh aware UTC at entry and repeats the predicate and snapshot check within SqlStore.save's writer transaction. Designation-only replacement and unchanged-snapshot clock expiry tests passed. Existing change/bulk/stock/safety/resident validation hooks remain in place.
* PC-004: funding approve/submit/confirm append separate supplied-reference, case, route, actor and designation events. Status/reference compatibility remains, without grant/provider-finance promotion. Reopened event assertions passed.
* PC-005: old completed history is not rewritten; missing-currency pending grants refuse and can be withdrawn/re-proposed. Unknown preparer refuses at entry. Current legacy identity behavior inside the transaction is qualified by RV-001.
* PC-006: test fixture isolation, semantic grant/application coverage, current actor/authority refusal, SQL failure diagnostics, prior legitimate audit preservation and rowversion checks are substantive. However, the missing legacy-preparer transaction rebind case allows the shared helper regression in RV-001. This disposition is therefore not fully achieved.
* No material divergent decision or unsupported early resumption was found. The defect fits the approved architecture and routes to implementation, not replanning or a human decision blocker.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Full PRD pack/form/version/export acceptance | Explicit issue/caller exclusion; current work only hardens recorded lifecycle authority and separation | Separate form/application workflow owner maps FR-019/042 and AC-022/050 to pack/version/export evidence | Remains distinct follow-up; not a missing active task or acceptance claim |
| Real company delegation and human acceptance | Trusted Synthetic exercise designation is not a real scheme of delegation, legal approval or staff acceptance | Owner/Finance authority owner supplies and verifies actual delegation before any operational adoption | Remains distinct follow-up; not a human blocker to correcting RV-001 |

Unresolved follow-ups do not become implementation defects or new active P01 tasks merely because they remain open.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Legacy preparer fallback is frozen before transaction validation

* Related scope: P01-T02; preservation of #94; PC-006 transaction-time alias checks.
* Evidence: src/core/src/zava_forward/core/finance.py:179-182 now appends the resolved preparer identity to the transaction context instead of preserving the original absent identity. validate_sql at lines 64-65 therefore does not repeat the registered-email fallback at write time. This changes existing finance approvals as well as new grant approvals.
* Exact reproduction: instantiate the existing SqlGrantChecks synthetic fixture; open a grant and remove only pending.identity while retaining its explicit GBP provenance (or propose a finance budget and remove proposed_identity). Wrap store.save so that, immediately before its original implementation starts the SQL writer transaction, the persisted preparer staff row's oid or code becomes the approver's corresponding identifier, without changing case sequence or approver identity/designation. Call grant_approve with the designated independent-by-old-snapshot approver, or budget_approve for the legacy finance budget.
* Observed independently: all four grant/finance x code/OID combinations commit; reopened grant is Opportunity and reopened budget is Approved, although persisted preparer and approver now share the identifier. A direct fresh registered-email _independent call with identity=None correctly raises PermissionError in all four cases, proving the transaction is checking the wrong retained provenance rather than the helper being unable to detect the alias. The first two OID probes also verified intact audit chains with success records. No source/test file was changed for these in-memory diagnostics.
* Impact: the changed helper regresses #94's current legacy fallback and permits self-approval under a transaction-time registered identity rebind. Newly captured immutable preparer identities are a separate, valid historical contract; the defect concerns records without a captured identity.
* Destination: rpi-implement.
* Smallest useful next action: retain unresolved-versus-captured identity provenance in the validation context so legacy fallback runs against current persisted staff inside the writer transaction; add grant and preserved-finance regressions for code/OID rebinding with unchanged case sequence and no success/audit leakage.
* Status: unresolved implementation defect, not a human blocker. No correction was performed by this Review.

Reproduction command from the worktree root, using only the existing fictional fixture and cleaning its own runtime files:

```bash
mkdir -p .copilot-tracking/reviews/logs/2026-10-17/grant95-runtime
TMPDIR="$PWD/.copilot-tracking/reviews/logs/2026-10-17/grant95-runtime" \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests \
.venv/bin/python - <<'PY'
import copy
import json
from unittest.mock import patch
from test_grant_lifecycle_controls import SqlGrantChecks
from zava_forward.core.finance import _independent

for path in ("grant", "finance"):
    for identifier in ("code", "oid"):
        f = SqlGrantChecks("test_legacy_pending_requires_reproposal_and_unknown_identity_refuses")
        f.setUp()
        try:
            s = f.store
            if path == "grant":
                f.grant(f.a, "grant_open", scheme="SYN-95", source="SYN legacy")
                with s.lock:
                    s._case("ZF-1")["grants"][0]["pending"].pop("identity")
                    s.save()
            else:
                s.finance_action(f.a, "ZF-1", dict(action="budget_propose", amount=100))
                with s.lock:
                    s._case("ZF-1")["finance"]["budget"].pop("proposed_identity")
                    s.save()
            original = s.save
            def save():
                changed = copy.deepcopy(f.a)
                changed[identifier] = f.b[identifier]
                s.db.execute("UPDATE staff SET body=? WHERE email=?",
                             (json.dumps(changed), f.a["email"]))
                original()
            with patch.object(s, "save", side_effect=save):
                if path == "grant":
                    f.grant(f.b, "grant_approve", id="GR-1")
                else:
                    s.finance_action(f.b, "ZF-1", dict(action="budget_approve"))
            state = f.record(f.open())
            try:
                _independent(s, f.b, f.a["email"], None, "approve")
            except PermissionError:
                print(path, identifier, "incorrectly committed; fresh fallback refuses",
                      state["grants"][0]["state"] if path == "grant"
                      else state["finance"]["budget"]["status"])
            else:
                raise AssertionError("Expected fresh independence check to refuse")
        finally:
            f.doCleanups()
PY
rmdir .copilot-tracking/reviews/logs/2026-10-17/grant95-runtime
```

## Defects

* RV-001: High, shared legacy-identity transaction revalidation regression; route to later rpi-implement.
* No other substantive in-scope implementation defect established. Passing normal cases do not negate RV-001.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent/coordinator assigns the already-authorized correction cycle ONE to preserve current legacy lookup and add grant/finance transaction regressions | Concrete in-scope implementation regression, not a research or owner-decision gap |

Later implementation does not require another Review. This record retains its original adverse verdict; this Review does not execute the correction cycle.

## Residual Work

* Full pack/form/version/export acceptance and actual verified delegation/human acceptance remain the two distinct plan follow-ups, with owners/actions above.
* No new residual work is manufactured from the implementation defect.

## Blockers and Remaining Work

* Review blockers: none.
* Acceptance blocker: RV-001 remains unresolved; this is fixable implementation work, not a human blocker.
* Remaining active correction: restore legacy-preparer transaction-time independence without weakening captured historical identities, scoped designation, SQL diagnostics or prior-audit preservation.
* Supplied state and changes correctly described a pre-Review stage. Their continuation/reconciliation belongs to the parent; this read-only Review does not mutate them.

## Validation Evidence

Independent checks used the worktree .venv/bin/python with PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests. Tests used only tiny fictional fixtures; local runtime files were removed.

| Command or check | Scope | Status | Summary |
| --- | --- | --- | --- |
| ZF_GRANT_BROWSER=1 .venv/bin/python -m unittest test_grant_lifecycle_controls.JsonGrantChecks test_grant_lifecycle_controls.SqlGrantChecks test_grant_lifecycle_api test_finance_match_controls.JsonFinanceChecks test_finance_match_controls.SqlFinanceChecks test_finance_match_api -q | Independent JSON/SQLite grant/application, preserved finance, authenticated loopback HTTP and actual Chromium | Passed | 60 tests, no skips, 33.108s. Expected API diagnostics explicitly report law store absent and rule checks unknown; not treated as legal-rule acceptance. |
| .venv/bin/python -m unittest test_finance_signoffs test_scenario_manifest -q | Independent existing signoff flows plus manifest integrity | Passed | 37 tests, no skips, 4.303s; 29 signoff cases plus eight manifest cases. |
| RV-001 in-memory SQL probe | Independent transaction-time registered legacy preparer code/OID rebind | Failed required invariant | Four of four combinations incorrectly commit; fresh fallback control refuses each. Success-state reopen is verified. |
| AST/base/hash comparison | Independent DATA AST, manifest and immutable documentation claims | Passed | DATA unchanged; only fixture SHA-256 changes in manifest and matches actual bytes; all other manifest claims identical; KB log is exact old prefix; original case, addendum and memory equal base. |
| .venv/bin/ruff check on finance.py, grants.py, store.py and both new test modules; git diff --check | Independent changed backend/tests and tracked whitespace | Passed | All checks passed. |
| Fresh web-interface-guidelines source retrieval and changed fundingPanel read | Independent changed web scope | Completed, qualified | Source retrieved successfully; native semantics/visible label/name/autocomplete/spellcheck/uncontrolled input and neutral confirmation reviewed. Shared pre-existing form behavior is disclosed below. No complete-app or WCAG acceptance. |
| Focused final 89-test run | Supplied implementation evidence | Reported passed; not this Review's single command | Independently reproduced the same 60 focused cases and 29 signoff cases in two commands; not claiming identical timing or a fresh unified 89-test run. |
| Actual Docker SQL Server 34 tests: 15 grant, 19 preserved finance | Supplied implementation evidence only | Reported passed; not independently rerun | Caller/changes report 162.730s and removal of task-owned loopback zf-grant95-ef8f1fc88d01 after owned database cleanup. No SQL container was created by this Review. SQLite reproduction is sufficient to establish RV-001 in the shared validator; no independent MSSQL result is claimed. |
| Full core discovery, final 724 tests with 35 skips | Supplied implementation evidence only | Reported passed; not independently rerun | 230.155s. Preserve earlier full-core failure: two stale manifest hashes; repaired actual digest and full rerun reported passing. Independent eight manifest tests and structural checks passed. |
| Full API discovery, 588 tests with 121 skips | Supplied implementation evidence only | Reported passed; not independently rerun | 347.576s; explicit skips retained, not silently counted as passes. |
| Final changed-label HTTP/browser 2/2 | Supplied implementation evidence, plus independent current browser execution | Reported passed / independently covered | Supplied 6.458s; actual current browser test also passed within the independent 60-test run. |
| Migration 25/25; core/API Ruff/check-format/mypy, 112/52 files | Supplied implementation evidence only except narrow Ruff above | Reported passed; broader checks not independently rerun | Caller/changes retain initial missing-package restoration history. No packages installed by Review. |
| Raw implementation logs | Caller-supplied locations outside permitted review file-operation boundary | Not read | Broader timings/results are attributed to caller/changes, not independently attested by inspecting raw logs. |
| Azure/model/private data/real finance/delegation/human acceptance/full PRD pack export/full WCAG | Explicitly outside boundary | Not run | No operational or full-product acceptance inferred. |

### Scoped web guideline evidence

Fresh source: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-17. Scope: changed fundingPanel lines 878-905 and its existing shared refresh/error behavior, not the complete application.

#### src/api/src/zava_forward/api/web/app.js

* src/api/src/zava_forward/api/web/app.js:884 - changed evidence input has a visible wrapping label, accessible name, meaningful name, autocomplete off and spellcheck false; native input/button behavior retained.
* src/api/src/zava_forward/api/web/app.js:887 - neutral application confirmation and explicit not-award/not-cash explanation passed actual mixed-state browser exercise.
* src/api/src/zava_forward/api/web/app.js:885 - existing shared refresh reports errors in the case status region, not field-inline with first-error focus; no pending spinner or unsaved-draft navigation guard is added. These shared pre-existing limitations prevent a complete fetched-guideline/WCAG conformance claim; they are not a new grant-authority defect or a reason to expand this task into a redesign.

## Outcome

* Outcome: Not accepted.
* Rationale: existing lifecycle delivery is real and substantially hardened. Exact opportunity presentation/separation has affirmative static, projection and actual browser evidence; GBP 40 million remains only unverified opportunity evidence. Designated current actors, exact scopes, production refusal, fresh UTC and event provenance have meaningful passing evidence. However, RV-001 materially regresses required #94 independence at the SQL write boundary for supported records without captured preparer identity. A Complete implementation/Review execution and green focused suites cannot override that reproduced defect.
* Severity summary: one High; no Critical, Medium or Low substantive in-scope findings.
* No real delegation is claimed. All references remain supplied/unverified, and synthetic exercise approval does not establish operational authority.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement, RV-001 | Parent/coordinator owns authorized correction cycle ONE; preserve this original record and use concrete regression evidence |
| Decision gap or invalid assumption | None established | No replanning/user decision required for the approved-direction correction |
| Material evidence gap | None blocking this verdict | Supplied broad checks explicitly distinguished from independent runs; no extra research required to establish the reproduced defect |
| Non-blocking residual work | Distinct existing plan follow-ups | Form workflow owner for full packs/export; owner/Finance authority owner for verified operational delegation and human acceptance |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: 97 independently passing tests in two focused commands, including actual Chromium; four independently reproduced failing legacy-independence scenarios; independent evidence-integrity/Ruff/whitespace checks. Broad SQL Server/core/API/migration/type results are supplied evidence, not independent reruns.
* Blockers: none to Review completion; RV-001 blocks acceptance and is routed implementation work.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md](.copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md) | Existing-delivery audit and baseline fail-before evidence |
| [.copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md](.copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md) | Current full implementation plan and separate follow-ups |
| [.copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md](.copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md) | Phase/task requirements and validation allocation |
| [.copilot-tracking/reviews/plans/2026-10-17/grant-lifecycle-controls-95-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/grant-lifecycle-controls-95-plan-critique.md) | Original Revise and PC-001 through PC-006 |
| [.copilot-tracking/changes/2026-10-17/grant-lifecycle-controls-95-changes.md](.copilot-tracking/changes/2026-10-17/grant-lifecycle-controls-95-changes.md) | Final implementation, validation and failure/repair history |
| [.copilot-tracking/rpi-sessions/2026-10-17/grant-lifecycle-controls-95-state.json](.copilot-tracking/rpi-sessions/2026-10-17/grant-lifecycle-controls-95-state.json) | Read-only parent continuation state |
| [.copilot-tracking/reviews/logs/2026-10-17/grant-lifecycle-controls-95-review.md](.copilot-tracking/reviews/logs/2026-10-17/grant-lifecycle-controls-95-review.md) | This task's one complete independent Review |

## Next Steps

Return this record to the active coordinator. The coordinator may invoke the separately authorized rpi-implement correction cycle ONE for RV-001; this reviewer stops without fixes, state changes, commits or another Review. Existing pack/export and real-authority follow-ups remain separate. No user clarification is required.
