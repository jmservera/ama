<!-- markdownlint-disable-file -->
# RPI Phase Details: Read-only CSV copy of unaccepted handoffs (#1419)

## Metadata

* Task ID: 1419-handoff-csv-research-1110
* Task slug: issue-1419-handoff-csv-research-1110
* Related plan: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-research-1110-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md (C1 to C28)

All content is a proposal for a later admitted implementation. Nothing here was executed. Line numbers are at frozen HEAD 12d3ac842 and will move; re-locate by symbol.

## Phase Index

| Phase ID | Name                               | Status    | Detail sections |
|----------|------------------------------------|-----------|-----------------|
| P01      | Pre-flight and integration order   | not_started | P01, P01-T01, P01-T02 |
| P02      | Server route                       | not_started | P02, P02-T01 |
| P03      | Tests                              | not_started | P03, P03-T01 |
| P04      | Panel link                         | not_started | P04, P04-T01 |
| P05      | Docs and validation                | not_started | P05, P05-T01 |

Owned-hunk table and integration order (proposed):

| Order | File | Owned hunk | Overlap risk |
|-------|------|------------|--------------|
| 1 | `src/api/src/zava_forward/api/server.py` | new module-level `max_age_hours` helper; replace the body of the `/api/handoffs/unaccepted` branch (around L724-735) with a shared JSON and CSV branch; one separate-line `EXPORT_KINDS` entry (around L174) | `LIST_EXPORTS`, `EXPORT_KINDS` and the long `get_kind` dict line are shared by other #80 children; add on separate lines. Equal to main at the pin |
| 2 | `src/api/tests/test_role_endpoint_inventory.py` | one `GET_ENDPOINTS` entry | none known |
| 3 | `src/api/tests/test_unaccepted_handoff_csv_api.py` | new file | none |
| 4 | `src/api/src/zava_forward/api/web/app.js` | link block inside `pendingHandoffs()` only (around L754-775) | never the retry and session helpers (about L54-85), `startupFailure`, `fetchReadRetrying`. Equal to main at the pin |
| 5 | `src/api/README.md` | ageing paragraph (around L4265) and export section (around L5670) | shared doc; small paragraphs |

Never touched: `ops.js`, `capacity_browser_check.py`, core sources, core README, Capacity and aftercare checkers, `projection.py`, `list_export.py`.

<!-- rpi:phase id=P01 -->
## P01: Pre-flight and integration order

### Context

The parent is unpublished and active with a checker-only correction. At the frozen pin it differs from main only in `ops.js` and `capacity_browser_check.py` (C27). That is an observation at one commit, not a guarantee.

### Intent

Know the base, the overlap and the Root decisions before touching source.

### Boundaries

* Included: diff review, decision record.
* Excluded: any source edit, fetch or rebase without explicit instruction.

### Likely Targets

* none (read-only).

### Dependencies

* Root admission and explicit pin and ownership reconciliation.

### Validation Expectations

* Recorded `git diff --name-only` of base against the then-current parent showing owned files untouched, or a written reconciliation.

### Completion Evidence

* Diff output in the changes record.

### Unresolved Items

* Which commit is the integration base.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Re-diff and reconcile

#### Context

C27.

#### Intent

Confirm `server.py`, `app.js` and the three API test files are unchanged by the parent, or reconcile.

#### Boundaries

* Included: read-only diff.
* Excluded: touching parent worktree or its tracking state.

#### Likely Targets

* none.

#### Dependencies

* none.

#### Validation Expectations

* Overlap statement with exact SHAs.

#### Completion Evidence

* Changes-record entry.

#### Unresolved Items

* none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Record Root decisions

#### Context

Research Unresolved Decisions.

#### Intent

Fix: dedicated branch (recommended) versus registry; filename; wording owner; validation tier; inventory hunk; "fourteen" correction.

#### Boundaries

* Included: recording answers.
* Excluded: approving export purpose, retention, actual-record use or thresholds.

#### Likely Targets

* none.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Each decision has a named owner and date.

#### Completion Evidence

* Changes-record entry.

#### Unresolved Items

* All six pending Root.

<!-- rpi:phase id=P02 -->
## P02: Server route

### Context

JSON route reads blank-retaining query, validates, calls the store, returns 400 or 403 (C2). Generic CSV dispatch uses a non-blank-retaining `q` and catches only PermissionError (C3, C6). A bare registry entry would map to a kind outside `STAFF_GET` (C5).

### Intent

One parse, one store call, two serializations.

### Boundaries

* Included: helper, shared branch, `EXPORT_KINDS` entry.
* Excluded: `LIST_EXPORTS` registration (recommended design), `list_rows` signature change, any `projection.py` change.

### Likely Targets

* `src/api/src/zava_forward/api/server.py`: helper, branch, kind mapping.

### Dependencies

* P01.

### Validation Expectations

* Existing JSON test (`test_handoff_api.py`) passes unchanged; new parity tests pass.

### Completion Evidence

* Test output and diff limited to owned hunks.

### Unresolved Items

* Filename override (optional one line, Root).

<!-- rpi:task id=P02-T01 -->
### P02-T01: Shared parser and branch, kind mapping

#### Context

Helper takes `url.query`, runs `parse_qs(..., keep_blank_values=True)`, takes the first `max_age_hours`, treats missing or `""` as none, otherwise `float` and requires `0 < v < 1e6`, and raises or returns a signal that yields the existing 400 body `{"error": "max_age_hours must be a positive number of hours."}`. Shared branch order stays: auth and kind gate already ran, parse, call `unaccepted_handoffs`, PermissionError 403, then JSON `_send` or CSV with `to_csv(rows)`, `text/csv; charset=utf-8` and attachment disposition. Kind for the `.csv` path comes from `EXPORT_KINDS` as `handoffs`. HEAD follows GET through `do_HEAD`.

#### Intent

Preserve JSON byte-for-byte behavior and add the CSV representation.

#### Boundaries

* Included: only the owned server hunks.
* Excluded: registering in `LIST_EXPORTS`, new roles, selectors, defaults.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`.

#### Dependencies

* none.

#### Validation Expectations

* Both routes return identical 400 for invalid values; POST to either returns 404; unknown query keys ignored.

#### Completion Evidence

* Focused tests (P03) green.

#### Unresolved Items

* Plan of record is the shared branch. Design A (registry) is rejected: it needs a `list_rows` raw-query change, a typed 400, a registry-test edit and more shared-line churn.

<!-- rpi:phase id=P03 -->
## P03: Tests

### Context

Harness precedents: `SqlStore`, `App(store, "synthetic-check")`, loopback server, `call(actor, path)` (C22); handoff seed users (C24); clock patch (C23); role inventory (C21).

### Intent

Compare every CSV cell, row and order to JSON deterministically.

### Boundaries

* Included: new module, one inventory entry.
* Excluded: copying cases into mirrored files; changing the registry test unless Design A is chosen; running browser tests unless prerequisites exist.

### Likely Targets

* `src/api/tests/test_unaccepted_handoff_csv_api.py` (new), `src/api/tests/test_role_endpoint_inventory.py`.

### Dependencies

* P02.

### Validation Expectations

* Commands from `src/api`: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_unaccepted_handoff_csv_api tests.test_role_endpoint_inventory tests.test_list_export_api tests.test_handoff_api -q`.

### Completion Evidence

* Recorded results; skipped or unrun checks stated.

### Unresolved Items

* none.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Inventory entry and focused regression module

#### Context

Controlled clock: patch `zava_forward.core.workflows._now` to a fixed minute-precision string; offer through the API, then overwrite `store.cases[...]["handoff"]["offered_at"]` and `due_at` to constants so ages are exact. Decode with `csv.reader(io.StringIO(text, newline=""))`.

#### Intent

Cover these cases, each written once:

1. Parity: for one multi-row scenario, header equals the 13 JSON keys in order; for one fixed row assert literal expected cells written by hand (not derived through the serializer's own rules); the remaining cells equal the normalised JSON value (None to empty, bool to Yes or No, list to compact sorted-key ASCII JSON, leading apostrophe for `= + - @ TAB CR`); row order equals JSON order including an age tie.
2. States: Offered (status `Sent`), Received and Escalated included; Accepted, Completed, Declined and Withdrawn excluded.
3. Reasons: due-time reason only, age reason only, both; no limit gives empty `approved_limit_hours` and the OD-09 note; limit 2 echoes `2.0`; `needs_escalation` false for Escalated.
4. Query parity table for JSON and CSV: missing, blank, blank then value, repeated (first wins), valid fraction, whitespace-only, `abc`, `0`, `-3`, `nan`, `inf`, `1000000`, unknown key. Compare status and error body.
5. Roles: 401 signed out; 403 contractor, Application Administrator, unknown role; sender, receiver and manager see rows; unrelated staff get the blank-header body `\r\n`; 403 happens before the parser (invalid value for a denied role still 403).
6. CSV edge text: staff names with quote, comma, newline and a leading `=`; assert exact decoded cell text and apostrophe protection.
7. Headers: content type, attachment disposition and filename (derived `unaccepted.csv` or the Root-chosen name).
8. Projection privacy: planted synthetic resident, address, contact, note and evidence markers absent from the body; header set exact.
9. Immutability: deep-copy snapshots of cases, handoffs, ownership and audit before and after success, denied and invalid reads.
10. POST and wrong-method returns 404; HEAD behavior matches GET headers.
11. Static check that the panel link in `app.js` targets exactly `/api/handoffs/unaccepted.csv`, carries no query, is distinct from `/api/handoffs.csv`, and appears only in the success branch.

Row-count-only checks and uncontrolled `as_of` comparison are not acceptable.

#### Boundaries

* Included: synthetic data only.
* Excluded: private datasets, real credentials, network.

#### Likely Targets

* The two test files above.

#### Dependencies

* P02-T01.

#### Validation Expectations

* New module fails against the pre-change server (route absent) and passes after; existing tests stay green.

#### Completion Evidence

* Before and after results recorded honestly.

#### Unresolved Items

* none.

<!-- rpi:phase id=P04 -->
## P04: Panel link, after web guidance fetch

### Context

`pendingHandoffs()` fetches `/api/handoffs`, hides itself when empty, shows an alert on error and otherwise renders "Download for Excel" to `/api/handoffs.csv` (C17, C18). Existing link text is asserted on other screens and must not change (C19).

### Intent

Add one sibling link with a different label and an honest helper line.

### Boundaries

* Included: link block on the success path.
* Excluded: threshold input, filters, a rendered queue, error-path link, retry and session helpers.

### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`.

### Dependencies

* Current web-design-guidelines source fetched and read; selected skills read (redesign-existing-projects, design-system, content standard, WCAG baseline).

### Validation Expectations

* Static route and wording test (P03); optional browser handoff test when Playwright exists, not run in this launch.

### Completion Evidence

* Diff limited to the block; stated unrun checks; no accessibility conformance claim.

### Unresolved Items

* Final wording owner.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Link block in pendingHandoffs

#### Context

Proposed wording for owner or content review, plain ASCII, short active sentences:

* Link text: "Download handoff waiting times for Excel".
* Helper line: "Shows how long each handoff you can see has waited. This is not the list above. It has no resident details. The file is a read-only copy; changes in it are not imported back. No time limit is set, so only handoffs past their own due time are marked. A file with no rows has no column names."

Native anchor with `href` set to `/api/handoffs/unaccepted.csv` and a `download` attribute (the server disposition filename wins if it differs).

#### Intent

Make the download discoverable and not mistaken for the pending list.

#### Boundaries

* Included: one anchor and one helper paragraph.
* Excluded: everything else in `app.js`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`.

#### Dependencies

* P02-T01; web guidance fetch.

#### Validation Expectations

* Anchor appears only with pending rows; absent when the panel is hidden or in the error state.

#### Completion Evidence

* Diff and static test.

#### Unresolved Items

* Because the panel hides when empty, an empty unaccepted queue is not reachable from the UI by source reading; stated as a limitation, not a guarantee.

<!-- rpi:phase id=P05 -->
## P05: Docs and validation

### Context

API README documents the JSON route (C25) and the export section (C28). Validation tier: full tier by default (authorization-sensitive route; doubt takes the full tier), with the complete local gate and a verified external full receipt. Root may record a downgrade only with its basis.

### Intent

Document the route, the reuse of the gate, the 13 fields, the blank-header empty limitation and the unchanged OD-09 position; record what ran.

### Boundaries

* Included: `src/api/README.md` only.
* Excluded: knowledge base, core README, regulatory material.

### Likely Targets

* `src/api/README.md`.

### Dependencies

* P02 to P04.

### Validation Expectations

* Documentation link and diff review; the commands in P03; hosted CI read for the exact head; independent exact-head review and human approvals remain required.

### Completion Evidence

* Changes record stating run versus not run.

### Unresolved Items

* Full-gate requirement if Root classifies as security-sensitive.

<!-- rpi:task id=P05-T01 -->
### P05-T01: API README and validation record

#### Context

C25, C28.

#### Intent

Update two paragraphs and record validation.

#### Boundaries

* Included: README hunks.
* Excluded: other docs.

#### Likely Targets

* `src/api/README.md`.

#### Dependencies

* P02-T01, P03-T01, P04-T01.

#### Validation Expectations

* Diff shows only these paragraphs.

#### Completion Evidence

* Changes record.

#### Unresolved Items

* none.
