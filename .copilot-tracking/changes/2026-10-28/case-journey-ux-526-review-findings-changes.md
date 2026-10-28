---
title: Case journey 526 later findings implementation
description: Original Review disposition and subsequent implementation evidence
ms.date: 2026-10-28
---

## Invocation opening

Full findings plan scope P01/P02. First dependency-ready boundary P01-T01.
RV-001..004 are compatible defects within confirmed requirements; no new
decision, research, critique or repeated original Review. Source mutation was
paused for Review and resumes only in this separately recorded invocation.
Expected targeted regressions, admitted browser checks and full committed gate.
Publication blocked until all four repairs and required gate evidence pass.

## P01-T01 local gate import parity

Add API/core/agents test fixture paths after the safety path in both execution
and trusted receipt reconstruction. Import-only journey command now succeeds;
31 runner tests pass, including the exact expected PYTHONPATH regression.
No safety bootstrap or receipt policy bypass.

## P01-T02 submitted controls, asynchronous drafts and counts

refresh accepts explicit submitted control references and clears only those
whose values still match the dispatched request, after success. All relevant
action/form helpers forward their own controls; unrelated same-card drafts and
edits typed during an in-flight save remain dirty. A departed case session
cannot trigger a stale-case redraw. Failures do not clear submitted drafts.

Proposal controls carry proposal ID/revision keys. Restore captured edits after
the async loader renders, not only synchronously at case construction. Changed
or unavailable proposals never inherit old edits; copyable read-only earlier
edits remain until explicitly discarded or the user leaves this case. Loading
failure preserves them through the same recovery route. Verification/revision,
roles and server source checks remain authoritative.

Document reading emits count-change events when replacing/removing outputs.
Known local review drafts are also counted in an unavailable-total tab label
without pretending that the total is known. Review completion removes that
local count, not a case approval.

## P01-T03 actual execution

browser-retry-07 preserved failure: second page shared the signed-in cookie,
so no login fields appeared. Isolate the manager browser context.
browser-retry-08 preserved failure: the old synthetic metadata had no blob.
Exercise actual constructed text upload with source/version/reason first.
browser-retry-09 preserved failure: unavailable assistant totals must stay
unknown while known local draft counts are shown. Preserve that distinction.

browser-retry-10 passed, admitted 19:46:13Z, immediately released 19:46:49Z.
journey-10: Chromium 156.0.8078.4, pinned axe 4.10.3, 37 scans, no pageerrors,
actual chrome.tabs.setZoom=2, all focused tabs visible, all original keyboard,
draft, pagination and reflow contracts. Same-card success/failure uses explicit
HTTP outcomes to isolate client preservation; it is not a real finance
commitment claim. Document upload/read/review uses the actual local endpoints.
Assistant suite: 27 scenarios pass, including real synthetic provider/review
APIs, pending call preservation, async same-revision edits, externally changed
revision isolation and copy recovery across another refresh. Case-preservation
baseline is recaptured after the intentional unrelated call, not after AI writes.
24 focused API semantic/design/content tests and 31 runner regressions pass.
API and runner Ruff/format/mypy pass; Ruff limit remains 100.

## Publication boundary

P01 complete, P02 pending. Preserve the Complete / Defects found Review.
No repeated Review or inferred human acceptance. Existing ignored validation
environments/caches remain untouched. Use an external clean exact-commit
worktree for the gate, so clean-input enforcement remains enabled without
destroying this worktree's existing inputs. Final receipt and publication state
stay external; any later tracked correction requires a new committed gate.
