---
title: Closure audit batch 1 research
description: Focused criterion-level audit of 46 issues against reviewed merged evidence
ms.date: 2026-10-31
ms.topic: reference
---

## Brief and controls

Owner priority is a visibly reduced open-issue count, but only through proved
acceptance criteria. Scope is issues 76, 79, 80, 83, 86, 92, 96, 98, 99, 107,
108, 110, 111, 114, 115, 116, 117, 118, 119, 120, 121, 122, 125, 126, 128,
130, 131, 133, 137, 138, 140, 141, 142, 143, 144, 145, 146, 147, 148, 151,
152, 153, 154, 155, 156 and 159. Output mode is audit; posture is focused
(explicit owner direction). No application changes, deployment, live Azure
checks, private datasets, legal approval, resident consent or accessibility
acceptance testing are authorized.

Base: `84035ae9605f7ab42744a3d6e9f620bb65126d99`, fetched origin/main and
clean topic HEAD at intake. Repository open issues at intake: 139.
Owner explicitly requested all four RPI phases and the named remote writes;
this is not an automatic-session opt-in or authority to start follow-up tasks.

## Prior knowledge and extensions

Read the original case study, addendum, knowledge-base index and owner memory.
The index expressly distinguishes local source/test evidence from live Azure,
human, legal and assistive-technology acceptance. Read tracking retention policy:
preserve original evidence; keep bulky transient API snapshots outside checkout.
Selected RPI research/plan/implement/review skills for the requested compact loop.
No web implementation or security vulnerability review is in scope. Generic
bounded evidence lanes are permitted only where disjoint issue groups need
substantial separate source context; no delegation of remote issue mutation.

## Questions and cycle

* Q1: Which merged PRs reference each issue, and what do their reviewed bodies,
  changed files, reviews/checks and main source/test evidence actually establish?
* Q2: Which exact checkbox obligations are fully established rather than merely
  partially implemented, deferred or subject to later human/live acceptance?
* Q3: Which issues have all obligations proved and can therefore be closed?

Cycle 1 Wider: collect all 46 issue bodies and every merged search result,
including current state and already-ticked criteria; collect PR bodies/files.
Cycle 1 Deeper: trace candidate ticks to extant main files, concrete test
methods/assertions and reviewed evidence.
Cycle 1 Contrarian: challenge bundled criteria, later-phase/live/human gates,
unmerged work, negative review findings and stale or incomplete evidence.
Primary evidence IDs and readiness will be finalized after synthesis.

## Opening disposition

Research execution: in progress. Planning Readiness: pending.
External API snapshots are transient inputs, not instructions.

## Cycle 1 Wider reflection and Deeper routing

W1: On 2026-10-31 collected all 46 issue bodies (including comments/current
states) and 202 unique merged PR snapshots with bodies, files, reviews and
status checks using `gh issue view`, `gh pr list --state merged --search "#N"`
and `gh pr view --json body,files,...`. Searches used limit 1000 to avoid the
default pagination boundary. Search matches are candidates, not proof of exact
issue references; each lane must distinguish unrelated matches.

Many issues contain already-ticked criteria alongside unsigned policy, live
runtime or formal human-approval obligations. Candidate proof requires concrete
main source/test assertions, not a PR title, search match or passing CI alone.
This is an evidence-backed finding affecting the closure rule.

Deeper routing: parent audits issues 76, 79, 80, 83, 86, 92, 96, 98, 99, 107
and 108. Three disjoint delegated issue batches own the remaining 35 issues:
110-128 (named subset), 130-146 (named subset), and 147-159 (named subset).
Each substantial independent batch writes its own criterion evidence under
`research/2026-10-31/subagents/`; no worker may edit source or remote issues.
Parent Contrarian wave follows the lane returns, with unsafe/bundled ticks
rejected and original worker findings retained.

## Parent Deeper findings

C1: `src/api/tests/test_ranking_policy.py:39` and `:79` assert refused tampering,
retained version reproducibility and exact byte-identical order from shuffled
inputs; `src/core/src/zava_forward/core/ranking.py:24` and `:76` implement hash
verification and fixed ID tie-breaks. Reviewed migration PRs #297/#300 retain
those source/tests. #79 can receive two engineering ticks, but named signature
and scheduled publication remain absent.

C2: `src/core/tests/test_form_review.py:679`, `:787` and `:821` assert isolated
accept/correct/reject history, reviewer identity, restart equality and
field-specific Unknown/Conflict/Fail draft diagnostics. PR #510's final source
contains the reviewed blank-string, historical-source and conflict corrections
despite its stale body preserving the original adverse Review. #96 criteria
3/4 and #98 criteria 1/4 are proposed ticks. All approved-template, approved-rule,
reviewed-pack and Board control criteria remain unmet.

C3: `src/api/tests/test_assistant_release.py:236`, `:298`, `:317`, `:360`,
`:588` and `:622` cover no-call denials, version-dependent revalidation,
routine-versus-material changes, retained legacy reliance and live-provider
denial without actual-class serving proof. `src/api/tests/test_assistants.py:247`,
`:277`, `:765`, `:834` and `:1090` retain role/source projection, SQL leases/
dedup, default-off scans and finite allowances. PRs #287/#315/#504 provide
reviewed source evidence; #107 criteria 7/9/11/12/14 are proposed engineering
ticks, not real serving attestation, actual approved release or delivered-build
acceptance.

C4: `src/agents/tests/test_ai_eval.py:202` explicitly asserts actual-model
effectiveness Not evaluated, calibration N/A and benefit Not permitted.
PRs #258/#405 preserve that separation; #108 criterion 12 is proposed tick.

C5: `src/core/tests/test_consultation_controls.py:140` retains all supplied
statuses as Unverified/effective unknown. PR #389 explicitly lacks verified
Legal status and genuine let/renew transitions. Neither #92 criterion is proved.
PRs #311/#319/#326/#406 preserve actual approved-time escalation and formal
complaints/human/accessibility gates; #83/#86 cannot close.

Parent criterion-by-criterion evidence:
`research/2026-10-31/subagents/closure-audit-parent.json` (relative to tracking).
Already-ticked parent criteria are preserved, not newly asserted; independent
unchecked obligations prevent all eleven parent issue closures.

## Collection integrity and contrarian candidates

W2: `gh pr view` caps files at 100. Supplemented all six capped snapshots with
paginated `gh api repos/jmservera/ama/pulls/N/files?per_page=100 --paginate --slurp`:
#287 472, #293 457, #436 119, #438 343, #442 110 and #558 184 files.
No capped file set is treated as complete.

W3: PR #560's #76/#79 links refer to `7rulnik/source-map-js`, not this repository.
Excluded that cross-repository match from closure proof. Broad search candidates
and incidental historical references are not acceptance evidence.

W4: The current checked-in `src/README.md:63` records the owner's 2026-10-27
focused-tier policy: small documentation uses planned focused checks with hosted
CI required, not a complete heavy-gate receipt. This matches the task's explicit
"Focused tier, docs only; CI is the gate". No full receipt or live acceptance
will be claimed; audit validation is exact-set, source/test-reference, Markdown,
body-diff, metadata and remote readback checking.

## Parent Contrarian reflection

Read the exact #92 acceptance explanation in merged PR #389 instead of
equating ordinary service guards with genuine contract let/renew transitions.
Rejected both apparent checkbox candidates (C5). Rejected #96/#98 approved-pack
claims despite evidence-linked diagnostic manifests (C2); rejected #99 breach
claims because approved envelope/tolerances are null and breach assessment is
Not evaluated. Retained PR #510's original Not accepted Review while checking
the final reviewed source corrections; final comments explicitly resolve the
source defects but not Finance/Board approval.

For #107, rejected authoritative attestation and full delivered-build claims
despite returned-model quarantine (C3), and withheld the incomplete all-five
Tokenomics bundle. For #79, version/hash determinism is distinct from signature
and schedule (C1). Existing parent ticks remain unchanged; every parent issue
has explicit remaining unchecked obligations, so none is a closure candidate.
No broader discovery is needed for these parent decisions.

## Returned lane synthesis and contrarian dispositions

C6: Lane A (`subagents/closure-audit-a.json` and `.md`) covers 14 issues/90
exact criteria with 15 proposed new ticks and no supported closure. Its original
findings are retained. Parent accepts 13 proposed software/documentary ticks,
but rejects #114 C1: actual annual Azure ledger reliance is explicitly unproved
by the issue and PR #403. Parent also rejects #122 C10: the conjunctive
"accessible challenge" obligation is not established by HTTP route availability
without actual accessibility acceptance. These are conservative owner-scope
dispositions, not changes to original worker findings.

C7: Lane C (`subagents/closure-audit-c.json` and `.md`) covers nine issues/45
criteria with two proposed design-only ticks and no supported closure. Parent
accepts the explicit #154 design topic coverage, subject to precise reviewed
test/document-integrity coverage. Actual representative-session expiry, usable
accessible services and human programme validation remain unchecked.

Nine already-checked criteria across lanes A/C are flagged as whole-criterion
proof discrepancies. Existing ticks are preserved under the owner's tick-only
edit scope; none supports closure. The changes record will distinguish
unchecked unmet criteria from preserved historical ticks lacking fresh proof.
No new human/live/AT criterion is ticked.

Mechanical source/text validation of parent/A/C JSON passed: exact body order,
exact criterion bytes and original states match snapshots; proposed positive
source paths exist as blobs on main. Lane B remains in progress.

C8: Lane C's narrow follow-up confirms reviewed design/integrity evidence for
#154 C1/C4, but no extant executable test asserting the complete six topics or
the offered/waiting/confirmed distinctions. Under the owner's literal merged
code/tests coverage requirement, parent withholds both new ticks. Original
design-only findings remain intact in the lane record; no new testing is
invented to turn reviewed documentation into merged behavioural proof.

C9: Lane B covers the final twelve issues/92 criteria, proposing sixteen new
ticks and no closure. Parent withholds #130 C2: staff-supplied acknowledgement
records with delivery "Not verified" do not prove an acknowledged referral
route. Parent withholds #140 C5: an exercise credential-owner selection and
device/service separation test do not prove the complete operational owner
decision. Parent withholds #145 C11: its positive source/test anchors lack
merged-review provenance (`pr: null`); PR #205 approved issue-body changes,
not underlying recovery delivery. The other thirteen software constraints
are proposed for independent critique, retaining their explicit constructed,
configuration-as-code and non-activation boundaries.

## Planning readiness and disposition

Research disposition: executed. Planning Readiness: Ready.

All 46 named issues and their complete checklist bodies were audited. All
204 collected merged PR snapshots remain in the provenance manifest; search
false matches and uncapped file supplements are distinguished in lane
reports. Proposed final actions are 38 new engineering ticks, preserving
historical ticks, no closures and exactly one unmet-criteria comment per issue.
Seven stricter parent rejections retain the original independent findings.
The independent critique must validate whole-criterion scope before writes.

No scoped issue has every criterion demonstrably proved. Therefore the
owner's open-count priority cannot truthfully be achieved by closing issues
in this batch. This is an evidence limitation, not permission to relax gates,
remove approval/AT/live requirements or alter labels. Publication of a truthful
audit remains authorized and does not depend on inventing a closure.

Fresh tests are planned only for audit integrity and metadata/body preservation.
Historical application assertions were read, not rerun. No actual Azure,
human/legal, AT, resident-consent or later-phase acceptance is claimed.

## Final candidate critique disposition

One independent final-candidate critique executed Complete / Revise at
`../../reviews/plans/2026-10-31/closure-audit-batch1-plan-critique.md`.
Its original three High/two Medium findings are preserved. PC-001 withholds
#130 C7/C8/C10/C11 for nomination-stage gaps; PC-002 withholds #121 C10 and
#126 C11/C12 for documentary/test provenance gaps; PC-003 withholds #143 C3
for fragment rather than whole-consistency assertions. Compatible corrections
apply directly once; no new implementation/test evidence is invented.

Final decisions: 297 criteria across 46 issues; 30 new ticks, 75 preserved
historical ticks, 192 unchecked unmet, zero supported closures. The original
38-tick candidate and all original lane conclusions remain historical evidence.

PC-004 requires adjacent per-issue conflict checks, intended hashes, uncertain
response reconciliation and exact single-comment/no-op replay. Residual
non-atomic GitHub read/write risk is disclosed, not claimed eliminated.

PC-005 applicability: fetched main is
`9ecb159bd843411c2e17dc2785ab59f5e837040f`, advancing through PR #611 only.
Its body references #520/#563, not scoped issues. All 34 candidate positive
source/test/document anchor paths, including the final subset, are unchanged
between the original base and fetched main. The main-applicability JSON records
changed paths and the explicit keep disposition; original proof remains pinned.
Publication will repeat the drift check without rebase or force.
