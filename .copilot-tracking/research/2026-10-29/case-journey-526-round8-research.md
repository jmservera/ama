---
title: Case journey round eight correction research
description: Pending mutation identity and shared review draft preservation
ms.date: 2026-10-29
---

## Research Brief

Correct round-seven RV-001 and RV-002 for PR #529, Refs #526. Audience:
implementation and independent review. Focused convergence research, preparing
planning. Audit sibling employee mutation paths without visual redesign,
Azure, private data, secrets, remote writes or changes to historical outcomes.

## Research Parameters

Root: `.copilot-tracking/research/2026-10-29/`. Questions: which mutation
entries lack persistent action/target identity, and which refreshes discard
unsubmitted review fields? Required evidence: unit and actual journey/assistant
browser checks with axe. Heavy checks require nonblocking shared-lock admission,
retrying for at most 40 minutes as explicitly authorized.

## Extension Registry and Provenance

Repository instructions and RPI phase skills selected. Web interface guidelines
retrieved 2026-10-29; Fluent, existing plain language and ASCII conventions take
precedence over cosmetic advice. No redesign skill: behavioral correction only.
Research performed inline because the mutation lifecycle is one coupled trace.
Independent plan critique and final review will use bounded separate contexts.

## Direction Controls and Prior Knowledge

Explicit full-loop request authorizes phase progression. Existing automatic
round-seven session completed with Not accepted; this is its selected child,
not a rewrite. Clean topic branch and open matching PR verified; fetched topic
has no remote-only bot commit, so no pull required. PR body already says
`Refs #526`. Local commits only. No user interaction available or needed.

## Research Cycle Log

Cycle 1 opening: Wider inventories the changed employee web mutation paths;
Deeper traces pending identity and queue draft lifetime; Contrarian challenges
DOM-local disabling and stale/revised evidence restoration.

## Evidence Log

* C1: `src/api/src/zava_forward/api/web/app.js:638` field-key exclusion omits
  fieldless refreshes; `:37` is the shared API boundary for all non-raw POSTs.
* C2: `src/api/src/zava_forward/api/web/panels.js:158` and `:347` raw resident
  and challenge handlers bypass that boundary and keep only DOM-local disabling.
* C3: `src/api/src/zava_forward/api/web/assistants.js:225` replaces the queue
  without capturing edits; case restoration helpers at `app.js:878` already
  preserve revision-bound fields and copy-only recovery.
* C4: `src/api/src/zava_forward/api/web/ops.js:187` capacity reconstruction
  resets its local pending flag. Its POSTs share api, so central exclusion also
  protects reconstruction without another local state machine.
* C5: `src/api/src/zava_forward/api/web/case-workspace.js:1` owns projections,
  navigation and observers only. chat, timecapture and role screens either use
  api or have no mutations. No extra mutation transport found.
* C6: `src/api/tests/test_case_journey.py:375` holds raw requests only against
  the original form; `checks/assistants_browser_check.py:265` explicitly expects
  queue reason loss. These are measurable regression gaps.
* W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-29: accessible async feedback and unsaved draft warnings.

## Research Cycle Synthesis

Wider completed: all changed web files and sibling employee transports inventoried.
Deeper completed: pending locks need transport-level ownership outside rendered
DOM; queue drafts can reuse existing revision-keyed snapshot/recovery helpers.
Contrarian completed: disabling buttons or using field-value identities fails
reconstruction and changed-field retries. Locking by complete request bodies
would permit bypass by editing a note; locking globally would block unrelated
targets. Reusing the case session for the queue would lose drafts when no case is
open. Reads must never release pending locks. A lock must include response-body
parsing, not just receipt of HTTP headers.

Accepted: one shared mutation transport lock keyed by endpoint, action and target;
raw forms use that transport, retaining their current status/outcome behavior.
Queue owns a session keyed to the authenticated session and captures latest edits
at replacement time, with existing revision-safe recovery and explicit discard.
Rejected: DOM-only guards, whole-payload keys, automatic mutation retries, applying
old edits to changed revisions. No architecture, authority or visual change.
No further research cycle required: all task questions have direct code evidence.

## Findings and Decision State

Research disposition: executed. Planning Readiness: Ready.
Remaining uncertainty: actual regression results and independent review, owned by
later phases. Publication and human/hosted acceptance remain separate gates.
