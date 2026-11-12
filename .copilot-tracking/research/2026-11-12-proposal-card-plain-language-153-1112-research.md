---
title: Issue 153 proposal card plain-language default research
ms.date: 2026-11-12
task_id: 153-proposal-card-1112
---

## Status

Original dated research, 2026-11-12, branch `feat/demo-proposal-card-plain-language-153-1112`, base `b6f61b1204c294c0922922af5b451de09b8ad97a`. Local-only frozen candidate: no push, PR, issue or board edit.

## Authority

Owner approved on 2026-11-12: "Approve plain-language default with technical evidence retained". Bounded scope: default employee proposal cards become task-focused and plain language; complete technical evidence stays reachable through an explicitly labelled technical disclosure. No audit removal, permission or approval change, or human resident-wording acceptance.

## Sources read

* Issue #153 body and all comments (to 2026-11-11): C1 ticked; C2, C3 and C5 unproven. Staff-time (#1335) and personal-handoff (#1367/#1376, #1449) slices are merged and not rebuilt.
* Both case studies, `docs/reference/README.md`, `docs/reference/memory.md`, and the UX content standard, design system and WCAG baseline (disclosures keep native semantics; owner Fluent 2 preserved).
* Web Interface Guidelines fetched 2026-11-12 from `vercel-labs/web-interface-guidelines/main/command.md` (complete). The `redesign-existing-projects` skill was read; its visual-overhaul rules are out of scope by owner direction, so only structure and copy change.

## Source facts (base b6f61b120)

`src/api/src/zava_forward/api/web/assistants.js`, `assistantProposal()`:

* Two separate collapsed `details` hold raw `JSON.stringify` output of `p.snapshot` ("Permitted sources, versions and hashes") and `{envelope, history}` ("AI usage and changes to this suggestion"). Their `pre` blocks are not keyboard focusable, so a scrollable region is unreachable by keyboard.
* The Edit button reveals a textarea whose label and `aria-label` are "Edited evidence proposal JSON", with no explanation of why raw JSON is shown. The edit path (`act("edit-accept")` with `JSON.parse`) is operationally required and stays.
* Safety text (AI-not-approved label, nothing-sent notice, draft-review notice, unknowns, stale and denial status, reason, verification and review controls) is already outside the details and must stay there.

Dependents of the label: `src/api/checks/assistants_browser_check.py` (many locators, including "Earlier ..." recovery labels derived in `app.js`), `src/api/tests/test_case_journey.py:1299`. Guard `test_content_standard.py` allows only the identifiers `envelope: p.envelope` and `p.snapshot`; these remain valid because the JSON key and identifiers are unchanged. No exemption is removed.

Environment fact: `zava-forward-api` is installed editable from a different checkout (`/home/azureuser/source/ama`), so browser checks need explicit `PYTHONPATH` entries for this worktree's `src/*/src`, and a short working directory (Chromium socket path limit).

## Planning readiness

Ready. Smallest change: one native `details` disclosure grouping both technical records with labelled headings, keyboard-focusable named `pre` blocks, and a purposeful label and note on the edit field. No narrative summary is generated; no field is dropped.
