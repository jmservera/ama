<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #108 Cycle 1 Independent Review Fixes and Parent Rebase

## Metadata

* Task ID: issue-108-heldout-eval-c1
* Task slug: ai-108-heldout-eval-c1
* Related plan: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-c1-research.md, .copilot-tracking/reviews/logs/2026-11-15/ai-108-heldout-eval-review.md

## Phase Index

| Phase ID | Name                                                                                             | Status    | Detail sections       |
|----------|--------------------------------------------------------------------------------------------------|-----------|-----------------------|
| P01      | Rebase onto Latest Parent Branch and Align `GET /api/ai/report`                                  | Complete | P01, P01-T01          |
| P02      | Content Standard Fix, Pinned Freeze Digests, Drift Check, and Statement Support in `heldout_eval` | Complete | P02, P02-T01, P02-T02 |
| P03      | Harden Tokenomics Candidate Comparison and Summary-Payload Guards                                | Complete | P03, P03-T01          |
| P04      | Regression Tests and Focused-Tier Validation                                                     | Complete | P04, P04-T01          |

<!-- rpi:phase id=P01 -->
## P01: Rebase onto Latest Parent Branch and Align `GET /api/ai/report`

### Context

`feat/ai-108-heldout-eval-0228` (`18dc9d132`) is stacked on `02ab20cac`, while `origin/feat/demo-164-chat-grounding-provenance-0900` advanced to `7f83f4749` (`#1761`). Commit `7f83f4749` modified `src/api/src/zava_forward/api/server.py` in `GET /api/ai/report` to import `chat_eval` alongside `ai_eval` and return `"chat_evaluation": chat_eval.run_eval()` as a top-level key (`C1`).

### Intent

Rebase cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` without losing untracked `c1` `.copilot-tracking/` files (none overlap tracked paths in `7f83f4749` or `18dc9d132`) and reconcile `GET /api/ai/report` so both `chat_evaluation` and `evaluation.{held_out,tokenomics_comparison}` are returned.

### Boundaries

* Included: `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, conflict resolution in `src/api/src/zava_forward/api/server.py`, and top-level key description update in `src/api/README.md`.
* Excluded: Force-pushing or modifying unrelated `chat_eval` / `regulatory_chat` files introduced by `7f83f4749`.

### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/README.md`

### Dependencies

* None.

### Validation Expectations

* `git merge-base --is-ancestor origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` exits 0 and `GET /api/ai/report` returns `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}`.

### Completion Evidence

* Rebase completes cleanly and `server.py` compiles and passes `ruff` and `mypy`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` and reconcile `server.py` and `src/api/README.md`

#### Context

In `server.py`, `7f83f4749` imports `from zava_forward.agents import ai_eval, chat_eval` and adds `"chat_evaluation": chat_eval.run_eval()` to the `GET /api/ai/report` response dict, whereas `18dc9d132` enriches `evaluation = dict(ai_eval.run_eval())` with `evaluation["held_out"]` and `evaluation["tokenomics_comparison"]`.

#### Intent

Run `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`; if `server.py` conflicts during `git rebase`, resolve it by keeping `from zava_forward.agents import ai_eval, chat_eval`, keeping the `evaluation["held_out"]` and `evaluation["tokenomics_comparison"]` enrichment, and returning `"chat_evaluation": chat_eval.run_eval()` alongside `"evaluation"`, `"live"`, `"registry"`, and `"consumption"`, then finish the rebase with `GIT_EDITOR=true git rebase --continue` and update `src/api/README.md` to mention `chat_evaluation` among preserved top-level keys.

#### Boundaries

* Included: `server.py` `GET /api/ai/report` merge resolution and `src/api/README.md` top-level key list.
* Excluded: Changing `chat_eval.run_eval()` semantics.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/README.md`

#### Dependencies

* None.

#### Validation Expectations

* `git status` shows clean rebase completion on `feat/ai-108-heldout-eval-0228` ahead of `7f83f4749`.

#### Completion Evidence

* Rebased commit sits cleanly atop `7f83f4749`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Content Standard Fix, Pinned Freeze Digests, Drift Check, and Statement Support in `heldout_eval.py`

### Context

Independent review Findings 1, 2, 4, and 5 identify four issues in `src/core/src/zava_forward/core/heldout_eval.py` (and `src/core/README.md`):
1. Unauthorized `"human-approved"` strings violate `CopyAudit.test_ai_label_is_exact_and_never_implies_approval` (`C2`, `C3`, `C4`).
2. `canonical_heldout_manifest()` calls `approve_manifest(...)` dynamically on live `_capability_version_snapshot()` instead of pinning `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` for `HELDOUT-FREEZE-2026-10-15`, and `check_heldout_freeze()` does not detect live capability-version drift (`C5`, `C6`, `C9`).
3. `_evaluate_assistant_case()` and `_evaluate_legacy_case()` lack `_check_statement_support()` to flag ungrounded `\b\d+\b` numbers and `ZF-*` case IDs (`C7`).
4. `evaluate_heldout()` gates per-case scoring on `not freeze["blockers"]` rather than `freeze["ready_for_evaluation"]` (`C8`).

### Intent

Fix all four `heldout_eval` / `src/core/README.md` items cleanly while preserving 16/16 pass behavior on the canonical offline baseline suite.

### Boundaries

* Included: `src/core/src/zava_forward/core/heldout_eval.py` and `src/core/README.md`.
* Excluded: Network calls or changes to `assistants.py` / `ai_tasks.py`.

### Likely Targets

* `src/core/src/zava_forward/core/heldout_eval.py`
* `src/core/README.md`

### Dependencies

* P01.

### Validation Expectations

* `test_content_standard.py` and `test_heldout_eval.py` pass, `mypy` and `ruff` pass in `src/core`.

### Completion Evidence

* Static `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` constants match `canonical_heldout_manifest()`, live capability drift produces `"capability_version_drift:..."` blockers, ungrounded numbers/`ZF-*` IDs increment `unsupported_claims`, and unmet sample floors skip per-case scoring (`evaluated_total == 0`, `outcome == "insufficient"`).

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Replace `"human-approved"` wording and pin `FROZEN_THRESHOLDS_DIGEST` / `FROZEN_MANIFEST_DIGEST` with live drift checks

#### Context

`CopyAudit.test_ai_label_is_exact_and_never_implies_approval` forbids `"human-approved"` unless followed by `" by"`. Meanwhile, `canonical_heldout_manifest()` must never dynamically sign live mutated prompt/policy/task versions at runtime.

#### Intent

1. Replace `"human-approved"` with `"human-authorized"` in `src/core/src/zava_forward/core/heldout_eval.py` (module docstring and `canonical_heldout_manifest` docstring) and `src/core/README.md`.
2. Define module constants in `heldout_eval.py`:
   * `CANONICAL_FREEZE_ID = "HELDOUT-FREEZE-2026-10-15"`
   * Static `FROZEN_VERSIONS: dict[str, str]` and `FROZEN_CAPABILITY_VERSIONS: dict[str, dict[str, str]]` capturing the exact frozen versions at `HELDOUT-FREEZE-2026-10-15` (so live edits to `assistants` or `ai_prompts` do not mutate the canonical frozen manifest!).
   * `FROZEN_THRESHOLDS_DIGEST = "<64-hex-sha256>"` and `FROZEN_MANIFEST_DIGEST = "<64-hex-sha256>"` pinned as literal 64-char hex constants, embedded directly inside `canonical_heldout_manifest()["threshold_approval"]` (alongside `"freeze_id": CANONICAL_FREEZE_ID` on the manifest) without calling `approve_manifest(...)` at runtime.
3. In `check_heldout_freeze(manifest, *, live=False)`:
   * Compare `manifest.get("capability_versions")` against live `_capability_version_snapshot()` across `("task", "model", "prompt", "policy", "source")` for every capability in `ALL_CAPABILITIES` that has a valid version map. Whenever any key differs from live `_capability_version_snapshot()`, collect `f"{cap}.{vkey}"` into `drifted`, include `"drifted_capability_versions": drifted` on the freeze dict, and append both `"capability_version_drift"` and `f"capability_version_drift:{','.join(drifted)}"` to `blockers`. Also enforce non-string sequence guards (`not isinstance(..., (str, bytes, bytearray))`) in `check_prompt_tuning_isolation()` for `rendered_prompts` and `tuning_examples` (raising `ValueError` on bare strings/bytes).
4. In `evaluate_heldout(..., expected_serving_model: str | None = None)`:
   * Validate optional `expected_serving_model` (if provided, must satisfy `rai_release.named`; otherwise raise `ValueError`) and use `expected_serving_model.strip()` instead of `frozen_versions.get("model")` when checking per-case response `serving_version` / `provider_result.model` mismatches, while recording both `expected_frozen_model` and `expected_serving_model` in `actual_serving_version` and keeping `manifest` immutable.
5. In `baseline_candidate_from_evaluation()`:
   * Include `"manifest_digest": hashes.get("manifest_digest")` and `"seed": evaluation.get("seed")` on the returned baseline dict so `tokenomics_comparison._validate_baseline_artifact` binds baselines directly to `freeze["manifest_digest"]`.

#### Boundaries

* Included: `heldout_eval.py` constants, `canonical_heldout_manifest`, `check_heldout_freeze`, `evaluate_heldout`, `baseline_candidate_from_evaluation`, and `src/core/README.md`.
* Excluded: Re-signing manifests dynamically inside `canonical_heldout_manifest`.

#### Likely Targets

* `src/core/src/zava_forward/core/heldout_eval.py`
* `src/core/README.md`

#### Dependencies

* P01.

#### Validation Expectations

* `test_content_standard.py` passes; `check_heldout_freeze(canonical_heldout_manifest())` has `frozen=True` and `manifest_digest == FROZEN_MANIFEST_DIGEST`; monkeypatching a prompt/policy/task version triggers `capability_version_drift`.

#### Completion Evidence

* Literal `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` constants verified by unit tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add `_check_statement_support()` for numbers and `ZF-*` IDs and gate scoring on `freeze["ready_for_evaluation"]`

#### Context

Candidate statements that preserve valid citation tags and `required_tokens` could previously inject invented numeric claims (`\b\d+\b`) or foreign `ZF-*` case IDs without incrementing `unsupported_claims`, and `evaluate_heldout()` scored individual cases even when `not freeze["sample_sufficient"]`.

#### Intent

1. Add `_check_statement_support(statement: str, grounded_corpus: str) -> list[str]` in `heldout_eval.py`:
   * Strip 64-character SHA-256 hex digests (`re.sub(r"\b[0-9a-f]{64}\b", " ", grounded_corpus, flags=re.IGNORECASE)`) from `grounded_corpus` first so hex substrings inside `survey.evidence_hash`, `funding.terms_hash`, or `content_sha256` cannot accidentally ground invented numbers.
   * Extract grounded `ZF-*` identifiers (`{m.casefold() for m in re.findall(r"\bZF-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b", cleaned_corpus, flags=re.IGNORECASE)}`) and grounded digit tokens (`set(re.findall(r"\d+", cleaned_corpus))`).
   * On `statement`, strip bracketed citation markers `[[...]]` and fixed UK retrofit standard designations (`\bPAS\s+2035\b`, `\bPAS\s+2030\b`, case-insensitive) so standard titles are not treated as case measurements.
   * Scan `statement` for `\bZF-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b` (case-insensitive): any match not in grounded `ZF-*` IDs is recorded as an ungrounded token; remove `ZF-*` spans before scanning `\b\d+\b` so a foreign `ZF-HO-999` is counted cleanly rather than double-counted for `999`.
   * Scan the remaining text for `\b\d+\b`: any number token not in grounded digit tokens is recorded as an ungrounded token.
   * Return the list of ungrounded tokens.
2. Call `_check_statement_support` in:
   * `_evaluate_assistant_case()`: build `grounded_corpus` from `json.dumps({"case_id": fixture["record"]["id"], "sources": snap["sources"], "citations": list(snap["citations"].keys())}, sort_keys=True)` and check `output["summary"]` and each `finding["text"]`. If any ungrounded tokens are returned, increment `unsupported_claims += len(ungrounded)`, set `passed = False`, and append `"unsupported_factual_claim"` to `critical_errors` (if not already present).
   * `_evaluate_legacy_case()`: build `grounded_corpus` from `json.dumps(sources, sort_keys=True)`:
     * For `priority`, check each validated item's `reason` string against `json.dumps({item["case_id"]: sources.get(item["case_id"], [])})`.
     * For text/bullet families (`briefing`, `message`, `summary`, `funding_draft`, `read_document`), check each statement `st["text"]` from `statements`.
     * Any ungrounded tokens increment `unsupported_claims += len(ungrounded)`, set `passed = False`, and append `"unsupported_factual_claim"` to `critical_errors` (if not already present).
3. In `evaluate_heldout()`, change `if not freeze["blockers"] and isolation["isolated"]:` to `if freeze["ready_for_evaluation"] and isolation["isolated"]:` so unmet sample floors (`not freeze["sample_sufficient"]`) skip per-case scoring (`case_results == []`, `evaluated_total == 0`) while keeping `outcome == "insufficient"` and preserving `denominators` and `insufficient_reasons`.

#### Boundaries

* Included: `_check_statement_support`, `_evaluate_assistant_case`, `_evaluate_legacy_case`, and `evaluate_heldout` in `heldout_eval.py`.
* Excluded: Modifying `core.ai_tasks.analyse` global behavior outside `heldout_eval`.

#### Likely Targets

* `src/core/src/zava_forward/core/heldout_eval.py`

#### Dependencies

* P02-T01.

#### Validation Expectations

* All 16 canonical baseline responses pass (`unsupported_claims == 0`); injected ungrounded numbers (`99 days`, `45%`) or foreign case IDs (`ZF-HO-999`) fail with `unsupported_claims > 0` and `"unsupported_factual_claim"`; unmet cohort floors yield `evaluated_total == 0` and `outcome == "insufficient"`.

#### Completion Evidence

* Unit tests in `test_heldout_eval.py` cover assistant and legacy ungrounded number/`ZF-*` injection and sample-floor short-circuiting.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Harden Tokenomics Candidate Comparison and Summary-Payload Guards

### Context

Independent review Findings 2 and 3 identify bypasses in `src/core/src/zava_forward/core/tokenomics_comparison.py`:
1. `_manifest_for_candidate_model()` mutates `versions["model"]` and calls `approve_manifest(...)` at runtime (`C11`).
2. `_validate_baseline()` does not verify `baseline.get("manifest_digest") == freeze["manifest_digest"]` (`C10`).
3. Summary-only candidates (omitting `responses`) default missing `accepted_case_ids` to `case_ids` and missing `evaluation_outcome` to `"pass"`, omit `gate_failures`, skip `candidate_usage.currency == baseline_usage.currency` checks, and never pass candidate `lever_config.get("prompt")` values through `check_prompt_tuning_isolation()` (`C12`).

### Intent

Eliminate dynamic manifest re-signing and close all summary-only, currency, baseline-digest, and candidate prompt-lever isolation bypasses in `tokenomics_comparison.py`.

### Boundaries

* Included: `src/core/src/zava_forward/core/tokenomics_comparison.py`.
* Excluded: Breaking `POST /api/ai/candidate-comparison` route signatures for well-formed payloads.

### Likely Targets

* `src/core/src/zava_forward/core/tokenomics_comparison.py`

### Dependencies

* P02.

### Validation Expectations

* `test_tokenomics_comparison.py` and `test_heldout_eval_api.py` pass with strict negative tests for every closed bypass.

### Completion Evidence

* Zero `approve_manifest` calls exist in `tokenomics_comparison.py`; all four summary/baseline/currency/isolation invariants are enforced and reported.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Remove manifest re-signing and enforce summary verification, currency parity, baseline digest binding, and prompt-lever isolation

#### Context

Callers of `compare_candidates()` (including `POST /api/ai/candidate-comparison`) may submit either full `responses` or pre-evaluated summary metrics. Summary metrics must never get implicit `"pass"` or implicit accepted-case defaults, cross-currency subtraction, unbound baselines, or uninspected prompt-lever text.

#### Intent

1. Delete `_manifest_for_candidate_model()` from `tokenomics_comparison.py`. When `isinstance(candidate.get("responses"), Mapping)`, pass `manifest` untouched to `heldout_eval.evaluate_heldout(manifest, candidate["responses"], rendered_prompts=cand_prompt_texts, tariff=cand_tariff, offline_scripted=offline_flag, expected_serving_model=cand_levers["model"])`.
2. Rename/alias `_validate_baseline_artifact(baseline, frozen_case_ids, freeze, approval_manifest_digest, default_tariff)` (retaining `_validate_baseline` alias):
   * Require `rai_release.named(baseline.get("manifest_digest"))`, raising `ValueError("Baseline must include a non-empty manifest_digest.")` when missing or blank.
   * When `freeze["frozen"]` is `True` (or when `rai_release.named(approval_manifest_digest)` and `str(baseline["manifest_digest"]).strip() != str(approval_manifest_digest).strip()`), verify `str(baseline["manifest_digest"]).strip() == freeze["manifest_digest"]`, raising `ValueError("Baseline manifest_digest must match the frozen held-out manifest_digest.")` on mismatch; when `not freeze["frozen"]` due to post-approval manifest tampering, also append `"baseline_manifest_digest_mismatch"` to `suite_blockers` if `str(baseline["manifest_digest"]).strip() != freeze["manifest_digest"]`.
   * Extract and validate `base_currency` as a non-empty string (`rai_release.named(usage_raw.get("currency"))`, raising `ValueError` if missing/blank).
3. Harden `_extract_candidate_metrics()` across both `responses` and summary-only branches:
   * On the `responses` branch, populate `"gate_failures"` (`list(eval_report.get("insufficient_reasons", []))` plus `f"eval_outcome:{eval_report['outcome']}"` if `eval_report["outcome"] != "pass"`).
   * On the summary-only branch (when `responses` is absent):
     - Require `"evaluation_outcome" in candidate` and `candidate["evaluation_outcome"] in heldout_eval.OUTCOMES` (never defaulting missing `evaluation_outcome` to `"pass"`; raise `ValueError` if missing or invalid).
     - Require `"accepted_case_ids" in candidate` as a non-string sequence whose elements are a subset of `case_ids` (never defaulting missing `accepted_case_ids` to `case_ids`; raise `ValueError` if missing, non-sequence, or containing IDs outside `case_ids`).
     - Require `"gate_failures" in candidate` as a non-string sequence of `rai_release.named` strings (raise `ValueError` if missing, non-sequence, or containing blank/non-string entries), storing normalized `gate_failures` in metrics, folding `evaluation_outcome`, `sorted(accepted_ids)`, and `gate_failures` into the summary `evaluation_digest`, and appending `f"candidate_gate_failure:{gf}"` to `failure_reasons` whenever `gate_failures` is non-empty.
     - On non-offline summary candidates (`not offline_flag`) where `rai_release.named(actual_serving)`, compare `actual_serving` against `expected_serving` when set or `cand_levers["model"]` otherwise.
4. Enforce currency parity (`candidate_usage.currency == baseline_usage.currency`):
   * Extract candidate usage currency (`cand_currency = usage_dict.get("currency")`). If `usage_dict` is non-empty and `not rai_release.named(cand_currency)`, raise `ValueError("Candidate usage must specify a non-empty currency.")`. Whenever `rai_release.named(cand_currency)` and `str(cand_currency).strip() != base_currency`, record `"currency_mismatch"` (`f"currency_mismatch:{str(cand_currency).strip()}!={base_currency}"`) in `failure_reasons` and forbid cost delta subtraction (`nominal_delta_str = ai_consumption.UNKNOWN`, `net_saving_str = "0.000000"`, `cheaper_nominal = False`, `is_saving = False`). Also verify candidate tariff currency (if `responses` + `tariff` used) matches `base_currency` in the same way.
5. Candidate prompt-lever isolation (`holdout_leakage_clear`):
   * Reject bare `str | bytes | bytearray` (raising `ValueError`) for top-level and per-candidate `rendered_prompts` and `tuning_examples`.
   * For each candidate, inspect `cand_levers["prompt"]` (plus any validated optional `candidate.get("rendered_prompts")` strings) through `heldout_eval.check_prompt_tuning_isolation(manifest, rendered_prompts=[*validated_rendered_prompts, cand_levers["prompt"], ...], tuning_examples=validated_tuning_examples)`.
   * Record `"holdout_leakage_clear": bool(cand_isolation["isolated"])` on each evaluated candidate row and at the suite level (`"holdout_leakage_clear": bool(suite_isolation["isolated"] and all(c["holdout_leakage_clear"] for c in evaluated_candidates))`). If `not cand_isolation["isolated"]`, append `"prompt_or_tuning_heldout_leak"` to that candidate's `failure_reasons` so `outcome == "failure"` and `is_saving is False`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/tokenomics_comparison.py`.
* Excluded: Altering `Decimal` precision formatting (`6` decimal places) for valid same-currency candidates.

#### Likely Targets

* `src/core/src/zava_forward/core/tokenomics_comparison.py`

#### Dependencies

* P02-T01.

#### Validation Expectations

* Unit and API tests verify rejection of missing `evaluation_outcome` / `accepted_case_ids` / `gate_failures`, non-empty `gate_failures`, `USD` vs `GBP` currency mismatch, tampered `baseline["manifest_digest"]`, and held-out case ID or 6-word answer shingle inside `lever_config["prompt"]`.

#### Completion Evidence

* `tokenomics_comparison.py` passes `mypy`, `ruff`, `test_tokenomics_comparison.py`, and `test_heldout_eval_api.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Regression Tests and Focused-Tier Validation

### Context

Existing summary-candidate fixtures in `test_tokenomics_comparison.py` and `test_heldout_eval_api.py` must include explicit `evaluation_outcome` and `gate_failures`, `test_heldout_eval_api.py` must expect `"chat_evaluation"` in `GET /api/ai/report` after rebase onto `7f83f4749`, and dedicated focused tests must verify every resolved review finding before committing.

### Intent

Lock test governance (`0` removals, `0` new test files, `<= 16` new focused test methods across the 3 branch test files), update existing test fixtures, add negative regression cases for Findings 1–5, run the full Focused-tier validation command set, and prepare a clean workspace for `rpi-review`.

### Boundaries

* Included: `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py`, and Focused-tier validation runs.
* Excluded: Deleting existing assertions, creating extra test files, or running Docker/complete gate commands.

### Likely Targets

* `src/core/tests/test_heldout_eval.py`
* `src/core/tests/test_tokenomics_comparison.py`
* `src/api/tests/test_heldout_eval_api.py`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* Focused-tier commands (using `.venv/bin` when present, respecting `pyproject.toml` legacy exclusions on untouched `v0.21.0` files while also verifying `--isolated --line-length 100` on all Cycle 1 modified files):
  * `PYTHONPATH=src/core/src:src/core/tests:src/api/src:src/api/tests:src/agents/src python3 -m unittest src/api/tests/test_content_standard.py src/core/tests/test_heldout_eval.py src/core/tests/test_tokenomics_comparison.py src/api/tests/test_heldout_eval_api.py src/api/tests/test_role_endpoint_inventory.py -v`
  * `(cd src/core && ../.venv/bin/python -m mypy && ../.venv/bin/python -m ruff check src tests && ../.venv/bin/python -m ruff format --check src tests && ../.venv/bin/python -m ruff check --isolated src/zava_forward/core/heldout_eval.py src/zava_forward/core/tokenomics_comparison.py tests/test_heldout_eval.py tests/test_tokenomics_comparison.py && ../.venv/bin/python -m ruff format --isolated --line-length 100 --check src/zava_forward/core/heldout_eval.py src/zava_forward/core/tokenomics_comparison.py tests/test_heldout_eval.py tests/test_tokenomics_comparison.py)`
  * `(cd src/api && PYTHONPATH=../core/tests:../agents/tests ../.venv/bin/python -m mypy && ../.venv/bin/python -m ruff check src tests && ../.venv/bin/python -m ruff format --check src tests && ../.venv/bin/python -m ruff check --isolated tests/test_heldout_eval_api.py && ../.venv/bin/python -m ruff format --isolated --line-length 100 --check tests/test_heldout_eval_api.py)`
  * `python3 tools/rename-zava-tests.py`

### Completion Evidence

* All four validation commands exit 0 with zero skips or errors.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Update and expand `test_heldout_eval.py`, `test_tokenomics_comparison.py`, and `test_heldout_eval_api.py` and run Focused validation

#### Context

Each of the 5 findings needs a focused regression test that would fail on `18dc9d132` and passes after `P01`–`P03`.

#### Intent

1. In `src/core/tests/test_heldout_eval.py`:
   * Verify `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` match `canonical_heldout_manifest()` (`freeze_id == "HELDOUT-FREEZE-2026-10-15"`).
   * Verify mutating a live capability version (e.g. patching `ai_prompts.PROMPTS["briefing"]` or passing a manifest with stale `capability_versions`) appends `"capability_version_drift:..."` to `check_heldout_freeze()["blockers"]` and fails `evaluate_heldout()`.
   * Verify injecting an ungrounded number (`99`) or foreign `ZF-*` identifier (`ZF-HO-999`) into an otherwise cited assistant finding and legacy statement increments `unsupported_claims` and fails with `"unsupported_factual_claim"`.
   * Verify unmet cohort sample floor skips per-case scoring (`evaluated_total == 0`, `cases == []`, `outcome == "insufficient"`).
2. In `src/core/tests/test_tokenomics_comparison.py`:
   * Update all existing non-schema-error summary-only test fixtures (both passing and quality-regression cases) with explicit `"evaluation_outcome": "pass"` and `"gate_failures": []`.
   * Add tests verifying: (a) omitting `evaluation_outcome`, `accepted_case_ids`, or `gate_failures` on a summary candidate raises `ValueError`, and non-empty `gate_failures` forces `outcome == "failure"` (`is_saving=False`); (b) mismatched currency (`USD` vs `GBP`) fails closed (`currency_mismatch`, `is_saving=False`); (c) mismatched or missing `baseline["manifest_digest"]` raises `ValueError`; (d) embedding a held-out case ID (`HO-AST-FE-02`) or 6-word `expected_answer` shingle in candidate `lever_config["prompt"]` sets `holdout_leakage_clear=False` and fails the candidate (and bare-string `rendered_prompts` raises `ValueError`); and (e) model-lever response candidates preserve `manifest_digest == heldout_eval.FROZEN_MANIFEST_DIGEST` without re-signing.
3. In `src/api/tests/test_heldout_eval_api.py`:
   * Update `test_get_ai_report_preserves_top_level_keys_and_embeds_heldout_summaries` to expect `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}`.
   * Update all non-schema-error summary candidates in `test_post_candidate_comparison_evaluates_candidates_and_records_audit_entry` (both `cheap-valid-caching` and `cheap-regresses-overrides`) with `"evaluation_outcome": "pass"` and `"gate_failures": []`, and assert HTTP 400 when summary candidates omit `evaluation_outcome` / `accepted_case_ids` / `gate_failures` or pass a tampered baseline `manifest_digest`.
4. Run all Focused-tier validation commands from Exact Task step 6 (plus `test_ai_consumption_api.py` targeted report test if helpful).

#### Boundaries

* Included: The 3 branch test files and Focused validation commands.
* Excluded: Unrelated test files.

#### Likely Targets

* `src/core/tests/test_heldout_eval.py`
* `src/core/tests/test_tokenomics_comparison.py`
* `src/api/tests/test_heldout_eval_api.py`

#### Dependencies

* P01, P02, P03.

#### Validation Expectations

* All Focused-tier commands exit 0.

#### Completion Evidence

* Full command exit codes and counts recorded in `.copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-c1-changes.md`.

#### Unresolved Items

* None.
