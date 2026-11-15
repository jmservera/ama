<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #133 Aftercare Accessible Concern Routes and Neutral-Text Enforcement in src/core

## Metadata

* Task ID: 133-aftercare-concern-2142
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Issue #133 (`FR-049`, `AC-063`) on branch `feat/quality-133-aftercare-concern-2142`. Authoritative scope requires delivering inside `src/core` only (no edits to `src/api` or shared `~/.local`): (1) a household or representative can raise an aftercare concern through an accessible route including a non-digital one, and (2) no causation, blame, or savings promise appears in any generated or templated text; writing all four `.copilot-tracking/` stage artifacts (`research/`, `plans/`, `changes/`, `reviews/`); passing bare `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` in `src/core`; and committing locally with the Copilot trailer without pushing (`git status --short` empty).
* Research and evidence considered: .copilot-tracking/research/2026-11-14/133-aftercare-concern-2142-research.md (`C1`-`C16`), .copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md, .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md, src/core/src/zava_forward/core/aftercare.py, src/core/src/zava_forward/core/aftercare_intake.py, src/core/src/zava_forward/core/aftercare_store.py, src/core/pyproject.toml, src/core/tests/test_aftercare.py, src/core/tests/test_aftercare_intake.py, src/core/tests/test_aftercare_store.py, src/core/tests/test_dependency_rule.py, src/core/README.md, src/api/src/zava_forward/api/web/aftercare.js, and src/api/tests/test_aftercare_screen.py.
* Decisions, dependencies, and acceptance criteria considered: Separate household/representative self-service digital intake (`household_form`, `submit_household_concern`, `household_receipt`, `/api/aftercare/household-*`) alongside preserved staff-gated `form` and `record_concern` non-digital channels (`phone`, `in_person`, `paper`, `assisted_visit`); optional `support_needed` communication adjustments without justification; hardened `neutral_text`, `strip_unsafe_sentences`, and `assert_templates_neutral` across all three `src/core` aftercare modules while preserving verbatim household `statement` and `representative_basis`; 100% backward compatibility with `zf-aftercare-intake/1` snapshots and `aftercare.js`; locked test budget (at most 14 added test methods, 0 removals); Focused-tier local validation.
* Assessment boundary: Evaluates `src/core` domain, validation, persistence, neutral-text, documentation, and bare test-execution credibility from supplied repository evidence. Cannot certify live served browser assistive-technology WCAG 2.2 AA acceptance, real operational human owner assignment, evaluator role approval, or Data Protection Officer sign-off, which the plan explicitly scopes out as external follow-up gates.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Issue #133 AC1 (`FR-049`, `AC-063`, `C1`-`C3`, `C5`, `C6`, `C8`-`C10`, `C12`, `C15`) | Partial | Digital + non-digital household/representative routes and optional `support_needed` adjustments are well structured, but `P02-T01` has a cross-day replay fingerprint bug when `next_update` is omitted (`PC-001`) and unsafe direct key subscripts for `digital` / legacy records (`PC-003`). |
| Issue #133 AC5 (`C4`, `C5`, `C7`, `C9`, `C11`, `C13`, `C15`) | Partial | Clause-boundary and template coverage are thorough, but `P01-T01` rejects the existing `AftercareService._comparison` disclaimer (`"promise savings"`), risks soft-wrap newline and `mis-use` evasions, and leaves `neutral_text` echoing banned phrases into HTTP 400 error payloads (`PC-002`). |
| Caller scope, artifacts, and git rules | Covered | Restricts code edits to `src/core` and `src/core/README.md`, preserves `src/api` and `~/.local` untouched, tracks all four `.copilot-tracking/` artifact stages, and specifies local-only commit with Copilot trailer. |
| Bare verification and worktree import (`C14`) | Partial | `aftercare_fixture.py` addresses `~/.local` `.pth` shadowing, but `P03-T01` must specify `ruff` `F401`/`I001`-clean imports and eviction of preloaded stale `zava_forward.core*` entries from `sys.modules` (`PC-004`). |
| `P01` / `P01-T01` | Partial | Needs `PC-002` fixes for negated-verb `"promise savings"`, two-stage newline folding, `mis-use` pattern, non-echoing `ValueError`, and `from_state` neutrality check. |
| `P01` / `P01-T02` | Partial | Needs `PC-003` alignment so `intake_errors` delegates directly to `normalize_support_needed` (including whitespace-only strings and empty iterables) and `from_state` enforces canonical `list[str]` shape when present. |
| `P02` / `P02-T01` | Partial | Needs `PC-001` caller-supplied `next_update` fingerprinting + post-replay date defaulting/validation and `PC-003` `.get(...)` handling for omitted `channel`/`recorded_by` on `digital` concerns and omitted `support_needed` on legacy snapshots. |
| `P02` / `P02-T02` | Covered | Guards module constants and runtime dynamic strings across `aftercare_intake.py` and `aftercare_store.py` once `PC-002` preserves `_comparison` neutrality. |
| `P03` / `P03-T01` | Partial | Stays within the 14-test budget (9 planned test groups), but needs `PC-004` `ruff` `F401` / `sys.modules` details and `PC-001` cross-day omitted-`next_update` replay assertion. |
| `P03` / `P03-T02` | Covered | Updates `src/core/README.md` (`C16`) honestly and executes the exact bare verification chain plus `test_dependency_rule.py` and read-only `src/api/tests/test_aftercare_screen.py`. |

## Verdict

* Verdict: Revise
* Rationale: The architecture and separation between household self-service digital intake (`household_form`, `submit_household_concern`, `household_receipt`) and staff-assisted non-digital intake (`form`, `record_concern`) are sound, backward-compatible, and well within caller scope, but four concrete defects in the task specifications (`PC-001` through `PC-004`) would cause runtime regressions (`ValueError` on `evaluator_view()`, `ConflictError` on cross-day retries, `KeyError`/`StateInvalid` on digital concerns) or linter/import failures (`ruff` `F401`, stale `sys.modules`) during implementation if not corrected in the plan details first. All four findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Defaulted next_update in submit_household_concern breaks idempotent request_id replay across UTC date boundaries

* Related IDs: `FR-049`, `AC-063`, `C8`, `C9`, `P02`, `P02-T01`, `P03-T01`
* Evidence: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md (`P02-T01`), src/core/src/zava_forward/core/aftercare.py (`intake_form`, lines 194-252), src/core/src/zava_forward/core/aftercare_intake.py (`_fingerprint`, `_receipt_fingerprint`, `record_concern`, lines 178-196, 391-440), src/core/tests/test_aftercare_intake.py (`ReplayAfterDateTests`, lines 610-655)
* Concern: `P02-T01` defaults omitted `next_update` on `submit_household_concern` to `today + 7 days` (`DEFAULT_UPDATE_DAYS = 7`), hashes `[route, raised_by, basis, home, kind, statement, channel, next_update, support_needed]` in `_fingerprint` and `_receipt_fingerprint`, and states that it supports idempotent `request_id` replay including after `next_update` has passed. Because `household_form()` omits `next_update`, standard household digital submissions omit `next_update`. If `today + 7 days` is substituted into `next_update` before computing `_fingerprint`, retrying the identical omitted-`next_update` request after UTC midnight (or after `next_update` has passed, such as during `UNCONFIRMED` recovery) computes a different date, mismatches `seen["fingerprint"]`, and raises `ConflictError` instead of replaying the original receipt. Similarly, if an explicitly supplied `next_update` is checked against `self._today()` before checking `doc["requests"].get(request_id)`, post-date replay raises `ValidationError`.
* Impact: Breaks idempotent retry guarantees and `DocumentStateStore` unconfirmed-write reconciliation for household and representative digital submissions across UTC date boundaries.
* Smallest useful change: Specify in `P02-T01` that digital/extended fingerprints hash the caller-supplied `requested_next_update` (`None` when omitted, ISO date string when explicitly supplied) and store `"next_update": requested_next_update` inside `receipt["original"]` for digital concerns (with `_receipt_fingerprint` and `_validate` reading `receipt["original"].get("next_update", receipt["next_update"])` when `"next_update" in receipt["original"]`, keeping legacy `staff_recorded` receipts and their 7-item fingerprints unchanged), and compute `today + 7 days` or enforce `next_update >= self._today()` only inside `work(doc)` after `doc["requests"].get(request_id)` replay resolution. Include an omitted-`next_update` cross-day replay check in `P03-T01`.
* Action owner: planning parent
* Exact resolving evidence: Revised `P02-T01` and `P03-T01` in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md defining caller-supplied `next_update` fingerprinting (`None` when omitted), post-replay date defaulting/floor checking, and cross-day digital replay test coverage.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Proposed PARAPHRASE_PATTERNS and _variants rules in P01-T01 break AftercareService._comparison, leave soft-wrap and mis-use gaps, and echo banned phrases in HTTP 400 errors

* Related IDs: Issue #133 AC5, `C4`, `C9`, `C15`, `P01`, `P01-T01`, `P02-T02`, `P03-T01`
* Evidence: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md (`P01-T01`, `P02-T02`, `P03-T01`), src/core/src/zava_forward/core/aftercare.py (`BANNED_PHRASES`, `_NEGATED_CLAIM`, `_variants`, `neutral_text`, lines 62-141), src/core/src/zava_forward/core/aftercare_intake.py (`_comparison`, `handle`, lines 725-728, 747-748)
* Concern: Four concrete interactions in `P01-T01` will cause immediate test failures or neutrality bypasses if implemented literally: (1) `AftercareService._comparison` (`src/core/src/zava_forward/core/aftercare_intake.py:725-727`) passes `"Descriptive observed means only. They do not show a cause, assign fault or promise savings."` to `neutral_text()`, which is not matched by `_NEGATED_CLAIM` (`(?:no|not a|never a) (?:claim|promise|guarantee)s? (?:of|about)`), so adding `(?:guarantees?|guaranteeing|promis(?:e|es|ed|ing)) (?:any |you )?(?:savings?|...)` to `PARAPHRASE_PATTERNS` raises `ValueError` on every `AftercareService.evaluator_view()` call and breaks `JoinedViewTests` and `src/api/tests/test_aftercare_screen.py`; (2) converting `\n` to `"; "` or keeping `\n` in `_variants` without also checking whitespace-collapsed text prevents single-space `BANNED_PHRASES` and `PARAPHRASE_PATTERNS` from catching line-wrapped claims like `"You will\nsave money"` or `"Your bills will\nfall"`; (3) hyphen-to-space folding turns `"mis-use"` into `"mis use"`, which still misses `"misuse"` in `BANNED_PHRASES`; and (4) `neutral_text` currently raises `ValueError(f"Generated text must not contain '{phrase}'.")` (`src/core/src/zava_forward/core/aftercare.py:134`), which `AftercareService.handle()` (`src/core/src/zava_forward/core/aftercare_intake.py:747-748`) returns in `{"error": str(exc)}`, echoing the banned phrase into generated HTTP error payloads and failing `P03-T01` error-payload neutrality scans.
* Impact: Breaks existing `evaluator_view()` and `src/api` screen contract tests, permits multi-line soft-wrap and `mis-use` evasions, and leaks banned causation/blame/savings phrases into HTTP 400 responses.
* Smallest useful change: Revise `P01-T01` so that: (a) `_NEGATED_CLAIM` also matches narrow negated-verb disclaimers such as `\b(?:do|does|did)\s+not\s+(?:show a cause,\s*assign fault\s+or\s+)?(?:claim|promise|guarantee)\s+(?:any\s+)?savings?\b` without a trailing wildcard that could mask a second clause; (b) `_variants` preserves `\n` while `neutral_text` checks `BANNED_PHRASES` against `" ".join(lowered.split())`, applies `_UNCERTAIN` and `_NEGATED_CLAIM` (substituting `" ; "`) while `\n` is still intact, and then runs `PARAPHRASE_PATTERNS` against both `folded` and `" ".join(folded.split())`; (c) `PARAPHRASE_PATTERNS` includes `\bmis[-_ ]?us(?:e|ed|es|ing)\b`; and (d) `neutral_text` raises a fixed neutral `ValueError` message without echoing `{phrase}`, and `AftercareRegister.from_state` also validates `owner` and `sensor_context` neutrality.
* Action owner: planning parent
* Exact resolving evidence: Revised `P01-T01` in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md incorporating negated-verb disclaimer compatibility, two-stage newline evaluation, `\bmis[-_ ]?us(?:e|ed|es|ing)\b`, non-echoing `ValueError`, and `from_state` neutrality enforcement.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Direct dictionary subscripts for channel, recorded_by, and support_needed in AftercareService will fail on digital concerns and legacy snapshots

* Related IDs: `FR-049`, `AC-063`, `C6`, `C8`, `C9`, `C12`, `P01-T02`, `P02-T01`
* Evidence: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md (`P01-T02`, `P02-T01`), src/core/src/zava_forward/core/aftercare.py (`AftercareRegister.raise_concern`, lines 394-429), src/core/src/zava_forward/core/aftercare_intake.py (`_validate`, `_receipt`, `_display`, lines 216-243, 456-505)
* Concern: `AftercareRegister.raise_concern` (`src/core/src/zava_forward/core/aftercare.py:394-403`) only adds `"channel"` and `"recorded_by"` keys to `rec` when `route == "staff_recorded"`; for `route == "digital"`, those keys are absent from `rec`. Existing `AftercareService._validate`, `_receipt`, and `_display` index `rec["channel"]` and `rec["recorded_by"]` directly, which raises `KeyError` (turning `_validate` into `StateInvalid` 503) as soon as a digital concern is stored. Likewise, legacy `zf-aftercare-intake/1` receipts omit `"support_needed"`, and `P01-T02` checks `values.get("support_needed") not in (None, "", [], ())` before calling `normalize_support_needed`, which diverges on whitespace-only strings or empty iterables.
* Impact: Causes `StateInvalid` or `KeyError` crashes when storing, validating, or displaying household digital concerns or restoring legacy persisted state documents.
* Smallest useful change: Specify in `P01-T02` that `normalize_support_needed` maps `None`, blank/whitespace-only strings, and empty non-mapping iterables to `[]`, `intake_errors` calls `normalize_support_needed(values.get("support_needed"))` directly, and `from_state` defaults absent `support_needed` to `[]` while requiring any present `support_needed` in a snapshot to be a canonical deduplicated `list[str]`. Specify in `P02-T01` that `_receipt`, `_display`, and `_validate` access `rec.get("channel")`, `rec.get("recorded_by")`, and `receipt.get("support_needed", [])` (requiring `"channel" not in rec and "recorded_by" not in rec and receipt["channel"] is None and receipt["recorded_by"] is None` when `rec["route"] == "digital"`).
* Action owner: planning parent
* Exact resolving evidence: Revised `P01-T02` and `P02-T01` in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md specifying `.get(...)` key handling for `digital` concerns and legacy receipts plus canonical `normalize_support_needed` delegation.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Worktree import fixture in P03-T01 must satisfy ruff F401/I001 rules and evict preloaded stale zava_forward.core modules

* Related IDs: `C14`, `P03`, `P03-T01`
* Evidence: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md (`P03-T01`), src/core/pyproject.toml (`[tool.ruff]` and `[tool.ruff.lint]`, lines 26-31)
* Concern: `src/core/pyproject.toml` enables `ruff` lint rules `E`, `F` (`F401` unused import), `I` (`I001` import sorting with `src = ["src", "tests"]`), `B`, and `UP` across `test_aftercare*.py` and `aftercare_fixture.py` without per-file ignores. Importing `aftercare_fixture` solely for import-time side effects in `test_aftercare_intake.py` (where `CORE_SRC` is not currently planned to be referenced) will fail `python3 -m ruff check .` with `F401`. Additionally, if a broader `unittest discover -s tests` run imports `zava_forward.core.*` from stale `~/.local` `.pth` in an earlier test file before loading `test_aftercare*.py`, mutating `sys.path` and namespace `__path__` will not replace already-cached `sys.modules["zava_forward.core.*"]` entries.
* Impact: Causes `python3 -m ruff check .` to fail in the mandatory bare verification command or leaves `zava_forward.core.*` pointing at stale `~/.local` modules when full-directory test discovery runs.
* Smallest useful change: Update `P03-T01` so `aftercare_fixture.py` exposes an explicit helper (such as `ensure_worktree_src() -> Path` alongside `CORE_SRC`) that prepends `CORE_SRC` to `sys.path`, prioritizes `CORE_SRC` in `zava_forward.__path__` / `zava_forward.core.__path__`, and removes any preloaded `zava_forward.core*` module in `sys.modules` whose `__file__` is outside `CORE_SRC`; and ensure all three test modules (`test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`) reference the imported symbol (`aftercare_fixture` sorts alphabetically ahead of `dataset`, `sqlguard`, and `zava_forward` under `ruff` `I001`, avoiding both `F401` and `E402`).
* Action owner: planning parent
* Exact resolving evidence: Revised `P03-T01` in .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md specifying stale `sys.modules` eviction and explicit symbol usage in all three aftercare test files.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Separating `household_form`, `submit_household_concern`, and `household_receipt` (`/api/aftercare/household-*`) from staff-only `form` and `record_concern` (`/api/aftercare/form`, `/api/aftercare/concerns`) cleanly delivers household and representative self-service digital intake while preserving 100% of existing role-gating and non-digital channel tests (`C10`).
* Preserving household `statement` and `representative_basis` verbatim (`C11`) while enforcing `assert_templates_neutral` and `neutral_text` across fixed templates, dynamic receipts, `owner` strings, `sensor_context`, and store errors accurately matches Issue #133 AC5 without censoring residents who report broken savings promises in their own words.
* Residual risk (explicitly accepted in plan Scope and Follow-Up Items): `src/core` tests and read-only `src/api/tests/test_aftercare_screen.py` prove domain contracts, plain language, and neutral-text guards, whereas served resident-UI assistive-technology WCAG 2.2 AA validation, real named operational owners, evaluator role authorization, and DPO sign-off remain external Issue #133 gates and are documented as undelivered in `src/core/README.md`.

## Questions or Blocking Evidence Gaps

* None. All four findings are resolvable directly from supplied codebase evidence without user clarification.

## Limitations

* Critique is read-only over supplied plan, research, `src/core`, and `src/api` files and does not execute live MSSQL (`ZF_RESIDENT_MSSQL=1`) or browser assistive-technology checks, which are outside the caller's `src/core` Focused-tier boundary.

## Recommended Next Action

* Highest-impact finding: `PC-001` (alongside `PC-002` at High severity)
* Action owner: planning parent
* Smallest next action: Directly revise `P01-T01`, `P01-T02`, `P02-T01`, and `P03-T01` in `.copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md` and record dispositions for `PC-001` through `PC-004` in `.copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md`, then finalize the plan for implementation without another critique pass.
* User response required: no
