<!-- markdownlint-disable-file -->
# Implementation Changes: Issue #216 Child Hardening Pass 5 (`216-citation-eval-2142-c5`)

* Task ID: 216-citation-eval-2142-c5
* Plan reference: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c5-plan.md
* Execution status: Complete

## `P01`: Enforce strict JSON-compatible comparison inputs and base-type canonical digest/replay invariance

* Completed `P01-T01` in `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Updated `_normalize_json_value` to tag exact base JSON primitives (`["null"]`, `["bool", value]`, `["str", value]`, `["int", str(value)]`, `["float", (0.0 if value == 0.0 else value).hex()]`) while letting primitive subclasses fall through to `["repr", ...]` (`PC-001`).
  * Added `_is_strict_json_value` (accepting only exact `None`, `bool`, `int`, `str`, finite `float`, non-bytes `Sequence`s, and `str`-keyed `Mapping`s) and `_normalize_cost_inputs_for_json` (serializing aware `datetime` `authority.expires_at` to `.isoformat()`; `PC-002`).
  * Enforced `_is_strict_json_value` in `agreement_gaps` and `compare_chat_against_rule_cards`, projected all 6 canonical case fields (`id`, `set_name`, `scenario`, `question`, `expected`, `actual`) and `normalized_cost_inputs` through `_to_plain_json`, verified `re_gates_check == dict(gates_report)` before recording `verified_comparison_inputs`, and sanitized fallback `beside_cost` rate/outcome fields (`RV-001`, `RV-002`, `PC-001`..`PC-003`).
* Completed `P01-T02` in `src/core/tests/test_regulatory_eval_gates_216.py`:
  * Added regression tests for non-serializable `scenario` (`object()`), `bytes` inside `expected`, mutating `str` subclasses (`_MutatingStr`), `NaN`/non-string `checks` inside unverified `gates_report`, and positive JSON round-trip replay with `tuple`, `UserDict`, `-0.0`, and aware `datetime` `authority.expires_at`.
  * Validation passed in `src/core`: `mypy` (318 source files), `ruff check .`, `ruff format --check .` (265 files), `test_*216*.py` (9 tests), `test_dependency_rule.py` (2 tests), `test_live_doc_links.py` (2 tests), `test_regulatory_chat.py` (25 tests), and `test_gates.py` (31 tests).
* Blockers: None.
* Remaining work: None in declared scope.
* Review readiness: Ready.
