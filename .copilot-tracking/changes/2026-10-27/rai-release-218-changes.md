<!-- markdownlint-disable-file -->

# Changes: rai-release-218

Date: 2026-10-27; task #218; automatic ordered loop.

## Scope and Decisions

Executing P01-P02 of the bounded plan, then independent P03 Review/publication.
Original critique Revise retained; PC-001 applied through mapping/order probes.
No actual manifest approval, evaluator implementation, participants, live
appointment, Azure action, ranking change or acceptance tick is authorized here.
P03 publication remains pending until evidence reconciliation and Review.

## P01: Release Binding

P01-T01: three regression methods ran before source changes and produced five
assertion failures: ranking binding, checklist binding, mapping-only binding,
mapping-order binding and stale default-bound stock capture.
Command (from src/api, session venv Python):
`PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_assistant_release.DependentPolicyRelease -q`.
An initial root-directory attempt failed import; rerunning from the documented
project directory produced the actual five behavior failures above.

P01-T02: assistant release policy includes current ranking policy_hash or the
quality-owned checklist/mapping fingerprint as applicable; retained priority
binds the same ranking hash. Other capabilities retain their previous policy
binding. Stock capture now explicitly resolves ranking.CURRENT. No policy rules,
resident data, role grants or actual release records changed.

## P02: Validation and Oversight

Missing editable distributions reproduced with system Python; session-owned
venv created, pip installed editable core/agents/API with declared dev extras.
This environment reads only public synthetic fixtures under temporary paths.
No shared environment was modified.

### Executed local checks

All commands below use the session-owned venv Python/tools, with installed
editable packages. They use constructed temporary stores only.

| Check | Command / directory | Observed result |
| --- | --- | --- |
| Failing first | src/api; `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_assistant_release.DependentPolicyRelease -q` | Before fix: 3 methods, 5 failures |
| Initial binding lifecycle | Same selector after fix | 7 methods passed |
| Integrated release/oversight/incident/challenge | src/api; `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_assistant_release test_assistants.HumanReviewMechanics test_assistants.ReviewTests test_continuity test_continuity_epoch_export test_operator_suspension test_resident_api -q` | 166 run, 129 passed, 37 environment-gated skips, 202.851s |
| Final new regressions | src/api; `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_assistant_release.DependentPolicyRelease test_assistants.HumanReviewMechanics -q` | All 12 passed, 24.160s |
| Core static | src/core; `ruff check . && ruff format --check . && mypy` | Pass; 100 formatted files, 153 type-checked source files |
| API static | src/api; same commands | Pass; 46 formatted files, 88 type-checked source files; final two supplemental tests also Ruff-clean |
| Agents static | src/agents; same commands | Pass; 19 formatted files, 23 type-checked source files |
| Agents suite | src/agents; `PYTHONPATH=tests:../core/tests python -m unittest discover -s tests -q` | 105 passed, 58.982s |
| Core suite | src/core; `PYTHONPATH=tests python -m unittest discover -s tests -q` | 1429 run, 1243 passed, 186 skipped; 841.211s |
| API suite | src/api; `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` | 1131 run, 817 passed, 314 skipped; 919.253s |
| Whitespace | root; `git diff --check` | Pass |

Two supplemental test methods (untrusted declared ranking hash and retained
priority accept/edit denial) were added after broad discovery began; the final
twelve-test selector covers their actual final source. No production change
was made after the suites began.

Expected missing-law-store, synthetic rollback/cleanup and malformed-release
diagnostics are negative-fixture output, not unhandled test failures. SQL Server
opt-in skips are not passes. Browser, native SQL Server/container, actual model,
Azure and human participant checks are not claimed. No full gate is run and no
heavy scoped gate is justified by this small three-module production change;
the owner's one allowed scoped invocation remains unused.

### Scope evidence: #219 / PRD FR-051, AC-069

| Issue criterion | Evidence and remaining boundary |
| --- | --- |
| Absent/expired/model/prompt/policy/data/permission mismatch causes zero provider calls | Existing TaskReleaseRecord/Release/Legacy regressions plus actual dependent-policy mutations; fresh/proactive/queued zero-call checks pass |
| Missing evidence, owner/manual route visible and denial retained | Existing release negative tests pass; no actual authority is supplied |
| Approved matching exercise record permits bounded proposals only | Constructed matching renewal generates and accepts a proposal without a domain write; actual approved evaluation/release evidence remains unavailable, so whole criterion is not proven |
| Material use/model/prompt/policy/evidence/permissions change invalidates dependents | Existing BOUND, prompt, evidence renewal and task-contract tests plus new actual ranking/checklist/mapping/order tests; queued denial, in-flight quarantine, ready/verified/accepted reliance denial, retained priority review denial and superseded-record rollback all covered locally |
| OQ-017 authority named or gap stated | Gap remains explicit in registry, denial and component documentation; no invented holder |

### Scope evidence: #222 / PRD FR-054, AC-073, NFR-014, OQ-018

| Issue criterion | Evidence and remaining boundary |
| --- | --- |
| Approved paired manifest covering completeness/contact/appointment factors | Blocked: corrected proposal in open PR #421 is not merged/approved; no evaluator or labels authored here |
| All seeded unjustified exclusions/deprioritisations detected | Not run against an approved manifest; no detection claim |
| Cohort counts/errors/burden/uncertainty reconcile | Not run; no success-shaped aggregate or fabricated uncertainty |
| Small/missing samples remain insufficient | No evaluation sample or sufficiency approval supplied; remains insufficient/unproved, not zero-error success |
| Exceeded/unapproved thresholds block activation pending human disposition | No threshold approval supplied; absent release evidence remains denied, but a dedicated cohort-evaluation/threshold integration is not implemented or claimed |
| Owner-approved lawful cohorts/fields/thresholds before live use; synthetic not fairness | OQ-018 decisions remain unknown; no live use or fairness claim |

### Scope evidence: #223 / PRD AC-070, FR-026/027, NFR-009

| Issue criterion | Evidence and remaining boundary |
| --- | --- |
| Seeded critical defects detected/prevented from controlled gates | Script rejects wrong/unsupported/incomplete/stale proposals; no case/control writes; competent human detection remains unmeasured |
| Reviewer/source/reason retained | Synthetic actor, source snapshot/signature, note, original output and corrected output persist across reopen in new mechanics tests |
| Detection/corrections/total effort against identical workflow-only scenarios | Actual paired human study Not run; scripted checks do not measure preparation/review time or comparative effectiveness |
| Default acceptance/citation validity alone cannot pass | Direct accept without source verification denied; explicit false attestation can still accept semantically wrong text. Negative control preserves this unresolved human-effectiveness boundary |
| Automation-bias test; reviewer authority/evidence defined | Scripted false-attestation negative control executed. Competent independent reviewer, participant protocol approval and OQ-017 authority remain unfilled, not invented |

There are no participant counts, human detection rates, corrections-per-hour,
effort savings or release scores to report. All such results are Not run, not
zero. The twelve new tests are development regressions, not held-out evaluation.

### Scope evidence: #221 / PRD FR-053, AC-072; BRD RULE-020/024

| Issue criterion | Evidence and remaining boundary |
| --- | --- |
| Incident/threshold breach blocks dispatch and pending/ready reliance | Existing continuity/operator-suspension constructed regressions pass; actual threshold monitoring acceptance not inferred |
| Versions/scope/owner/evidence/containment/impact/remediation retained | Existing retained snapshot, malformed evidence and reopen regression coverage passes |
| Manual/emergency/statutory hazard routes independent | Existing synthetic manual-hazard drill passes; no hazard clock/consent change in this patch |
| Restart requires corrective tests and distinct authorized human approval | Existing negative matrix and constructed distinct-capability drill pass; actual authorized competent corrective-test acceptance remains unavailable |
| Breach names RULE-024 restart authority | Constructed authority reference and explicit unavailable actual OD-35/OQ-017 state retained; no actual appointment |
| Suspension/manual fallback drill tested | Automated constructed drill covered; actual named independent human witness/drill acceptance remains Not run |

### Scope evidence: #220 / PRD FR-052, AC-071

| Issue criterion | Evidence and remaining boundary |
| --- | --- |
| Digital and staff-recorded non-digital constructed challenges | Existing core and HTTP retained-priority tests cover digital/phone/letter/in-person routes; broader assistant/form coverage remains unimplemented |
| Permitted explanations/owner/next update/resolution visible | Existing retained-priority tests cover these fields; not whole-system coverage |
| Only dependent proposals/reviews stale | Existing source/policy/exact-version/cross-case challenge tests; broader assistant/form dependency handling remains unproved |
| No consent/refusal/sanction/unrelated closure/hazard-clock inference | Existing challenge negative-boundary tests preserve case state; no new domain writer |
| No retaliation/inferred refusal/delayed hazard response | Existing constructed state-invariance and independent hazard-route checks; representative resident/human/live acceptance not established |

### Epic closure and decisions needed

All issues remain Refs. Existing checked issue criteria are not changed and no
new whole-issue criterion is ticked. #218 cannot close: #224 and #440 are outside
the requested delivery list and remain open; children are not all closed or
owner-deferred. Actual approved evaluations, OQ-017 named holders, OQ-018 lawful
analysis/threshold decisions and competent/witnessed review remain unavailable.
RAI engineering checks above are separate from the real-AI delivery gate,
which was not run and is not passed by disabling inference.

Owner/competent functions must supply actual release/residual-risk/reviewer/
restart appointments and authorize/accept the reviewer/drill protocol; owner
must approve the corrected cohort manifest before evaluator work. No Legal,
DPO or Compliance decision is inferred. No actual participants, model use or
activation is attempted while those boundaries remain unresolved.

## Amendments and Divergences

None. Independent human/manifest decisions remain blockers, not approved
deferrals. Other assistant/form challenge coverage remains unimplemented.

## Review Handoff

Ready for independent Review of the bounded engineering slice. P01/P02 are
complete; P03 Review/publication remains. Base and freshly fetched origin/main
were `0ded682bab690d24eb59b78e704be82d337bf6cd` at the validation checkpoint.
Production diff is restricted to three core modules. No UI, deployment, actual
release or policy rules changed. Original critique and failing-first evidence
remain intact. Review must distinguish bounded implementation correctness from
unmet whole-epic/human acceptance and must preserve its original outcome.

## Independent Review Result and Publication Boundary

Exactly one independent Review completed at
.copilot-tracking/reviews/logs/2026-10-27/rai-release-218-review.md.
Execution: Complete. Outcome: Residual work. No introduced implementation
defect identified; independently reran all 12 new tests plus 25 existing tests.
Original critique Revise and Review residual findings are preserved.

RV-001: #222 approval dependency; RV-002: #223/#221 real competence/authority/
witness evidence; RV-003: wider #220 coverage and #224/#440; RV-004: final
publication/hosted controls. These remain routed, not closed or waived.
The user's explicit instruction authorizes push and one PR while prohibiting
the repository's usual full gate; this is a narrow task-specific publication
boundary, not a passing receipt or general policy change. Open a draft,
Refs-only PR; owner merge/hosted/human approval gates remain untouched.

At pre-publication fetch, main advanced to
`09099ecd1a66ee9d37ad993707d1f2eda07cdfd4` via unrelated infrastructure PR #498.
The tested/reviewed source base remains
`0ded682bab690d24eb59b78e704be82d337bf6cd`. Upstream paths include the shared
knowledge index/log, so integration may require owner reconciliation. No
rebase, merge or history rewrite is performed or tested-main claim invented.

## Publication and Main Integration

Source and original RPI evidence committed at
`63e9074ae35cc0f5a593980daf1e76ae840d273b`, pushed normally, and draft PR
https://github.com/jmservera/ama/pull/504 opened to main. Remote identity and
the draft state were verified. No issue was closed or acceptance tick changed.

The initial remote PR reported a conflict with concurrent main #498.
Subsequent integration merges pinned main
`09099ecd1a66ee9d37ad993707d1f2eda07cdfd4` without rebase/force or PR merge.
The only manual resolution preserves both independent knowledge-index entries;
the append-only logs merged automatically. Original upstream artifacts/rubric/
infra changes are retained without manual alterations. The three RAI source
modules and twelve tests remain byte-identical to the independently reviewed
candidate. Original Review is not rewritten or repeated.

Post-integration verification: 35 tests passed in 11.924s using the final
twelve-test selector plus existing Release, Legacy and ReviewTests classes.
`git diff 63e9074a --exit-code --` over the three production modules and two
test files returned zero; `git diff --check` and staged whitespace check pass,
with no unresolved index entries. Final integration metadata is committed and
pushed normally to the same draft PR. This does not turn original dirty-tree
Review into an exact-head gate receipt or satisfy hosted/human approval.
