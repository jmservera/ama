<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #99 Investment Envelope, Liquidity and Downside Tolerance Controls

## Metadata

* Task ID: fin-99-investment-envelope-2142
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver both locally verifiable Issue #99 acceptance criteria in `src/core` ("Envelope and tolerances are recorded as human-approved inputs, not invented" and "A breach produces a pause signal for a human decision"), write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), verify in `src/core` using bare `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*99*.py' -v`, and commit cleanly with the `Co-authored-by` trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md, .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md, .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md, src/core/src/zava_forward/core/exposure_limits.py, src/core/src/zava_forward/core/finance.py, src/core/tests/test_issue_99_acceptance.py, src/core/tests/test_exposure_limits.py, src/core/pyproject.toml.
* Decisions, dependencies, and acceptance criteria considered: Zero invented Zava North Homes figures (`OD-12`, `OD-15`); 3-argument `record_limits(approval, envelope, tolerances)` compatibility for `finance.py` and `src/api`; strict `mypy` and `ruff` (`select = ["E", "F", "I", "B", "UP"]`) compliance; shared-environment constraint forbidding `~/.local` site-packages mutation; test scope lock (`<= 12` new test methods across `test_issue_99_acceptance.py` and `test_exposure_limits.py`, `none` removed); `Refs #99` non-closing boundary.
* Assessment boundary: Evaluates completeness, internal consistency, backward compatibility, edge-case safety, and local verification reliability across all supplied artifacts and `src/core` source/test files. Out-of-scope files (`src/api/tests/test_finance_exposure_api.py`, `src/api/tests/test_finance_exposure_screen.py`, and `docs/brds/agentic-retrofit-programme-brd.md`) were assessed strictly via the cited evidence in the supplied research artifact (`C1`-`C8`) without performing unrequested external reads.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Issue #99 AC1 (human-approved inputs, never invented) | Partial | Covered for core attribution and optional liquidity/covenant recording, but `PC-001` finds a breaking conflict with `src/core/tests/test_exposure_limits.py:38-44` plus Python 3.12 compact/week ISO parsing bypasses, and `PC-003` finds silent dropping of confirmed `annual_plan` / unknown control keys. |
| Issue #99 AC2 (breach produces human-decision pause signal) | Partial | Covered for upper-ceiling breaches and non-negative floor breaches, but `PC-002` finds negative liquidity/covenant headroom (`< 0`, such as overdraft or underwater covenant headroom) misclassified as `Unknown` rather than `Breach`, silent scalar `covenant_unit` defaulting, non-dict `exposure` crash, and `OverflowError` on huge integers. |
| Research C1, C2 (`BG-008`, `RULE-011`, `RULE-012`) | Partial | Liquidity/covenant floors (`BG-008`, `RULE-011`) and 6 downside dimensions (`RULE-012`) are planned, but Research's confirmed optional `envelope["annual_plan"]` cap (`RULE-011` `AC-037`) is omitted from the plan without disposition (`PC-003`). |
| Research C3, C7 (`OD-12`, `OD-15` non-invention boundary) | Covered | Plan and phase details strictly prohibit default figures, preserve synthetic-only test fixtures, and require `Refs #99`. |
| Research C4, C5 (contrarian validation hardening) | Partial | Canonical `assess()` validation and non-negative ceiling guards are planned, but `PC-001`, `PC-002`, and `PC-003` identify concrete edge-case defects in the proposed checks. |
| Research C6 (`FinanceMixin.exposure_signal` compatibility) | Covered | Keyword-optional `liquidity=None` preserves 3-argument calls and `finance.py:351-368` behavior. |
| Research C8 (worktree `sys.path` test isolation) | Partial | Covered for standalone `test_issue_99_acceptance.py`, but `PC-004` finds `test_exposure_limits.py` lacks worktree bootstrap, PEP 420 namespace caching breaks multi-file bare discovery when `test_exposure_limits.py` runs first, and top-of-file `sys.path` edits trigger Ruff `E402` unless explicitly handled. |
| P01 / P01-T01 | Partial | Requires revision for `PC-001`, `PC-002` (`_number` overflow), and `PC-003`. |
| P01 / P01-T02 | Partial | Requires revision for `PC-002` and `PC-003`. |
| P02 / P02-T01 | Partial | Requires revision for `PC-001` (existing test alignment) and `PC-004` (namespace-safe, Ruff-clean worktree isolation in both test files). |
| P02 / P02-T02 | Covered | Concise `src/core/README.md` documentation and full verification command are well-scoped once `P01` and `P02-T01` revisions are applied. |

## Verdict

* Verdict: Revise
* Rationale: The architecture and additive design direction are sound, but four concrete, evidence-backed defects in `P01-T01`, `P01-T02`, and `P02-T01` would cause immediate existing-test regressions (`test_exposure_limits.py:38-44`), misclassify severe negative liquidity/covenant deficits as `Unknown` instead of `Breach`, permit Python 3.12 compact/week ISO dates to corrupt `approved_on` or silently drop human-supplied keys (`annual_plan` and unknown dict keys), and fail bare multi-file `unittest` or Ruff `E402` checks. Every finding is a direct, deterministic planner correction requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Alias-conflict rule breaks existing `test_exposure_limits.py:38-44` and ISO parser specification allows compact/week formats that corrupt `approved_on`

* Related IDs: Issue #99 AC1, Research C4, Research C6, P01-T01, P02-T01, P02-T02
* Evidence: src/core/tests/test_exposure_limits.py:18-24, src/core/tests/test_exposure_limits.py:38-44, src/core/src/zava_forward/core/exposure_limits.py:51-72, .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md
* Concern: First, `P01-T01` specifies that when both `approved_by` and `approver` (or both `approved_at` and `approved_on`) are present, `_approval()` raises `LimitsError` unless they match. However, `ExposureLimits.test_attribution_is_required_and_never_defaulted` in `src/core/tests/test_exposure_limits.py:38-44` explicitly calls `limits.record_limits(dict(APPROVAL, approved_by="Named person", approved_at="2026-01-01T10:00:00Z"), ENVELOPE, TOLERANCES)`, where `APPROVAL` already contains `approver="Test approver"` and `approved_on=(date.today() - timedelta(days=30)).isoformat()`. Implementing `P01-T01` without updating `test_exposure_limits.py:38-44` (or checking caller override semantics) guarantees a test failure in `P02-T02`. Second, `P01-T01` replaces the regex check with `date.fromisoformat` (when 10 chars) or `datetime.fromisoformat` (when `"T"` is supplied). In Python 3.12, `date.fromisoformat("2026-W01-1")` (10 chars) and `datetime.fromisoformat("20260101T100000")` (contains `"T"`) both succeed, setting `approved_on = approved_at[:10]` to `"2026-W01-1"` or `"20260101T1"`, so `record_limits()` accepts a record that later fails `date.fromisoformat(approved_on)` inside `stale_reason()`. Strings without `"T"` of length != 10 (such as `"2026-01-01 10:00:00"`) are also left implicit.
* Impact: Breaks `P02-T02` unit regression gate immediately and allows non-`YYYY-MM-DD` ISO strings to pass `record_limits()` while failing downstream `assess()` / `stale_reason()` reads.
* Smallest useful change: In `P01-T01`, require `approved_at[:10]` to match `r"\d{4}-\d{2}-\d{2}"` and parse via `date.fromisoformat(approved_at[:10])`; if `len(approved_at) > 10`, require `approved_at[10] == "T"`, no whitespace, and valid `datetime.fromisoformat(approved_at)` (rejecting all other lengths/separators), and apply the exact 10-char `YYYY-MM-DD` check to `approved_on`. For alias handling, update `P02-T01` to construct the canonical-attribution test dict in `src/core/tests/test_exposure_limits.py:38-44` without conflicting legacy keys (keeping the method, zero removals) while adding an explicit conflicting-alias `LimitsError` assertion.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` specifications in `.copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md` fixing the `YYYY-MM-DD` prefix + `datetime.fromisoformat` contract and updating `test_exposure_limits.py:38-44` so both existing and conflicting-alias tests pass.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Minimum-floor assessment misclassifies negative liquidity/covenant deficits as `Unknown` instead of `Breach`, defaults omitted scalar `covenant_unit`, and leaves `OverflowError` and non-dict `exposure` unguarded

* Related IDs: Issue #99 AC2, Research C1, Research C2, Research C5, P01-T01, P01-T02
* Evidence: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md, src/core/src/zava_forward/core/exposure_limits.py:39-49, src/core/src/zava_forward/core/exposure_limits.py:143-186, src/core/src/zava_forward/core/finance.py:366, src/core/tests/test_exposure_limits.py:123-127
* Concern: Four runtime correctness gaps exist in `P01-T02` (and `_number` in `P01-T01`):
  1. Applying `_comparable_observation` (`value >= 0`) to `liquidity` and `covenant` minimum-floor observations causes negative available cash (overdraft/deficit, e.g. `-50000`) or negative covenant headroom (underwater cover, e.g. `-0.15`) to return `state="Unknown"` (`"Exposure not supplied or not comparable"`) rather than `state="Breach"` (`"Below approved minimum"`). Unlike upper ceilings (`committed`, `tolerances`) where `< 0` would falsely satisfy `value <= maximum` (`"Within"`), any finite negative number compared against a non-negative floor `minimum >= 0` is strictly `< minimum` and represents a genuine financial breach that can never evaluate to `"Within"`.
  2. For scalar `covenant` observations, `P01-T02` specifies `exposure.get("covenant_unit", liq["covenant_unit"]) == liq["covenant_unit"]`, which defaults a missing `covenant_unit` to `liq["covenant_unit"]` so unitless scalar covenant observations silently match any unit, contradicting both the dict-form `covenant` rule (`requiring explicit unit if dict is used`) and the `envelope`/`liquidity` currency requirement.
  3. `assess()` keeps `exposure = exposure or {}` without checking `isinstance(exposure, dict)`, so a truthy non-dict `exposure` (such as `[]` or `"invalid"`) raises an unhandled `AttributeError` on `exposure.get(...)`.
  4. `_number()` in `exposure_limits.py:39-44` calls `math.isfinite(value)` directly on `int | float`; a huge integer (such as `10**400`, cf. `test_exposure_limits.py:124`) in `record_limits`, `load_limits`, or a forged raw `limits` dict passed to `assess()` raises `OverflowError` (`ArithmeticError`), which escapes `P01-T02`'s `except (LimitsError, KeyError, TypeError, ValueError)` guard.
* Impact: Severe liquidity deficits or underwater covenants are misreported as missing/incomparable data (`Unknown`) instead of an active `Breach`; unverified covenant units can falsely report `Within limits`; malformed runtime inputs to `assess()` or `_number()` can raise unhandled `AttributeError` or `OverflowError`.
* Smallest useful change: Update `P01-T01` and `P01-T02` so: (1) upper-ceiling observations (`committed`, optional `annual_plan`, `tolerances`) require `_non_negative_finite_observation` (`_finite_observation(v) and v >= 0`), whereas minimum-floor observations (`liquidity` available, `covenant` headroom) accept any `_finite_observation(v)` so negative finite deficits trigger `state="Breach"`; (2) scalar `covenant` observations require explicit `exposure.get("covenant_unit") == liq["covenant_unit"]` (no fallback to `liq["covenant_unit"]`); (3) `assess()` normalizes non-dict `exposure` (`exposure = exposure if isinstance(exposure, dict) else {}`, marking all findings `Unknown` when `exposure` was not a dict); and (4) `_number()` catches `OverflowError` around `float(value)` / `math.isfinite(...)` and raises `LimitsError`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, and `P02-T01` in `.copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md` and `.copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md` distinguishing non-negative ceiling observations from signed finite floor headroom, requiring explicit `covenant_unit`, guarding non-dict `exposure`, and catching `OverflowError` in `_number()`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Confirmed research `annual_plan` control (`RULE-011`) is omitted without disposition and unknown dict keys can be silently dropped across `load_limits`, `envelope`, `approval`, and `tolerances`

* Related IDs: Issue #99 AC1, Issue #99 AC2, Research C2, Research C4, P01-T01, P01-T02
* Evidence: .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md, .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md, .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md, src/core/src/zava_forward/core/exposure_limits.py:75-101, src/core/src/zava_forward/core/exposure_limits.py:217-231
* Concern: Research `C2`, Parent Synthesis and Disposition, Selected Recommendation, and Current Decisions explicitly confirmed adding optional human-approved `envelope["annual_plan"]` (`RULE-011` `AC-037`: board-approved investment envelope before exceeding annual plan), yet the Plan and Phase Details drop `annual_plan` completely without recording any scope exclusion or rationale. Compounding this, `record_limits` currently extracts only fixed keys from `envelope` (`amount`, `currency`, `period`), `approval`, and each `tolerances[name]` (`maximum`, `unit`), and `P01-T01` leaves top-level key checking in `load_limits` equivocal (`"also rejecting unknown top-level keys in load_limits if needed, or keeping..."`). Consequently, if a human supplies `"annual_plan": 80` inside `envelope`, `"liquidity_minimum": 50` at top level, or `"minimum": 5` inside `tolerances["capital"]`, the unrecognized key is silently discarded and `assess()` can return `"Within limits"` while ignoring a human-supplied limit.
* Impact: Breaks research-to-plan traceability for `RULE-011` (`AC-037`) and permits misspelled or extra control keys in human-supplied JSON/dicts to be silently ignored instead of failing closed (`LimitsError` / `Held`).
* Smallest useful change: In the Plan and `P01-T01`/`P01-T02`, include optional `annual_plan` in `envelope` (when present and not `None`, validated via `_number(..., "envelope annual_plan")`, preserved on `record["envelope"]["annual_plan"]`, and checked in `assess()` against `committed` as ceiling limit `"annual_plan"`), and enforce strict allowed-key sets raising `LimitsError` on unknown keys in top-level `load_limits` / `assess(limits, ...)` (`{"approval", "envelope", "tolerances", "liquidity"}`), `approval` (`{"approved_by", "approved_at", "approver", "approved_on", "role", "evidence_ref", "restart_owner"}`), `envelope` (`{"amount", "currency", "period", "annual_plan"}`), and each `tolerances[name]` (`{"maximum", "unit"}`), matching `liquidity`.
* Action owner: planning_parent
* Exact resolving evidence: Updated Plan requirements/scope and `P01-T01`/`P01-T02` details specifying optional `envelope["annual_plan"]` ceiling handling and strict unknown-key rejection across all input dicts.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Worktree `sys.path` bootstrap omits `test_exposure_limits.py`, misses PEP 420 namespace-package caching order, and collides with Ruff `E402`

* Related IDs: Research C8, NFR1, P02-T01, P02-T02
* Evidence: src/core/pyproject.toml:26-34, src/core/pyproject.toml:48-52, src/core/tests/test_issue_99_acceptance.py:1-7, src/core/tests/test_exposure_limits.py:1-15, .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md
* Concern: `P02-T01` adds the local worktree `src/` path guard only to `test_issue_99_acceptance.py`, leaving `test_exposure_limits.py` dependent on `PYTHONPATH=src:tests`. Because `zava_forward` / `zava_forward.core` are PEP 420 namespace packages (`src/core/pyproject.toml:26-28`) and `test_exposure_limits.py` (`test_e...`) sorts alphabetically before `test_issue_99_acceptance.py` (`test_i...`), any bare `python3 -m unittest` discovery spanning both files (or the full `tests/` directory) imports `zava_forward.core.exposure_limits` from `/home/azureuser/source/ama/src/core/src` first, caches it in `sys.modules`, fails the new unit tests in `test_exposure_limits.py`, and causes `test_issue_99_acceptance.py`'s `Path(limits.__file__).resolve()` assertion to fail even after `sys.path.insert(0, ...)`. Additionally, `src/core/pyproject.toml:34` enforces Ruff `"E"` (`E402` module-level import not at top of file) on both test files (neither is in `per-file-ignores`), so placing `sys.path.insert` statements above top-level `from zava_forward.core ...` imports will fail `python3 -m ruff check .` unless structured via `importlib` or explicit `# noqa: E402`.
* Impact: Multi-file bare `unittest` discovery loads stale sibling-worktree code from `~/.local`, and naive `sys.path` insertion fails the required `ruff check .` gate.
* Smallest useful change: In `P02-T01`, apply a tiny Ruff-clean bootstrap (using `importlib` or `# noqa: E402` on post-bootstrap imports) in both `test_issue_99_acceptance.py` and `test_exposure_limits.py` that prepends `Path(__file__).resolve().parents[1] / "src"` to `sys.path` and evicts any already-cached `zava_forward` / `zava_forward.core` / `zava_forward.core.exposure_limits` entries in `sys.modules` whose paths resolve outside this worktree's `src/` before importing `zava_forward.core`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T01` in `.copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md` specifying Ruff-clean (`E402`-compliant), `sys.modules`-safe worktree isolation in both `test_issue_99_acceptance.py` and `test_exposure_limits.py`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strong architectural boundary: Keeping `liquidity` (and `annual_plan`) optional preserves 100% 3-argument compatibility for `FinanceMixin.exposure_signal` (`src/core/src/zava_forward/core/finance.py:351-368`) and out-of-scope `src/api` callers while refusing unattributed or malformed inputs whenever supplied.
* Honest governance boundary: The plan strictly respects `OD-12` and `OD-15` by refusing to invent Zava North Homes thresholds, keeping `automatic_cut=False` on `pause_signal`, preserving upper-limit breach reason wording (`"Over approved limit: ..."`), and using `Refs #99` rather than a closing keyword.
* Disciplined test budget: The `<= 12` new test method cap easily accommodates all acceptance, boundary, and regression assertions across `test_issue_99_acceptance.py` and `test_exposure_limits.py` without bloat.
* Accepted residual risk: Real Zava North Homes Board/Finance figures (`OD-12`, `OD-15`) and web Finance workbench UI rendering of floor findings remain external/follow-up work outside `src/core`, explicitly recorded in the plan.

## Questions or Blocking Evidence Gaps

* none

## Limitations

* Out-of-scope `src/api` test files (`src/api/tests/test_finance_exposure_api.py` and `src/api/tests/test_finance_exposure_screen.py`) were not directly opened per the caller's bounded read scope; backward compatibility was assessed from `exposure_limits.py`, `finance.py`, and Research `C6`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md` and `.copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md` to incorporate `PC-001`, `PC-002`, `PC-003`, and `PC-004`, record their disposition in `Critique Disposition`, mark planning status ready, and proceed directly to `rpi-implement` without re-running critique.
* User response required: no
