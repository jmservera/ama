<!-- markdownlint-disable-file -->
# Research: #80 exception-register CSV contract clarification (issue-80-exception-contract-2122)

Research disposition: executed (static source and artifact reading only). Planning Readiness: Ready for a documented PROPOSED contract; not Ready for any source change, which is not admitted.

## Scope and admission

* Worktree issue-80-exception-contract-2122, branch docs/exception-export-contract-80-2122, initial main 077ad5ad20293a1d79932ea14e9f639dd11e5a22, target main, Refs #80 only.
* Root admits only completion of the known exception-list CSV contract clarification. No source correction, no operational export approval, no new source allowance, no Capacity C1-C5 reset, no new issue, no runtime or full gate, no cloud, model, spend, private data or real operational export.
* Not repeated: the universal inventory ([qualified audit](../2026-11-10/issue-80-qualified-audit-1110-research.md), [main audit](../2026-11-10/issue-80-main-export-audit-1110-research.md)), Capacity C1-C5, merged #1419 and #1423, and existing implemented exports.
* Issue state read: #80 OPEN. Criterion 2 (every list offers Excel or CSV) and criterion 4 (owner thresholds) are unmet; criteria 1 and 3 are ticked. Nothing here ticks or relaxes any criterion.

## Prior inventory and refinement (reused, not redone)

* Qualified audit row M2 lists "Resident choice queue and exceptions: no CSV (gap)". The 2026-11-05 #80 comment lists "restricted retention/exception queues" as a real gap and says these are not an instruction to expose all stores; personal and operational lists need their existing role, row, field and suppression contracts preserved.
* The resident choice queue half of M2 is now delivered by the #1420 line (see `issue-1420-choice-csv-implementation-changes.md`); this task does not touch it.
* #135 (open) states: "The register is read-only and records views/denials; a read is not a zero-audit mutation guarantee." That is the existing refinement. A blanket "zero audit write" requirement for any exception export is therefore contradictory and is not used here.

## Current source facts (static, at 077ad5ad)

Endpoint and store

* `server.py:714-718`: `GET /api/exceptions` returns `s.exception_register(u, exception_register.staff_from_env(os.environ))` as JSON, `403 {"error"}` on `PermissionError`. There is no `.csv` route and no entry in `LIST_EXPORTS`; `get_kind` maps the path to `exceptions` (`server.py:258`).
* `exception_register.py` `exception_register(user, staff)`:
  * No staff configured: managers get `state: "roles_not_named"`, `items: []`, audit `viewed_exception_register state=roles_not_named`; non-managers get `PermissionError` and audit `denied`.
  * Staff configured but caller not named: `PermissionError`, audit `denied`.
  * Named caller: `state: "ok"`, `items` = `queue.queue(email)`, filtered by `owner_role in roles` (steward sees source/identity conflicts and failed imports; operator sees failed AI runs and stranded tasks, including unaccepted handoffs raised as `stranded_task`; `exception_feeds.py:103-105`). Audit `viewed_exception_register items=N`.
  * `_audit_register` calls `Store.audit`, which appends one hash-chained line to the separate audit ledger file (`store.py:121-125`), not to the case/recommendation/refusal document in `self.data`. The queue's own in-memory audit list is rebuilt per request and never persisted.
  * Nothing else is written: no case, recommendation, import-refusal, task, handoff or stock record is modified (existing test `test_reading_changes_nothing`, `test_repeat_transfer_changes_nothing_and_reading_writes_only_audits`).
* Item reference `EX-NNN` is assigned by insertion order inside each request (`exception_queue._add`: `seq = len(items)+1`). It is a per-view label, not a durable identifier; the same underlying exception can carry a different reference after data changes.
* `item.owner` is the configured email of the first named person holding the role; with two stewards an item can show a colleague's email. `item.owner_role` is a closed two-value vocabulary (`data_steward`, `digital_operator`). `status` is currently always `open`; `eligibility` is the constant `Unknown`.
* Free text and linked identifiers exist on items (`summary`, `error`, `runbook`, `original_source` with record, batch, case and query ids, conflict `values` with source, date and version). Some derive from imported rows or provider errors and are not under the register's control.

UI

* `role-screens.js:868-962`: the register panel is reached only through the explicit link `screen=data-operator&exceptions=1` (the entry panel makes no request). `exceptionRegisterView` performs one `api("/api/exceptions")`, then renders `exceptionRegisterPanel` or `exceptionUnavailable` (403 shows "Access denied", every other failure and malformed data shows "could not be shown ... Do not read this as all clear"; 401 is rethrown).
* The panel table "Exception items returned for you" lists every readable item (limit `Infinity`), eight columns. `unreadable = data.items.length - items.length` produces a visible "This list is not complete" notice. The empty state already says "not an all clear".
* Existing tests assert: exactly one `/api/exceptions` call for the full view and none for the entry (`test_reads_only_the_existing_endpoint_with_no_write`), and no `button`, `form`, `input`, `select`, `textarea` anywhere in the screen (`test_no_controls_and_entry_is_a_plain_link`). A control therefore needs a deliberate, documented change to that test, in a later admitted slice.

Export prior art

* `list_export.to_csv` / `safe_cell`: values-only, formula prefixes `= + - @ TAB CR` get a leading apostrophe, booleans become Yes/No, mappings and lists become sorted JSON, CRLF rows from `csv.writer`, UTF-8. With zero rows it emits a single blank line and no header (relevant to empty semantics; used by cases, handoffs and similar). Contractors get no export.
* Fixed-column encoders (`progress.closed_csv`, `resident_choice_export`) keep the header on zero rows, write only closed vocabularies, integers and a reference, state unknowns as `Unknown`, and send an attachment only on success; denial and anonymous responses carry no attachment. Both are server routes, so each download is a second authorised read.
* No browser-built download exists (`new Blob` is not used; `URL.createObjectURL` in `app.js:231` is for a photo preview).

## Design-gap resolution

1. Contradiction resolved. The register GET persists one audit line on view and on denial, and that is existing, intended behaviour. The export contract must permit those audit lines and prohibit only writes to the controlled domain (case, recommendation, import-refusal, task, handoff, stock, queue, rule, funding, finance, governance records and the AI/registry stores).
2. A server `.csv` route would be a second GET, add a second `viewed_exception_register` audit line (or need its own action), need a new `get_kind`/inventory entry, and add a 403 path that audits denials. A browser-only summary built from the already-authorised, already-rendered response makes no second request, so the activation itself adds no audit line, and it cannot widen what the signed-in role can see. This is the smaller and safer shape and fits the "authorised visible summary" framing.
3. Negative semantics are what was missing, and they are the substance of the contract. An empty or header-only file is indistinguishable from an all-clear and the register already states that an empty list is not one (sources not connected, health Unknown, unrouted records). A CSV cannot carry that caveat without polluting the data, so no file is offered when there is nothing readable to list.
4. Free text, owner emails, source ids and conflict values are excluded. A four-field allowlist of reference, kind, state and owner role needs no new privacy or retention decision because each value is a closed vocabulary or a per-view label already on the signed-in user's screen.

## Role and company interpretation

* Helpful but not required. A data-role reading (Housing Data and Performance Lead, or the Data steward map in the customer journey atlas) can inform only which four columns a steward would triage in Excel (reference, kind, state, owner role) and the caution that a file with no rows must not read as "all clear". That is a sector-informed hypothesis. It is not evidence of what Zava North Homes needs, does not name the steward or operator (still an open owner decision on #135), and does not authorise any permission, retention or sharing change or waive any human gate. No role agent was run; none was needed to settle a contract that adds no authority.
* Company-role opinion remains hypothesis; the engineering contract rests on repository facts above.

## Overlap check

* #135 owns the register source, producers, appointments and recovery; this contract does not alter any of them. Existing #135 work (#1081, #1260, #1361) is read-only context. #1360 (closed) concerns importer transfer wording and is unrelated.
* #225 (finance exception explanations) is a different "exception" concept (invoice match exceptions) and is not touched.
* No actual overlap requires naming a different owner for the proposed export. Owner of the future slice would be #80 criterion 2, consuming #135's served register unchanged.

## Owner policy position

* No actual owner policy is needed to complete this proposed contract for the synthetic demonstrator: it adds no data, role, retention or sharing authority.
* Policy questions that remain open for operational use (stated in the plan, not assumed): who is named as data steward and digital operator (existing #135 open decision), handling and retention of a downloaded copy outside the application, and whether an operational all-clear notice is wanted. None blocks the proposal; all block any operational claim.

## Limits

* Static reading only; no browser, test run or runtime observation. Not an accessibility, WCAG, live or operational conclusion. No private data read.
* Whole-issue #80 stays open: every-list export and owner thresholds remain unproved.
