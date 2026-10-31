---
title: Closure audit batch 2 phase details
ms.date: 2026-10-31
---

Task ID: closure-audit-batch2-2026-10-31
Baseline: 84035ae9605f7ab42744a3d6e9f620bb65126d99.

<!-- P01 -->
## P01: Evidence and guarded issue updates

### P01-T01

Read every matched merged PR even if irrelevant. Record every checkbox with
exact original text and zero-based issue-body line index. Require complete
coverage, unique issues and no false-positive PR reliance. Preserve prior ticks
without retroactively asserting independent proof of them. Cite code/test
names and document paths for newly accepted items. Reject any unproven
conjunct or prohibited approval/live requirement.

### P01-T02

Before the first action re-fetch current body/state and compare with its original
snapshot. Later actions compare to the exact verified preceding audit-owned
body/state, never to a normalized or silently accepted concurrent update.
Replace only `[ ]` with `[x]` on approved lines. Never reconstruct the whole
issue from a summary. Persist an intent before every request with issue/action
identity, exact predecessor and intended body/state/comment. Persist verified
success afterward, including exact remote comment ID/URL. Reconcile pending
intents with remote state/comments before any retry; confirmed success is not
replayed, and ambiguous outcomes quarantine the issue. A partially completed
close/comment is recorded explicitly rather than repeating the combined command.
If all criteria are ticked,
use `gh issue close --comment` naming relevant PRs. Otherwise use exactly one
comment listing each unmet criterion with its missing evidence. Re-fetch to
verify the exact expected body, state and exact one comment. Skip initially
closed issues. GitHub lacks atomic compare-and-swap; unexpected post-write
differences are recorded as blocked, not automatically overwritten.
Fetch main before mutations. If it advanced, revalidate only cited source/test
paths and contradictory changes; unresolved affected criteria cannot be ticked.

<!-- P02 -->
## P02: Durable record and publication

### P02-T01

Generate the owner-requested table with all matching PR numbers, newly ticked
and pre-existing counts, unmet criterion numbers and closed status. Preserve
exact per-criterion evidence, action outcomes and failures. Independent Review
assesses the artifacts and mutation receipts once. Findings affecting current
eligibility, mutation integrity or published accuracy block publication.
Direct in-scope artifact corrections may be dispositioned with resolving
evidence without another Review, preserving its original outcome. Only excluded
product/live work routes to original issues. No automatic reopening/unticking
authority is inferred.

### P02-T02

Resolve `gh api user`, configure local privacy-safe noreply author/committer
email, commit dated artifacts and required trailer. Fetch current main before
publication; record the current SHA and revalidate cited paths against intervening
changes if main advances. Unresolved affected evidence blocks publication.
Preserve prior mutation outcomes honestly; do not silently rebase or rewrite
ancestry.
Owner explicitly selected focused documentation/CI gate, so no full local gate
or fabricated receipt. Push with `git push -u origin HEAD`. Create a main PR
containing Refs references only, exact count changes, reviewed evidence and
CI-as-gate disclosure. Do not merge.

## Execution reconciliation

P01-T01/P01-T02 and the changes/evidence preparation in P02-T01 are complete:
62 issues, 365 criteria, 56 new ticks, seven verified closures and 55 verified
unmet comments. Observed global open count is 139 before and 132 after.
115 prior ticks were preserved. All 62 final bodies/states and audit comment
URLs were verified. No pending or ambiguous remote actions remain.

Main advanced before mutation to
9ecb159bd843411c2e17dc2785ab59f5e837040f; the assigned evidence owner
revalidated the three changed resident API/docs/test paths without weakening
any accepted evidence. Final remote-verification main is the same SHA.
No branch rewrite or source fix occurred. Independent Review is the next gate;
P02-T02 publication remains intentionally pending that one Review.
