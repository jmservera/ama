<!-- markdownlint-disable-file -->
# RPI Phase Details: Read-only CSV copy of unaccepted handoffs, implementation (#1419)

## Metadata

* Task ID: 1419-handoff-csv-implementation-1110
* Task slug: issue-1419-handoff-csv-implementation-1110
* Related plan: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-implementation-1110-research.md (C1 to C15)

Line numbers are at merged head 4350c3063f; re-locate by symbol.

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Environment and server route | not_started | P01, P01-T01 |
| P02 | Server tests | not_started | P02, P02-T01 |
| P03 | Panel link and UI evidence | not_started | P03, P03-T01, P03-T02 |
| P04 | Docs and validation | not_started | P04, P04-T01 |

Owned hunks and order:

| Order | File | Owned hunk |
|-------|------|------------|
| 1 | src/api/src/zava_forward/api/server.py | module-level `max_age_hours` helper; shared branch replacing the JSON `/api/handoffs/unaccepted` body; one separate-line EXPORT_KINDS entry |
| 2 | src/api/tests/test_role_endpoint_inventory.py | one GET_ENDPOINTS entry |
| 3 | src/api/tests/test_unaccepted_handoff_csv_api.py | new |
| 4 | src/api/src/zava_forward/api/web/app.js | link and helper in `pendingHandoffs` success branch only |
| 5 | src/api/tests/test_unaccepted_handoff_download_ui.py | new (Node slice plus opt-in browser class) |
| 6 | src/api/README.md | ageing and export paragraphs |

Never touched: ops.js, capacity_browser_check.py, core sources and README, projection.py, list_export.py, app.js retry and session helpers, startupFailure, fetchReadRetrying.

<!-- rpi:phase id=P01 -->
## P01: Environment and server route

### Context

Own venv `/home/azureuser/.venvs/issue1419` with editable installs from this worktree (C14).

### Intent

One shared parser and branch; JSON behavior unchanged.

### Boundaries

* Included: server.py hunks above.
* Excluded: LIST_EXPORTS registration, list_rows, serializer, new methods.

### Likely Targets

* src/api/src/zava_forward/api/server.py

### Dependencies

* none

### Validation Expectations

* Existing handoff API tests unchanged and green; new module green.

### Completion Evidence

* Changes record entry with diff hunk.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Shared helper, branch, kind mapping, filename

#### Context

C1 to C3.

#### Intent

Helper `_max_age_hours(url)` uses `parse_qs(url.query, keep_blank_values=True)`, first value, blank or missing is None, float parse, range `0 < v < 1e6`, else ValueError with the existing text. Branch handles `("/api/handoffs/unaccepted", "/api/handoffs/unaccepted.csv")`: parse, call `s.unaccepted_handoffs`, JSON route returns as today; CSV route sends `list_export.to_csv(rows)` with `text/csv; charset=utf-8` and filename `unaccepted-handoffs.csv`. 400 and 403 bodies are JSON like the JSON route.

#### Boundaries

* Included: those hunks.
* Excluded: other server code.

#### Likely Targets

* server.py near the EXPORT_KINDS dict and the existing JSON branch.

#### Dependencies

* none

#### Validation Expectations

* P02 tests; ruff; mypy.

#### Completion Evidence

* git diff of server.py.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Server tests

### Context

C4 to C8.

### Intent

Prove parity and boundaries under a controlled clock.

### Boundaries

* Included: one inventory entry; new module with its own raw-text helper and setUp copy (no subclassing of HandoffApi).
* Excluded: changing existing tests.

### Likely Targets

* src/api/tests/test_role_endpoint_inventory.py, src/api/tests/test_unaccepted_handoff_csv_api.py

### Dependencies

* P01 (tests are written to fail without the route; the pre-route failure is not required to be run separately but is recorded if run)

### Validation Expectations

* Matrix: header and every cell and order versus JSON; literal fixed row; states (Sent, Received, Escalated included; Accepted, Completed, Declined, Withdrawn excluded); due-only, age-only, both reasons; null OD-09 text; query matrix; roles; privacy markers; formula, quote, newline cells; immutability; POST and HEAD current behavior; empty body.

### Completion Evidence

* Raw unittest output.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Inventory entry and focused module

#### Context

Role matrix test calls every GET for every role (hazard).

#### Intent

Add `"/api/handoffs/unaccepted.csv"` to GET_ENDPOINTS; build the module with `workflows._now` patched to a fixed minute-precision string and handoff dicts crafted exactly.

#### Boundaries

* Included: synthetic data only, temp seed.
* Excluded: private data, uncontrolled as_of comparisons, row-count-only proxies.

#### Likely Targets

* the two test files

#### Dependencies

* P01-T01

#### Validation Expectations

* Module and inventory test green.

#### Completion Evidence

* Test output.

#### Unresolved Items

* none

<!-- rpi:phase id=P03 -->
## P03: Panel link and UI evidence

### Context

C9 to C13, C15.

### Intent

Truthful distinct link, tested by Node slice and a real minimal browser check.

### Boundaries

* Included: `pendingHandoffs` success branch.
* Excluded: error, empty and loading branches; existing link; any other app.js code.

### Likely Targets

* src/api/src/zava_forward/api/web/app.js, src/api/tests/test_unaccepted_handoff_download_ui.py

### Dependencies

* P01

### Validation Expectations

* node --check; Node slice test; browser check under non-blocking heavy lock.

### Completion Evidence

* Output; precise partial if the lock is busy.

### Unresolved Items

* none

<!-- rpi:task id=P03-T01 -->
### P03-T01: Link and helper

#### Context

C10: link and helper in one paragraph pattern.

#### Intent

After the existing link add `h("p", {}, h("a", {class:"btn alt", href:"/api/handoffs/unaccepted.csv", download:"unaccepted-handoffs.csv"}, "Download handoff waiting times for Excel"), " helper text")`. Helper meaning: separate from the pending list; all handoffs you can see; no resident contact details; read-only copy, not imported back; no waiting-time limit chosen for the whole queue, and past-due handoffs can still show as overdue; an empty file has no column names. Plain ASCII, short active sentences.

#### Boundaries

* Included: one block.
* Excluded: styles, new classes.

#### Likely Targets

* app.js pendingHandoffs

#### Dependencies

* none

#### Validation Expectations

* P03-T02.

#### Completion Evidence

* git diff of app.js.

#### Unresolved Items

* none

<!-- rpi:task id=P03-T02 -->
### P03-T02: UI tests and browser check

#### Context

Existing Node slice pattern in test_handoff_read_guidance.py.

#### Intent

Node slice: success shows both links with exact attributes and helper claims; error, empty and loading show neither new link; still one GET /api/handoffs and no POST. Browser class (opt-in ZF_BROWSER_TESTS=1): synthetic owned server with a real offered handoff; locate by role and name; assert href, download attribute, click yields download file `unaccepted-handoffs.csv` with the expected row; keyboard Enter on focused link; store unchanged. Plan before run: take `/tmp/ama-rpi-heavy.lock` non-blocking, run only this class.

#### Boundaries

* Included: this panel only.
* Excluded: capacity browser suite.

#### Likely Targets

* the new UI test module

#### Dependencies

* P03-T01

#### Validation Expectations

* Recorded raw results, first adverse attempts preserved.

#### Completion Evidence

* Output.

#### Unresolved Items

* lock availability

<!-- rpi:phase id=P04 -->
## P04: Docs and validation

### Context

Validation Override in the plan.

### Intent

README paragraphs; targeted checks run and recorded.

### Boundaries

* Included: API README ageing and export paragraphs.
* Excluded: core README, KB files.

### Likely Targets

* src/api/README.md

### Dependencies

* P01 to P03

### Validation Expectations

* Checks listed in P04-T01.

### Completion Evidence

* Changes record.

### Unresolved Items

* none

<!-- rpi:task id=P04-T01 -->
### P04-T01: README, lint, type and tests

#### Context

C14.

#### Intent

From src/api with the venv: unittest for the new modules, test_handoff_api, test_list_export_api, test_role_endpoint_inventory, test_handoff_read_guidance, and other tests that read app.js pendingHandoffs or the export link text (grep first); ruff check and format --check on touched Python; the existing affected API mypy command; node --check app.js. No SQL, Docker or full gate.

#### Boundaries

* Included: the commands above.
* Excluded: tools/rpi-checks.py full gate.

#### Likely Targets

* none

#### Dependencies

* P01 to P03

#### Validation Expectations

* Pass, or a recorded failure fixed in the batch.

#### Completion Evidence

* Command lines and raw exit codes in the changes record.

#### Unresolved Items

* none
