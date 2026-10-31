---
title: Closure audit batch 1 phase details
description: Exact write boundaries, sequencing and focused audit validation
ms.date: 2026-10-31
ms.topic: reference
---

## P01 - Candidate and independent critique

Inputs are the research manifest, four original lane JSON records and original
external issue snapshots. The final decisions JSON contains only scoped issue
ids, approved new tick indexes, preserved ticks, unmet indexes, supporting PRs,
body hashes and parent rejection dispositions. Original lane proposals are
historical evidence, not direct write authority.

Reject #114 C1, #122 C10, #154 C1/C4, #130 C2, #140 C5 and #145 C11 for the
recorded whole-criterion/live/AT/test/provenance gaps. One independent
final-candidate critique checks remaining scope-sensitive RAI and Bicep ticks,
original-byte preservation, closure and idempotence safeguards.
Compatible critique findings are applied once and recorded; no repeated
critique or inferred human approval.

The original critique executed Complete / Revise. All five findings are
compatible direct corrections. Additionally withhold #130 C7/C8/C10/C11,
#121 C10, #126 C11/C12 and #143 C3. Final candidate: 30 new ticks, 75 preserved,
192 unchecked unmet, zero closures. No original outcome is erased.

## P02 - Safe remote writes and readbacks

Fetch all 46 current issue bodies and metadata first. If any body differs from
the original, do not overwrite it blindly. Fail the conflicting write and
record/reconcile without discarding owner work. Derive edits by replacing only
the single unchecked character at exact matched indexes. Preserve CRLF and all
other body bytes, titles, labels, assignees and milestones.

Use `gh issue edit --body-file`; never interpolate issue text into a command.
Compare the readback with the exact expected body/hash and prior metadata.
Use `<!-- closure-audit-batch1-2026-10-31 -->` in one unmet-criteria comment
per nonclosed issue. Check existing comments and the external journal before
retrying; verify exactly one matching comment with the expected content.
Retain prior comments and all criterion wording.

Immediately before each write, reread that issue's exact body/state/metadata.
A conflicting reread blocks that operation. Persist intended hashes before
submission. After an uncertain response, inspect actual body/comment bytes
before any retry. A single exact marked comment is reused; conflicting or
duplicate markers block without editing/deleting them. Test no-op replay and
uncertain-success reconciliation. Adjacent reads cannot eliminate GitHub's
non-atomic read/write race; do not claim transactional isolation.

Only a fully checked, wholly proven matrix can authorize `gh issue close`
with a PR-naming comment. No matrix currently qualifies. Count all repository
open issues before/after separately from the 46 scoped issues; concurrent
external changes are not credited to this audit.

## P03 - Changes, Review and publication

Changes must include the requested 46-row issue/PR/ticked/unmet/closed table,
accepted/rejected counts, operation results, provenance pointers, body/metadata/
comment hashes, live/AT/approval limits and actual attributable closure delta.

One independent post-implementation Review assesses exact final decisions,
remote readbacks and focused documentary evidence. It may find nonconformance;
retain that outcome and route findings later, never claim approval or rerun
Review to erase it. Source bugs are out of scope.

Resolve authenticated account id/login using `gh api user` immediately before
commit; configure repository-local noreply email for author/committer. Include
the owner-specified Copilot trailer. Commit task-owned evidence only. Fetch
main before push; qualify any drift without rebase/amend/force. Use
`git push -u origin HEAD`; create a main PR with Refs-only references to all
scoped issues. Verify push/PR and leave merge/CI/human approval pending.

## Execution status

P01 and P02 complete; P03-T01/T02 complete; P03-T03 pending. Research
executed/Ready; one critique Complete/Revise with all five findings disposed.
Remote 30 ticks/46 exact comments verified, zero closures; 132 global open
before/after writes, 46 scoped before/after. Final no-op remote preflight found
zero pending edits/comments. Changes and compact receipt reconcile all297
criteria. Focused validation does not replace hosted
CI or human acceptance, and no full-gate receipt is fabricated.

The single independent post-implementation Review executed Complete /
Residual work. No audit defect or Review blocker was found. RV-001 retains
the unmet count priority, RV-002 routes historical unsupported ticks and
RV-003 retains the non-atomic platform limitation as distinct follow-ups.
No source repair, unticking, child work or second Review is performed.
