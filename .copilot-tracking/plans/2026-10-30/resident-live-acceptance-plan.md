<!-- markdownlint-disable-file -->
# Implementation Plan: resident-live-acceptance

Task ID: resident-live-acceptance-2026-10-30. Date: 2026-10-30.
Status: Research/Plan/Implement/Review complete; parent local persistence pending.
Mode: explicitly requested full loop.

## Executive Summary

The supplied resident identity signed in through the real form with HTTP 200
on its only submitted login. Actual consent gating, two-turn chat, keyboard,
three-width reflow and honest rat fallback were observed. Both replies used
rules; no AI-generated answer, exact 200ms loading, full accessibility or
employee map/case acceptance follows. Original critique is preserved.
Independent Review is Complete with outcome Residual work, one Medium and
three Low evidence/provenance findings routed to later work. A local Refs-only
commit/gate remains. No push or issue-state update is authorized.

### What You May Not Know

A generic 401 cannot distinguish account, domain or password rejection.
The resident has one fixed assistant; the employee skill-picker and expanded
map/case obligations cannot be accepted by testing this resident site.

## Sources

Research: .copilot-tracking/research/2026-10-30/resident-live-acceptance-research.md.
Details: .copilot-tracking/details/2026-10-30/resident-live-acceptance-phase-details.md.
Original sibling Review is C1; exact issue criteria are W1-W3 in Research.
Baseline branch: chore/resident-acceptance-1030, initially clean, no prior PR.

## User Decisions and Requirements

* Full dated Research, Plan, Implement and Review under .copilot-tracking/.
* Resident site only; credentials from the named local two-line file, read
  inside automation only, with whitespace/line-ending trimming.
* Real form POST /demo/login with CSRF; maximum two attempts and immediate
  stop on a 401. No secrets, screenshots, trace, HAR or video.
* After access, test consent before data use for AI, bottom-right persistent
  chat, Enter/Shift+Enter, thin labels, agent selector, rat-question relevance
  and accessibility basics.
* Record proven/unmet criterion evidence. Local commit, Refs only; no push.
* No vault, Container App secrets, Azure writes or auth-policy changes.

## Goals

Obtain honest resident live acceptance or a definitive bounded access blocker.
Preserve earlier adverse results and explain compound-criterion limits.

## Scope and Non-Goals

One supplied identity, one target origin, normal resident UI and read-only
advisory chat. No callback booking, consent-to-works action, employee access,
map/case proxy acceptance, product edits or remediation.

## Functional Requirements

Use the live app's form and CSRF machinery. Observe only endpoint path/status
and selected public/control text; never headers, bodies, cookies or identities.
Keep all 19 original criteria in an ordered matrix, with resident subparts
and employee-only/out-of-resident-scope obligations explicitly separated.
Also record the owner's resident agent-dropdown check, even though issue
550-04's selector is explicitly employee-scoped.

## Non-Functional Requirements

Credential values never enter source, CLI argv, environment, tool calls or
output. Mask both DOM input types before filling, allow no recording, close the
ephemeral browser in finally, and emit only allowlisted sanitized observations.
Disable Playwright debug/protocol logging in automation. Do not retain response
bodies or raw DOM snapshots. Error handling emits fixed stage/category only,
not exception text. Fingerprint exact executed script before/after execution.
Use existing /tmp/mv Playwright if still available; restore a pinned
task-owned external runtime only after an actual missing-dependency failure.

## Acceptance Criteria

* AC-01: Actual real-form submission with trimmed two-line credentials,
  at most two attempts; stop live execution immediately after any 401.
* AC-02: All nine chat, four map and six case criteria have evidence-linked
  proven/unmet outcomes; source/shell observations are not authenticated proof.
* AC-03: If access succeeds, exercise actual consent, multi-turn chat,
  Enter/Shift+Enter/Send, disabled capability reasons, selector, answer label/
  sources, rat fallback and basic keyboard/reflow/motion semantics.
* AC-04: Dated original critique and independent Review persist, with honest
  blockers and a local Refs-only commit. No remote write.

## Test Ownership and Change Budget

Canonical targets: one task-specific Playwright script and sanitized JSON
under .copilot-tracking/changes/2026-10-30/resident-live-acceptance/.
Generated targets: its JSON evidence and external gate output only.
Removals: none. Maximum additions: one automation script, one primary run JSON,
six phase artifacts (research/plan/details/critique/changes/Review), one state.
Implementation amendment: one extra sanitized pre-login-timeout JSON preserves
the initial failure (zero credential reads/submissions), without overwriting it.
If actual browser failures need additional evidence, amend the budget explicitly.
Semantic checks: directly observed UI/request ordering and measured geometry.
Regression coverage: no application changes; no new local product tests claimed.
Validation: script syntax, exact script SHA-256, JSON shape/secret exclusion in
automation, 19-row matrix, Git diff, independent Review, local commit, then
required full local gate with --lock-timeout 0 and external output.
Busy shared gate or missing prerequisite blocks publication, never auth evidence.
No full accessibility, deployed-source parity, model-use or human approval claim.

## Ordered Issue Requirements Baseline

Source: issue bodies retrieved with gh on 2026-10-30 (Research W1-W3).
Any unproven required subpart keeps a whole compound criterion Unmet.

| ID | Complete compound requirement | Observation owner and boundary |
| --- | --- | --- |
| 550-01 | Both sites use one shared component, bottom-right icon launcher opens popup | Resident launcher/popup live; employee/shared-use unproven |
| 550-02 | Persistent scrolling chronological thread, newest bottom, pinned input, stays open after send | Conditional authenticated resident multi-turn/geometry |
| 550-03 | Enter sends, Shift+Enter newline, send button present | Conditional actual resident composer |
| 550-04 | Compact input-area selector changes employee agent/skill and shows active one | Employee outside scope; separately observe fixed resident selector |
| 550-05 | Attach and Voice present or disabled with stated unsupported reasons | Conditional resident controls/reason association |
| 550-06 | AI-generated content has thin label and collapsed sources, HAX/Teams pattern | Actual generated resident response only; rules output insufficient |
| 550-07 | Resident consent remains before any data use | UI consent state and assistant request ordering; server-only use unproven |
| 550-08 | Rat-like free text gets relevant answer or honest inability plus contact, not home summary | Actual rat answer text after record-use permission |
| 550-09 | Loading after 200ms, errors shown, keyboard/screen-reader semantics, reduced motion | Actual resident timing/errors plus keyboard/live/reflow/motion; no full AT claim |
| 551-01 | Expanded map has compact header filters at top | Employee map outside resident scope, Unmet |
| 551-02 | Filter updates markers and header state consistently | Employee map outside resident scope, Unmet |
| 551-03 | Keyboard operation, non-colour selected state, readable narrow | Employee map outside resident scope, Unmet |
| 551-04 | Behavior covered by browser or unit test | Historical source coverage only, not re-executed live proof |
| 552-01 | Workflow steps use presentation icon set with text labels | Employee case outside resident scope, Unmet |
| 552-02 | Visibly thinner layout, less vertical space per step | Employee case outside resident scope, Unmet |
| 552-03 | One-line blocker summary plus full keyboard/touch tooltip/popover | Employee case outside resident scope, Unmet |
| 552-04 | Attached tabs/panel outside inner scroll box, panel scrolls beneath | Employee case outside resident scope, Unmet |
| 552-05 | Preserve Fluent 2 and WCAG baselines | Full case criterion outside resident scope; no global conformance |
| 552-06 | Desktop and narrow browser evidence | Actual case unavailable on resident site, Unmet |

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Bounded live execution

* [x] P01-T01: Create safe automation; record fingerprint; perform real login.
* [x] P01-T02: On 401 stop; otherwise execute authenticated resident checks.

<!-- rpi:phase id=P02 -->
### P02: Evidence reconciliation and local persistence

* [x] P02-T01: Write complete ordered matrix, amendments and blockers.
* [x] P02-T02: Obtain one independent original Review and route its findings.
* [ ] P02-T03: Commit locally with privacy-safe identity and Refs; attempt gate.

## Critique Disposition

One independent critique executed; original verdict Revise is preserved in
.copilot-tracking/plans/2026-10-30/resident-live-acceptance-critique.md.

* PC-001: Rejected. The critic's claimed blanket prohibition of temporary
  paths does not exist in this parent's applicable execution instructions.
  Existing /tmp/mv use is explicitly documented in src/api/README.md:95.
  No new environment or input copying is needed. Browser scratch is owned
  by its ephemeral context and closed in finally; no foreign paths deleted.
* PC-002: Applied directly. The complete ordered 19-entry compound baseline
  above is persisted before execution with planned evidence boundaries.
* PC-003: Applied directly. Details require inspecting initial consent first,
  with unconsented, already-consented and indeterminate branches; only the
  unconsented branch may attempt a negative no-request check.

No unresolved significant decision; no second critique authorized or needed.

## Follow-Up Items

No child work selected. Actual AI label/sources, precise 200ms behavior,
independent employee acceptance and human accessibility remain later work.
No repair, model-enablement, Azure or employee-access authority follows.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-30/resident-live-acceptance-changes.md.
Before handoff reconcile critique, summary, requirements and task details.
