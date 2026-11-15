<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #133 Criterion 5 — No Causation, Blame, or Savings Promise in Aftercare Text

## Metadata

* Task ID: rpi-133-no-causation-blame-savings-20261115T0316Z
* Task slug: 133-no-causation-blame-savings
* Related plan: .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/133-no-causation-blame-savings-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, src/core/src/zava_forward/core/aftercare.py, src/core/src/zava_forward/core/aftercare_intake.py, src/core/src/zava_forward/core/quality.py, src/api/src/zava_forward/api/web/aftercare.js

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Harden Core `neutral_text` Guard and `AftercareRegister` Boundaries | Ready | P01, P01-T01, P01-T02 |
| P02 | Enforce Neutral-Text Boundaries in `AftercareService` and Handover Quality Notes | Ready | P02, P02-T01, P02-T02 |
| P03 | Expand Core & API Test Coverage and Run Validation | Ready | P03, P03-T01, P03-T02 |

## Test Ownership & Budget Lock

* Canonical test targets:
  * `src/core/tests/test_aftercare.py` (semantic unit tests for `neutral_text`, `neutral_violations`, `AftercareRegister` write/template/proposal/restore boundaries; max `+12` test methods, exact removals: `none`).
  * `src/core/tests/test_aftercare_intake.py` (service & route contract tests for `AftercareService` template neutrality, verbatim resident statements, HTTP 400 `ValidationError` on prohibited `/outcome`, `/remedy`, `/sensor-context`, and `propose_pack`/`review_pack` inputs, and receipt restore validation; max `+8` test methods, exact removals: `none`).
  * `src/api/tests/test_aftercare_served.py` (served HTTP API tests over `App` covering `/api/aftercare/*` and `/api/cases/ZF-1/quality-aftercare` neutrality and 400 non-mutation across restart; max `+4` test methods, exact removals: `none`).
* Generated targets: `none`.
* Regression suites preserved unchanged: `src/core/tests/test_aftercare_store.py`, `src/api/tests/test_aftercare_screen.py`, `src/core/tests/test_quality_procurement.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/agents/tests/test_epic104_bounded_ai_invariants.py`.

<!-- rpi:phase id=P01 -->
## P01: Harden Core `neutral_text` Guard and `AftercareRegister` Boundaries

### Context

`zava_forward.core.aftercare` defines `neutral_text` and `AftercareRegister`. Research (`C1`, `C12`..`C15`, `C18`, `C20`, `C22`, `CF1`, `CF2`) identified four gaps: (1) missing Unicode/invisible/quote/whitespace normalization, (2) whole-string short-circuiting when `_UNCERTAIN` matches a single clause, (3) missing lexical patterns for housing lifestyle blame, measure-causation proof, and currency/percent/payback savings promises, and (4) unguarded fields in `record_outcome`, `set_remedy`, `review_pack`, `_context` keys, `raise_concern` `owner`, `record_closure` `recorded_by`, form/template helpers, and `from_state`.

### Intent

Make `neutral_text` normalization-hardened and clause-precise, and enforce it at every `AftercareRegister` write, template, proposal, review, and snapshot-restore boundary while preserving verbatim resident `statement` and `representative_basis`.

### Boundaries

* Included: `src/core/src/zava_forward/core/aftercare.py`.
* Excluded: HTTP routing, store adapters, and web UI assets.

### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Harden `neutral_text`, expose `neutral_violations`, split unconditional vs uncertainty-qualifiable paraphrase patterns, guard all register methods and `from_state`.

### Dependencies

* None.

### Validation Expectations

* `python3 -m unittest discover -s tests -p 'test_aftercare.py' -q` in `src/core` passes, and every existing literal in `src/api/src/zava_forward/api/web/aftercare.js` continues to pass `aftercare.neutral_text`.

### Completion Evidence

* Updated `src/core/src/zava_forward/core/aftercare.py` passing `ruff`, `mypy`, and `test_aftercare.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Normalize text, scope clause uncertainty, and expand prohibited phrasing detection in `aftercare.py`

#### Context

`neutral_text` (`aftercare.py:113-124`) already uses span-bounded `_UNCERTAIN.sub(" ", ...)` on indirect `whether|if` clauses and `_NEGATED_CLAIM.sub(" ", ...)`, but lacks Unicode `NFKC`/invisible-character folding, newline-to-delimiter normalization, conjunction/dash stop-lookaheads (`however`, `therefore`, `yet`, `so`, `while`, `though`), and full coverage of lifestyle blame, measure-causation proof, and currency/percent/payback savings promises.

#### Intent

Provide `neutral_violations(text: str) -> tuple[str, ...]` and `neutral_text(text: str) -> str` with canonical normalization, tight clause-bounded `whether|if` uncertainty and negated-claim folding, and complete causation/blame/savings coverage without breaking committed `whether|if` assertions (`test_aftercare.py:256-258`).

#### Boundaries

* Included:
  * `_normalize_for_guard(text: str) -> str`: `unicodedata.normalize("NFKC", text)`, strip invisible chars (`[\u200b-\u200f\u2060\ufeff\u00ad]`), map curly quotes/apostrophes (`\u2018`, `\u2019` -> `'`; `\u201c`, `\u201d` -> `"`), lower-case, convert `[\r\n]+` to `"; "` **before** collapsing horizontal whitespace `[ \t\f\v]+` to `" "`.
  * Keep `BANNED_PHRASES` unconditional across normalized text (matching multi-space, newline-wrapped, fullwidth, or zero-width-obfuscated variants when collapsed to single spaces for phrase checking).
  * Retain span-bounded `_UNCERTAIN` (`\b(?:cannot determine|can ?not determine|unknown|not known|no evidence)\s+(?:whether|if)\b`) and `_NEGATED_CLAIM` (`\b(?:no|not a|never a)\s+(?:claim|promise|guarantee)s?\s+(?:of|about)\b` plus `\b(?:do|does|did|can)\s*not\s+(?:show|prove|establish|claim|promise|assign|attribute)\b`) with tight stop-lookaheads halting at `[.!?;:,\n\u2014\u2013]`, ` - `, `--`, or `\s(?:and|but|or|however|therefore|thus|hence|consequently|yet|so|whereas|while|though|although)\b` (or `$`).
  * Expand `PARAPHRASE_PATTERNS` to cover resident lifestyle attribution (`drying (?:clothes|laundry|washing)`, `windows? (?:kept |left )?(?:closed|shut)`, `not opening windows?`, `(?:lack of|failing to|failure to) (?:ventilate|ventilation|heat)`, `(?:resident|occupant|household|tenant)s?'?s? lifestyle`, `lifestyle choice`, `(?:heating|occupant|resident|household|tenant) habits?`, `(?:improper|incorrect) use`, `(?:user|operator) error`, `misus(?:e|ing)`, `negligen(?:ce|t)|careless`, `blamed on`, `to blame`, `fault of (?:the )?(?:resident|household|tenant|occupant)s?`), measure-causation proof (`(?:proven|proved) to cause`, `proves (?:that|the)\b`, `attribut(?:able|ed) to`, `caused (?:the )?(?:damp|mould|mold|condensation|cold|higher|heat loss)`, `is why (?:the|your)\b`, `reason (?:your bills?|the (?:room|home|house))\b`), and financial/energy savings promises (`sav(?:e|es|ing)\s+(?:up to\s+|around\s+|over\s+)?(?:£|\$|€|gbp\s*)?\d+(?:\.\d+)?\s*(?:%|percent|per cent|pounds?|gbp|a year|per year|a month|per month)?`, `pay-?back`, `pays? for itself`, `slash(?:es|ing)? (?:your |the )?(?:energy |heating )?(?:bills?|costs?)`, `(?:promised|guaranteed) (?:savings?|reductions?)`, `(?:energy|bill|cost|financial) savings?`, `cheaper to run`).
* Excluded: Rewriting or altering valid caller strings; `neutral_text` returns the exact original `text` when `neutral_violations(text)` is empty.

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Normalization, pattern tables, `neutral_violations`, and `neutral_text`.

#### Dependencies

* None.

#### Validation Expectations

* All existing `EvaluatorTests` (including `test_aftercare.py:216-218,252-260`) and `test_aftercare_screen.py::test_every_literal_string_passes_the_neutral_language_guard` pass alongside new obfuscation, multi-clause, lifestyle, causation, and savings test cases.

#### Completion Evidence

* `neutral_violations` and `neutral_text` implemented with strict type annotations.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce `neutral_text` across all `AftercareRegister` write, template, proposal, and `from_state` boundaries

#### Context

`record_outcome`, `set_remedy`, `review_pack`, `_context` keys, `raise_concern` `owner` / `recorded_by`, `record_closure` `owner` / `home_ref`, `evaluator_view` `unknowns`, parts of `intake_form`/`intake_errors`, and `from_state` currently omit `neutral_text` (`C12`..`C15`, `C18`, `C20`, `PC-002`).

#### Intent

Guarantee no unguarded staff/system/AI string can enter or be emitted from `AftercareRegister`, whether via method calls, templates, or `from_state` snapshot restoration.

#### Boundaries

* Included:
  * `_context`: validate both keys and values through `neutral_text`.
  * `intake_form()` & `intake_errors()`: pass `title`, `intro`, `accessible_route`, `protection`, field/option/channel labels, and error strings through `neutral_text`.
  * `raise_concern`: validate `home_ref`, `owner` (`neutral_text(_text(owner, "Human owner"))`), optional `staff_recorded` `recorded_by` (`neutral_text(_text(recorded_by, "Recording staff member"))`), `accessible_route` (`neutral_text(ACCESSIBLE_ROUTE)`), and `sensor_context` (`_context`). Keep `statement` and `representative_basis` verbatim (`_text(...)` only).
  * `record_outcome`: validate `evidence` (`neutral_text(_text(evidence, "Outcome evidence"))`).
  * `set_remedy`: when `status in ("completed", "not_needed")`, require `evidence = neutral_text(_text(evidence, "Remedy evidence"))` and `rec["investigation"] == "outcome_recorded"`; when `status in ("open", "in_progress")`, store `neutral_text(evidence.strip())` if `isinstance(evidence, str) and evidence.strip()` else `None`.
  * `record_closure`: validate `home_ref` and `owner` (`neutral_text(_text(owner, "Closure owner"))`).
  * `view`: attach `neutral_text(PROTECTION)`.
  * `evaluator_view`: wrap `unknowns` items and `EVALUATOR_NOTICE` in `neutral_text`.
  * `propose_pack`: pass `facts`, `questions`, optional `ai_summary`, `EVALUATOR_NOTICE`, `PACK_MANUAL_ROUTE`, and `PACK_NOT_REVIEWED` through `neutral_text`.
  * `review_pack`: validate `reviewer` and `reason` with `neutral_text(_text(...))` before mutating `pack`.
  * `from_state`: validate concern `home_ref`, `owner`, optional `staff_recorded` `recorded_by`, `accessible_route`, `sensor_context` (via `_context`), `outcome.evidence`, and `remedy.evidence` (required for `status in ("completed", "not_needed")` and checked if non-None for `"open"` / `"in_progress"`); closure `home_ref` and `owner`; and pack `reviewer_function`, `recorded_facts`, `questions_for_investigator`, optional `ai_summary`, `notice`, `manual_route`, `approval`, optional `review` (`by`, `action`, `reason`), and absence of `"sensor_context"`.
* Excluded: Censoring `rec["statement"]` or `rec["representative_basis"]`.

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: `intake_form`, `intake_errors`, `_context`, `from_state`, `raise_concern`, `record_outcome`, `set_remedy`, `record_closure`, `view`, `propose_pack`, `review_pack`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Mutating any persisted field in `to_state()` to include causation, blame, or savings-promise text causes `AftercareRegister.from_state` to raise `ValueError`.

#### Completion Evidence

* All `AftercareRegister` entry/exit/restore methods enforce `neutral_text`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Enforce Neutral-Text Boundaries in `AftercareService` and Handover Quality Notes

### Context

`AftercareService` (`aftercare_intake.py`) maps domain validation into structured field-level `ValidationError` HTTP `400` responses without echoing user input, persists receipts alongside the register, and renders staff/evaluator payloads (`C16`, `C17`, `C19`, `C21`). Separately, `Store.add_aftercare` (`quality.py:392-402`) records handover aftercare notes on `/api/cases/{cid}/quality-aftercare` (`C6`).

### Intent

Ensure every `AftercareService` write, bounded pack proposal/review helper, template render, receipt restore, and `quality.py:add_aftercare` call enforces `neutral_text` with plain-language, copy-standard-compliant error messages.

### Boundaries

* Included: `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/quality.py`, and `src/core/README.md`.
* Excluded: Adding new HTTP endpoints to `server.py` (`test_role_endpoint_inventory.py` invariant) or enabling live AI model calls (`ai_registry.py` `FR-036` invariant).

### Likely Targets

* `src/core/src/zava_forward/core/aftercare_intake.py`: Neutral-text validation in `_free_text` (optional flag), `_context_errors`, `record_outcome`, `set_remedy`, `propose_pack`, `review_pack`, `_validate`, and templated output builders.
* `src/core/src/zava_forward/core/quality.py`: `add_aftercare` memory-reference and `neutral_text` guard.
* `src/core/README.md`: Update `#133` section prose.

### Dependencies

* P01.

### Validation Expectations

* Prohibited `/outcome`, `/remedy`, `/sensor-context`, and service `propose_pack`/`review_pack` inputs raise `ValidationError` with field-keyed plain-language messages, zero caller echo, and unchanged store bytes; prohibited `/api/cases/{cid}/quality-aftercare` notes return HTTP `400`.

### Completion Evidence

* Updated `aftercare_intake.py`, `quality.py`, and `src/core/README.md` passing lint, typing, copy audit, and service tests.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Guard `AftercareService` write, pack-proposal, template-render, and `_validate` restore paths in `aftercare_intake.py`

#### Context

`AftercareService.record_outcome` and `set_remedy` (`aftercare_intake.py:648-668`) do not check `neutral_text` in `_free_text`, and `_context_errors` (`aftercare_intake.py:286-308`) checks privacy/length without `neutral_text`, causing `add_sensor_context` to leak a raw `ValueError` instead of `ValidationError({"context": ...})` (`C16`, `C17`). Receipt restoration in `_validate` and several constants (`SYNTHETIC_NOTICE`, `CLOSURE_NOTE`, `SENSOR_NOTE`, `FIXED_UNKNOWNS`, `WINDOWS`, `owner_note`, `manual_route`, `_comparison` unknown `reason`) also omit explicit `neutral_text` wrapping (`C19`, `C21`).

#### Intent

Enforce plain-language, no-echo `ValidationError` (`NEUTRAL_NOTE_ERROR`) across all guarded `AftercareService` inputs, add bounded owner-gated `propose_pack` and `review_pack` methods on `AftercareService`, and self-guard every templated string and restored receipt through `neutral_text`.

#### Boundaries

* Included:
  * Plain-language error constant containing zero words banned by `test_content_standard.py` and zero prohibited n-grams (passing `neutral_text(NEUTRAL_NOTE_ERROR)` directly): `NEUTRAL_NOTE_ERROR = "Keep this note factual and observational. Record only what was reported, observed or checked."`
  * `_free_text(..., require_neutral: bool = False)` checking `neutral_violations(value)` after length and privacy checks, setting `errors[field] = NEUTRAL_NOTE_ERROR` with zero caller echo.
  * `_context_errors`: check `neutral_violations` on each key and value, returning `{"context": f"Note {position}: {NEUTRAL_NOTE_ERROR}"}` before entering `_txn` (`ValidationError` subclasses `ValueError`, preserving compatibility with `assertRaises(ValueError)`).
  * `record_outcome`: call `_free_text(evidence, "evidence", "The evidence", EVIDENCE_MAX, errors, require_neutral=True)`.
  * `set_remedy`: when `status in ("completed", "not_needed")` or `(isinstance(evidence, str) and evidence.strip())`, validate `evidence` via `_free_text(..., require_neutral=True)`; when `status in ("open", "in_progress")` and `evidence` is `None` or blank, normalize to `None`.
  * `propose_pack(self, user, cid, ai_summary=None)` and `review_pack(self, user, pack_id, action, reason)`: gated on `VIEW_ROLES`; `propose_pack` rejects whitespace-only `ai_summary` (`ValidationError({"ai_summary": ...})`) and checks non-None `ai_summary` via `_free_text(..., require_neutral=True)`; `review_pack` requires non-blank neutral `reason` (`ValidationError({"reason": ...})`), refuses when the concern owner is `UNKNOWN_OWNER`, and passes `owner_label(actor["role"])` as `reviewer` to `reg.review_pack` (matching `_owner_action` semantics); neither makes any model call or registers a new server HTTP route.
  * Wrap all templated strings in `form`, `_receipt`, `_display`, `concerns`, `evaluator_view` (including `unknowns`), and `_comparison` (when `status == "Unknown"`) with `neutral_text(...)`, and validate restored receipt fields (`what_happens_next`, `protection`, `accessible_route`, `synthetic_notice`, `recorded_by.name`, and `owner.label` requiring `UNKNOWN_OWNER` when `status == "unknown"`) in `_validate`.
* Excluded: Modifying HTTP route table in `handle()` or censoring resident `statement` / `representative_basis`.

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare_intake.py`.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `test_aftercare_intake.py` passes all existing 44+ tests plus new neutral-boundary and pack tests; error messages pass `test_content_standard.py` vocabulary rules and `neutral_text`.

#### Completion Evidence

* `AftercareService` methods and `_validate` enforce `neutral_text` with structured `ValidationError`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Guard `quality.py:add_aftercare` and update `src/core/README.md`

#### Context

`Store.add_aftercare` (`src/core/src/zava_forward/core/quality.py:392-402`) appends staff aftercare notes to handed-over quality records via `/api/cases/{cid}/quality-aftercare` without checking `controls.is_memory_reference` or `aftercare.neutral_violations` (`C6`, `PC-004`).

#### Intent

Reject memory references and causation, blame, or savings-promise phrasing inside `with self._quality_operation(user, case_id) as (c, user):` (preserving `PermissionError` -> HTTP `403` precedence for unauthorized actors while halting before `_qrec` / `rec["aftercare"].append`) with fixed plain-language non-echoing `ValueError` messages, and update `src/core/README.md` to reflect the hardened #133 neutral-text boundary.

#### Boundaries

* Included: `src/core/src/zava_forward/core/quality.py` (`add_aftercare`) and `src/core/README.md` (`## Aftercare concern route and evaluator view (#133)`).
* Excluded: Reformatting legacy `quality.py` lines excluded by `[tool.ruff.format].exclude` (`PC-005`) or changing other quality workflow states.

#### Likely Targets

* `src/core/src/zava_forward/core/quality.py`
* `src/core/README.md`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_quality_procurement.py` and `test_role_matrix.py` remain 100% green, and prohibited notes on `/api/cases/ZF-1/quality-aftercare` return HTTP `400` without altering the case or audit trail.

#### Completion Evidence

* `add_aftercare` enforces `controls.is_memory_reference` and `neutral_text`; `src/core/README.md` updated cleanly.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Expand Core & API Test Coverage and Run Validation

### Context

Scope 3 and 4 require focused unit and API tests verifying zero causation, blame, or savings promises across all templated outputs and deterministic rejection of prohibited generated/draft phrasing, validated by `ruff check`, `ruff format --check`, `mypy`, and the full `test_aftercare*` suites in `src/core` and `src/api`. Because `src/api` puts `../core/tests` on `mypy_path` and `PYTHONPATH` (`C25`), `test_aftercare_intake.py` lives in `src/core/tests/` while served HTTP tests live in `src/api/tests/test_aftercare_served.py`.

### Intent

Add high-signal, strictly typed tests in `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, and `src/api/tests/test_aftercare_served.py`, and run all required linters, type checks, and test suites.

### Boundaries

* Included: `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/api/tests/test_aftercare_served.py`, and validation execution.
* Excluded: Modifying `pyproject.toml` or weakening strict typing overrides.

### Likely Targets

* `src/core/tests/test_aftercare.py`
* `src/core/tests/test_aftercare_intake.py`
* `src/api/tests/test_aftercare_served.py`

### Dependencies

* P01, P02.

### Validation Expectations

* Zero failures across `ruff check`, `ruff format --check`, `mypy`, `src/core` `test_aftercare*`, `src/api` `test_aftercare*`, `test_quality_procurement`, `test_content_standard`, `test_role_endpoint_inventory`, and `test_epic104_bounded_ai_invariants`.

### Completion Evidence

* Recorded command outputs and test counts in `.copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add unit, intake-service, and HTTP-served neutral-text boundary tests

#### Context

Existing tests verify basic `BANNED_PHRASES` on `neutral_text`, `add_sensor_context`, and `propose_pack`, plus JS string literals in `aftercare.js`, but do not cover obfuscation, multi-clause `_UNCERTAIN` bypasses, lifestyle/measure-causation/currency-savings corpora, `record_outcome`, `set_remedy`, `review_pack`, snapshot/receipt restore refusal, or served HTTP 400 non-mutation on `/outcome`, `/remedy`, `/sensor-context`, and `/quality-aftercare`.

#### Intent

Add focused, non-redundant test cases that fail without P01/P02 and prove every boundary.

#### Boundaries

* Included:
  * `src/core/tests/test_aftercare.py`: normalization/obfuscation bypasses, multi-clause uncertainty whitewash refusal vs single-clause uncertainty & negated disclaimer acceptance, lifestyle/causation/blame/savings corpus, `record_outcome`/`set_remedy`/`review_pack`/`_context`-key/`owner` refusals, recursive neutrality audit of `intake_form`/`intake_errors`/`view`/`evaluator_view`/`propose_pack`, and `from_state` tampered-snapshot refusals.
  * `src/core/tests/test_aftercare_intake.py`: recursive neutrality audit across `form`, `record_concern` receipt, `concern` detail, `concerns` list, and `evaluator` view; verbatim preservation of household `statement`/`representative_basis` containing installer-promise or causal quotes while generated fields stay neutral; HTTP 400 `ValidationError` (no echo, unchanged bytes) on prohibited `/outcome`, `/remedy`, and `/sensor-context` calls; bounded `AftercareService.propose_pack` / `review_pack` owner & neutral-draft enforcement; tampered receipt restore refusal.
  * `src/api/tests/test_aftercare_served.py`: end-to-end HTTP `App` verification (constructing inline typed quality-submission evidence without importing untyped `test_quality_procurement` or `dataset`, `PC-005`) that served `/api/aftercare/*` templated payloads pass `neutral_text` and prohibited `/outcome`, `/remedy`, `/sensor-context`, and `/api/cases/ZF-1/quality-aftercare` requests return HTTP `400` without echoing input or mutating SQLite state across restart.
* Excluded: Duplicate module creation in `src/api/tests/`.

#### Likely Targets

* `src/core/tests/test_aftercare.py`
* `src/core/tests/test_aftercare_intake.py`
* `src/api/tests/test_aftercare_served.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* All added tests are strictly typed (`-> None`, explicit collection types) and pass both `mypy` and `unittest`.

#### Completion Evidence

* Passing test runs in `src/core` and `src/api`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run `ruff`, `mypy`, `test_aftercare*` in `src/core` and `src/api`, and cross-cutting invariant suites

#### Context

Repository focused-tier rules and prompt Scope 4 require running `ruff check`, `ruff format --check`, `mypy`, and the full `test_aftercare*` suites in `src/core` and `src/api`, plus verifying tightly coupled suites (`PC-004`, `PC-005`).

#### Intent

Prove complete static and runtime conformance with zero regressions.

#### Boundaries

* Included:
  * Package-level `python3 -m ruff check` and `python3 -m ruff format --check` in `src/core` and `src/api` (honoring `pyproject.toml` `[tool.ruff.format].exclude`).
  * Package-level `python3 -m mypy` in `src/core` and `src/api`.
  * `src/core`: `python3 -m unittest discover -s tests -p 'test_aftercare*.py' -q` and `python3 -m unittest discover -s tests -p 'test_quality_procurement.py' -q`.
  * `src/api`: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p 'test_aftercare*.py' -q` and `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests/test_content_standard.py tests/test_role_endpoint_inventory.py tests/test_role_matrix.py -q`.
  * `src/agents`: `PYTHONPATH=../core/tests python3 -m unittest discover -s tests -p 'test_epic104_bounded_ai_invariants.py' -q`.
* Excluded: Hosted CI triggers or `git push`.

#### Likely Targets

* Read-only verification commands recorded in `.copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md`.

#### Dependencies

* P03-T01.

#### Validation Expectations

* Exit code `0` on every command.

#### Completion Evidence

* Exact command outputs recorded in changes artifact.

#### Unresolved Items

* None.
