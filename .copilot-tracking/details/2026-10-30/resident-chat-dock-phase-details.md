---
title: Resident chat fallback and dock phase details
ms.date: 2026-10-30
---

Task: resident-chat-dock-520-563. Planning candidate, automatic local-only loop.

<!-- P01 -->
## P01: Repair bounded admission and diagnostics

P01-T01: chat.py complete-match grammar owns admission (research C1/C2).
Accept exact polite envelopes only around recognised messages, plus small
specific case/retrofit, document-warning/upload and smell paraphrases.
Do not strip arbitrary suffixes or permit mixed instructions. Keep hazard
detection on original text before normalisation; test additions with hostile
suffix/prefix cases through actual HTTP and verify no reservation/model call.

P01-T02: aoai.py already has bounded projection, strict schema/IDs, finish reason,
expiry and precommitted accounting (C3/C4). Reuse it. Map only known
AssistantUnavailable reasons to fixed labels/log codes; unknown exceptions
become generic unavailable without exception content. Cover expiry, budget,
payload limits and invalid/truncated outputs, with no change to default-off,
cost/expiry or payload/response limits. Keep human-help sources/facts unchanged.

<!-- P02 -->
## P02: Resident sizing and docking

P02-T01: opt-in create option in chat-widget.js, enabled only by resident
assistant.js. Native details/labelled range inputs for width and height, native
pressed-state dock button. CSS custom properties set geometry; max viewport
bounds and safe-area padding. Dock fixes top/right/bottom to zero and hides
the launcher only while docked/open to avoid covering controls; hide restores
launcher before focus return. Dock height is fixed with its height control
disabled. No persistence or custom pointer handlers. Existing log/composer,
consent clearing, pending guards and employee default remain unchanged.
Sizing/dock/undock preserve the historical first-visible message anchor and
proportional within-message offset (browser tolerance 3px or 2% of a message),
or keep bottom-following readers within 3px of the end. Focus remains on the
operated control. Reopening retains the existing scroll-to-bottom behavior.

P02-T02: extend existing generated-answer check using actual constructed HTTP
app and scripted transport, blocked external traffic. Verify native range Arrow
keys/Home/End and pointer operation, exact right/top/bottom geometry, long reply
readability by scrolling, draft/thread preservation, Escape focus return,
reopen/undock, 320/390/1280, enlarged text, short viewport and reduced motion.
Assert both historical-anchor and bottom-following states across geometry
changes, including expanded controls at short heights. Keep existing consent,
source details, label, escaped text, disabled/outage
checks. Re-run shared employee/resident widget check with pinned axe when
available. Document control behavior and limitations in src/api/README.md.

<!-- P03 -->
## P03: Validate and review

P03-T01: use existing /tmp/mv tools only as executables with explicit source
PYTHONPATH, not mutate shared editable distributions. Plain python3 lacks
Playwright; /tmp/mv has the existing dependency. Run full user-specified API
discovery and project Ruff/format/mypy under flock -w 600
/tmp/ama-rpi-heavy.lock. Keep outputs in a fresh external session evidence
directory. Refresh web rules and inspect every changed web file.

P03-T02: independent exact working-candidate Review once, artifact records
execution separately from outcome. Findings route to later work, not repeated
Review. Material in-scope findings block acceptance and are explicitly routed;
never claim completion/conformance over an unresolved material finding.
Commit implementation plus original evidence with privacy-safe identity
and required coauthor trailer; no push.

P03-T03: after clean commit fetch main for receipt comparison only (no rebase).
Run tools/rpi-checks.py --all with its native --lock-timeout 600 (it owns the
same lock; outer flock would deadlock). Missing local prerequisites are honest
blockers; no cloud fallback, live credential lookup or protection changes.
Keep final receipt external and do not claim publication approval.
