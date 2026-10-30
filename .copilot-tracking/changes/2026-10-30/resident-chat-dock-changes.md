---
title: Resident chat fallback and dock changes
ms.date: 2026-10-30
---

Task: resident-chat-dock-520-563. Full plan in scope, implementation started.
Plan/details/critique under their dated 2026-10-30 resident-chat-dock paths.
Refs #520 and Refs #563. No live AI, ledgers, credential files, Azure or push.

## P01: Admission and diagnostics

P01-T01/T02 implemented. Exact polite envelopes and common retrofit/document
upload/smell questions now pass complete-message admission. Original-text
hazard handling and remaining protected token priority stay in place.
One added test method exercises allowlisted diagnostics on typed and legacy
paths, including private string/dictionary/error canaries. Existing question
and hostile-suffix tables extend semantic generation/isolation coverage.
Focused 43-test suite passed after preserving the pre-existing warning-question
refusal; no test removal or arbitrary admission.

## P02: Native resident resizing and docking

Implemented resident-only opt-in with native size details, labelled ranges and
pressed-state dock button. Dock fills right/top/bottom, disables height control
and hides the launcher only while open. Escape restores its focus.
History-anchor fraction/bottom following survive changes; reopen retains the
old end-follow behavior. No persistence or custom gesture handling.
The first successful generated browser run proved actual local HTTP/model
adapter generation, geometry, keyboard, escaped text, source details and
fallback; final expanded-control axe/shared regression still in progress.

## P03: Validation and review handoff

Implementation complete, final validation in progress. Required commands and
browser checks are recorded with actual outcomes, not historical proxies.
Live/human/AT acceptance unproven.

Full required API discovery completed: 1380 tests in 482.094s, OK with 320
existing integration/opt-in skips. Ruff and format passed; the chained mypy
found one TypedDict dynamic-key use in the new browser harness. Replaced that
with literal width/height accesses; final targeted/type execution is queued.
The first lint-only attempt also found a 101-character test line, corrected.
No application test failed after the bounded warning-question amendment.

External evidence root:
/home/azureuser/.copilot/session-state/14a25525-dc6f-4329-9a2d-51155d0f7b03/files/resident-validation/.
Original logs: api-full.log, focused-1.log, shared-widget.log.
generated-2/results.json is the first passing scripted-generation/resize
browser record. Pinned axe 4.10.3 SHA256:
880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
Subsequent checks use that exact asset. Final-targeted.log records Ruff pass,
61 files formatted, mypy pass for 117 source files, and all 43 targeted tests
passed in 20.177s, including the final polite safety/legal/consent cases.

The shared-widget-2 retry exhausted the caller's 600-second lock wait before
execution; its output log is empty. Process metadata confirmed another
session's heavy check owns the lock. No other session/process was stopped or
changed, and no lock bypass/private lock was used. Generated-3 and final
targeted checks were queued under the same lock. Generated-3 also timed out
before execution. Final targeted checks subsequently acquired the lock and
passed. The consolidated final browser retry also exhausted its 600-second
wait before execution (empty browsers-final.log). Three final-browser attempts
were lock-blocked; no final-candidate browser/axe pass is claimed.
The earlier generated-2 pass predates final geometry cleanup and is historical,
not substitute final-candidate evidence. Independent Review must retain this
validation blocker. P03-T01 is incomplete for final browser verification.

Fetched origin/main for gate comparison: 9b13cef9e9ea8034e2ab65ff796eed65d2edb166,
while the owner-selected branch remains based on d986c4c4. The complete gate
requires the current reviewed main base as ancestor. Do not silently rebase,
merge or change the requested base; final publication therefore requires
coordinator reconciliation even if all feature checks pass.

### Web guideline review

Fresh full source fetched on 2026-10-30 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed all changed web files against all fetched rules, with repository
Fluent/plain-ASCII/sentence-case standards taking precedence for copy.

## src/api/src/zava_forward/api/web/chat-widget.js

Pass for changed behavior: named native controls, no drag-only action,
autocomplete off, no persistence, fixed-state dock and focus restoration.

## src/api/src/zava_forward/api/web/chat-widget.css

Pass for changed behavior: Fluent tokens, viewport/safe-area bounds,
scrollable overflow, no size animation, reduced-motion handling retained.

## src/api/src/zava_forward/api/resident_demo/web/assistant.js

Pass: resident-only opt-in, existing consent/manual/late-result guards retained.
This is scoped engineering review, not whole-site or WCAG/AT acceptance.

Final local geometry cleanup: use stable percentage preferences rather than
resetting range values when size details reopen; restore a hidden launcher on
dispose; bound floating width by both actual safe-area insets. These changes
are source-reviewed and JS parses, but the final browser lock failure means
their exact candidate remains browser-unverified.

## Independent Review and local persistence

The one independent Review executed Complete, outcome Not accepted, with
RV-001 High (missing final browser evidence) and RV-002 Medium (gate/current-main
prerequisite). No source defect was demonstrated. Original Review outcome,
findings and critique remain unchanged. An editorial reference-wording correction
removes prohibited issue-action wording without another Review or verdict change.
Source diff digest independently reviewed:
222faedfd9740a83e7abdb287bcd113c9edcbb3f0cd178dde84fd40497d354bf.

Local implementation/evidence commit:
734be219cd8cd47fcfefa72d698d0e4f685b50e9.
Required privacy-safe author/committer identity and Copilot trailer applied.
No push, PR, rebase or merge. Later tracking-only handoff bookkeeping does not
change the reviewed src/api diff or erase the unaccepted original outcome.

## Complete gate attempt and handoff limits

After committing, fetched main at f168d0799624e7f8e943fde6ef6fb08a17db151d.
Command: /tmp/mv/bin/python tools/rpi-checks.py --all --lock-timeout 600
--base f168d0799624e7f8e943fde6ef6fb08a17db151d
--out /home/azureuser/.copilot/session-state/14a25525-dc6f-4329-9a2d-51155d0f7b03/files/resident-validation/complete-gate-734be219.
The runner owns the mandated shared lock; no nested outer flock.
Exit 1: "BLOCKED: Candidate has ignored inputs; move all scratch outside the
checkout". Its preflight stopped before heavy execution, tool/cloud calls or
receipt creation. External log: complete-gate-734be219.log.
No ignored input was removed, moved or read; preserve unknown/pre-existing
inputs pending coordinator retention-backed selection. This is not a scanner,
SQL or browser pass. Current-main ancestry is an additional known prerequisite,
not the observed first rejection. No final receipt exists to verify.

P03-T02 and the P03-T03 attempt are complete; P03-T01 remains incomplete.
The loop reached its one Review, but the candidate remains Not accepted.
Coordinator owns final browser/axe/shared-widget recovery, authorized checkout/
base reconciliation and a clean exact-head complete gate before any push.
No subsequent source fix or second Review was performed.

## Criteria proven and not proven

* AC1/AC2: local constructed HTTP tests prove recognised paraphrases reach
  generation, own-case projection/consent/protected routes remain, and fixed
  fallback reasons preserve facts/human help without private exception data.
* API discovery: 1380 tests, 320 skips; final targeted 43 tests, Ruff, format,
  mypy and JS parse checks pass within their recorded boundaries.
* AC3: native resize/dock code, browser assertions and historical generated-2
  evidence exist; final geometry/focus/axe/shared regression is NOT proven.
* AC4: original dated research, plan/details, critique, changes and independent
  Review are persisted locally. Final browser and passing complete gate are
  NOT proven. No live model/configuration, authenticated live acceptance,
  human/AT conformance, formal approval or whole-issue acceptance is claimed.

## Amendments and divergences

No material divergence. Critique PC-002 rejected with evidence of the caller's
explicit /tmp shared-lock instruction; no actual temporary-directory prohibition.
PC-001 and PC-003 dispositions are in the plan.

Local corrections before Review: the first browser check needed to await
native keyboard scrolling, rather than asserting before the browser finished.
The shared regression exposed reduced history height hiding focused Sources;
moving the dock button inside Chat size and restoring the original header
layout fixes the root geometry, rather than weakening that assertion.
Keep the original failed external logs.
The draft warning-paraphrase expansion conflicted with an existing intentional
refusal regression; removed that unnecessary expansion and kept its test.
No agents change is warranted: resident inference does not call its employee
regulatory retrieval. No configuration or model activation was attempted.
