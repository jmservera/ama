<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #133 Aftercare Accessible Concern Routes and Neutral-Text Enforcement in src/core

## Metadata

* Task ID: 133-aftercare-concern-2142
* Task slug: 133-aftercare-concern-2142
* Related plan: .copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md (`C1`-`C16`), `docs/prd-zava-north-homes-retrofit-demonstrator.md` (`FR-049`, `AC-063`), `docs/reference/research/ux/content-standard.md`

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Harden Neutral-Text Guard and Accessible Register Contract in aftercare.py | ready | P01, P01-T01, P01-T02 |
| P02 | Add Accessible Household Digital Intake, Support Adjustments, and Template Guards in aftercare_intake.py and aftercare_store.py | ready | P02, P02-T01, P02-T02 |
| P03 | Worktree Test Resolution, Focused AC1/AC5 Tests, Documentation, and Bare Verification | ready | P03, P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Harden Neutral-Text Guard and Accessible Register Contract in aftercare.py

### Context

Research (`C3`-`C7`, `C12`, `C15`) showed that `aftercare.py` already defines `ROUTES`, `NON_DIGITAL_CHANNELS`, `RAISED_BY`, `BANNED_PHRASES`, `PARAPHRASE_PATTERNS`, and partial `SUPPORT_OPTIONS` / `_variants` / `intake_error_summary` helpers, yet still permits clause-masking bypasses after newlines, colons, question/exclamation marks, dashes, and parentheses in `_UNCERTAIN` and `_NEGATED_CLAIM`, misses several causal/blame/savings paraphrases and hyphenated tokens, leaves error/unknown/approval templates outside `assert_templates_neutral`, and does not validate or persist requested `support_needed` adjustments on concerns.

### Intent

Make `aftercare.py` enforce neutrality across every template, dynamic string, and adversarial paraphrase/clause variant, and support optional `support_needed` adjustments and plain-language error summaries across `intake_form`, `intake_errors`, and `AftercareRegister`.

### Boundaries

* Included: `src/core/src/zava_forward/core/aftercare.py`
* Excluded: Filtering verbatim household/representative `statement` or `representative_basis` through `neutral_text`; modifying `src/api`.

### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Neutral-text normalization/regexes, template assertions, accessible support options, `intake_form`, `intake_errors`, `intake_error_summary`, and `AftercareRegister`.

### Dependencies

* None.

### Validation Expectations

* Strict `mypy`, `ruff check`, `ruff format --check`, and `test_aftercare.py` pass with zero errors.

### Completion Evidence

* Updated `aftercare.py` passing import-time `assert_templates_neutral` and unit tests in `P03-T01`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden neutral_text, strip_unsafe_sentences, and template assertions in aftercare.py

#### Context

Contrarian research (`C4`) proved that `_variants` collapsed `\n` to `" "` before `_UNCERTAIN` and `_NEGATED_CLAIM` ran, while `_UNCERTAIN` and `_NEGATED_CLAIM` only terminated at `\s(?:and|but|or)\s|[.;,]|$`. Thus `"Unknown whether draughts changed: the tenant is at fault."`, `"Unknown whether draughts changed! Bills will fall."`, `"Unknown whether draughts changed\nBills will drop."`, and `"No promise of savings — the tenant is at fault."` swallowed the second clause and bypassed `neutral_text`. Additional paraphrases (`because of the tenant/household/occupant/retrofit`, `attributable/attributed to`, `guarantee/promised savings`, `save/pay less on bills`, `blamed/blaming`, `wastes/wasted heat/energy`, `fault/error of the household`) and hyphenated evasions (`mis-use`, `resident-error`) also passed (`C4`), and several fixed strings (`PACK_NOT_REVIEWED`, pack approval labels, `intake_form` title, `intake_errors` messages, `evaluator_view` unknowns, `propose_pack` questions, and `owner` names flowing into pack facts) lacked `assert_templates_neutral` or `neutral_text` (`C5`-`C7`).

#### Intent

Eliminate clause-boundary, separator, and paraphrase bypasses in `neutral_text` and `strip_unsafe_sentences`, and check every template and generated text in `aftercare.py`.

* Boundaries

* Included:
  * Preserve `\n` in `_variants` (`re.sub(r"[\r\n]+", "\n", ...)` and horizontal whitespace collapsed), check `BANNED_PHRASES` against whitespace-collapsed `" ".join(lowered.split())` so soft line-wraps (`"bills will\nfall"`) cannot evade matching, apply `_UNCERTAIN` and `_NEGATED_CLAIM` (substituting `" ; "`) while `\n` is intact, and then check `PARAPHRASE_PATTERNS` against both `folded` and `" ".join(folded.split())`.
  * Terminate `_UNCERTAIN` and `_NEGATED_CLAIM` at `[.!?;,:\n\u2013\u2014()]` as well as `\s(?:and|but|or|while|yet|though|because|so)\s` or `--`, and include a narrow negated-verb disclaimer pattern (`\b(?:(?:do|does|did|can|will)\s+not|cannot|never)\s+(?:show a cause,\s*assign fault\s+or\s+)?(?:claim|promise|guarantee)\s+(?:any\s+)?(?:energy\s+|bill\s+|cost\s+)?savings?\b`) without a trailing wildcard so `AftercareService._comparison` (`"They do not show a cause, assign fault or promise savings."`) continues to pass without masking any second clause (`PC-002`).
  * Include hyphen/underscore-to-space folded variants alongside invisible-character joined and spaced variants, and match `\bmis[-_ ]?us(?:e|ed|es|ing)\b` explicitly so both `"mis-use"` and `"resident-error"` are caught (`PC-002`).
  * Expand `PARAPHRASE_PATTERNS` to cover `because of (?:the |your )?(?:tenant|resident|household|occupant|retrofit|works|insulation|measures|installation|upgrade|heating|ventilation)`, `(?:attributable|attributed) to`, `(?:guarantees?|guaranteeing|promis(?:e|es|ed|ing)) (?:any |you )?(?:savings?|lower|cheaper|reduced)`, `(?:save|pay less) on (?:your |their |the )?(?:energy )?bills?`, `\bblam(?:e|ed|es|ing)\b`, `\bmis[-_ ]?us(?:e|ed|es|ing)\b`, `\bwast(?:e|ed|es|ing) (?:heat|energy|power|money)\b`, and `(?:fault|error|mistake) of (?:the )?(?:tenant|resident|household|occupant)`.
  * Raise a fixed neutral `ValueError("Causation, blame or savings claim is not allowed in generated or templated text.")` in `neutral_text` without echoing the matched banned `{phrase}` so HTTP 400 responses never echo banned wording (`PC-002`).
  * Update `strip_unsafe_sentences` to split on sentence punctuation or line breaks (`(?<=[.!?])\s+|\s*\n+\s*`) so unsafe lines in multi-line text cannot survive attached to an unpunctuated line.
  * Pass all fixed templates in `aftercare.py` (`ACCESSIBLE_ROUTE`, `PROTECTION`, `EVALUATOR_NOTICE`, `PACK_MANUAL_ROUTE`, `PACK_NOT_REVIEWED`, `PACK_APPROVALS`, `SUPPORT_OPTIONS`, `SUPPORT_NOTE`, `FORM_TITLE`, `FORM_INTRO`, `INTAKE_ERROR_MESSAGES`, `EVALUATOR_UNKNOWNS`, `PACK_QUESTIONS`) to `assert_templates_neutral` at import time, and check `owner` and `sensor_context` in `AftercareRegister.raise_concern`, `record_closure`, `attach_sensor_context`, and `from_state` with `neutral_text` (`PC-002`).
* Excluded: Running `neutral_text` on household `statement` or `representative_basis` (`C11`).

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`

#### Dependencies

* None.

#### Validation Expectations

* All existing positive and negative cases in `EvaluatorTests` and `TemplateGuardTests` continue to pass, and new contrarian clause/paraphrase/separator cases are rejected with `ValueError`.

#### Completion Evidence

* `neutral_text`, `strip_unsafe_sentences`, and `assert_templates_neutral` updated in `aftercare.py` and verified by unit tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add accessible support adjustments and plain-language error summary to intake_form, intake_errors, and AftercareRegister

#### Context

`SUPPORT_OPTIONS` (`large_print`, `interpreter`, `call_back`, `support_person`) and `SUPPORT_NOTE` were introduced on `intake_form()` without a corresponding optional field, validation helper, or persistence on `AftercareRegister` (`C5`, `C6`). Downstream `aftercare.js` renders any entry in `form["fields"]` with `options` as a native `<select>` with an empty placeholder option when `required` is `False` (`C15`), and `test_aftercare.py` asserts `set(intake_errors({})) == {"raised_by", "home_ref", "kind", "statement"}` (`C12`).

#### Intent

Allow households, representatives, and recording staff to select zero, one, or multiple `SUPPORT_OPTIONS` (`support_needed`) without needing to explain why, validate selections in plain language, and persist `support_needed` on concern records and snapshots backward-compatibly.

#### Boundaries

* Included:
  * Export `SUPPORT_OPTION_CODES = tuple(code for code, _ in SUPPORT_OPTIONS)` and `normalize_support_needed(value: object) -> list[str]` mapping `None`, blank/whitespace-only strings, and empty non-mapping iterables to `[]`; a single valid `str` code to `[code]`; or an `Iterable` (non-`str`, non-`bytes`, non-`Mapping`) of valid codes deduplicated in order to `list[str]`, raising `ValueError` otherwise (`PC-003`).
  * Include optional field `{"name": "support_needed", "label": "Would any of these help us communicate with you?", "required": False, "options": _labelled(SUPPORT_OPTIONS)}` in `intake_form()["fields"]` (while keeping top-level `support_note` and `support_options` on `intake_form()`).
  * Validate `support_needed` in `intake_errors(values)` by calling `normalize_support_needed(values.get("support_needed"))` directly, returning plain-language guidance `"Choose from the listed support options, or leave this blank."` on `ValueError` so `intake_errors({})` and whitespace/empty inputs stay unchanged (`PC-003`).
  * Keep `intake_error_summary(errors)` returning `""` when empty and a neutral plain-language lead sentence naming the staff-assisted fallback when non-empty.
  * Add optional `support_needed: object = None` to `AftercareRegister.raise_concern(...)`, storing `"support_needed": normalize_support_needed(support_needed)`; in `from_state`, default absent `"support_needed"` on legacy snapshots to `[]` while requiring any present `"support_needed"` to be a canonical deduplicated `list[str]` of `SUPPORT_OPTION_CODES` (`PC-003`).
* Excluded: Mandatory accessibility disclosures or medical-reason fields.

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `intake_errors({})` returns exact keys `{"raised_by", "home_ref", "kind", "statement"}`; valid single and multi-item `support_needed` values normalize cleanly; invalid codes produce a plain `support_needed` field error; `from_state` accepts legacy snapshots without `support_needed` and rejects tampered invalid `support_needed` entries; `aftercare.js` renders `ac-support_needed` with a matching `<label>`.

#### Completion Evidence

* `AftercareRegister` and `intake_form`/`intake_errors` changes verified by `mypy` and unit tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Add Accessible Household Digital Intake, Support Adjustments, and Template Guards in aftercare_intake.py and aftercare_store.py

### Context

`AftercareService` (`aftercare_intake.py`) currently supports only staff-recorded concerns (`route == "staff_recorded"`, gated by `RECORD_ROLES` and `NON_DIGITAL_CHANNELS`, `C8`-`C10`), and several templates and formatted strings in `aftercare_intake.py` and `aftercare_store.py` are not verified by `assert_templates_neutral` or `neutral_text` (`C9`, `C13`).

### Intent

Provide an accessible self-service digital concern route (`household_form`, `submit_household_concern`, `household_receipt`, and `/api/aftercare/household-*`) for households and representatives alongside the staff-assisted non-digital channels, carry `support_needed` end-to-end across receipts and views with 100% snapshot compatibility, and enforce neutrality and plain language across every template and generated message in `aftercare_intake.py` and `aftercare_store.py`.

### Boundaries

* Included: `src/core/src/zava_forward/core/aftercare_intake.py`, `src/core/src/zava_forward/core/aftercare_store.py`
* Excluded: Altering existing `/api/aftercare/form` or `/api/aftercare/concerns` staff-role and non-digital channel rules (`C10`); exposing pack routes (`C10`); filtering household verbatim `statement` or `representative_basis` with `neutral_text` (`C11`).

### Likely Targets

* `src/core/src/zava_forward/core/aftercare_intake.py`
* `src/core/src/zava_forward/core/aftercare_store.py`

### Dependencies

* P01.

### Validation Expectations

* All existing `test_aftercare_intake.py` and `test_aftercare_store.py` suites pass unchanged, and new household/representative digital + non-digital + `support_needed` + neutral-text tests pass.

### Completion Evidence

* Updated `aftercare_intake.py` and `aftercare_store.py` passing strict `mypy`, `ruff`, and contract tests.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Extend AftercareService with household digital route, support_needed persistence, and backward-compatible state validation

#### Context

Research (`C2`, `C8`, `C9`, `C10`) established that `AftercareService.record_concern` must remain staff-gated (`RECORD_ROLES`) and non-digital (`NON_DIGITAL_CHANNELS`), while households and representatives also need an accessible direct digital intake over the same atomic `StateStore` document (`zf-aftercare-intake/1`), plus end-to-end `support_needed` persistence across both routes.

#### Intent

Add household/representative self-service digital intake and receipt readback alongside staff-assisted non-digital intake in `AftercareService`, with `support_needed` preserved on concerns, receipts, and views and zero breaking changes to pre-existing state documents.

#### Boundaries

* Included:
  * Define `DEFAULT_UPDATE_DAYS = 7` for household digital submissions when `next_update` is omitted (so residents do not have to pick an internal staff SLA date, while still validating an explicit `next_update >= today` if supplied).
  * Add `household_form(self) -> Record` returning `intake_form()` enriched with `assisted: False`, `homes`, `synthetic_notice`, `owner_note`, and plain-language `manual_route` pointing to phone, in-person, paper, and assisted-visit channels.
  * Add `submit_household_concern(self, values: Mapping[str, Any]) -> tuple[Record, bool]` accepting `request_id`, `raised_by` (`household` or `representative` with mandatory verbatim `representative_basis`), `home_ref` (checked against `self.homes` allowlist when configured), `kind`, `statement` (checked by length cap and synthetic privacy guard, kept verbatim), optional `support_needed`, and optional `next_update`: hash the caller-supplied `requested_next_update` (`None` when omitted, ISO date string when supplied) and store `"next_update": requested_next_update` inside `receipt["original"]` for digital concerns; inside `work(doc)`, check `doc["requests"].get(request_id)` replay FIRST before computing `today + 7 days` or enforcing `requested_next_update >= self._today()` so retries across UTC midnight or after `next_update` has passed replay identically instead of raising `ConflictError` or `ValidationError` (`PC-001`); refuses `owner_role`; records a `"digital"` concern on `AftercareRegister` with `UNKNOWN_OWNER`, stores durable receipt `RC-AC-nnn` (`route: "digital"`, `channel: None`, `recorded_by: None`, `support_needed`), and logs action `"household_concern_submitted"` with actor `raised_by`.
  * Add `household_receipt(self, cid: str, request_id: str) -> Record` returning a household-safe status and receipt view (matching `cid` AND `receipt["request_id"] == request_id`, raising `PermissionError` if `request_id` is missing/mismatched and `KeyError` if `cid` is unknown) containing receipt details, current `owner`, `investigation`, `outcome`, `remedy`, `next_update`, `unresolved`, `support_needed`, `protection`, `accessible_route`, and `synthetic_notice`, and omitting `sensor_context` and staff audit history.
  * Wire `GET /api/aftercare/household-form`, `POST /api/aftercare/household-concerns`, and `GET /api/aftercare/household-concerns/<cid>` (reading `query.get("request_id")`) in `AftercareService._route` (updating `known` top-level segments for 404/405 mapping without touching `/api/aftercare/form`, `/api/aftercare/concerns`, or pack 404 behavior).
  * Carry normalized `support_needed` in `record_concern`, `submit_household_concern`, `_receipt`, and `_display` using `.get("channel")`, `.get("recorded_by")`, and `.get("support_needed", [])` so omitted keys on `digital` concerns and legacy receipts never raise `KeyError` (`PC-003`).
  * Maintain 100% fingerprint compatibility in `_fingerprint` / `_receipt_fingerprint`: when `route == "staff_recorded"` and `support_needed == []`, hash the exact legacy 7-item list `[raised_by, basis, home, kind, statement, channel, next_update]`; when `route == "digital"` or `support_needed` is non-empty, hash `[route, raised_by, basis, home, kind, statement, channel, requested_next_update, support_needed]` where `_receipt_fingerprint` reads `receipt["original"].get("next_update", receipt["next_update"])` (`PC-001`).
  * Generalize `_validate(doc)` to accept both `"staff_recorded"` concerns (requiring `rec.get("channel") in NON_DIGITAL_CHANNELS` and matching `recorded_by` dict) and `"digital"` concerns (requiring `"channel" not in rec`, `"recorded_by" not in rec`, `receipt.get("channel") is None`, and `receipt.get("recorded_by") is None`), while cross-checking `rec.get("support_needed", []) == receipt.get("support_needed", [])` (`PC-003`).
* Excluded: Pack proposal/review routes; unauthenticated listing of all concerns.

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare_intake.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Existing staff role, replay-after-date, blank-state, corrupt-state, and route status tests pass 100%; new household/representative digital and assisted `support_needed` submissions, replays, conflicts, and bounded `household_receipt` readbacks pass.

#### Completion Evidence

* `AftercareService` digital + non-digital routes and state validation verified by `test_aftercare_intake.py` and `test_aftercare_store.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Guard all fixed templates and generated strings in aftercare_intake.py and aftercare_store.py

#### Context

Research (`C9`, `C13`, `C15`) identified fixed error/status templates and dynamic string builders in `aftercare_intake.py` (`UNKNOWN_OWNER`, `OWNER_SUFFIX`, `COHORT_LABEL`, `_PRIVACY_LABELS`, comparison unknown reason, validation/permission/conflict/persistence/state-invalid messages, `owner_label`, `_flagged`) and `aftercare_store.py` (`UNCONFIRMED`, conflict message, persistence message) that were not asserted with `assert_templates_neutral` or `neutral_text`.

#### Intent

Ensure every fixed template and dynamically generated system message in `aftercare_intake.py` and `aftercare_store.py` is checked by `assert_templates_neutral` at import time and `neutral_text` at runtime, using plain everyday English with zero banned jargon (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).

#### Boundaries

* Included:
  * Check wording of any new or updated message against `JARGON` (`gates?`, `holds?`, `provenance`, `traces?`, `snapshots?`, `envelopes?` — note: avoid words like "holds" in any new message, and verify existing templates pass `neutral_text`).
  * Register all module-level notice, label, unknown, comparison-reason, and error-message constants in `aftercare_intake.py` and `aftercare_store.py` with `assert_templates_neutral(...)`.
  * Pass dynamically formatted strings (`owner_label`, `_flagged`, `_free_text` / `_context_errors` / `_staff` messages, `_receipt` `what_happens_next`, `ValidationError` message) through `neutral_text(...)`.
* Excluded: Modifying exact substrings asserted by existing error tests (`"Nothing was saved"`, `"left unchanged"`, `"may or may not"` in JS, `"No owner is named"`, `"named owner"`).

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare_intake.py`
* `src/core/src/zava_forward/core/aftercare_store.py`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* Import-time `assert_templates_neutral` succeeds across all three modules, and exhaustive payload/error scanning in tests confirms zero causation, blame, or savings wording.

#### Completion Evidence

* Updated template assertions and runtime `neutral_text` wrappers verified by tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Worktree Test Resolution, Focused AC1/AC5 Tests, Documentation, and Bare Verification

### Context

Research (`C14`) found that bare `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` in `src/core` imports stale `/home/azureuser/source/ama/src/core/src` via `~/.local` `.pth` unless the aftercare tests prepend their sibling `../src` directory. In addition, `src/core/README.md` (`C16`) needs a concise update describing the accessible household/staff routes, support adjustments, and tightened neutral-text guard while preserving honest "Not delivered" boundaries for external gates.

### Intent

Guarantee deterministic worktree-local imports under bare `unittest discover`, add focused AC1/AC5 tests within the locked 14-test budget, update `src/core/README.md`, and run complete Focused-tier verification.

### Boundaries

* Included: `src/core/tests/aftercare_fixture.py`, `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/core/tests/test_aftercare_store.py`, `src/core/README.md`
* Excluded: Touching `~/.local` site-packages or unrelated test modules.

### Likely Targets

* `src/core/tests/aftercare_fixture.py`
* `src/core/tests/test_aftercare.py`
* `src/core/tests/test_aftercare_intake.py`
* `src/core/tests/test_aftercare_store.py`
* `src/core/README.md`

### Dependencies

* P01, P02.

### Validation Expectations

* Exact command `cd /home/azureuser/source/ama-demo-wt/feat-133-aftercare-concern-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` exits `0`, plus `test_dependency_rule.py` and `src/api/tests/test_aftercare_screen.py` pass.

### Completion Evidence

* Clean verification output recorded in `.copilot-tracking/changes/2026-11-14/133-aftercare-concern-2142-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add worktree-local src resolver and focused AC1/AC5 unit and contract tests

#### Context

Because `zava_forward` is a PEP 420 namespace package (`C14`), prepending `Path(__file__).resolve().parents[1] / "src"` to `sys.path` (and ensuring `zava_forward.__path__` / `zava_forward.core.__path__` prioritize the worktree's `src` if already imported) in a small `aftercare_fixture.py` module imported first in `test_aftercare.py`, `test_aftercare_intake.py`, and `test_aftercare_store.py` ensures bare `unittest discover` always exercises the active worktree without `# noqa: E402` or `~/.local` mutations.

#### Intent

Add `aftercare_fixture.py` and focused tests (at most 14 new test methods, 0 removals) covering every new AC1 and AC5 behavior and edge case.

#### Boundaries

* Included:
  * `src/core/tests/aftercare_fixture.py`: defines `ensure_worktree_src() -> Path` (called on module import and exported alongside `CORE_SRC`) which prepends sibling `src` to `sys.path`, prioritizes sibling `src/zava_forward` and `src/zava_forward/core` in any loaded namespace `__path__`, and evicts any preloaded `zava_forward.core*` entry in `sys.modules` whose `__file__` is outside `CORE_SRC`; all three `test_aftercare*.py` files import and reference `CORE_SRC` cleanly under `ruff` `F401`/`I001` (`PC-004`).
  * `src/core/tests/test_aftercare.py`: tests for (1) `support_options`, `support_note`, `support_needed` validation/persistence/snapshot round-trip + legacy snapshot compatibility + `intake_error_summary`, (2) invisible-character, full-width, soft-wrap newline, and hyphenated (`mis-use`, `resident-error`) evasions in `neutral_text` plus non-echoing `ValueError`, (3) multiline, colon, exclamation, question, and dash second-clause bypasses after `_UNCERTAIN` / `_NEGATED_CLAIM` plus newly covered causal/blame/savings paraphrases, negated-verb `"do not ... promise savings"` compatibility, and newline splitting in `strip_unsafe_sentences`, and (4) `owner` and `from_state` neutrality guard + all `aftercare.py` generated/error/unknown/pack strings passing `neutral_text`.
  * `src/core/tests/test_aftercare_intake.py`: tests for (5) household and representative self-service accessible digital route (`household_form`, `submit_household_concern`, cross-day omitted-`next_update` idempotent replay (`PC-001`), conflict, and `/api/aftercare/household-*` routes), (6) `household_receipt` readback requiring matching `request_id` and omitting staff `sensor_context`, (7) `support_needed` preserved across both `record_concern` (non-digital channels) and `submit_household_concern` (digital) plus legacy `zf-aftercare-intake/1` fingerprint compatibility, (8) verbatim household `statement` and `representative_basis` allowed to mention bills/savings promises without being blocked while all generated/templated/error payloads pass `neutral_text`.
  * `src/core/tests/test_aftercare_store.py`: test for (9) `UNCONFIRMED`, conflict, and persistence messages passing `neutral_text` and worktree `CORE_SRC` provenance check.
* Excluded: Trivial constant/getter assertions; exceeding 14 added test methods.

#### Likely Targets

* `src/core/tests/aftercare_fixture.py`
* `src/core/tests/test_aftercare.py`
* `src/core/tests/test_aftercare_intake.py`
* `src/core/tests/test_aftercare_store.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* All new tests fail against unpatched code and pass with the P01-P02 implementation under bare `unittest discover`.

#### Completion Evidence

* Passing test run output with exact test counts and 0 failures.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Update src/core/README.md and run bare verification plus compatibility checks

#### Context

`src/core/README.md` documents the aftercare modules and their explicit evidence boundaries (`C16`).

#### Intent

Update the `#133` section of `src/core/README.md` to reflect `support_needed` adjustments, `intake_error_summary`, `AftercareService` household digital + staff non-digital routes, and comprehensive neutral-text template/generated-string enforcement while keeping external human/WCAG, named-owner, evaluator-role, DPO, and pack-screen gates clearly distinguished, then run full Focused-tier verification.

#### Boundaries

* Included: `src/core/README.md` and verification runs.
* Excluded: Unrelated README sections; overclaiming human/operational criteria.

#### Likely Targets

* `src/core/README.md`

#### Dependencies

* P03-T01.

#### Validation Expectations

* Bare verification command in `src/core` exits `0`; `test_dependency_rule.py` exits `0`; `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_aftercare_screen.py` from `src/api` exits `0`.

#### Completion Evidence

* Command exit codes and outputs recorded in `.copilot-tracking/changes/2026-11-14/133-aftercare-concern-2142-changes.md`.

#### Unresolved Items

* None.
