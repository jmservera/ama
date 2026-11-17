<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #133 Aftercare Concern Route and Lived-Performance Review

## Metadata

* Task ID: aftercare-133-2346
* Task slug: aftercare-133-2346
* Related plan: .copilot-tracking/plans/2026-11-14/aftercare-133-2346-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/aftercare-133-2346-research.md, .copilot-tracking/reviews/logs/2026-11-14/133-aftercare-concern-2142-review.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/reference/research/ux/customer-journeys/programme.md

## Phase Index

| Phase ID | Name                                                                     | Status | Detail sections        |
|----------|--------------------------------------------------------------------------|--------|------------------------|
| P01      | Intake Channel Parity, Receipt Isolation, and Fixture Safety             | Ready  | P01, P01-T01, P01-T02  |
| P02      | Deterministic Causation, Resident-Blame, and Savings-Promise Guard       | Ready  | P02, P02-T01, P02-T02  |
| P03      | Evaluator Unknown Preservation, FR-036 Pack Governance, and Accessible Web UI | Ready  | P03, P03-T01, P03-T02  |
| P04      | Focused Core and API Tests, Documentation Sync, and Verification         | Ready  | P04, P04-T01, P04-T02  |

<!-- rpi:phase id=P01 -->
## P01: Intake Channel Parity, Receipt Isolation, and Fixture Safety

### Context

`src/core/tests/aftercare_fixture.py` currently pops `zava_forward.core*` modules from `sys.modules` when tests execute against the shared Python environment, risking split class identity across `unittest discover` (`C1`, `C2`). Meanwhile, `aftercare.py` defines `NON_DIGITAL_CHANNELS = ("phone", "in_person", "paper", "assisted_visit")` without `"representative"`, `normalize_support_needed` rejects legacy `"call_back"` instead of normalizing to `"callback_window"` (`C3`, `C4`), and `AftercareService.household_receipt` (`aftercare_intake.py`) permits reading `staff_recorded` concern receipts on the household endpoint if the `request_id` is supplied (`C5`).

### Intent

Ensure worktree-first module resolution without `sys.modules` eviction, complete non-digital channel and support-option parity, and enforce strict digital-route isolation on `household_receipt`.

### Boundaries

* Included: `src/core/tests/aftercare_fixture.py`, `src/core/src/zava_forward/core/aftercare.py` (`NON_DIGITAL_CHANNELS`, `intake_form`, `normalize_support_needed`), and `src/core/src/zava_forward/core/aftercare_intake.py` (`CHANNEL_LABELS`, `household_receipt`).
* Excluded: Staff server authentication middleware in `src/api/src/zava_forward/api/server.py` (`C14`, `C15`).

### Likely Targets

* `src/core/tests/aftercare_fixture.py`: Remove `sys.modules.pop` loop; prepend `str(CORE_SRC)` to `sys.path` and prepend `str(CORE_SRC / "zava_forward")` and `str(CORE_SRC / "zava_forward" / "core")` to in-memory package `__path__` lists when already imported.
* `src/core/src/zava_forward/core/aftercare.py`: Add `"representative"` to `NON_DIGITAL_CHANNELS` and its neutral label `"Through a representative"` in `intake_form`; normalize `"call_back"` -> `"callback_window"` in `normalize_support_needed` before validating against `SUPPORT_OPTIONS`.
* `src/core/src/zava_forward/core/aftercare_intake.py`: Add `"representative": "Through a representative"` to `CHANNEL_LABELS`; require `rec.get("route") == "digital"` in `household_receipt`, raising the existing uniform `PermissionError` otherwise.

### Dependencies

* None.

### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_aftercare*.py" -q` in `src/core` runs cleanly with zero `sys.modules` removals.

### Completion Evidence

* Updated `aftercare_fixture.py`, `aftercare.py`, and `aftercare_intake.py` passing `mypy` and `ruff`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Remove bulk `sys.modules` eviction from `src/core/tests/aftercare_fixture.py`

#### Context

Research `C1` found a `for name in list(sys.modules): sys.modules.pop(name, None)` loop in `src/core/tests/aftercare_fixture.py`. If an earlier test file imports `ValidationError` or `AftercareRegister` before `aftercare_fixture` runs without worktree `PYTHONPATH`, evicting `zava_forward.core*` creates duplicate class objects across test modules.

#### Intent

Configure `sys.path` and package `__path__` in-place without deleting or popping any entry from `sys.modules`.

#### Boundaries

* Included: `src/core/tests/aftercare_fixture.py`.
* Excluded: Global editable `.pth` files outside the worktree.

#### Likely Targets

* `src/core/tests/aftercare_fixture.py`: Keep `sys.path.insert(0, str(CORE_SRC))` and in-place `__path__` prepending on `sys.modules.get("zava_forward")` and `sys.modules.get("zava_forward.core")` if present.

#### Dependencies

* None.

#### Validation Expectations

* Inspect `aftercare_fixture.py` and run `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` in `src/core`.

#### Completion Evidence

* Zero `sys.modules.pop` or `del sys.modules` statements in `src/core/tests/`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `"representative"` non-digital channel, `"call_back"` support alias, and digital-only `household_receipt` check

#### Context

Issue #133 and the caller brief name `phone`, `paper`, `in_person`, `representative`, etc. as staff-recorded non-digital channels (`C3`, `C4`). Prior review `RV-002` and `RV-003` also identified legacy `"call_back"` support values and `staff_recorded` concern exposure on `household_receipt` (`C5`).

#### Intent

Support `"representative"` as a first-class staff-recorded non-digital channel, normalize `"call_back"` -> `"callback_window"`, and restrict `household_receipt` strictly to `route == "digital"`.

#### Boundaries

* Included: `aftercare.py` (`NON_DIGITAL_CHANNELS`, `intake_form`, `normalize_support_needed`) and `aftercare_intake.py` (`CHANNEL_LABELS`, `household_receipt`).
* Excluded: Changing existing channel codes (`phone`, `in_person`, `paper`, `assisted_visit`).

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Extend `NON_DIGITAL_CHANNELS` to `("phone", "in_person", "paper", "assisted_visit", "representative")`, include `"representative"` in `ACCESSIBLE_ROUTE` and `raise_concern` invalid-channel `ValueError`, add `"representative": "Through a representative"` to `intake_form` `channel_labels`, set `"multiple": True` on the `support_needed` field spec in `intake_form()`, and map `"call_back"` to `"callback_window"` inside `normalize_support_needed`.
* `src/core/src/zava_forward/core/aftercare_intake.py`: Add `"representative": "Through a representative"` to `CHANNEL_LABELS`; in `household_receipt`, check `rec is None or rec.get("route") != "digital" or not req or rec.get("request_id") != req` before returning receipt data.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Existing dynamic channel loops in `test_aftercare.py` pass for all five non-digital channels, `"call_back"` normalizes cleanly, and `GET /api/aftercare/household-concerns/<staff_cid>` returns `403` even with matching `X-Aftercare-Request-Id`.

#### Completion Evidence

* Unit tests in `test_aftercare.py` and `test_aftercare_intake.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Deterministic Causation, Resident-Blame, and Savings-Promise Guard

### Context

Research `C6`, `C7`, `C8`, and `C9` identified three concrete gaps in the deterministic neutral-language guard:
1. `strip_unsafe_sentences` splits on `\s*\n+\s*` and joins kept fragments with `" "`, letting `"Bills will\nfall."` pass per-fragment checks and recombine into `"Bills will fall."` (`C6`).
2. `PARAPHRASE_PATTERNS` misses common resident-blame phrasings around occupant lifestyle/habits, thermostat/heating-control settings, ventilation/window/trickle-vent/drying-clothes habits, `"user error"`, finite causal verbs (`"stems from"`, `"arises from"`, `"results from"`, `"is responsible for"`), and broader bill-reduction promises (`"guaranteed bill reduction"`, `"slash your bills"`) (`C7`).
3. Staff-authored `evidence` in `record_outcome`, `set_remedy`, `review_pack` (`reason`), and `from_state` bypass `neutral_text` (`C8`, `C9`).

### Intent

Make the deterministic neutral-language guard comprehensive across single-line and multiline generated, templated, evaluator, pack, and staff-authored outcome/remedy/review outputs while preserving verbatim household statements and avoiding false positives on neutral uncertainty or negations.

### Boundaries

* Included: `src/core/src/zava_forward/core/aftercare.py` (`PARAPHRASE_PATTERNS`, `strip_unsafe_sentences`, `record_outcome`, `set_remedy`, `review_pack`, `from_state`) and `src/core/src/zava_forward/core/aftercare_intake.py` (`record_outcome`, `set_remedy`).
* Excluded: Household `statement` and `representative_basis` fields (which must remain verbatim) and `#87` `src/core/src/zava_forward/core/quality.py:add_aftercare` (`C16`).

### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Update `PARAPHRASE_PATTERNS`, `strip_unsafe_sentences`, `AftercareRegister.record_outcome`, `AftercareRegister.set_remedy`, `AftercareRegister.review_pack`, and `AftercareRegister.from_state`.
* `src/core/src/zava_forward/core/aftercare_intake.py`: Catch or pre-validate `neutral_text` on `evidence` in `AftercareService.record_outcome` and `AftercareService.set_remedy` so violations return field-scoped `ValidationError({"evidence": ...})` (`HTTP 422`).

### Dependencies

* P01.

### Validation Expectations

* Positive neutral corpus (plain factual investigation notes, `"Not sure how to use the controls"`, `"Concern kind: control_use."`, `"Cannot determine whether thermostat settings contributed"`, `"We do not guarantee or promise savings."`) passes `neutral_text`; negative corpus (causation claims, occupant behaviour/thermostat/ventilation/lifestyle blame, multiline `"Bills will\nfall."`, bill-reduction guarantees) fails `neutral_text` and is stripped cleanly by `strip_unsafe_sentences`.

### Completion Evidence

* Updated `aftercare.py` and `aftercare_intake.py` verified by `mypy`, `ruff`, and `test_aftercare*.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Harden `strip_unsafe_sentences` and expand `PARAPHRASE_PATTERNS` in `aftercare.py`

#### Context

`strip_unsafe_sentences` splits on newlines before checking `neutral_text`, allowing intra-sentence line wraps to split a banned phrase across two fragments that later rejoin (`C6`). Meanwhile, `PARAPHRASE_PATTERNS` needs explicit coverage for occupant behaviour/lifestyle/habits, thermostat/heating-control blame, ventilation/window/drying-clothes blame, `"user error"`, finite causal verbs, and bill-reduction promises (`C7`).

#### Intent

Prevent multiline recombination bypasses in `strip_unsafe_sentences` and expand `PARAPHRASE_PATTERNS` cleanly without breaking neutral statements, negations, or explicit-uncertainty clauses.

#### Boundaries

* Included: `PARAPHRASE_PATTERNS` and `strip_unsafe_sentences` in `src/core/src/zava_forward/core/aftercare.py`.
* Excluded: LLM or non-deterministic classifiers.

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`:
  * In `strip_unsafe_sentences`: normalize whitespace/intra-sentence newlines into single spaces before splitting on sentence-ending punctuation `(?<=[.!?])\s+` (or split on paragraph breaks `\n\s*\n` + sentence punctuation while folding single newlines), filter each candidate with `neutral_text`, and verify `neutral_text` as sentences are accumulated into `kept` so joining two sentences can never form a banned span.
  * In `PARAPHRASE_PATTERNS`: add targeted compiled regexes for:
    * finite & participial causal verbs: `\b(?:stems|stemmed|stemming|arises|arose|arising|results|resulted|resulting)\s+from\s+(?:[\w'-]+\s+){0,4}(?:{_RETROFIT}|{_HOUSEHOLD}(?:s'|'s|s)?|thermostat|heating\s+controls?|controls?|ventilation|windows?|trickle\s+vents?|lifestyle|habits?|behaviour|behavior)\b` and general finite causal claim `\b(?:stems|stemmed|arises|arose|results|resulted)\s+from\b`, plus scoped `responsible for` matching either causal/fault subjects `(?:{_RETROFIT}|{_HOUSEHOLD}(?:s'|'s|s)?|thermostat|heating\s+controls?|ventilation|windows?|trickle\s+vents?|lifestyle|habits?|behaviour|behavior)\s+(?:is|are|was|were)\s+responsible\s+for\b` or adverse-outcome objects `\b(?:is|are|was|were)\s+responsible\s+for\s+(?:[\w'-]+\s+){0,3}(?:damp|mould|mold|condensation|chill|cold|discomfort|higher\s+bills?|heat\s+loss)\b` (keeping neutral ownership notes like `"named owner is responsible for arranging the home visit"` valid)
    * occupant/resident lifestyle, habits, or user error blame (with singular `'s` and plural `s'`): `\b(?:resident|occupant|tenant|household|user)(?:s'|'s|s)?\s+(?:error|mistake|misuse|neglect|lifestyle|habits?|behaviour|behavior)\b`, `\bpoor\s+(?:ventilation|heating|thermostat|control)\s+(?:habits?|use|practice)\b`
    * thermostat/heating-control & ventilation blame (past, present, and gerund): `\b(?:blam\w+\s+(?:on\s+)?|(?:due|owing|down)\s+to\s+)(?:[\w'-]+\s+){0,4}(?:thermostat|heating\s+controls?|ventilation|windows?|trickle\s+vents?|occupant|resident|tenant|household|lifestyle|habits?|behaviour|behavior)\b`, `\b(?:incorrect|wrong|improper|poor)\s+(?:use\s+of\s+(?:the\s+)?)?(?:thermostat|heating\s+controls?|ventilation|trickle\s+vents?)\b`, `\b(?:resident|occupant|tenant|household)(?:s'|'s|s)?\s+(?:turns?|turned|turning|sets?|setting|keeps?|kept|keeping|leaves?|left|leaving)\s+(?:the\s+)?(?:thermostat|heating|controls?|windows?|trickle\s+vents?)\b`, `\b(?:leaving|keeping|left|kept)\s+(?:the\s+)?(?:windows?|trickle\s+vents?)\s+(?:closed|shut)\b`, `\b(?:turning|turned)\s+(?:the\s+)?(?:thermostat|heating)\s+(?:down|off)\b`, `\bnot\s+ventilating\s+properly\b`, `\bdrying\s+(?:wet\s+)?(?:clothes|laundry)\s+indoors\b`
    * bill-savings / reduction promises: `\b(?:promis\w+|guarante\w+|assur\w+)\s+(?:[\w'-]+\s+){0,4}(?:lower|cheaper|reduced)\s+(?:energy\s+|heating\s+)?bills?\b`, `\b(?:guaranteed|promised|assured)\s+(?:[\w'-]+\s+){0,2}(?:bill\s+(?:reduction|cut|drop)|lower\s+bills?)\b`, `\bslash(?:es|ing)?\s+(?:your\s+|energy\s+|heating\s+|household\s+)?bills?\b`

#### Dependencies

* P01-T02.

#### Validation Expectations

* Verify zero false positives on all existing fixtures (`aftercare_store.py`, `test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_screen.py`) and deterministic rejection on all new causation/blame/promise cases.

#### Completion Evidence

* Unit tests covering multiline stripping and every blame/causation/savings category.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Enforce `neutral_text` on staff outcome, remedy, pack-review, and restored evidence fields

#### Context

Staff-recorded investigation outcome `evidence`, remedy `evidence`, pack-review `reason`, and persisted state restores currently bypass `neutral_text` (`C8`, `C9`). Those fields appear in `closure_status()`, concern detail views, and evaluator outputs.

#### Intent

Enforce `neutral_text` on staff-authored `record_outcome`, `set_remedy` (when `evidence` is non-empty), `review_pack` (`reason` when non-empty), and `from_state` (`outcome["evidence"]`, non-empty `remedy["evidence"]`, and stored `packs` fields), and map HTTP service errors to field-level `ValidationError`.

#### Boundaries

* Included: `AftercareRegister.record_outcome`, `set_remedy`, `review_pack`, `from_state` in `aftercare.py`, and `AftercareService.record_outcome`, `set_remedy` in `aftercare_intake.py`.
* Excluded: Household `statement` and `representative_basis` (never filtered by `neutral_text`).

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Call `neutral_text(ev)` in `record_outcome`; if `ev` is non-empty in `set_remedy`, call `neutral_text(ev)`; if `reason.strip()` is non-empty in `review_pack`, call `neutral_text(reason)`; in `from_state`, check `_present(out.get("evidence"))` then call `neutral_text(str(out["evidence"]))`, check non-empty `rem.get("evidence")` with `neutral_text`, and validate stored pack fields (`ai_summary` when non-null, items in `recorded_facts` and `questions_for_investigator`, `approval`, `manual_route`, `notice`, and `review["reason"]` when `review` is a dict, explicitly exempting verbatim `household_statement`).
* `src/core/src/zava_forward/core/aftercare_intake.py`: Validate `neutral_text(evidence)` in `AftercareService.record_outcome` and (when `evidence` is non-empty) in `AftercareService.set_remedy`, raising `ValidationError({"evidence": ...})` (`HTTP 400`).

#### Dependencies

* P02-T01.

#### Validation Expectations

* Posting resident-blame or savings-promise text to `/api/aftercare/concerns/<id>/outcome` or `/remedy` returns `HTTP 400` with an `"evidence"` field error, while raising a household concern with `"My bills went up and staff blamed how I use the thermostat"` succeeds and preserves the resident's exact words.

#### Completion Evidence

* Unit tests in `test_aftercare.py` and `test_aftercare_intake.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Evaluator Unknown Preservation, FR-036 Pack Governance, and Accessible Web UI

### Context

Research `C10`, `C11`, `C12`, and `C13` identified UI and evaluator contract gaps:
1. `AftercareRegister.propose_pack` and `AftercareService.evaluator_view` do not include explicit `FR-036` `ai_registry` metadata (`CONCERN_PACK_TASK = "aftercare-concern-pack"`) confirming that optional AI concern packs are unapproved, human-reviewed proposals with `live_authorized: False` (`C12`, `C13`).
2. `src/api/src/zava_forward/api/web/aftercare.js` lacks channel labels (`phone`, `in_person`, `paper`, `assisted_visit`, `representative`, plus digital online self-service), ignores `spec.multiple` on `support_needed`, renders `<p>Unknown</p>` when `owner_note` is absent on `household_form()`, and coerces missing/null/`"unknown"` `row.concerns` via `(row.concerns || []).length` to `"0"` and `"No concerns raised"` in `aftercareEvaluatorView` (`C10`, `C11`).

### Intent

Bind `FR-036` AI registry governance metadata into `propose_pack` and `evaluator_view`, and update `web/aftercare.js` (after loading `web-design-guidelines`) so channel/route/support labels, multi-select `support_needed`, digital/staff forms, `unknown` non-coercion, and the `FR-036` human-review boundary render cleanly and accessibly.

### Boundaries

* Included: `src/core/src/zava_forward/core/aftercare.py` (`propose_pack`), `src/core/src/zava_forward/core/aftercare_intake.py` (`evaluator_view`), and `src/api/src/zava_forward/api/web/aftercare.js`.
* Excluded: Adding live HTTP endpoints to create or approve AI concern packs (`test_aftercare_intake.py:592-600` requires `404`/`405`), or altering visual styling outside `aftercare.js`.

### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Import `CONCERN_PACK_TASK` and `default_registry` from `zava_forward.core.ai_registry` and attach `task_id`, `ai_task_kind`, `approval_state`, `live_authorized`, `requires_human_review: True`, and `manual_route` on `propose_pack` records.
* `src/core/src/zava_forward/core/aftercare_intake.py`: Include `concern_pack_task` dictionary in `AftercareService.evaluator_view()` built from `default_registry().get(CONCERN_PACK_TASK)` (`task_id`, `requirement: "FR-036"`, `kind`, `state`, `approval_state`, `live_authorized: False`, `requires_human_review: True`, `manual_route`, `plain_reason`).
* `src/api/src/zava_forward/api/web/aftercare.js`: Add `AC_CHANNEL_LABELS` and `AC_SUPPORT_LABELS`, update `acField` and `acReadValues` for `spec.multiple` while preserving `id="ac-support_needed"` and `label[for="ac-support_needed"]`, guard optional `owner_note`/`support_note` in `aftercareFormView`, support `opts.household` in `aftercareSubmit`, display recorded `support_needed` in receipt/concern views, preserve `"Unknown"` for non-array/null/`"unknown"` `row.concerns` and `homes_with_usable_comparison` in `aftercareEvaluatorView`, guard nested `cmp.baseline`/`cmp.late`, and render the `FR-036` proposal-only human-review notice when `view.concern_pack_task` is present.

### Dependencies

* P01, P02, and loading `web-design-guidelines` skill before editing `web/aftercare.js`.

### Validation Expectations

* `src/api/tests/test_aftercare_screen.py` and `src/api/tests/test_aftercare_served.py` pass, including label association, `autocomplete="off"`, `spellcheck="false"`, `aria-live`, `unknown` non-coercion, multi-select `support_needed`, and `FR-036` notice assertions; changed web file reviewed against `web-design-guidelines`.

### Completion Evidence

* Passing `core` and `api` tests plus `web-design-guidelines` review recorded in changes artifact.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Attach `FR-036` `ai_registry` proposal-only governance metadata in `aftercare.py` and `aftercare_intake.py`

#### Context

Issue #133 Objective 3 requires verifying that any optional AI concern pack stays a registered proposal requiring human review (`FR-036`). `ai_registry.py` already defines `CONCERN_PACK_TASK = "aftercare-concern-pack"` (`kind="proposal-pack"`, `state="disabled"`, `approval_state="unapproved"`, `authorizes_live=False`), and wiring that registry entry directly into `propose_pack` and `evaluator_view` links the runtime payloads to `FR-036` deterministically (`C12`, `C13`).

#### Intent

Include explicit `FR-036` registry fields on `propose_pack` dicts and `AftercareService.evaluator_view()` responses while keeping HTTP pack endpoints disabled (`404`/`405`).

#### Boundaries

* Included: `AftercareRegister.propose_pack` (`aftercare.py`) and `AftercareService.evaluator_view` (`aftercare_intake.py`).
* Excluded: Changing `ai_registry.py` task state (`enabled` remains `False`, `approval_state` remains `"unapproved"`).

#### Likely Targets

* `src/core/src/zava_forward/core/aftercare.py`: Import `ai_registry` (`CONCERN_PACK_TASK`), bind `_registry_get = cast(Callable[[str], dict[str, Any]], ai_registry.get)` and `_authorizes_live = cast(Callable[[str], bool], ai_registry.authorizes_live)` for strict `mypy`, and record `task_id`, `requirement: "FR-036"`, `kind`, `state`, `approval_state`, `live_authorized: _authorizes_live(CONCERN_PACK_TASK)` (`False`), `requires_human_review: True`, and `manual_route` on `propose_pack`.
* `src/core/src/zava_forward/core/aftercare_intake.py`: Add `"concern_pack_task"` to `AftercareService.evaluator_view()` (`GET /api/aftercare/evaluator`) built from `_registry_get(CONCERN_PACK_TASK)` (`task_id`, `requirement: "FR-036"`, `kind`, `state`, `approval_state`, `live_authorized: False`, `requires_human_review: True`, `manual_route`, `purpose`, `influence`) with all text strings checked through `neutral_text`.

#### Dependencies

* P02-T02.

#### Validation Expectations

* `propose_pack` and `GET /api/aftercare/evaluator` include `FR-036` governance fields with `live_authorized is False` and `requires_human_review is True`, and `neutral_text` passes on every string in `concern_pack_task`.

#### Completion Evidence

* Unit tests in `test_aftercare.py` and `test_aftercare_intake.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Update `src/api/src/zava_forward/api/web/aftercare.js` for channel/support labels, multi-select, `unknown` non-coercion, and `FR-036` notice

#### Context

In `web/aftercare.js` (`C10`, `C11`):
* `AFTERCARE_LABELS.representative` is `"A person acting for the household"` (appropriate for `raised_by`), which collides if reused for `channel === "representative"` (`"Through a representative"`), while `phone`, `in_person`, `paper`, `assisted_visit`, and digital self-service have no channel labels at all.
* `acField` renders `<select>` without `multiple` even when `spec.multiple === true` (`support_needed`), and `acReadValues` reads only scalar `el.value`.
* `aftercareFormView` unconditionally renders `<p>${acEsc(acText(form.owner_note))}</p>`, producing `<p>Unknown</p>` for `household_form()`.
* `aftercareEvaluatorView` uses `const concerns = row.concerns || [];`, turning `"unknown"` (a 7-character string!) or `null`/`undefined` into `"7"` or `"0"` / `"No concerns raised"`, violating the non-coercion invariant.

#### Intent

Render accurate plain-language labels, multi-select `support_needed`, clean digital/staff forms, strict `"Unknown"` preservation in `aftercareEvaluatorView`, and a neutral `FR-036` proposal-only notice.

#### Boundaries

* Included: `src/api/src/zava_forward/api/web/aftercare.js`.
* Excluded: Framework swaps, global stylesheet overhauls, or breaking `test_aftercare_screen.py` label/input ID invariants (`id="ac-support_needed"`).

#### Likely Targets

* `src/api/src/zava_forward/api/web/aftercare.js`:
  * Add `AC_CHANNEL_LABELS` (`digital: "Online self-service"`, `phone: "By phone"`, `in_person: "In person"`, `paper: "On paper or by post"`, `assisted_visit: "During a home visit"`, `representative: "Through a representative"`) and `AC_SUPPORT_LABELS` matching exact `SUPPORT_OPTIONS` (`large_print`, `easy_read`, `interpreter`, `bsl`, `callback_window`, `paper_letter`, `support_person`), plus helpers `acChannelLabel(route, channel)` and `acSupportList(items)`. Ensure all strings and comments pass `neutral_text` and `test_content_standard.py` lexical checks.
  * In `acField`: when `spec.multiple` is true on a `select` field, add `multiple` attribute, omit the blank `"Choose one..."` option, and preserve array selections via `Array.isArray(value) ? value.includes(o.value) : o.value === value` while keeping `id="ac-${spec.name}"`, `autocomplete="off"`, `spellcheck="false"`, and `aria-describedby`. Update `acReadValues` to return `Array.from(el.selectedOptions || [], (o) => o.value).filter(Boolean)` when `el.multiple` is true.
  * In `aftercareFormView`: guard optional `owner_note`, `support_note`, `next_update_note`, `synthetic_notice`, and `manual_route` via `h(...)` so bare `intake_form()` never renders `"Unknown"`. In `aftercareSubmit`, select the POST subpath dynamically (`const target = opts && opts.household ? "household-concerns" : "concerns"; await api(\`${AFTERCARE_API}/\${target}\`, body, signal);`) so `test_list_export_inventory.py` sees no spurious list path.
  * In `aftercareReceiptView` and `aftercareConcernView`: format digital vs staff-recorded route/channel via `acChannelLabel(data.route, data.channel)`, handle null `receipt.recorded_by` on digital receipts (`"Submitted directly online"` instead of `"Unknown (Unknown)"`), and show recorded `support_needed` adjustments when non-empty.
  * In `aftercareEvaluatorView`: guard `Array.isArray(v.rows)` (rendering an explicit `"Unknown"` cohort message instead of `"No homes are in the synthetic cohort."` when `v.rows` is `"unknown"` or non-array), validate `totals.concerns_raised` with `acWhole`, check `const hasConcerns = Array.isArray(row.concerns);` (rendering `"Unknown"` in `Concerns`, `Outcomes`, and `Unresolved` columns when `!hasConcerns`), guard `cmp.status === "sufficient" && cmp.baseline && cmp.late`, keep `${usable.count} of ${usable.denominator} homes have a usable comparison` when valid and `"Unknown"` otherwise, and render a plain-language `FR-036` note when `v.concern_pack_task` is present.

#### Dependencies

* P03-T01 and `web-design-guidelines` skill activation.

#### Validation Expectations

* Run `src/api/tests/test_aftercare_screen.py` and review `web/aftercare.js` against `web-design-guidelines`.

#### Completion Evidence

* Passing Node VM UI tests and clean `web-design-guidelines` check.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Focused Core and API Tests, Documentation Sync, and Verification

### Context

Every functional and guard refinement in `P01`–`P03` needs focused semantic test coverage that would fail without the change, updated component README notes (`src/core/README.md` and `src/api/README.md`), and clean execution of `mypy`, `ruff check`, `ruff format --check`, and `unittest discover` in both modified packages.

### Intent

Prove all three Issue #133 objectives and test-isolation constraints through automated tests, static analysis, and accurate package documentation.

### Boundaries

* Included: `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, `src/api/tests/test_aftercare_screen.py`, `src/api/tests/test_aftercare_served.py`, `src/core/README.md`, `src/api/README.md`.
* Excluded: Creating redundant test files or using `del sys.modules` / `sys.modules.pop`.

### Likely Targets

* `src/core/tests/test_aftercare.py`: Add focused tests for `"representative"` non-digital channel, `"call_back"` -> `"callback_window"` normalization, multiline `strip_unsafe_sentences` (`"Bills will\nfall."`), thermostat/ventilation/lifestyle blame + finite causal verbs + bill-reduction promises, `record_outcome`/`set_remedy`/`review_pack`/`from_state` `neutral_text` enforcement, `FR-036` fields on `propose_pack`, and AST/source verification that `aftercare_fixture.py` performs no `sys.modules` eviction.
* `src/core/tests/test_aftercare_intake.py`: Add focused tests for `"representative"` option in `staff_form`, `household_receipt` rejecting `staff_recorded` concerns (`403`), `HTTP 422` field-keyed `ValidationError` on non-neutral `outcome`/`remedy` evidence while preserving household `statement` verbatim, and `concern_pack_task` `FR-036` metadata in `evaluator_view`.
* `src/api/tests/test_aftercare_screen.py` and `src/api/tests/test_aftercare_served.py`: Add focused tests for `representative` channel label, multi-select `support_needed` read/render, digital `household_form` without `"Unknown"` paragraph and digital receipt/concern channel label, `aftercareEvaluatorView` preserving `"Unknown"` when `row.concerns` is `"unknown"` or `null` and when `homes_with_usable_comparison` is `"unknown"`, and `FR-036` notice rendering across the served `/api/aftercare/evaluator-view` payload.
* `src/core/README.md` and `src/api/README.md`: Update aftercare contract notes (`representative` channel, staff outcome/remedy neutral guard, `FR-036` `concern_pack_task` metadata, and evaluator `unknown` preservation).

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` exits `0`.
* `cd src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q` exits `0`.

### Completion Evidence

* Command exit codes and test counts recorded in `.copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Extend `test_aftercare.py` and `test_aftercare_intake.py` in `src/core`

#### Context

Existing `src/core` tests cover baseline `#133` structures (`94aa804a5`) but do not test `"representative"` as a non-digital channel, `"call_back"` normalization, digital-only `household_receipt`, multiline `strip_unsafe_sentences`, occupant thermostat/ventilation/lifestyle blame variants, staff outcome/remedy/pack-review neutrality, `FR-036` `concern_pack_task` metadata, or `sys.modules` fixture safety.

#### Intent

Add <= 13 high-signal semantic unit tests across `test_aftercare.py` and `test_aftercare_intake.py`.

#### Boundaries

* Included: `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`.
* Excluded: New test files or `sys.modules` mutation.

#### Likely Targets

* `src/core/tests/test_aftercare.py` and `src/core/tests/test_aftercare_intake.py`.

#### Dependencies

* P01, P02, P03-T01.

#### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_aftercare*.py" -v` in `src/core` passes.

#### Completion Evidence

* Passing `src/core` unit tests and full `unittest discover` run.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Extend `test_aftercare_screen.py` and `test_aftercare_served.py`, update READMEs, and run `mypy`, `ruff`, and `unittest`

#### Context

`src/api/tests/test_aftercare_screen.py` executes `web/aftercare.js` inside Node's `vm` context, and `test_aftercare_served.py` exercises live authenticated HTTP calls against `server.py`.

#### Intent

Add <= 5 focused UI/API tests verifying `aftercare.js` channel/support/multi-select rendering, strict `"Unknown"` preservation, and `FR-036` evaluator payload rendering; sync `src/core/README.md` and `src/api/README.md`; and run full package checks (`mypy`, `ruff check`, `ruff format --check`, `unittest discover`).

#### Boundaries

* Included: `src/api/tests/test_aftercare_screen.py`, `src/api/tests/test_aftercare_served.py`, `src/core/README.md`, `src/api/README.md`.
* Excluded: Modifying unrelated endpoints or tests.

#### Likely Targets

* `src/api/tests/test_aftercare_screen.py`, `src/api/tests/test_aftercare_served.py`, `src/core/README.md`, `src/api/README.md`.

#### Dependencies

* P03-T02, P04-T01.

#### Validation Expectations

* All `mypy`, `ruff check`, `ruff format --check`, and `unittest discover` suites pass in `src/core` and `src/api`.

#### Completion Evidence

* Clean verification output recorded in `.copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md`.

#### Unresolved Items

* None.
