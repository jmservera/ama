---
title: Case journey round seven changes
description: Original implementation and validation evidence for PR 529
ms.date: 2026-10-29
---

Task 526-round7; full plan P01/P02. Research Complete / Ready; sole critique
Complete / Revise, PC-001/002/003 applied directly, no repeated critique.
Implementation starts P01-T01 at intake HEAD 815aa615.

No Azure/az, secrets/.env, private data, push or thread/PR mutation authorized.
Heavy checks use flock -n /tmp/ama-rpi-heavy.lock with <=2400-second admission.
Publication complete gate is not run because it requires az; no receipt claimed.
Original earlier-round evidence remains unchanged. Refs #526.

## P01 implementation

API errors now retain outcome; a shared classifier gives committed/uncertain
precedence over HTTP status. Shared case refresh keeps a session history barrier,
including fieldless/different-key actions. Case reads capture the barrier before
dispatch; older reads cannot repaint or unlock, and failed GETs preserve it.
Proposal state objects similarly require a matching post-outcome listing
snapshot; constructing/replacing a card alone cannot recover it.

Sibling audit/corrections: aiNotes retains blocked review actions until workspace
reload; priority reviews retain input and disable actions rather than repainting
actionable stale data; assistant invocation shares pending/history state across
panel replacement and recovers after a causally fresh case GET. Procurement has
outcome-aware exclusion, causal package/order reads and read-only recovery.
Upload prepares the file inside its existing form exclusion, then dispatches
inside shared refresh; local file errors remain retryable and uncertain uploads
stay disabled. Raw resident and challenge forms treat uncertain like committed.
case-workspace.js has no mutations or network ownership and needs no source edit.
No authority, approval, consent or design-system changes.

Four added unit methods exercise actual API errors, causal reads, upload/file
preparation, priority/invocation/procurement, and both raw forms. Existing case,
proposal and draft review matrices extended. One helper added per browser suite;
no tests removed. README explains recovery boundaries.

## Preserved initial validation

External root:
/home/azureuser/.copilot/session-state/266fad4a-d7af-4dcd-8086-dac71170cbfd/files/.
round7-units-01: 25 tests, two new fixture failures (wrong source extraction and
resident form wrapper assumption), plus three new >100-column JS fixture lines.
round7-units-02: one remaining fixture extraction included a beforeunload
registration. Corrected exact source slice; no product fallback introduced.
Original logs retained. Ruff's one formatting difference corrected by formatter.
round7-units-03: 25 requested tests pass. Focused Ruff at 100 columns passes.
Pinned axe 4.10.3 SHA256:
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
No dependency installation needed; existing .venv used.

## Initial browser pass and final audit refinement

round7-browsers-01: journey passes 42 pinned axe states, no page errors, actual
Chromium 200% zoom; assistants passes 173 checks / 40 axe states / no page errors.
Both include committed/uncertain 409/503, pre-outcome deferred reads, duplicate
POST exclusion and subsequent authoritative recovery. Browser versions:
journey 156.0.8078.4; assistants 155.0.8059.39.
Owning Ruff passes, 51 source/test files formatted; mypy 99 source files passes.

A final direct audit applied the same causal case barrier to raw resident/
challenge failures, including transport uncertainty, so an older concurrent
case GET cannot replace their disabled controls. Added corresponding session
assertions and strengthened priority input retention/refusal retry plus
procurement stale/fresh-read coverage within existing four added unit methods.
These later bytes require final reruns; initial results are not attributed to
the final candidate. This is a plan-consistent local correction, not a new
critique or post-implementation Review.

Current Web Interface Guidelines fetched completely again before this source
read. Changed native action/status paths preserve semantics, keyboard, labels,
focus, draft warnings and Fluent controls; no visual/CSS/framework changes.
Existing repository ASCII and plain-language rules override generic typography.
Manual contrast/screen-reader/staff acceptance remain unperformed.

## Final candidate validation

Source stopped changing before round7-final lock admission
2026-10-29T00:45:34Z. Persistent case/procurement generation tokens prevent an
ABA reset: pre-outcome reads stay stale even after newer recovery clears the
barrier flag. Both stale-before-recovery and stale-after-recovery orders execute
in the shipped-code unit matrices. All following evidence covers final source:

* test_case_journey + test_workspace_scripts: 25 tests pass.
* Accessibility/design/content, procurement API and resident API: 67 tests pass,
  one existing skip. Constructed rule-store-unavailable logging is expected,
  not a silently configured legal/rules service.
* Owning Ruff at 100 columns passes; 51 source/test files formatted.
* Mypy passes all 99 owning source files; five audited JS modules parse.
* Journey: 259 PASS assertions, 42 pinned axe 4.10.3 states, zero violations,
  zero page errors, browser 156.0.8078.4, real chrome.tabs.setZoom=2.
* Assistants: 173 checks, 40 axe states, zero violations/page errors,
  browser 155.0.8059.39.
* git diff --check passes. No dependencies, generated targets or test removals.

Authoritative external directory: session files/round7-final (full root above).
Journey results SHA256:
6a30e6f88d2e546fa56dbda3049d46e73a8c5951c47a1aa523dacfff769fb30f.
Journey log SHA256:
bb070e84c1f1bdb8776beae634de92f14e423303f84ae9162b4ecadb9122568d.
Assistants results SHA256:
70ce45f7edecd3634bbb84ad0e86b51a837ba95ee7d6877b2055a3829988331a.
Assistants log SHA256:
695c66e41ae370257945d3a2b0d92a8acf7e8f9b1122177455c43673818c677f.
Final API diff SHA256 against intake:
14b12fc8b83459e960adc9a8c39ea1e7302edec9439f78ab9c80a0fff4b2a746.
The 41 journey / 39 assistant incomplete axe items still require manual review;
zero automated violations is not WCAG conformance or staff acceptance.

## Sibling audit disposition

| Surface | Mutation/recovery evidence |
| --- | --- |
| ops.js quality Save and record actions | Shared refresh now returns check-history for structured outcomes; measure/tab/failed/old read browser matrix blocks repeated POSTs and preserves evidence. |
| app.js ordinary case, funding, handoff, safety and fieldless actions | Shared case barrier blocks same/different/empty-field action keys; causal case reads recover only current session/generation. |
| app.js upload | File preparation stays locally retryable under form pending exclusion; POST moves inside guarded refresh and outcome keeps the form disabled. |
| app.js draft and priority reviews | Structured outcomes disable all review actions; reason/replacement remain copyable; full workspace reload required for these separately retained resources. |
| assistants.js proposal review | ID/revision state snapshots; only post-outcome listing may reconcile uncertainty. Both case/queue HTTP matrices execute. |
| assistants.js invocation | Session capability map excludes pending/repeated requests across rebuilt panels, and relevant fresh case read recovers check-history state. |
| ops.js capacity/workorders | Outcome-aware mutation exclusion; package/workorder generation snapshots reject old responses; Try again reads only. |
| panels.js resident/challenge | Both raw-fetch families preserve structured/transport uncertainty in the same case generation barrier; explicit refusal remains correctable. |
| case-workspace.js | Pure projection, retained-panel navigation and count observers; no API/fetch/POST or mutation state owner. |
| Other app.js POSTs | Login/logout have session-specific authority and no committed-outcome contract; import-check and deterministic draft are previews; advisory AI generation/read-doc use their existing separate draft error handling, not a status-based refusal/unlock decision. No outcome-bearing review path is left on the old status-only predicate. |

Bounded changed-path guidelines source read result:
src/api/src/zava_forward/api/web/app.js:29 - pass: outcome/status feedback,
copyable review drafts and case history barrier.
src/api/src/zava_forward/api/web/assistants.js:12 - pass: source/revision gates,
native disabled actions and explicit fresh-read recovery.
src/api/src/zava_forward/api/web/ops.js:195 - pass: native busy action, focused
status and reload-only procurement recovery.
src/api/src/zava_forward/api/web/panels.js:145 - pass: local validation remains
separate from status feedback; uncertainty preserves input and history blocking.

P01 and P02-T01 complete; P02-T02 sole independent Review next. No source changes
after final validation, no publication gate/receipt, no push or thread mutation.

## Sole independent Review

Execution Complete; outcome Not accepted. Original record:
.copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round7-review.md.
The requested structured-outcome correction and causally fresh post-outcome
barriers pass, but two material sibling gaps remain:

* RV-001 High: fieldless shared actions and rebuilt raw resident/challenge forms
  can issue a second POST while the first is still pending. The new post-outcome
  history barrier cannot undo requests already dispatched.
* RV-002 Medium: a pre-outcome shared-queue listing keeps review actions blocked
  but loses the unresolved reason/edited JSON; the queue has no case draft cache.

Both independently reproduced with shipped JavaScript. Passing aggregate
validation does not cover these cases or establish acceptance. Preserve the
Review unchanged; route each to later rpi-implement, with RV-001 first. No
post-Review source fix, closure verification or repeated Review performed.
Only local retention/commit remains in P02-T02. Coordinator must address these
before publication, then perform its separate exact-head gate and hosted/human
approval workflow. No automatic child work selected in this non-interactive run.

## Local retention and coordinator handoff

Implementation plus all seven original dated RPI artifacts committed locally:
6e35341620686961e6c7e598cbc9caee42b35f37
(fix(web): preserve mutation outcomes and history barriers).
Authenticated account-derived privacy-safe repository-local email used for both
author and committer; required Conventional Commit and Copilot trailer retained.
P02-T02 and full-loop execution complete, while independent acceptance remains
Not accepted. This closeout updates tracking only; no source changes or second
Review. Automatic session remains at Follow-up awaiting coordinator selection.

Ranked next work: RV-001 pending-identity correction first (High, duplicate
mutation risk), RV-002 queue-draft retention second (Medium, recoverable-edit
loss), then coordinator exact-head publication/hosted/human gates. Original
Copilot thread PRRT_kwDOUU8JX86xX3Ek remains untouched and unresolved. PR body
remains unchanged with Refs #526. No push, az/Azure, deployment or new gate
receipt. The coordinator owns future push, reply and resolution after addressing
these findings. Source and final test evidence remain at the recorded boundary.
