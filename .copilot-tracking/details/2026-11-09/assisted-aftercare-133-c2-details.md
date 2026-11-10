# Details: assisted aftercare 133 C2

## F3 replay after the date passes (`aftercare_intake.py`)

* `_assisted_errors` keeps every stable check (request id format, channel, home, owner_role refusal, date parses, text caps and privacy guard). `_date` is called with floor `0001-01-01` there.
* In `record_concern` the `work(doc)` closure: exact lookup of `request_id` first (replay or 409 conflict), then, only for a new record, `if next_update < self._today(): raise ValidationError({"next_update": ...})` before `raise_concern`. Raised inside the transaction, so the stored document is unchanged.
* Fingerprint inputs are unchanged, so existing stored documents stay valid.

## F4 sensor context (`aftercare_intake.py`)

* New `_context_errors(context)` run in `add_sensor_context` after the role check and before the transaction. Rules: Mapping, 1 to `CONTEXT_MAX_ITEMS` (10) items, keys match `^[A-Za-z][A-Za-z0-9 _-]{0,39}$`, values are non-empty strings of at most `CONTEXT_VALUE_MAX` (200) characters, and keys and values both pass `_redact` with no flagged kinds.
* Errors go to `ValidationError({"context": "..."})` with per-key messages that name the kind and the key position, never the value. Nothing is logged or discarded silently. The register's own neutral-text guard still runs afterwards.
* Context never changes state, outcome or remedy (unchanged core behaviour; asserted).

## F1 unconfirmed save outcome (`aftercare.js`)

* `aftercareSubmit` returns `outcome`: `saved`, `replayed`, `refused` (400, 403, 409: the service answered and did not save) or `unconfirmed` (network error, empty or malformed reply, 5xx, 503, 401).
* `unconfirmed` message: "Saving could not be confirmed. The concern may or may not have been saved. Keep this page open and select Record Concern again to retrieve the receipt if it was saved. Check the concerns list before starting another record or using paper." `retainRequestId` true. `refused` keeps its definite wording; 409 and 400 keep the id rule (400, 403 clear; 409 asks for a new record).
* A reply is "malformed" when it lacks an object `receipt`.

## F2 unresolved fraction (`aftercare.js`)

* `acFraction(value, noun)`: `{count,denominator}` numbers with denominator above 0 gives "N of M"; denominator 0 gives "0 of 0, so no proportion is stated"; missing or non-numeric gives "Unknown". Count greater than denominator renders as Unknown. Applied to `concerns_unresolved`.

## Tests

* Core (`test_aftercare_intake.py`): replay with clock advanced, no version change and no duplicate; changed payload after advance is 409; new record with a past date still 400 and the document unchanged; flagged email/phone in key or value refused, long value refused, too many items refused, doc text identical, response and action log lack the raw value; valid context accepted and does not dismiss or touch remedy; route 400.
* Node (`test_aftercare_screen.py`): Python builds real payloads from `AftercareService` (form, receipt, concern, evaluator with records, evaluator empty) and passes JSON to node; assertions on fraction text, no `[object Object]`, and unconfirmed outcomes.

## Amendments from the single critique (PC2-01..08, all applied)

* PC2-01: `_txn(fn, writes=...)`; a replay returns the stored text unchanged, so `version` and bytes stay identical.
* PC2-02/03: `aftercareSubmit(api, values, requestId, signal, {unresolved})`. Outcomes `saved`, `replayed`, `refused`, `conflict` (409, ambiguous), `unconfirmed`. While `unresolved` is true, a refusal keeps `retainRequestId` and tells the user to send the original details unchanged or check the concerns list.
* PC2-04: merged context key count (max 10) checked inside the transaction.
* PC2-05: `_guard_kinds(text)` normalises (NFKC, strip zero-width, `_` and `-` to space) before `_redact`; keys use `re.fullmatch`; applied to free text and context.
* PC2-06: unconfirmed text adds ask-a-colleague and paper-route-after-checking.
* PC2-07: receipt shape check including matching `request_id`.
* PC2-08: keep synthetic adversarial node cases beside real service payloads.
