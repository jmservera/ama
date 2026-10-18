<!-- markdownlint-disable-file -->
# Issue 87 separate correction routing

## Identity and Boundary

* Date: 2026-10-18; parent issue87, hierarchy parent81.
* Original source: 22c98267ae6da365d6a2d9fceed7113c8f4578ea.
* Base: 99056cae7bc679d2ace3e42c75f28577cfce8887.
* Branch: feat/appointment-commitment-controls-87.
* Current status: authorized correction ONE implemented for all seven findings;
  fresh failing-first/current-source evidence is in the matching correction-one
  receipt. Original routing below remains history, not a second Review,
  independent acceptance, self-Pass or operational approval.
* Original Review execution: Complete; outcome: Not accepted; two High/five Medium.
* Owner: backlog coordinator delegates later rpi-implement correction work within
  issue87; no unrelated issue work or new automatic child is started.
* Original critique SHA256:
  044c3b5b9399522993ddb81ba4f90fe0f8a708960cc812169f306f29e80f7396.
* Original Review SHA256:
  b0759a56265e8f82a5db71a99443736e07cec597b0e5e17bcc2d9a7f1e6cba4b.

## Ranked Implementation Routing

Rank reflects severity, user impact and bounded correction leverage. All findings
have destination later rpi-implement, not a new policy/research decision.

| Rank | Finding | Severity | Required correction and exact proving boundary |
| --- | --- | --- | --- |
| 1 | RV-001 | High | Guard truthful committed outcome through response serialization before headers. Reproduce response-only encoder failure for confirmation and human closure; assert durable event, explicit committed/reconciliation response and one consumed retry. Do not promise repair after bytes sent. |
| 2 | RV-002 | High | Reuse existing role-sensitive resident-view/recorded-need projection for appointment reads. Domain/HTTP unrelated-staff and provider canaries must not reveal household reasons, authority sources, closure reasons or investigation circumstances; minimum scheduling state/instructions remain available. |
| 3 | RV-004 | Medium | Require bounded nonblank textual bundle competence reference, retaining exact-scope and explicit bundle agreement. Reject whitespace/nontext/empty/wrong-scope through domain and HTTP; no competence inference. |
| 4 | RV-005 | Medium | Derive non-current/ended appointment state for withdrawn order while preserving historical evidence. Assert staff/provider HTTP projection and consequential execution refusal. |
| 5 | RV-003 | Medium | Atomically apply changed threshold to already eligible evidenced-active same cases, at most one task, preserving history/closure/consumed references. Test lowering/raising/retry/inactive and actual SQL competing config/outcome/closure; no historical recount. |
| 6 | RV-006 | Medium | Display selected current offer date/period/instructions before confirmation to authorized staff/provider audiences, localized with Unknown/ended wording. Test new flow without appending legacy Booked to mask omission. |
| 7 | RV-007 | Medium | Integrate manual evidence forms with dirty-state and in-app navigation/unrelated refresh protection. Actual keyboard cancellation preserves draft; saved action clears only its own draft and does not lose another pending form. |

## Preserved Evidence and Human Limits

Full canonical finding details and source locations remain in the unchanged
original Review, not duplicated or re-adjudicated here. Final implementation
receipts include core323/59 skips, API85/1 skip, actual MSSQL61/61, current static
checks, actual browser and rebuilt hardened image. Review independently ran
core95/API12 and found counterexamples. These are distinct evidence sets.

No correction implemented or tested by the coordinator. Any later implementer
records failing-first reproductions, exact source changes, final local checks,
actual SQL/browser/image reruns where affected and cleanup in a new correction
receipt. Preserve original Review and critique byte-for-byte. No second Review
or corrected-self-Pass is required or authorized by this routing.

Correction ONE implementer has completed the coherent batch on HEAD49d3d663 plus
uncommitted source/tests/docs. Fresh core336/API93/actual MSSQL75, local Chromium,
configured static checks and latest src-context hardened image passed. Exact
owned SQL/app resources and synthetic scratch data are removed. See
.copilot-tracking/changes/2026-10-18/issue-87-appointment-controls-correction-one.md.
The coordinator did not implement source; the original Review/critique are
byte-exact and adverse outcome remains. No new acceptance verdict is supplied.

Live threshold/lifecycle/configuration ratification, real authority/competence/
capacity and resident/accessibility validation remain human-owned prerequisites.
No diagnosis/provider disclosure, real contact/schedule, spend, automatic consent/
refusal/sanction, urgent safety delay, new allocation or #92 blanket hold.

## Delivery Gate

Original correctness gate failed. No normal push or PR was attempted. Local
commits preserve source and all actual dated RPI artifacts. Fresh origin/main
remains the pinned base. No rebase, force-push, main write, merge, issue closure
or claimed remote exact head. Coordinator owns subsequent correction delegation
and acceptance/delivery decision. Stop after this bounded original issue87 loop.
