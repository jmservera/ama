<!-- markdownlint-disable-file -->

# Implementation Details: issue444-resident-feedback-preview

Plan: [plan](../../plans/2026-10-24/issue444-resident-feedback-preview-plan.md). Research: [research](../../research/2026-10-24/issue444-resident-feedback-preview-research.md).

## Phase 1: core boundary

Files: `src/core/src/zava_forward/core/resident_preview.py`, `src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py`. Core imports no workload.

### Fixture file (server-owned, beside the dataset, explicit path)

`resident-preview-fixture.json`:

* `fixture`: `{id, synthetic: true, disposable: true, lineage, limitations[]}`; the dataset JSON also carries top-level `"synthetic_preview": {"fixture_id", "disposable": true}` which must match.
* `subjects`: list of `{subject, label}`.
* `grants`: list of `{grant_id, subject, case_id, kind: "resident"|"representative", representative_ref (representative only), tasks (representative only, subset of AUTHORITY_TASKS), measure (representative only), fields (subset of FIELD_CATALOG), actions: [] (must be empty), valid_from, valid_to (ISO with offset), revoked: bool}`.

Strict schema: unknown keys, wrong types, non-empty `actions`, unknown field names, naive datetimes, or `*` values make a grant malformed, which counts as no grant (deny).

### Grant resolution (`resolve_grant(fixture_path, subject, now)`)

Re-reads the file on every call (revocation and expiry apply on the next protected request). Returns a `Grant` or raises `GrantDenied(reason_code)` with codes `fixture_unavailable`, `unknown_subject`, `no_grant`, `expired`, `revoked`, `ambiguous`, `malformed`. Rules: collect grants for the subject; discard none silently: malformed records for the subject deny; consider records valid now and not revoked; exactly one required; more than one denies as ambiguous; none denies with the most specific reason. A grant whose `case_id` is absent from the store denies (`no_case`). Case identifiers in requests are never read.

### Projection (`resident_view(store, grant, today)`)

Read of `store.cases[case_id]` and `store.data.get("procurement", {}).get("work_orders", [])` (never `_proc()`, which `setdefault`s into the store; C3); deep-copies nothing it returns beyond fixed strings and a few allowlisted scalar values. Output is built field by field from `FIELD_CATALOG = ("home", "measures", "progress", "next_step", "appointments", "help")`; a field absent from `grant.fields` is absent from the output.

* `home`: address, town, postcode of `case.home` (the resident's own home, as strings; length bounded).
* `measures`: `case_measures(c)` items, plain strings, length bounded.
* `progress` and `next_step`: from fixed `STAGE_TEXT[stage] = (progress, next_step)` for each of the 25 `STAGE_ORDER` stages; other values give "We do not have a plain-language update for this step yet" and "We cannot say what happens next. Please use the help route below". `closed` is shown only when it is exactly `True`; wording is "This case is recorded as closed"; any other value is not shown. No `waiting_on`, `reason`, `history`, `owner`, notes, contacts, decision or funding value is read.
* `appointments`: for each work order with `case_id` equal to the case, status from `store.appointment_status(w)` and the offer `date`/`period` when present: `Committed` goes to `confirmed` ("Confirmed arrangement"), `Offer` goes to `offers` ("Offered, not yet confirmed. Nothing is booked until all confirmations are recorded"), `Ended` or `Unknown` go to `unknown_or_ended` ("We cannot show a confirmed arrangement"). Legacy `case.appointments` are not read (their statuses are free staff text). No contact names, staff, contractor or notes.
* `help`: constant text: human help and non-digital routes exist, no phone/email/address is invented, "ask your housing officer, or write or visit your local Zava North Homes office"; no commitments (no response times).
* `unavailable`: constant list of `{feature, reason}` for messages, uploads, downloads, appointment responses, consent changes, AI answers.

Representative grants (C2): before calling `authority_for`, require `current_context(c, measure)` is a dict with an integer `revision`, require the stored authority list/last record to be a dict with the expected keys, and wrap the domain call so `ValueError`, `KeyError`, `TypeError` and `AttributeError` all mean task denied. The view starts empty. For each task the grant lists: `authority_for(c, ref, task, measure, context)` with `context = current_context(c, measure)` must pass, otherwise that task's fields are omitted and the response lists "not currently confirmed for this task" without naming reason beyond that. Mapping: "Receive information" shows `measures` (that one measure), `progress`, `next_step`; "Attend" shows `appointments` only for work orders whose resident-bindings measure equals the grant measure (else none); other tasks show nothing and are listed as unavailable. If no task passes, the result is `GrantDenied("no_current_authority")` (403). Grant `fields` only narrows further (intersection).

### Safe-start guards (`require_safe_environment(env, dataset, fixture)`)

Refuse, using a prefix deny rule evaluated on the whole process environment (critique C1, C4): any variable named or prefixed `ZF_`, `AI_`, `IDENTITY_`, `MSI_`, `AZURE_`, `MSSQL`, `APPLICATIONINSIGHTS`, `OPENAI`, `PGHOST`, `SQL`; this covers `ZF_DATA`, `ZF_STORE`, `ZF_ENV`, `ZF_DOC_*`, `ZF_DIGEST_DIR`, `ZF_PASSWORD`, `ZF_AS_OF`, `AI_ENDPOINT`. Dataset and fixture paths must be existing regular non-symlink files, canonicalized with `Path.resolve(strict=True)` before any comparison, and refused if inside `~/.zava-forward` or the normal `data_file()` parent or equal to it (resolved). The dataset must carry the matching `synthetic_preview` marker and the fixture `synthetic`/`disposable`. Non-loopback host refused (only `127.0.0.1`, `::1`). Messages state reason and next action. Tests cover each family, symlink and `ZF_DATA`.

### Builder (`resident_preview_fixture.build(out_dir)`)

Creates a nonexistent directory (refuses existing, refuses paths under `~/.zava-forward`) with `dataset.json` and `resident-preview-fixture.json`, using a scratch `Store` and public operations (package, capacity, `issue_work_order`, appointment offer/confirm, resident scope, safe contact, representative authority). Cases: `SYN-C1` resident A, committed appointment; `SYN-C2` resident B, offer only; `SYN-C3` unrelated home with canaries; each case also carries canary strings in staff notes, hazard/vulnerability reason, finance, staff names/ids, contacts, history, `resident.phone`, chat/memory-like fields. Subjects: `SYN-RES-A`, `SYN-RES-B`, `SYN-REP-B` (representative for C2, valid Receive information and Attend), `SYN-REP-WRONG` (grant lists Attend, authority recorded for Receive information only), `SYN-RES-EXPIRED`, `SYN-RES-REVOKED`, `SYN-RES-AMBIG`. Everything is labelled fictional; lineage records the builder and that no source data is read.

## Phase 2: API package `src/api/src/zava_forward/api/resident_preview/`

Files: `__init__.py`, `__main__.py` (CLI `--dataset DIR/FILE --fixture FILE --subject ID --host --port`), `app.py` (handler), `web/` assets. Pyproject package-data adds `"zava_forward.api.resident_preview" = ["web/*"]`.

* The App takes `(store, fixture_path, subject)`. Identity is the constructor argument; nothing in the request (header, cookie, query, body, path) selects identity. Unknown subject or any denial returns 403 JSON `{"error": ..., "next_action": ...}` with generic text that never names other subjects or cases.
* Routes: `GET /` and `GET /resident` (page), `GET /resident/app.js`, `/resident/resident.css`, `GET /resident/api/view` (JSON), `GET /healthz` (store loaded and fixture readable). All else GET: 404. Any query string on the API: 400. Any `POST/PUT/PATCH/DELETE`: 405 for known paths and for named unavailable routes (`/resident/api/messages`, `/uploads`, `/downloads`, `/appointments/respond`, `/consent`, `/ai`) a 403 `{"error":"Not available in this preview"}` after grant check. HEAD and OPTIONS are 405. No CORS headers. `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, CSP `default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'`. Host header must be a loopback name with the bound port else 400 (DNS-rebinding defence).
* Staff routes (`/api/...`) do not exist here: 404. The staff `server.py` is not imported.
* Startup: parse, `require_safe_environment`, copy dataset into a private temp state directory, open `Store` there with explicit live/audit paths, check marker, resolve host loopback, bind loopback only, print URL and the fixture limitations. Missing store or fixture exits non-zero with a message before binding.
* `appointment_status` is called only when `store._proc_context` is absent (it is a fresh preview Store) and the store is opened with a deep-copy-compare test of `store.data` before and after, including a dataset without a `procurement` block (C3). Each GET calls `resolve_grant` then `resident_view`; the store is never saved; a test asserts the store's `version` and deep-copied data are unchanged after viewing and after denied writes.

## Phase 3: assets

* Page: `lang="en-GB"`, viewport without zoom block, skip link, persistent banner "Synthetic preview - not a live resident service" in the page header (also `<title>`), one `<h1>`, landmarks (`header`, `main`, `footer`), headings in order, sections for progress, next step, appointments (two distinct headings "Offered times (not confirmed)" and "Confirmed arrangements"), help, "Not available in this preview" list rendered as native disabled buttons with visible text reasons. Text shows status words, not colour only.
* JS builds DOM with `textContent` only (no `innerHTML` with data). Initial load shows "Loading your update…" with `aria-live="polite"`; on 403/404/network error shows an error panel with reason, next action and a "Try again" button; focus moves to the error heading; on success focus stays at document start (no autofocus). A "Refresh" button re-requests and announces completion politely.
* CSS: Fluent 2 token names as in `style.css`, teal brand, 16px body, 40px controls, two-tone `:focus-visible`, reduced-motion zero, `overflow-wrap:anywhere`, single column reflow at 320px, no `transition: all`, `touch-action: manipulation`, `color-scheme: light`, `theme-color` meta.
* Checked against the freshly fetched web-interface-guidelines rules (recorded in the changes file).

## Phase 4: tests (outside the package)

* `src/core/tests/test_resident_preview.py`: grant schema/validity/ambiguity, projection allowlist with canary scan, representative checks (valid, wrong task, expired authority, revoked grant), stage mapping incl. unknown, appointment offer vs confirmed vs unknown, environment guards.
* `src/api/tests/test_resident_preview_api.py`: real `ThreadingHTTPServer` on port 0 loopback; two residents see only their own case; unknown subject 403; forged `Cookie`/`Authorization`/`X-Subject`/`?case=` ignored or 400; staff routes 404; write methods denied; revoked/expired grant on next request; store unchanged; canaries absent from HTML, JS, CSS, JSON and error bodies; missing fixture/store fails safely; Host header guard; non-loopback bind refused.
* `src/api/checks/resident_preview_browser_check.py`: starts the real preview process from a freshly built fixture, Chromium via Playwright: banner and offer/confirmed text, tab order and visible focus, skip link, error state after grant revocation (edits the fixture file while running, then Refresh shows the error, focus on error heading), 320px reflow without horizontal scroll, reduced motion, no console errors, unavailable controls disabled, no non-loopback requests.
* Existing: `src/api` and `src/core` suites, dependency rule, design system, accessibility baseline, Ruff and mypy.

## Phase 5: docs and preview service

README sections in `src/api/README.md` and `src/core/README.md`, index row in `docs/reference/README.md`, appended entry in `docs/reference/log.md`. Build the fixture under `/tmp/ama-444-preview-data` (new), start `ama-444-resident` tmux with resident A on `127.0.0.1:8444` and a second window with representative B on `127.0.0.1:8445`; verify with curl.

## Dependencies

Phase 2 needs Phase 1; Phase 3 needs Phase 2 route shapes; Phase 4 after 1 to 3; Phase 5 after 4.
