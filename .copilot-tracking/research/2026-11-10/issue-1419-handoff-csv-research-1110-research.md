<!-- markdownlint-disable-file -->

# Task Research: issue-1419-handoff-csv-research-1110

| Field              | Value                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------|
| Date               | 2026-11-10                                                                                     |
| Researcher / agent | rpi-research, hve-core-all:rpi-agent (asserted model claude-sonnet-5.5, session label issue1419) |
| Status             | In progress (opening record; completed below)                                                  |
| Artifact path      | .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md         |

## Research Brief

* Topic: read-only CSV copy of the existing unaccepted-handoff ageing queue (`GET /api/handoffs/unaccepted`), issue #1419, child of #80 under #73.
* Purpose: verify the exact JSON contract, negative boundaries, serializer and empty-result semantics, and propose the smallest independently scoped CSV plus truthful handoff-panel affordance.
* Audience: the coordinating Root session deciding whether to admit source implementation.
* Output mode: analysis with a convergence recommendation for planning (a minimal scope proposal); no implementation, no review.
* Admission: RESEARCH + PLAN/DETAILS/CRITIQUE only. Implement and Review are not executed and no Review artifact exists.
* Frozen base: HEAD `12d3ac842c0474b424ed15498d6716d9c93099cf`, tree `7d3d053ce5e9a961b25e97dda4d08d3a3475dce4`, on branch `docs/handoff-unaccepted-csv-1419`; contains main `6d4cd62475ba89a214055f761b8e3276ef063d44`.

## Research Parameters

| Field                            | Value |
|----------------------------------|-------|
| Research question(s)             | See Research Questions Q1 to Q10 |
| Codebase scope                   | `src/api` (server, web, tests), `src/core` (workflows, projection, list_export), read-only |
| External scope                   | none (repository-internal contract research) |
| Initial internal candidate areas | `server.py`, `web/app.js`, `workflows.py`, `projection.py`, `list_export.py`, `test_handoff_api.py`, `test_list_export_api.py`, `test_role_endpoint_inventory.py`, READMEs |
| Initial external candidate areas | none |
| Research posture                 | focused |
| Posture provenance               | caller-specified bounded objective (named source targets, bounded contract) |
| Explicit limits / deadline       | static source reading only; no tests, browser, app, fixture driver, installs or edits to source; no deadline |
| Posture-specific completion basis| focused scope and materiality: every named contract item answered with C# evidence |
| Edits allowed during research?   | no, research-only (tracking artifacts only) |
| Resolved evidence root           | .copilot-tracking/ in this worktree |
| Known constraints / excluded sources | no private or default data; no parent worktree access; no other session tracking state; no BG-010 threshold decision |

## Pre-Marker Disclosure (adverse record kept)

* The launch witness record (seq 1) was written before any reading. Before this artifact and the state file existed, this session had already read the coordinator scope refinement, the issue body and the witness tool, and had read the eight named source files, `test_role_endpoint_inventory.py`, `test_progress_report_api.py` (clock-patch precedent), the API and core READMEs and the UX content standard for the handoff area. That reading is not covered by a `research-open` observation. The marker therefore attests only that the research artifact and state existed from the time it was written, not that all reading followed it.
* A first attempt to locate the RPI skill directories with a filesystem-wide `find` was stopped after it ran without output for 30 seconds. It changed nothing.

## Opening State

Research disposition will be `executed`. Planning Readiness is assigned only at the end of this artifact.

## Extension Registry and Provenance

| Kind                | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
|---------------------|-----------|----------------------|-------------------------------------|---------------------------|
| Instruction         | Repository instructions (AMA Repository Instructions, applyTo `**`) | Always applies | Evidence conventions, branch and commit rules, Web Development Guidance, validation tiers, no-KB-change unless asked | Selected. Web guidance applies only to a future web hunk; no web edit or accessibility claim in this launch |
| Instruction         | RPI Agent configuration | Selected agent | State contract, one critique, no Implement or Review here | Selected, narrowed by the owner brief to research and plan only |
| Skill               | rpi-research, rpi-plan, rpi-plan-critique | Phase skills | Artifact templates | Selected |
| Skill               | web-design-guidelines, design-taste-frontend, redesign-existing-projects | Web guidance names them for future web work | Fetch current guidelines before web edits | Skipped here: no web edit or review in this launch; recorded as a precondition for the later admitted app.js hunk |
| Research specialist | RPI Researcher and other subagents | Delegation allowed only for named independent uncertainty | none needed | Skipped: tightly coupled contract trace followed directly, inline fallback recorded |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
|------------------|---------------------------------------|----------------------|-------------------------------------------------|
| Intake           | Non-interactive run; the brief fixes scope, posture and limits | none requested | Proceed focused |
| Direction change | none arose | none | none |
| Convergence      | Non-interactive; unresolved product choices are recorded for the coordinator, not asked | unanswered by design | Listed under Unresolved Decisions |

## Scope and Success Criteria

* In scope: the exact existing JSON route and its permission, projection, ordering and query semantics; the CSV registry, dispatch, kind mapping and serializer; the handoff panel in `app.js`; existing tests and docs that a new route touches; ownership overlap with the parent topic.
* Out of scope: any code, test, config or knowledge-base edit; running anything; a rendered queue or filter UI; threshold approval; real data; hosted or SQL behavior.
* Success: each named contract item answered with codebase evidence, a smallest scope proposal, and a test and integration plan, with observed facts kept apart from proposals.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
|--------------|-----------------------|---------------------|--------|
| exclude | No role widening, selectors, pagination, default thresholds, escalation, mutation, global serializer change | owner brief | Proposals respect these |
| exclude | No Capacity (`ops.js`, `capacity_browser_check.py`), retry or session helper edits | owner brief | Overlap analysis only |
| narrow | Static reading only; no tests or runtime | owner brief | Behavior statements are source-derived and unexecuted |

## Research Questions

|   # | Sub-question | Type | Priority | Status |
|----:|--------------|------|----------|--------|
| Q1  | What is the exact JSON route contract: auth order, role kind, query parsing, errors? | depth | H | answered |
| Q2  | Which rows are visible to whom and which states qualify or are excluded? | depth | H | answered |
| Q3  | What are the exact fields, order, ageing, reasons and threshold semantics? | depth | H | answered |
| Q4  | What does the CSV serializer do to each field type and to an empty result? | depth | H | answered |
| Q5  | What is the registry, kind and dispatch structure, and the smallest correct place for a new route? | depth | H | answered |
| Q6  | What does the existing handoff panel render and where can a truthful affordance live? | depth | H | answered |
| Q7  | Which existing tests or docs a new route would break or contradict? | breadth | H | answered |
| Q8  | What overlap exists with the parent topic's owned hunks? | breadth | H | answered |
| Q9  | How can tests compare CSV to JSON under a controlled clock? | depth | M | answered |
| Q10 | What in the coordinator brief or refinement contradicts the source? | breadth | H | answered |

## Prior Knowledge Gate

Prior knowledge (the coordinator refinement) was treated as a hypothesis set, not evidence. Every claim below was re-derived from this worktree's source. Items that differ from the refinement are in Contradictions / Conflicts.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline (no worker). Candidate areas enumerated: server dispatch and registries (C1 to C8), core projection and serializer (C9 to C16), web panel (C17 to C19), tests and role inventory (C20 to C24), docs (C25 to C26), parent overlap (C27). Counter-areas: a `format=csv` selector on the JSON route, reuse of `/api/handoffs.csv`, a new core method, a rendered queue.

#### Wave 2: Deeper

Inline. Traced the request from socket to response for the JSON route and for the generic CSV path, the visibility and ageing code, the serializer per type, the panel life cycle, and each test that enumerates routes or the CSV registry.

#### Wave 3: Contrarian

Inline. Looked for evidence against the refinement and against the simplest design:

* Field count claim "fourteen" against the actual dict (13). Refinement is wrong on count, right on names (C12).
* Blank-value query parsing: the generic CSV path parses the query without blank retention, JSON with blank retention, so a naive reuse diverges for `max_age_hours=&max_age_hours=5` (C3, C6).
* Excluded states: refinement omits Withdrawn (C11).
* Registry route versus dedicated branch: registering in `LIST_EXPORTS` forces a signature or exception change (C5, C6, C7).
* Existing panel hides itself when there are no pending rows, so a link inside it is unreachable when the queue is empty, but the pending and unaccepted row sets come from the same state set and visibility rule (C17, C10).
* A roles-inventory test fails when a new `/api/...` literal is added to `server.py` without a matching GET entry (C21).
* Docs conflict: core README says the ageing view is not wired to an API route, the API README and `server.py` show it is (C25, C26).
* Alternative `?format=csv` on the existing JSON route or reuse of `/api/handoffs.csv` rejected (see Alternatives).

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale | Treatment |
|------------------|----------|-------------|-----------|-----------|
| JSON route contract and negative boundaries | C1 to C4, C8 | accepted | Directly read and consistent with existing test | Finding F1 |
| Visibility, states, exclusions | C10, C11 | accepted with correction (Withdrawn added) | Source defines `HANDOFF_PENDING` | F2 |
| "Fourteen fields" | C12 | rejected, actual 13 | Counted from the `dict(...)` keyword list | Contradiction recorded |
| Registry-based dispatch is the obvious home | C5, C6, C7 | rejected as primary, kept as alternative | Needs signature change or global exception catch and loses parse parity | Alternative A |
| Dedicated shared branch for JSON and CSV | C2, C3, C6 | accepted as recommendation | One parse path, no global change | Recommendation |
| Pending panel as host | C17, C10 | accepted with limits | Same membership by source, link absent when empty | F6 |
| No threshold control in UI | C11, C12 | accepted | Refinement and brief forbid; echo label "approved" for any supplied number is existing behavior | F3, risk R4 |
| Parent overlap limited to two files | C27 | accepted, observed only at the frozen pin | `git diff --name-only` main to HEAD | F8 |

#### Cycle Re-entry Evaluation

No second cycle. Every question is answered with code evidence, no wave produced a new material question that the focused posture could not close, and remaining items (product wording, filename, tier classification) are decisions, not missing evidence. The static-only limit prevents confirming behavior at runtime; that gap is recorded, not closed.

## Evidence Log

### Codebase Evidence

Paths are relative to the worktree root. All lines are at frozen HEAD `12d3ac842`.

| ID  | Claim / finding | Location | Tool | Confidence | Notes |
|-----|-----------------|----------|------|------------|-------|
| C1  | JSON route `/api/handoffs/unaccepted` exists; pending `/api/handoffs` is a separate route calling `pending_handoffs` | src/api/src/zava_forward/api/server.py:722-735 | read | high | |
| C2  | JSON route reads `max_age_hours` with `keep_blank_values=True`, takes the first value, blank or missing means None, else `float`, requiring `0 < v < 1e6`, else 400 `max_age_hours must be a positive number of hours.`; PermissionError gives 403 | src/api/src/zava_forward/api/server.py:724-735 | read | high | NaN and infinities fail the range test; unknown keys ignored; no as_of, paging, selector |
| C3  | Generic request query `q = parse_qs(url.query)` is parsed once without `keep_blank_values` | src/api/src/zava_forward/api/server.py:472 | read | high | A blank value is dropped, so `?max_age_hours=&max_age_hours=5` would read 5 through `q`, not blank as in JSON |
| C4  | Order of gates: unauthenticated gives 401 (L470), then `simulator_admin`, then kind-level `projection.allowed` gives 403 (L492), all before route branches | src/api/src/zava_forward/api/server.py:470-493 | read | high | |
| C5  | CSV registry `LIST_EXPORTS` and `EXPORT_KINDS`; `get_kind` consults `EXPORT_KINDS` before `LIST_EXPORTS`, and a `LIST_EXPORTS` path without a mapping gets kind `path[len("/api/"):]` | src/api/src/zava_forward/api/server.py:172-175,237-240 | read | high | A bare registration would yield kind `handoffs/unaccepted.csv`, not in `STAFF_GET`, so every staff role would get 403 |
| C6  | Generic CSV dispatch: `list_rows(s,u,path,q)`, catches only PermissionError (403), sends `text/csv; charset=utf-8` and `attachment; filename=<last path segment>`; `list_rows` has one caller | src/api/src/zava_forward/api/server.py:181-199,494-500 | read, grep | high | A ValueError would be uncaught; derived filename would be `unaccepted.csv` |
| C7  | `/api/handoffs.csv` calls `pending_handoffs` (different projection) | src/api/src/zava_forward/api/server.py:187-188 | read | high | |
| C8  | `get_kind` maps both `/api/handoffs` and `/api/handoffs/unaccepted` to kind `handoffs` | src/api/src/zava_forward/api/server.py:243 | read | high | |
| C9  | `handoffs` kind is in `STAFF_GET`; contractors only `me, cases, case, workorders`; Application Administrator only `me`; unknown roles denied; `STAFF_ROLES` are seven staff roles | src/core/src/zava_forward/core/projection.py:34-40,65-72 | read | high | `handoffs.csv` is also a kind string there (L39) |
| C10 | `unaccepted_handoffs`: re-checks `STAFF_ROLES`, `as_of = as_of or _now()` (minute precision), under lock keeps rows where the user is `from_code` or `to_code` or has a manager role (Retrofit Programme Manager, Programme Support Officer), sorted by descending age | src/core/src/zava_forward/core/workflows.py:13,27-28,336-350 | read | high | Stable sort: ties keep case insertion order. `pending_handoffs` uses the same states and the same visibility test (L322-334) |
| C11 | Qualifying states are `Offered`, `Received`, `Escalated` (`HANDOFF_PENDING`); `Accepted`, `Completed`, `Declined`, `Withdrawn` return None; `status` shows `Offered` as `Sent`; `Declined` as `Rejected` | src/core/src/zava_forward/core/workflows.py:17-20,43-57,60-67,290 | read | high | Withdrawn is set at L290 and is excluded; the refinement omitted it |
| C12 | Row has exactly 13 keys in this order: case_id, status, age_hours, due_at, chase_owner, chase_owner_code, proposed_receiver, escalated, needs_escalation, reasons, approved_limit_hours, limit_note, as_of | src/core/src/zava_forward/core/workflows.py:78-84 | read, count by hand | high | The brief and refinement say fourteen. Not executed; counted from the keyword list |
| C13 | Age is `round(hours, 2)` from `offered_at` to timezone-aware `as_of`; reason "Handoff due time has passed" if `due_at` < now; reason "Unaccepted for more than the approved {limit} hours" if limit given and age > limit; `needs_escalation` is false for Escalated; limit None gives `approved_limit_hours` None and note "Approved escalation time not set (OD-09)" | src/core/src/zava_forward/core/workflows.py:60-85 | read | high | Caller-supplied number is labelled "approved" (existing behavior) |
| C14 | Projection is a narrow explicit dict: no resident name, address, contact, note, evidence, raw handoff or history; `handoff_view` deep-copies so no mutation | src/core/src/zava_forward/core/workflows.py:43-57,78-84 | read | high | Contrast with `pending_handoffs` adding resident, address and the full handoff (L322-334) |
| C15 | Serializer: None gives empty, bool gives Yes or No, mapping or list or tuple gives compact sorted-key ASCII JSON, other values `str`; text starting `= + - @ TAB CR` gets a leading apostrophe; columns are first-seen keys; csv.writer default CRLF | src/core/src/zava_forward/core/list_export.py:15-41 | read | high | Empty reasons list becomes `[]`; a negative age (`-0.5`) becomes `'-0.5` |
| C16 | Empty rows: headers list is empty, so the output is a single blank record (`\r\n`) with no column names | src/core/src/zava_forward/core/list_export.py:31-41 | read | high | Static reasoning; not executed |
| C17 | Panel `pendingHandoffs()` reads `/api/handoffs`, hides itself when empty, links `/api/handoffs.csv` as "Download for Excel", renders only on the `mine` view | src/api/src/zava_forward/api/web/app.js:754-768,894 | read | high | No consumer of `/api/handoffs/unaccepted` exists in `web/*.js` |
| C18 | Panel error path shows an alert and no download link | src/api/src/zava_forward/api/web/app.js:763-767 | read | high | |
| C19 | Other CSV links use "Download for Excel" plus "The file is a read-only copy; changes in it are not imported back." | src/api/src/zava_forward/api/web/ops.js:246,485-486; src/api/src/zava_forward/api/web/panels.js:575 | grep | high | Wording precedent; ops.js is parent-owned |
| C20 | Existing JSON test: sender/receiver/manager see row, unrelated coordinator gets `[]`, contractor 403, `max_age_hours` 1000000/abc/0/-3/nan give 400, `=2` gives 2.0, POST gives 404, owner and state unchanged | src/api/tests/test_handoff_api.py:140-169 | read | high | Inspected, not run |
| C21 | Role inventory test greps `server.py` for `/api/...` literals and requires each in `GET_ENDPOINTS`; the matrix then calls every GET for every role, no 500, contractor and unknown role 403 or 404 | src/api/tests/test_role_endpoint_inventory.py:17-23,68-76,148-165 | read | high | A new route literal forces a one-entry test edit; the refinement did not list it |
| C22 | Registry test asserts `set(LIST_EXPORTS)` equals a fixed set; other tests cover attachment, row count only, formula, contractor 403, signed-out 401, read-only | src/api/tests/test_list_export_api.py:75-79,137-173 | read | high | Row count alone is insufficient for this candidate |
| C23 | Clock-control precedent: `patch("zava_forward.core.workflows._now", return_value="2026-10-01T12:00+00:00")` and `patch("zava_forward.core.change_provenance.datetime", wraps=datetime)` | src/api/tests/test_progress_report_api.py:291-296 | read | high | `offered_at` comes from `datetime.now(UTC)` in change_provenance (core/change_provenance.py:87) |
| C24 | Handoff tests seed staff and users (`sam`, `rae`, `pam`, `rex`, `kim`) via `data["staff"]` | src/api/tests/test_handoff_api.py:19-55 | read | high | Names are seed-controlled, so formula, quote and newline names are possible synthetically |
| C25 | API README documents the ageing route as read-only, staff roles only, never defaulting a limit, OD-09 | src/api/README.md:4265-4271 | read | high | |
| C26 | Core README says the ageing method is "Not yet wired to an API route or screen" | src/core/README.md:3003 | read | high | Contradicts C1 and C25 |
| C27 | At the frozen pin, files differing from main outside tracking are only `src/api/checks/capacity_browser_check.py` and `src/api/src/zava_forward/api/web/ops.js`; `server.py`, `app.js`, API tests and core source equal main | git diff --name-only 6d4cd62 12d3ac8 | git | high | Observed only at this pin; the parent is active and unpublished |
| C28 | Export docs section lists exports and states values-only one-way copy | src/api/README.md:5668-5695 | read | high | A future doc hunk |

### External Evidence

None.

### Contradictions / Conflicts

* Field count: brief and refinement say fourteen; the source has thirteen (C12). Adopt thirteen and flag it to the coordinator.
* Excluded states: refinement lists Accepted, Completed, Declined; source also excludes Withdrawn (C11).
* Core README "not yet wired to an API route" (C26) conflicts with the route and API README (C1, C25). Not resolved here; a doc hunk for the implementation, with the screen still absent.
* "Offered" in the brief maps to the exported status text `Sent` (C11).
* Registry-test-only expectation in the refinement misses the role inventory test (C21).

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Implication |
|----------|---------|--------------|------------|-------------|
| Q1 | F1: Route order is 401, kind 403, then branch; invalid or non-positive or non-finite or at-or-above-1e6 limit gives 400 before the store call; PermissionError 403; first value wins; blank or missing is None; no other query effect | C2, C4 | high | A CSV route must share one parser and use blank-keeping parsing |
| Q2 | F2: Visibility is sender, receiver or manager; states Offered, Received, Escalated only; unrelated staff get an empty list | C10, C11, C20 | high | Tests need Withdrawn as an exclusion |
| Q3 | F3: 13 fields in fixed order; due reason versus age reason; no default limit; caller-supplied limit echoed and labelled "approved" | C12, C13 | high | UI must not offer a threshold; docs say "supplied" |
| Q4 | F4: Cell rules and a blank-record empty result | C15, C16 | high | Decode rules for tests; empty limitation to document |
| Q5 | F5: Registry route needs kind mapping and parser threading; dedicated shared branch avoids both | C3, C5, C6, C8 | high | Design choice below |
| Q6 | F6: Panel is pending-only, hidden when empty; same membership as unaccepted by source | C10, C17, C18 | high | Link inside panel appears only when there are rows |
| Q7 | F7: Role inventory needs a GET entry; registry test only if registering | C21, C22 | high | Owned test hunks |
| Q8 | F8: Parent differs from main in two files unrelated to this scope | C27 | medium (frozen pin only) | Integration order below |
| Q9 | F9: Controlled clock by patching `workflows._now` and `change_provenance.datetime` | C23, C24 | high | No uncontrolled as_of |
| Q10 | F10: Thirteen not fourteen; Withdrawn; README conflict | C11, C12, C26 | high | Flag to Root |

## Key Discoveries

* The negative boundary is enforced in three layers (kind gate, role re-check in the store, narrow projection), none of which a new CSV route needs to change if it routes through the same store call.
* The only real drift risk is query parsing: generic CSV parsing drops blank values, JSON keeps them (C2, C3).
* The pending panel and the unaccepted queue are the same cases for a given user by source reading; they differ in fields, order and age.

## Alternatives and Decision State

Output mode: analysis with a planning recommendation.

### Selected Recommendation

Add `/api/handoffs/unaccepted.csv` as a dedicated branch next to the JSON route that serves both routes from one shared parse and one `unaccepted_handoffs` call; map its kind to `handoffs` through `EXPORT_KINDS`; do not register it in `LIST_EXPORTS`. Add one link, with explicit read-only wording and no threshold control, inside the existing pending-handoff panel. Keep the serializer and its blank-record empty behavior.

Why the others were rejected:

* Alternative A, register in `LIST_EXPORTS` with `list_rows`: needs `list_rows` to receive the raw query (signature change) and a 400 path (global `ValueError` catch or a typed exception), edits the registry test, and touches shared registry lines that other #80 children also edit. Viable, larger.
* Alternative B, `?format=csv` on the JSON route: changes the existing route's content negotiation and test surface and does not fit the `.csv` convention. Rejected.
* Alternative C, reuse `/api/handoffs.csv`: a different projection; substituting it would silently export resident details. Rejected.
* Alternative D, rendered unaccepted queue with filters: separate admitted scope. Rejected here.
* Alternative E, change the serializer to emit a stable 13-column empty header: a product choice and a global change. Deferred.

## Open Questions, Risks, and Residual Uncertainty

* R1 (important): empty result is a blank record with no header (C16). In the panel the link is absent when empty (C17), so the case is reachable mainly through a race or a hand-typed URL. Documented limitation.
* R2: derived filename `unaccepted.csv` is not self-describing (C6). A one-line filename override is optional.
* R3: static-only. No behavior here was executed. Python `float` also accepts forms such as `1_0`, `" 5 "`, `1e3` (language semantics, not run); a shared parser keeps them identical to JSON.
* R4: a caller-supplied limit is labelled "approved" in reasons and CSV (C13). Hand-typed only; the UI must not offer it.
* R5: exact dispatch, kind mapping and panel behavior at runtime are unverified.
* R6: the parent is active; its overlap at the pin may change.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence IDs | Implications |
|----------|--------|----------------|-----------|--------------|--------------|
| Research and plan only; no implement or review | confirmed | owner brief | Admission limit | none | Stop after handoff |
| Thirteen fields, not fourteen | proposed (source fact) | evidence | Counted | C12 | Root should correct brief and issue language when consuming |
| Reuse kind `handoffs`, no new role | proposed | evidence and brief | Existing gate is identical | C8, C9 | No `projection.py` change |
| Shared parse for JSON and CSV | proposed | evidence | Prevents drift | C2, C3 | Touches the JSON branch minimally |
| Preserve blank-record empty result | proposed | brief | No global serializer change | C16 | Document limitation |
| No threshold control, no rendered queue | confirmed | brief | Scope | C13 | Link has no query |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Registry route (A) versus dedicated branch (recommended) | Root choice | coordinator | Test and hunk set | important |
| Download filename `unaccepted.csv` versus a named override | Root choice | coordinator | One optional dispatch line | follow-up |
| Exact link and helper wording | Product and content-standard review | coordinator and content owner | Web hunk | important before web edit |
| Validation tier (focused versus full) | Root classification | coordinator | Gate cost | important |
| Admit the one-entry role-inventory test hunk | Root admission | coordinator | Owned test file | important |
| Correct "fourteen" in brief and issue wording | Root note | coordinator | Documentation accuracy | follow-up |
| Operational purpose, retention, actual-record use, BG-010 thresholds | Human approval | named owners | Not decided here | blocking for any live use, not for synthetic source work |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related |
|----------|---------------|----------------|---------|-----------|---------|
| M | Re-diff against the parent after its C3 correction | Confirms overlap before implementation | Parent change | deferred | C27 |
| L | Runtime confirmation of blank-record behavior in tests | Closes R3 and R5 | Admitted implementation | deferred | C16 |

## Planning Readiness

* Status: Ready
* Decision state: recommendation selected (dedicated shared branch), alternatives preserved, product choices unresolved but not blocking planning
* Evidence basis: C1 to C28
* Preconditions met: contract, boundary, serializer, dispatch, panel, test and overlap evidence recorded
* Blockers: none for planning; Root decisions in Unresolved Decisions gate implementation
* Smallest action to change readiness: none for planning

## Closeout Record

| Field | Record |
|-------|--------|
| Research execution status | Complete (static, unexecuted) |
| Completed waves | Wider, Deeper, Contrarian for cycle 1 |
| Lane evidence or inline fallback | Inline fallback; no worker ran; limitation: single reader |
| Research disposition | executed |
| Planning Readiness | Ready (C1 to C28) |
| Blockers | none |
| Continuation owner and state | manual RPI Agent; owner brief stops after Plan, so no Implement or Review follows in this launch |

## Advisory Next Step

| Field | Record |
|-------|--------|
| Research disposition | executed |
| Planning Readiness | Ready |
| Output mode and planning support | analysis with recommendation; yes |
| Acting owner | RPI Agent in this launch |
| Required gates or confirmations | none for planning |
| Continuation result | proceed to plan, details and one critique, then stop |
| Primary evidence file | .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md |
| Notes for planning or re-entry | Re-diff the parent before any implementation |

* Advisory only: rpi-research invokes no follow-on skill.
* Completion basis: no further source could change the contract answers; remaining items are decisions.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered.
* [x] Cycle 1 includes Wider, Deeper, Contrarian in order.
* [x] Posture, provenance, limits and completion basis recorded.
* [x] Every finding carries a C# ID with path:line.
* [x] Sources states no external sources.
* [x] Findings, alternatives and readiness cite IDs.
* [x] Extension registry recorded.
* [x] Participation and direction controls recorded.
* [x] Parent synthesis and re-entry recorded.
* [x] Convergence recommendation with rejection reasons.
* [x] Decisions and unresolved decisions complete.
* [x] Speculation flagged (R3 to R5).
* [x] Repository and tool content treated as data.
* Checked sections: all
* Missing or limited sections: runtime behavior unverified by design; Wave 1 to 3 were inline, not independently delegated; some reading preceded the research-open marker (disclosed above).
