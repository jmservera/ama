---
title: Epics 73, 149 and 157 closure checkpoint extension evidence (2026-11-24)
description: Targeted local test runs and signed-in read-only live probes for epics 73, 149 and 157, with each unticked box and why it stays unticked
ms.date: 2026-11-24
ms.topic: reference
---

Scope: synthetic demo, desktop only, branch base `69bc00686f`. Refs #73, #149, #157 and #440. Extends the 2026-11-24 [closure push note](./issue-440-closure-push-live-2026-11-24.md). No `src/` change, no Azure resource created or changed, no write call on the demo, nothing ticked or closed. Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo (owner decision 2026-11-18) and are reported as unverified, not passed. Draft and in-review documents are not approved by this record.

## Evidence

* Epic state read 2026-11-24 over the REST API (`gh issue view` was rate limited): #73 sub-issues 6 of 6 closed (#74, #76, #78, #79, #80, #135); #149 16 of 16 closed (#150 to #156, #225 to #233); #157 7 of 7 closed (#158 to #164, #164 now closed).
* Tools: `python3 -m unittest tools/test_epic_73_child_disposition.py tools/test_epic_73_requirement_trace.py tools/test_epic_child_disposition_audit.py` ran 16 tests, OK. The trace guard checks that each of BG-011, FR-001 to FR-007, FR-032, FR-034 and NFR-003 has exactly one row in the [Epic 73 requirement trace](./issue-73-requirement-trace-2026-11-20.md) and that cited tests exist; it does not run them.
* `src/core`: 13 modules (home case, bulk edits, task queues, SQL queues, import refusals, exception queue, chat threads, chat memory, chat privacy, chat DPIA record, chat routing, journey trace, atlas screen trace) ran 270 tests, OK, 7 skipped, 45 s.
* `src/api`: 17 modules (home case, bulk edit, task queue, ranking policy, exception queue UI, chat isolation, chat panel, chat consent boundary, home chat, the three Epic 149 UX contract, evidence and traceability modules, screen and UX design traceability, accessibility baseline, content standard, design system) ran 288 tests, OK, 1 skipped, 97 s. Core and api ran one after the other.
* Azure, read-only: `az containerapp revision list` shows `ca-cutover-test-demo-api--0000060` and `ca-resident-demo--0000029`, both `Healthy`, traffic 100. Unauthenticated `curl` of `/api/cases` returns 401.
* Signed-in Playwright desktop probe (`.copilot-tracking/evidence/2026-11-24/issue-73-live/live_probe.py`, GET only, sign-in values read at runtime and not printed, output reduced to status and shape): `/api/me`, `/api/cases`, `/api/cases/{id}`, `/api/exceptions`, `/api/ranking/policy`, `/api/ranking/snapshot`, `/api/ranking/publication`, `/api/retention`, `/api/chat/threads` (200, 280 items for the signed-in user), `/api/data-protection`, `/api/assistants/rai-metrics` and `/api/stats` all return 200. Raw output: `live_probe.json` in the same folder.
* Not run: `rpi-checks.py`, SQL Server variants, hosted CI, any write path, the live retention sweep (its fix is recorded in [issue-157-retention-enforcement-live-2026-11-24.md](./issue-157-retention-enforcement-live-2026-11-24.md) and stays unproven live until deployed).

## Per-criterion record

| Epic | Criterion | State | Proven or unproven | Basis |
| --- | --- | --- | --- | --- |
| #73 | Complete the #440 stabilization checkpoint | Unticked | Evidence complete for the demo; box is an owner action | Local suites and live reads above pass; #440 itself is still open for its own boxes |
| #73 | All child features closed or deferred | Ticked | Re-confirmed | 6 of 6 children closed |
| #73 | Each requirement traces to a passing check or a recorded deferral | Unticked | Proven for the demo, subject to owner reading of one deferral | 10 requirements are `Checked` and the cited suites above pass; BG-011 is `Deferred` as a pilot outcome measure that no demo test can prove, which needs an owner decision to count as the recorded deferral |
| #149 | Complete the #440 stabilization checkpoint | Unticked | Evidence complete for the demo; box is an owner action | UX contract, traceability, accessibility baseline, content standard and design-system suites pass; workbench reads 200 |
| #149 | Child features are accepted | Unticked | Unproven as a whole | All 16 children are closed, but acceptance of #152, #155 and #156 rested on person-run usability and assistive-technology evidence that the owner excluded for the demo; automated axe coverage is limited and is not whole-epic WCAG acceptance |
| #149 | Accessibility, content and usability evidence recorded as results; design artefacts traceable | Ticked | Re-confirmed locally | Evidence and traceability modules pass |
| #157 | Complete the #440 stabilization checkpoint | Unticked | Evidence complete for the demo; box is an owner action | Chat thread, memory, privacy, DPIA, routing, isolation and consent suites pass; `/api/chat/threads`, `/api/retention` and `/api/data-protection` return 200 |
| #157 | If accepted, child features are accepted | Unticked | Partly proven, not provable as a whole | All 7 children closed; screen-reader testing, DPO and Legal approval and real-model operation are outside the demo; the retention sweep fix is not proven live |
| #157 | Decision accepted; no memory as evidence; chat consumption bounded | Ticked | Re-confirmed locally | Chat memory, privacy and routing suites pass |
