<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 98 Deterministic Approved-Rule Validation, Version-Linked Review Pack, and Stale Propagation

## Metadata

* Task ID: issue-98-field-validation-2142
* Task slug: issue-98-field-validation-2142
* Related plan: .copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/issue-98-field-validation-2142-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, src/core/src/zava_forward/core/forms.py, src/core/src/zava_forward/core/form_review.py, src/core/src/zava_forward/core/form_export.py

## Phase Index

| Phase ID | Name                                                                                             | Status | Detail sections        |
|----------|--------------------------------------------------------------------------------------------------|--------|------------------------|
| P01      | Implement deterministic approved-rule validation, version-linked review pack, and stale propagation | Ready  | P01, P01-T01, P01-T02  |
| P02      | Update component documentation and pass local verification gate                                  | Ready  | P02, P02-T01, P02-T02  |

<!-- rpi:phase id=P01 -->
## P01: Implement deterministic approved-rule validation, version-linked review pack, and exact stale propagation

### Context

Research (`C1`–`C12`) established that `forms.py`, `form_review.py`, and `form_export.py` implement schema registration (`Unapproved` by default), evidence-bound candidate staging, reviewer audit history, and held working-note exports, while an aborted untracked draft at `src/core/src/zava_forward/core/form_validation.py` contains 3 strict `mypy` `no-any-return` errors and 6 behavioral gaps (`rule_refs` & funding-route gates, rule kinds & `sum` calculation reproduction, registered-reviewer confirmation checks, `open_issues` status precedence, deduplicated per-evidence `input_version` + single-pass hashing + `history`, and `pack_freshness`).

### Intent

Complete `form_validation.py` and prove all Issue #98 `src/core` requirements across both JSON `Store` and SQLite `SqlStore` with locked test ownership (`src/core/tests/test_issue_98_field_validation.py`, 0 removals, max 16 focused behavioral test methods).

### Boundaries

* Included: `src/core/src/zava_forward/core/form_validation.py` and `src/core/tests/test_issue_98_field_validation.py`.
* Excluded: `src/core/pyproject.toml`, `form_export.py` `BODY_KEYS`, `forms.register_schema` default `Unapproved` behavior, `src/api`, and fabricated live approvals.

### Likely Targets

* `src/core/src/zava_forward/core/form_validation.py`: Deterministic validation, review-pack assembly, and pack freshness logic.
* `src/core/tests/test_issue_98_field_validation.py`: Semantic behavioral test suite matching `-p 'test_*98*.py'`.

### Dependencies

* None (`forms.py`, `form_review.py`, and `form_export.py` are already present in `src/core`).

### Validation Expectations

* Bare `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` exit `0` in `src/core`.

### Completion Evidence

* Passing `mypy`, `ruff`, and `test_issue_98_field_validation.py` output recorded in `.copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md`.

### Unresolved Items

* None within `src/core` engineering scope (`FD-01`–`FD-14` recorded as external human follow-up).

<!-- rpi:task id=P01-T01 -->
### P01-T01: Complete and harden `src/core/src/zava_forward/core/form_validation.py`

#### Context

Wave 3 contrarian analysis (`C10`, `C11`) identified exact invariants needed in `form_validation.py` so deterministic validation never trusts unapproved/unbound rules or unconfirmed values, and `review_pack` / `pack_freshness` preserve version-linked provenance and exact field-level staleness.

#### Intent

Implement `validate(store, user, case_id, draft_id, rules)`, `review_pack(store, user, case_id, draft_id, rules)`, and `pack_freshness(store, user, case_id, saved, rules)` with full `mypy --strict` type annotations (`dict[str, Any]`, explicit `bool(...)` / `isinstance(...)` narrowing, zero `Any` returns).

#### Boundaries

* Included:
  * **Rule structure check (`_check_rules`)**: Enforce exact key sets (`SET_KEYS = {"id", "version", "approval", "bound", "rules"}`, `APPROVAL_KEYS = {"status", "approver", "evidence_ref"}`, `BOUND_KEYS = {"schema_id", "schema_version", "schema_digest", "template_id", "template_version"}`, `RULE_KEYS = {"rule_id", "field_id", "kind", "param", "message"}`). Permit `None` or blank `approver`/`evidence_ref` in `_check_rules` when `approval["status"] in ("Approved", "Unapproved")` so unapproved rule sets reach `_approval_gaps` and return `Not evaluated` (`AC-1`) rather than `ValueError`. Validate each item's `rule_id` is unique and nonblank, `field_id` exists in `schema["fields"]` and its `category not in forms.HUMAN_ONLY` (`AC-2`), `kind` is in closed vocabulary `{"min", "max", "max_length", "pattern", "equals", "one_of", "sum"}`, `message` is nonblank string, at most one `sum` rule targets a given `field_id`, and `param` matches the target field's schema type:
    * `min`, `max`: `integer` or `number` field, numeric non-`bool` finite `param`.
    * `max_length`: `string` field, non-negative `int` (non-`bool`) `param`.
    * `pattern`: `string` field, valid regex string `param` (`re.compile` succeeds).
    * `equals`: any non-`HUMAN_ONLY` scalar field (`string`, `integer`, `number`, `boolean`, `date`, `enum`), `param` valid for `field` via `form_review._valid(param, field)` (using `Decimal(str(...))` equality on `number` fields so `100` matches `100.0`, and `form_review._equal` on other types).
    * `one_of`: any non-`HUMAN_ONLY` scalar field, non-empty `list` where every element satisfies `form_review._valid(item, field)` (compared via `Decimal(str(...))` on `number` fields and `form_review._equal` on other types).
    * `sum`: `integer` or `number` field (not `HUMAN_ONLY`) whose `field["calculation_ref"]` is non-None; `param` is a `dict` with exact keys `{"calc_id", "calc_version", "addends"}`, `calc_id` and `calc_version` matching `field["calculation_ref"]["id"]` and `field["calculation_ref"]["version"]`, and non-empty unique `addends: list[str]` of distinct non-`HUMAN_ONLY` `integer`/`number` schema fields (excluding `field_id` itself).
    Raise `ValueError` on any structural mismatch before checking approval status.
  * **Unavailable / quarantined document guard (`DocumentUnavailable`)**: In both `validate` and `review_pack`, run `form_review._visible` and `form_review._report` inside `try ... except form_review.DocumentUnavailable as err` so missing, unscanned, quarantined, or policy-excluded source bytes return a controlled `status="Unavailable"` payload (with `pack_status="Held"`, `pack_ready_for_review=False`, `reviewed=False`, `submission="Not submitted"`, `eligibility="Not assessed"`, and recovery `notice = str(err)`) before disclosing draft state (`PC-002`).
  * **Fail-closed approval and binding gate (`_approval_gaps`)**: Return `Not evaluated` with explicit gap reasons unless:
    1. Registered schema row has `approval == "Approved"` and `_nonblank(row.get("approval_evidence"))`.
    2. Registered schema row has `source_policy_status == "Approved"`.
    3. For `schema["form_type"] == "funding"`, `schema["funding"]["status"] == "Evidenced"`.
    4. `row["digest"] == draft["schema_digest"]` (current registered schema matches draft's bound schema digest).
    5. `(rules["id"], rules["version"])` matches an entry `(ref["id"], ref["version"])` in `schema["rule_refs"]`.
    6. `rules["approval"]` has `status == "Approved"`, `_nonblank(approver)`, and `_nonblank(evidence_ref)`.
    7. `rules["bound"]` exactly matches `schema_id`, `schema_version`, `schema_digest`, `template_id`, and `template_version`.
  * **Strict reviewer-confirmed input gate (`_confirmed`)**: Verify confirmation provenance (`_provenance_confirmed`) separately from value/blankness checks (`PC-003`): provenance holds iff `form_review._reviewer_confirmed(draft, fid, row)` is true, the latest history entry for `fid` has `decision == ("accept" if row["state"] == "Accepted" else "correct")`, `_nonblank(last.get("reviewer"))` and `forms._registered(store, last["reviewer"]) is not None`, and `isinstance(row.get("evidence"), dict)` with non-None `"source"` and `"locator"` equal to `last["new"].get("evidence")`. Include `fid -> row["value"]` in `confirmed` iff `row["effective_state"] in ("Accepted", "Corrected")`, `_provenance_confirmed` holds, `form_review._valid(row["value"], field)` is true, and string values are nonblank. Emit `"Fail"`: `"Value lacks reviewer confirmation."` (deduplicated against `report["issues"]`) ONLY when `row["effective_state"] in ("Accepted", "Corrected")` fails `_provenance_confirmed`, so blank-string corrections stay `Unknown` and wrong-type acceptances keep `"Wrong schema value type."` (`PC-003`).
  * **Rule & calculation evaluation and status precedence**:
    * Persist `rule_id`, `field_id`, `kind`, `copy.deepcopy(param)`, `message`, `status`, and `reason` on every item in `validation["results"]` so `pack_freshness` can detect Pass-preserving rule `param`/`message` or target changes (`PC-001`).
    * Non-`sum` rules: if `fid not in confirmed`, emit `status="Unknown"`, `reason="Field lacks a current reviewer-confirmed value."` without reading `draft["fields"][fid]["value"]`. Otherwise evaluate deterministically (`Decimal(str(...))` for numeric comparisons so float binary rounding cannot distort decimal currency/area rules) and emit `Pass` or `Fail`.
    * `sum` rules: require `fid in confirmed` AND every `addend in confirmed`; if any is missing, emit `status="Unknown"` naming missing confirmed field(s); otherwise compare `Decimal(str(confirmed[fid])) == sum(Decimal(str(confirmed[a])) for a in addends)` (`Pass` if equal, `Fail` if unequal). Filter `_report`'s `"Approved calculation is unavailable."` issue only for `(fid, calc_id, calc_version)` covered by an approved `sum` rule; retain it in `open_issues` for any `calculation_ref` field lacking an approved `sum` rule.
    * Overall validation status: combine `{r["status"] for r in results} | {i["status"] for i in open_issues}` using precedence `Fail > Conflict > Unknown > Pass`.
  * **Single-report `review_pack` assembly**: Under `forms._actor` and `with store.lock:`, run `_report(store, case, draft, digests)` once, compute validation from that report, stamp deterministic `attachment_id = f"{att['id']}:v{att['version']}"` on each detached attachment entry (`PC-003`), and build canonical `PACK_BODY_KEYS` (`draft_id`, `case_id`, `form_type`, `pack_status`, `reviewed`, `submission`, `eligibility`, `input_version`, `template`, `template_version`, `schema_id`, `schema_version`, `schema_digest`, `rule_refs`, `fields`, `evidence`, `attachments`, `history`, `validation`, `stale_fields`) + `content_sha256` via typed `form_export._digest` (`PC-002`). Collect deduplicated `evidence` entries (keyed by `(source_id, source_version)` across fields where `row["evidence"] is not None`), each carrying `source_id`, `source_version`, `document_hash`, `attachment_id` (looked up by `(source_id, source_version)`, or `None` if tampered/absent from history), `field_ids`, `locators`, `template_version`, and `input_version = max(field_item["input_version"] for bound fields)`.
  * **Exact `pack_freshness(store, user, case_id, saved, rules)`**:
    * Verify `saved` is a `dict` containing all `PACK_BODY_KEYS`, `saved["case_id"] == case_id`, valid `fields`/`evidence`/`attachments`/`validation` structure, and matching `content_sha256` via `form_export._digest`; return `{"status": "Invalid", "stale_fields": [], "unaffected_fields": [], "reasons": [...], "reviewed": False}` on mismatch/cross-case/tamper (`PC-002`).
    * Re-assemble current pack (`current = review_pack(store, user, case_id, saved["draft_id"], rules)`), catching `KeyError` on missing `draft_id` as `status="Unavailable"` and returning controlled `status="Unavailable"` (`stale_fields=[]`, `unaffected_fields=[]`, `reasons=[current["notice"]]`, `reviewed=False`) whenever `current.get("status") == "Unavailable"` (`PC-002`).
    * Compute changed fields from:
      1. `current["stale_fields"]` (source hash/version/kind drift or registered schema impact from `_report`).
      2. Field state/value/evidence/`input_version`/`template_version` differences between `saved["fields"]` and `current["fields"]` (including removed/added schema fields).
      3. Per-field `open_issues` differences between `saved["validation"]` and `current["validation"]`.
      4. Rule-level differences between `saved["validation"]["results"]` and `current["validation"]["results"]` keyed by `rule_id` across `(field_id, kind, param, message, status)` (`PC-001`): if validation transitioned to/from `Not evaluated` (global authority/template/schema-binding change), mark fields targeted by rules or `calculation_ref` (or all active schema fields if template/approval revoked) stale; if individual rules were added, removed, or modified, mark both the saved and current `field_id`s stale.
      5. Fixed-point transitive propagation (`PC-001`): propagate staleness to any schema field `fid` where `any(c["field_id"] in stale_set for c in field["required_when"])` (`forms.py:201`), and to any `sum` rule target `field_id` (across active and saved `sum` rules on existing schema fields) where any `addend in stale_set`.
    * Append non-empty human-readable `reasons` for any field, rule, `input_version`, `schema_digest`, `rule_set`, or `content_sha256` drift whenever `status == "Stale"` (`PC-001`), and return `status="Current"` iff `current["content_sha256"] == saved["content_sha256"]` and `not stale_fields`, else `status="Stale"` with sorted `stale_fields`, sorted `unaffected_fields` (`[fid for fid in active_field_ids if fid not in stale_set]`), `reasons`, and `reviewed=False`.
* Excluded: Modifying `form_review.py` or `form_export.py` public contracts.

#### Likely Targets

* `src/core/src/zava_forward/core/form_validation.py`: Complete module implementation.

#### Dependencies

* `forms._actor`, `forms._registered`, `forms.HUMAN_ONLY`, `form_export._digest`, `form_review.DocumentUnavailable`, `form_review._draft`, `form_review._visible`, `form_review._report`, `form_review._reviewer_confirmed`, `form_review._schema`, `form_review._valid`, `form_review._equal`.

#### Validation Expectations

* `python3 -m mypy` reports 0 errors on `form_validation.py`; `ruff check` and `ruff format --check` pass.

#### Completion Evidence

* Clean static check output and passing unit assertions in `P01-T02`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Create `src/core/tests/test_issue_98_field_validation.py` for JSON and SQLite stores

#### Context

Caller verification runs `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` after bare `python3 -m mypy` (`strict = true` on `tests`). Existing `test_form_export.py` demonstrates reusing `test_form_review.FormReview` (`self.stores: list[Any]`) so strict `mypy` passes with zero `pyproject.toml` changes (`C7`, `C9`).

#### Intent

Write a focused, high-signal behavioral test module (`<= 16` test methods, 0 test removals, canonical target `src/core/tests/test_issue_98_field_validation.py`, generated targets `none`) testing every semantic edge case across both JSON `Store` and SQLite `SqlStore`.

#### Boundaries

* Included semantic test cases (each iterated over `Store` and `SqlStore`):
  1. Unapproved default registration, unapproved source policy, unknown funding route on `"funding"` schema, unapproved rules, unbound digest/template version, and `(id, version)` missing from `schema["rule_refs"]` all return `Not evaluated` and `pack_status="Held"`.
  2. Malformed rule sets (duplicate `rule_id`, unknown `field_id`, `HUMAN_ONLY` target or addend, mismatched `kind`/`param` for field type, invalid regex, duplicate `sum` rule on one field, `sum` unbound to `calculation_ref` or self-referencing/non-numeric addends) raise `ValueError`.
  3. Staged unreviewed candidates, rejected fields, blank strings (which remain `Unknown`, never `Fail`), stale fields, unregistered-reviewer history, and tampered draft values/evidence are excluded from `confirmed`; rules never evaluate unconfirmed candidate values (e.g., failing staged number yields `Unknown`, not `Fail`, while tampered `Accepted` row failing confirmation provenance yields `Fail` `"Value lacks reviewer confirmation."`).
  4. Approved rules across scalar types (`min`, `max`, `max_length`, `pattern`, `equals`, `one_of`, including `Decimal` `number` equality `100` vs `100.0`) and deterministic `sum` bound to `calculation_ref` (exact `Decimal` match -> `Pass` clearing `"Approved calculation is unavailable."`; mismatch -> `Fail`; missing calculation rule -> stays `Unknown` `"Approved calculation is unavailable."`; unreviewed conflict -> overall `Conflict` beats `Unknown`, `Fail` beats `Conflict`).
  5. `review_pack` links `fields`, deduplicated `evidence` (with deterministic `attachment_id` matching `attachments` and per-evidence `max` bound-field `input_version`, unaffected when an unrelated field on another document is reviewed), `attachments`, and `history` with `template_version` and `input_version`, hashes each distinct source document at most once per call, sets `Ready for Finance review` only when `Pass` and no stale fields, and keeps `reviewed=False`, `Not submitted`, `Not assessed`.
  6. `pack_freshness` detects tampered digests, missing keys, and cross-case `case_id` as `Invalid`, returns controlled `Unavailable` across `validate`/`review_pack`/`pack_freshness` when bound source bytes are missing/quarantined or `draft_id` is missing, reports `Current` when unchanged, and computes exact dependent-only `stale_fields` vs `unaffected_fields` with non-empty `reasons` when: (a) one source document updates, (b) one field-targeted rule in an approved rule set changes — including a Pass-preserving `param` tightening — with transitive propagation across `required_when` (`c["field_id"]`) and `sum` dependents while leaving unrelated fields unaffected, (c) schema changes one field, or (d) reviewer updates one confirmed input.
  7. Staff/tenant authorization guard rejects unauthenticated, resident, or out-of-scope callers.
* Excluded: Trivial constant checks, `pyproject.toml` edits, or duplicate coverage of staging mechanics already in `test_form_staging.py`.

#### Likely Targets

* `src/core/tests/test_issue_98_field_validation.py`: New unit test module.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* `python3 -m mypy` and `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` exit `0`.

#### Completion Evidence

* Verbose unittest execution log showing all `test_*98*.py` cases passing across JSON and SQLite stores.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Update component documentation and pass local verification gate

### Context

Repository code-change rules require updating directly related component documentation (`src/core/README.md`) and verifying both the targeted caller command and existing form regression tests.

### Intent

Document `form_validation` accurately in `src/core/README.md` and run the complete verification gate in `src/core`.

### Boundaries

* Included: `src/core/README.md` and read-only execution of `mypy`, `ruff`, and `unittest` in `src/core`.
* Excluded: Unrelated documentation files or `.copilot-tracking/` references in `README.md`.

### Likely Targets

* `src/core/README.md`: Form schema, staging, working review, held export, and approved-rule validation section.

### Dependencies

* `P01`.

### Validation Expectations

* Markdown links and code identifiers in `src/core/README.md` match implemented signatures; caller verification command and `test_form*.py` regression suite exit `0`.

### Completion Evidence

* Recorded command exit codes and summary in `.copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Document `form_validation` APIs and open `FD-01`–`FD-14` boundaries in `src/core/README.md`

#### Context

`src/core/README.md` currently documents `forms`, `form_review`, and `form_export` (`src/core/README.md:603-695`). Adding `form_validation` keeps the component guide authoritative.

#### Intent

Add concise documentation for `form_validation.validate`, `form_validation.review_pack`, and `form_validation.pack_freshness`, supported deterministic rule kinds, version-linked `fields`/`evidence`/`attachments`, exact stale propagation, and the preserved `Unapproved` registration boundary (`FD-01`–`FD-14`), while reconciling the earlier statements at `src/core/README.md` lines 668 and 692–693 ("Approved rules, calculations and reviewed packs still do not exist") so `README.md` remains internally consistent (`PC-003`).

#### Boundaries

* Included: `src/core/README.md` form section.
* Excluded: Citing `.copilot-tracking/` paths in `src/core/README.md`.

#### Likely Targets

* `src/core/README.md`: Form workflow documentation section.

#### Dependencies

* `P01-T01`.

#### Validation Expectations

* `git diff src/core/README.md` review confirms plain ASCII style, `*` bullets, accurate function names, and intact relative links.

#### Completion Evidence

* Updated `src/core/README.md` diff verified cleanly.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Execute required `mypy`, `ruff`, `test_*98*.py`, and form regression checks

#### Context

Caller prompt requires running `cd /home/azureuser/source/ama-demo-wt/feat-98-field-validation-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*98*.py' -v`.

#### Intent

Verify zero type, lint, format, unit, or regression failures across `src/core`.

#### Boundaries

* Included: Exact caller verification command plus `python3 -m unittest discover -s tests -p 'test_form*.py' -q`.
* Excluded: Modifying tool configurations to suppress errors.

#### Likely Targets

* `src/core` test and static-analysis runners (verification only).

#### Dependencies

* `P01-T01`, `P01-T02`, `P02-T01`.

#### Validation Expectations

* Exit code `0` for `mypy`, `ruff check .`, `ruff format --check .`, `test_*98*.py`, and `test_form*.py`.

#### Completion Evidence

* Command outputs captured in `.copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md`.

#### Unresolved Items

* None.
