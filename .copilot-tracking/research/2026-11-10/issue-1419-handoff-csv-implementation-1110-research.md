<!-- markdownlint-disable-file -->

# Task Research: issue-1419-handoff-csv-implementation-1110

| Field         | Value |
|---------------|-------|
| Date          | 2026-11-10 |
| Agent         | rpi-agent, asserted model claude-sonnet-5.5, session label issue1419 |
| Status        | In progress (opening record; completed below) |
| Artifact path | .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-implementation-1110-research.md |

## Research Brief

* Topic: implement the read-only CSV copy of unaccepted handoffs (#1419), now admitted by the coordinator after the earlier partial.
* Prior evidence (preserved, not edited): .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md, plan, details and critique (verdict Revise, 3 Medium, 2 Low, dispositions kept), state, and three partial witness events with verify exit 1 and a first wrong-flag attempt (exit 64). All remain historical.
* Base for this chain: merge commit 4350c3063f5e79703848ac4bdb136c219170d777 (tree 33daf78d81a344b191b269ea619b5aca608ac1a4) of parent 2cc340270b5fca04d8374f334a4a9fd6dc94a8e9 into branch tip 50d76a47b067ba92ffb7e40b369163fc60f21990, by ordinary merge, no conflict. This chain's launch event was recorded after the merge.
* Admitted decisions (coordinator): shared parser and shared JSON and CSV branch; exactly 13 fields in source order (the earlier 14 was wrong); Offered (exports Sent), Received and Escalated included, Withdrawn also excluded with Accepted, Completed, Declined; one EXPORT_KINDS mapping; no LIST_EXPORTS registration and no list_rows change; filename unaccepted-handoffs.csv by narrow override; one GET_ENDPOINTS inventory entry; new focused test module; only the pendingHandoffs success-path link and helper in app.js; API README ageing and export paragraphs; no core, role, projection, serializer, threshold or mutation change; no core README fix and no new issue.
* Validation override (owner demo policy): targeted modified and impacted validation, not the full local gate. Basis recorded prospectively in the plan. It overrides the earlier critique's PC-001 full-tier default; that finding stays as history. It is not a waiver of any failing or missing relevant check and not a green full receipt. Hosted source CI and independent exact-head assessment remain required.
* Posture: focused. Limits: own environment only, synthetic owned data, no SQL, Docker, cloud, full gate, push, PR, issue or board write, no fetch, merge or rebase after this chain begins.

## Pre-Marker Disclosure

* Before this artifact existed in this chain, the session had re-read the server.py CSV registry, query parsing, gate and JSON route sections at the merged head (for the unchanged-contract check), and had inspected installed package origins. The earlier chain's reading is likewise not re-attested. The research-open marker attests only that this artifact and the state existed from its time.
* Installed editable packages originally pointed at the main checkout, not this worktree; an own venv /home/azureuser/.venvs/issue1419 (system site packages for third-party dependencies, no-deps editable installs of src/core, src/agents and src/api from this worktree) was created and its import origins checked.

## Research Parameters and Extensions

| Field | Value |
|-------|-------|
| Posture | focused (bounded internal task, named source targets, provenance: coordinator brief) |
| Scope | server.py hunks, pendingHandoffs link, test harness and seeds, README paragraphs, web guidance, existing browser-check precedent |
| External scope | one fetch of the Vercel web interface guidelines source (required by repository web guidance) |
| Extensions selected | repository instructions; rpi-research, rpi-plan, rpi-plan-critique, rpi-implement, rpi-review; web-design-guidelines (fetched); redesign-existing-projects (read; its generic redesign rules are not applied because the repository design-system and content standard take precedence and no redesign is admitted); UX standards (content-standard, design-system, WCAG baseline) |
| Extensions skipped | design-taste-frontend family (public pages, not an app panel); specialist subagents (tightly coupled, inline) |
| Interaction | none possible; decisions were pre-supplied by the coordinator |

## Research Cycle Log (cycle 1)

* Wider: server hunks, test seeds (five cases, two managers needed), state transitions (offer, receive, escalate, accept, decline, withdraw, complete), panel code, precedent export links, web guidance, existing tests that pin wording or routes.
* Deeper: traced the handoff state machine to know how to reach each state; confirmed `handoff_view` and `handoff_ageing` at this head; confirmed the server gate order and that the unaccepted JSON branch sits after the kind gate.
* Contrarian: tested the shared-branch design against the earlier critique (PC-002 resolved), the single-case-per-test limit (re-offer is allowed after Declined or Withdrawn, but crafting handoff dicts directly is simpler and exact), and the claim that an empty CSV is practically unreachable from the panel.

Parent synthesis: all admitted decisions are consistent with the source. No second cycle: no material gap remains; browser evidence is an execution step, not missing evidence.

## Evidence Log

Paths relative to worktree root; lines at merged head 4350c3063f.

| ID | Finding | Location | Confidence |
|----|---------|----------|------------|
| C1 | JSON branch: blank-retaining first-value parse, range check `0 < v < 1e6`, 400 text, PermissionError 403, after the kind gate | src/api/src/zava_forward/api/server.py:722-735, gate at 492 | high |
| C2 | Generic `q` is parsed without blank retention; LIST_EXPORTS dispatch would use it and catch only PermissionError; filename is the last path segment | src/api/src/zava_forward/api/server.py:472, 494-500 | high |
| C3 | EXPORT_KINDS maps a csv path to a kind string; absent mapping derives a non-staff kind | src/api/src/zava_forward/api/server.py:172-175, 237-240 | high |
| C4 | Row projection of 13 keys in fixed order; states Offered, Received, Escalated only; Offered shows `Sent`, Declined `Rejected` (excluded) | src/core/src/zava_forward/core/workflows.py:20,43-86 | high |
| C5 | Visibility: sender, receiver or MANAGER_ROLES; stable sort by descending age | src/core/src/zava_forward/core/workflows.py:336-350 | high |
| C6 | State transitions reachable by API: offer, receive (recipient), escalate (offerer or manager, to a manager), accept, decline, withdraw, complete; re-offer allowed after non-active states | src/core/src/zava_forward/core/workflows.py:185-318; src/api/src/zava_forward/api/server.py:1425-1446 | high |
| C7 | Seed: five cases (ZF-1 to ZF-4 owned by Sam RLO-01, ZF-5 by Pam PM-01), two staff; tests add Rae, Rex, Kim and need a Programme Support Officer for the second manager | src/api/tests/test_handoff_api.py:19-55; core/tests dataset | high |
| C8 | Test harness: SqlStore on a temp seed, App, loopback server, cookie login helper; `call` is POST when a body is given and returns parsed JSON only, so a CSV test needs its own text helper | src/api/tests/test_handoff_api.py:75-99; test_list_export_api.py:30-60 | high |
| C9 | Panel success branch: heading, existing "Download for Excel" link to /api/handoffs.csv with download handoffs.csv, then list; hide on empty; alert on error | src/api/src/zava_forward/api/web/app.js:754-775 | high |
| C10 | Wording precedent: link plus helper in one paragraph, "It is a read-only copy; changes in it are not imported back." | src/api/src/zava_forward/api/web/ops.js:485-486; app.js finance link | high |
| C11 | Web guidance fetched 2026-11-10 from raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md: relevant rules are semantic anchor for navigation or download, visible focus, empty states, active voice, specific labels, no `transition: all`. Title Case for buttons in that source conflicts with the repository content standard (plain, sentence-style); repository standard and coordinator wording prevail | external, retrieved 2026-11-10 | high |
| C12 | Content standard: short sentences, active voice, everyday words, plain ASCII, no em dashes | docs/reference/research/ux/content-standard.md:18-31 | high |
| C13 | WCAG baseline records native links, 24 CSS px target size on link buttons, visible focus; no accessibility conformance claim is made by engineering checks | docs/reference/research/ux/wcag-conformance-baseline.md:44-50 | high |
| C14 | Installed editable packages point at the main checkout; an own venv with editable installs from this worktree is needed so tests exercise this source | pip list; venv import check | high |
| C15 | Existing browser harness `tests/test_handoff_read_guidance.py` is a Playwright test with the panel locator; no checker script covers the handoff panel | src/api/tests/test_handoff_read_guidance.py:217-235 | medium (read, not run) |

Contradictions: the earlier 14-field claim is wrong (13, C4); recorded in the issue tracking correction below. The core README "not yet wired" line (core/README.md:3003) is stale but out of scope per coordinator.

## Findings

* F1: Shared parser and branch are safe and minimal (C1 to C3). The CSV branch returns 400 and 403 with the JSON bodies; kind gate unchanged.
* F2: Tests can set each state exactly by crafting `store.cases[id]["handoff"]` under a patched clock, plus one real API offer for a realistic path (C4 to C8).
* F3: The link goes in the success branch directly after the existing link, as its own paragraph (C9, C10).
* F4: An empty CSV is reachable only by direct request; the panel hides when pending rows are empty and, by source, pending and unaccepted membership match (C4, C5, C9). Documented, not guaranteed.
* F5: Web guidance imposes nothing that the native anchor does not meet; no new style is needed (C11 to C13).

## Alternatives and Decision

Selected: as admitted. Rejected: registry registration, `format=csv`, reuse of `/api/handoffs.csv`, rendered queue, serializer change (reasons as in the earlier research).

## Validation Override Record (prospective)

* Earlier critique PC-001 defaulted to the full tier. The owner demo policy selects targeted modified and impacted validation. Basis: the exact permission check and store projection are reused; no new role, permission or persistence path; comprehensive negative-boundary and regression tests plus affected API lint and type checks and a real minimal affected browser check are planned; hosted source CI and independent exact-head assessment remain required. Not a waiver of any failing or missing relevant check, not a green full receipt. No SQL, Docker, full gate or cloud fallback. PC-001 stays as the original finding; the override is dated 2026-11-10.

## Unresolved

* Whether a heavy canonical browser lock exists and is free (checked at execution; precise partial if busy).
* Final wording refinement is native and within the coordinator's meaning.
* Hosted CI state and independent assessment: not available here.
* Issue-text correction: the public issue body does not contain a literal 14; the 14 was in the coordinator's brief and refinement. Recorded as a correction, no issue write.

## Planning Readiness

* Status: Ready. Research disposition: executed. Evidence: C1 to C15. Blockers: none for planning.

## Closeout

| Field | Record |
|-------|--------|
| Research execution status | Complete, inline (no worker), static plus one external guideline fetch |
| Waves | Wider, Deeper, Contrarian |
| Continuation | Plan with amended scope, then one critique, then implement and review |

## Sources

* https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-11-10 (web guidance rules, C11). All other evidence is repository-internal.

## Artifact Self-Check

* [x] Questions answered, three waves, posture and limits recorded, C# IDs with path:line, sources stated, override recorded prospectively.
* Limits: nothing executed yet; Playwright state and lock unverified; one reader.
