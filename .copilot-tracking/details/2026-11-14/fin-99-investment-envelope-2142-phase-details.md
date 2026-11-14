<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #99 Investment Envelope, Liquidity and Downside Tolerance Controls

## Metadata

* Task ID: fin-99-investment-envelope-2142
* Task slug: fin-99-investment-envelope-2142
* Related plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md, docs/brds/agentic-retrofit-programme-brd.md, src/core/src/zava_forward/core/exposure_limits.py, src/core/tests/test_issue_99_acceptance.py

## Phase Index

| Phase ID | Name                                                                               | Status    | Detail sections          |
|----------|------------------------------------------------------------------------------------|-----------|--------------------------|
| P01      | Harden `exposure_limits` approval, liquidity/covenant floor, and breach controls   | completed | P01, P01-T01, P01-T02    |
| P02      | Expand worktree-isolated Issue #99 tests, unit regressions, and `src/core` docs    | completed | P02, P02-T01, P02-T02    |

<!-- rpi:phase id=P01 -->
## P01: Harden `exposure_limits` approval, liquidity/covenant floor, and breach pause controls

### Context

`src/core/src/zava_forward/core/exposure_limits.py` currently records `approval`, `envelope`, and upper-bound `tolerances` across the six `RULE-012` dimensions (`safety`, `resident`, `quality`, `capital`, `grant`, `capacity`) and emits `pause_signal` (`automatic_cut=False`). Research (`C1`-`C6`) identified four concrete gaps: missing optional human-approved `liquidity` and `covenant` minimum headroom floor controls (`BG-008`, `RULE-011`, `OD-12`), lax ISO timestamp and conflicting-alias handling in `_approval()`, lack of canonical `limits` validation inside `assess()`, and negative finite observations evaluating as `"Within"`.

### Intent

Complete the pure-core human-approved input and breach pause-signal contract in `exposure_limits.py` with zero invented company defaults and 100% compatibility for existing 3-argument callers.

### Boundaries

* Included: `src/core/src/zava_forward/core/exposure_limits.py`
* Excluded: `src/api`, web templates, database schema changes, and invented Zava North Homes thresholds (`OD-12`, `OD-15`)

### Likely Targets

* src/core/src/zava_forward/core/exposure_limits.py: Add optional `liquidity` / `covenant` minimum floor validation and assessment, strict ISO timestamp and alias checks, canonical `limits` validation in `assess()`, and non-negative finite observation checks.

### Dependencies

* none

### Validation Expectations

* `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` pass in `src/core`.

### Completion Evidence

* `exposure_limits.py` implements all `P01-T01` and `P01-T02` contracts cleanly under strict `mypy`.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `_approval`, `record_limits`, and `load_limits` with optional liquidity/covenant floors

#### Context

Research `C4` and `C6` showed `_approval` currently validates only the first 10 characters with `date.fromisoformat` and a permissive regex (`r"\d{4}-\d{2}-\d{2}(T[0-9:.+\-Z]+)?"`), silently ignores disagreements when both `approved_by` and `approver` (or both `approved_at` and `approved_on`) are passed, and `record_limits` / `load_limits` have no representation for `BG-008` / `RULE-011` / `OD-12` liquidity and covenant minimum headroom controls.

#### Intent

Enforce unambiguous human attribution and allow recording human-approved `liquidity` (and optional paired `covenant` headroom) minimum floors without defaulting any figure or breaking 3-argument callers.

#### Boundaries

* Included: `_approval`, `_liquidity` helper, `record_limits`, and `load_limits` in `src/core/src/zava_forward/core/exposure_limits.py`.
* Excluded: Changing `FinanceMixin.exposure_signal` call sites or requiring `liquidity` on legacy 3-argument calls.

#### Likely Targets

* src/core/src/zava_forward/core/exposure_limits.py:
  * Catch `OverflowError` in `_number()` when converting `int | float` to `float` so extreme values raise `LimitsError` cleanly.
  * Enforce strict allowed-key checking (`_check_keys`) raising `LimitsError` on unrecognized keys in `approval` (`{"approved_by", "approved_at", "approver", "approved_on", "role", "evidence_ref", "restart_owner"}`), `envelope` (`{"amount", "currency", "period", "annual_plan"}`), each `tolerances[name]` (`{"maximum", "unit"}`), `liquidity` (`{"minimum", "currency", "covenant_minimum", "covenant_unit"}`), and top-level `load_limits` / `assess` (`{"approval", "envelope", "tolerances", "liquidity"}`).
  * Validate `approved_at` by requiring `approved_at[:10]` to match `r"\d{4}-\d{2}-\d{2}"` and `date.fromisoformat(approved_at[:10])`; when `len(approved_at) > 10`, require `approved_at[10] == "T"`, no whitespace, and valid `datetime.fromisoformat(approved_at)` (rejecting compact/week ISO forms and space separators). If both `approved_by` and `approver` are not `None`, require `_text(approved_by) == _text(approver)`; if both `approved_at` and `approved_on` are not `None`, validate `approved_on` as a 10-char `YYYY-MM-DD` date equal to `approved_at[:10]`.
  * Support optional `envelope["annual_plan"]` (`RULE-011` `AC-037`): when present and not `None`, validate via `_number(..., "envelope annual_plan")` and preserve `"annual_plan"` on `record["envelope"]` (omit when `None`/absent).
  * Add keyword-optional `liquidity: object = None` to `record_limits(approval, envelope, tolerances, *, liquidity=None)` and pass `liquidity=data.get("liquidity")` in `load_limits`. When `liquidity is not None`, require a `dict` with allowed keys only, validate `minimum` via `_number(..., "liquidity minimum")` and `currency` via `_text(..., "liquidity currency")`, and if either `covenant_minimum` or `covenant_unit` is not `None`, require both (`_number(..., "covenant minimum")` and `_text(..., "covenant unit")`). Include `"liquidity"` in the returned `record_limits` dict only when `liquidity is not None`.

#### Dependencies

* none

#### Validation Expectations

* Strict `mypy` passes; missing/blank/conflicting attribution or invalid `liquidity` inputs raise `LimitsError`.

#### Completion Evidence

* Updated `_approval`, `record_limits`, and `load_limits` in `src/core/src/zava_forward/core/exposure_limits.py`.

#### Unresolved Items

* none

<!-- rpi:task id=P01-T02 -->
### P01-T02: Harden `assess` with canonical limits validation, non-negative observation checks, and floor breach pause signals

#### Context

Research `C5` demonstrated that passing a raw unvalidated dictionary directly to `assess()` skips `record_limits()` validation, negative finite observations (`committed = -5`) pass `_finite_observation()` and evaluate as `"Within"`, and `assess()` has no minimum-floor comparison (`observed < minimum`) for recorded liquidity/covenant controls. Research also noted `src/api/tests/test_finance_exposure_screen.py` uses `"Over approved limit: ..."` for upper-limit breaches.

#### Intent

Ensure `assess()` validates `limits` canonically, treats negative or non-finite observations as `"Unknown"`, checks recorded liquidity and covenant minimum floors (`observed < minimum` -> `"Breach"`), and emits a deterministic human-decision `pause_signal` (`automatic_cut=False`) without breaking upper-limit breach reason formatting.

#### Boundaries

* Included: `_comparable_observation` and `assess` in `src/core/src/zava_forward/core/exposure_limits.py`.
* Excluded: Automatic live-activity cuts or workflow state mutations.

#### Likely Targets

* src/core/src/zava_forward/core/exposure_limits.py:
  * At the start of `assess`, if `limits is None`, return `held("No person-approved envelope or tolerances are recorded.")`. Validate `limits` is a `dict` with only allowed top-level keys `{"approval", "envelope", "tolerances", "liquidity"}` and canonicalize via `record_limits(limits.get("approval"), limits.get("envelope"), limits.get("tolerances"), liquidity=limits.get("liquidity"))`; on `LimitsError` or `(KeyError, TypeError, ValueError)`, return `held("The approved limits record is not readable, so it cannot be relied on.")`. Then check `stale_reason(canonical_limits, today)`.
  * Normalize `exposure = exposure if isinstance(exposure, dict) else {}` so truthy non-dict `exposure` values safely produce `Unknown` findings instead of `AttributeError`.
  * Guard upper-ceiling observations (`committed`, optional `annual_plan` against `exposure.get("annual_committed", committed)`, and `tolerances[name]`) with `_non_negative_finite_observation(value)` requiring `_finite_observation(value) and value >= 0`.
  * Guard minimum-floor observations (`liquidity` and `covenant`) with signed `_finite_observation(value)` so negative available cash or underwater covenant headroom (`< 0`) evaluates as `"Breach"` (`observed < minimum`) rather than `"Unknown"`. Accept `exposure.get("liquidity")` either as a `dict` (`{"available", "currency"}`) or a signed finite scalar when `exposure.get("liquidity_currency", exposure.get("currency")) == liq["currency"]`. When `"covenant_minimum"` is in `liq`, accept `exposure.get("covenant")` either as a `dict` (`{"headroom", "unit"}`) with matching `unit` or a signed finite scalar with explicit `exposure.get("covenant_unit") == liq["covenant_unit"]` (no default unit fallback).
  * Keep `"Over approved limit: ..."` when only upper-bound limits breach; use `"Below approved minimum: ..."` when only minimum-floor limits breach, or `"Over approved limit: ...; below approved minimum: ..."` when both breach simultaneously.

#### Dependencies

* P01-T01

#### Validation Expectations

* Upper-ceiling breaches, lower-floor breaches, forged raw `limits` dicts, stale records, and negative/non-finite/missing observations all emit `signal == UNAPPROVED` and `pause_signal == dict(paused=True, decision_required=True, decision_owner=..., automatic_cut=False, reason=...)`.

#### Completion Evidence

* Updated `assess` in `src/core/src/zava_forward/core/exposure_limits.py`.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Expand worktree-isolated Issue #99 acceptance tests, unit regressions, and `src/core` documentation

### Context

Research `C8` showed that `src/core/tests/test_issue_99_acceptance.py` exists untracked in this worktree and matches `-p 'test_*99*.py'`, while bare `python3` resolves `zava_forward.core` to `/home/azureuser/source/ama/src/core/src` unless `test_issue_99_acceptance.py` prepends the local worktree `src/` directory. `src/core/README.md` also lacks a section documenting `exposure_limits`.

### Intent

Lock in worktree-isolated acceptance tests, complementary `test_exposure_limits.py` unit coverage, and concise `src/core/README.md` documentation, then verify all required checks pass cleanly.

### Boundaries

* Included: `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`, `src/core/README.md`
* Excluded: Modifying shared `~/.local` Python site-packages or touching `src/api`.

### Likely Targets

* src/core/tests/test_issue_99_acceptance.py: Prepend worktree `src/` to `sys.path`, verify `limits.__file__` origin, and test all Issue #99 acceptance and boundary cases.
* src/core/tests/test_exposure_limits.py: Add focused unit regressions for liquidity/covenant floors, ISO timestamp/alias conflicts, forged `assess` dicts, and negative finite observations.
* src/core/README.md: Document `exposure_limits` controls, approval requirements, and boundaries.

### Dependencies

* P01

### Validation Expectations

* `cd /home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*99*.py' -v` exits `0`.
* `cd /home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142/src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_exposure_limits.py' -v` exits `0`.

### Completion Evidence

* Passing command outputs recorded in `.copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-changes.md`.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Isolate worktree imports and expand `test_issue_99_acceptance.py` and `test_exposure_limits.py`

#### Context

Test scope lock from the plan caps additions to `<= 12` focused test methods across `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`, with `none` removed.

#### Intent

Prove both Issue #99 acceptance criteria and contrarian anti-bypass cases directly against this worktree's `src/core/src/zava_forward/core/exposure_limits.py`.

#### Boundaries

* Included: `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`
* Excluded: Unrelated core test suites.

#### Likely Targets

* src/core/tests/test_issue_99_acceptance.py: Keep all 6 existing tests, add a PEP 420 namespace-safe, Ruff `E402`-compliant worktree `src/` bootstrap before importing `zava_forward.core`, assert `Path(limits.__file__).resolve()` is in this worktree, and add focused tests for human-approved `annual_plan` + `liquidity`/`covenant` recording & refusal, liquidity/covenant floor breach pause signals (including negative deficits, `automatic_cut=False`, named `decision_owner`), `load_limits` JSON round-trip, and forged-dict / negative-ceiling rejection.
* src/core/tests/test_exposure_limits.py: Add the same PEP 420 namespace-safe, Ruff `E402`-compliant worktree `src/` bootstrap, align `test_attribution_is_required_and_never_defaulted` so canonical `approved_by`/`approved_at` do not pass conflicting legacy `APPROVAL` keys while explicitly testing conflicting-alias refusal, and add focused unit tests for malformed/compact ISO dates, unknown keys / integer overflow, and negative ceiling vs negative floor observations.

#### Dependencies

* P01-T01, P01-T02

#### Validation Expectations

* All tests in `test_issue_99_acceptance.py` and `test_exposure_limits.py` pass with zero `mypy` or `ruff` warnings.

#### Completion Evidence

* Passing test output from bare `unittest discover -s tests -p 'test_*99*.py' -v` and `PYTHONPATH=src:tests` run of `test_exposure_limits.py`.

#### Unresolved Items

* none

<!-- rpi:task id=P02-T02 -->
### P02-T02: Document `exposure_limits` controls and boundaries in `src/core/README.md` and run verification gate

#### Context

`src/core/README.md` documents core modules and evidence boundaries (`#96, #98, #99` form-review holds at line 601), and repository instructions require updating directly related documentation when behavior is extended.

#### Intent

Add a concise subsection to `src/core/README.md` describing `exposure_limits.record_limits`, `load_limits`, `assess`, optional `liquidity`/`covenant` minimum floors, `pause_signal` non-decision semantics, and the remaining `OD-12`/`OD-15` human-governance boundary, then run the full `src/core` verification command.

#### Boundaries

* Included: `src/core/README.md`
* Excluded: Rewriting historical case studies or inventing company facts.

#### Likely Targets

* src/core/README.md: Add concise `## Investment envelope, liquidity and downside tolerance controls (#99)` subsection near the finance/form-review documentation.

#### Dependencies

* P02-T01

#### Validation Expectations

* Markdown links and formatting clean; exact user-requested verification command exits `0`.

#### Completion Evidence

* Updated `src/core/README.md` and clean verification output.

#### Unresolved Items

* none
