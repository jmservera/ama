<!-- markdownlint-disable-file -->

# Task Research: ai-108-heldout-eval-c1

| Field              | Value                                                                  |
|--------------------|------------------------------------------------------------------------|
| Date               | 2026-11-15                                                             |
| Researcher / agent | RPI Agent (`rpi-research`)                                             |
| Status             | Complete                                                               |
| Artifact path      | .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-c1-research.md |

## Research Brief

* What to research: Exact root causes, cross-module contracts, and parent-branch rebase interactions for Cycle 1 (`c1`) of Issue #108 on `feat/ai-108-heldout-eval-0228`, addressing `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) and all 5 findings from the independent exact-head review (`18dc9d132`).
* Why it matters: Before pushing `feat/ai-108-heldout-eval-0228` and opening its stacked PR against `feat/demo-164-chat-grounding-provenance-0900`, the branch must cleanly incorporate parent commit `7f83f4749`, pass `CopyAudit.test_ai_label_is_exact_and_never_implies_approval`, pin frozen manifest digests with live capability-version drift detection, close summary-only candidate comparison bypasses, detect injected ungrounded numbers/`ZF-*` case IDs, and enforce the pre-scoring sample-sufficiency gate.
* Audience or intended use: RPI planning, critique, implementation, and review for Cycle 1 (`c1`) of `feat/ai-108-heldout-eval-0228` (`Refs #108`).
* Scope: `src/core/src/zava_forward/core/heldout_eval.py`, `src/core/src/zava_forward/core/tokenomics_comparison.py`, `src/core/README.md`, `src/api/src/zava_forward/api/server.py`, `src/api/README.md`, `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py`, and parent commit `7f83f4749`.
* Non-goals: Live Azure OpenAI calls, actual human participant runs, Docker/full gate execution (Focused tier applies), or pushing to `origin`.
* Criteria: Resolve all 5 independent review findings plus rebase conflicts/test updates cleanly with zero regressions under `unittest`, `mypy`, `ruff check`, `ruff format --check`, and `tools/rename-zava-tests.py`.
* Requested outputs: Convergence design for all 6 remediation work items (`c1` rebase + 5 findings).
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How do parent commit `7f83f4749` and the 5 review findings interact with `heldout_eval.py`, `tokenomics_comparison.py`, `server.py`, and tests? |
| Codebase scope                       | `src/core`, `src/api`, `tools/rename-zava-tests.py`, `origin/feat/demo-164-chat-grounding-provenance-0900`                                 |
| External scope                       | none                                                                                                                                       |
| Initial internal candidate areas     | `heldout_eval.py`, `tokenomics_comparison.py`, `server.py`, `test_content_standard.py`, `test_heldout_eval.py`, `test_tokenomics_comparison.py`, `test_heldout_eval_api.py` |
| Initial external candidate areas     | none                                                                                                                                       |
| Research posture                     | focused                                                                                                                                    |
| Posture provenance                   | bounded remediation task with named source targets and supplied independent review findings                                                |
| Explicit limits / deadline           | Focused validation tier (no Docker/full gate); commit locally without pushing                                                              |
| Posture-specific completion basis    | focused scope coverage with complete `path:line` evidence across all 5 findings and parent rebase diff                                     |
| Edits allowed during research?       | no, research-only                                                                                                                          |
| Resolved evidence root               | .copilot-tracking/                                                                                                                         |
| Known constraints / excluded sources | Preserve `src/core` stdlib-only rule; preserve immutable frozen manifest digest; never put `.copilot-tracking/` paths in code/docs/commits |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                        | Scoped authority or output contract                      | Selected / skipped reason                                                       |
|---------------------|-----------------------------------|---------------------------------------------|----------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` repository-wide instruction | AMA content standard, validation tiers, and stacked branch rules | Selected: governs plain-language copy rules, focused tier, and stacked PR workflow |
| Research specialist | `hve-core-all:rpi-researcher`     | Available subagent for independent lanes    | Separate lane artifact                                   | Skipped: all 5 findings target 3 tightly coupled files inspectable directly inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                               | Answers / unanswered  | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------|-----------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive execution with explicit findings, file lines, and validation commands | N/A (non-interactive) | Proceed with `focused` posture and `convergence` output mode                    |
| Direction change | None                                                                                | N/A                   | Keep exact caller scope                                                         |
| Convergence      | Complete codebase and git diff evidence resolves every design question unambiguously | N/A (non-interactive) | Converged on pinned freeze constants, immutable candidate model override, fail-closed summary schema, grounded number/`ZF-*` checks, and `chat_evaluation`-aware rebase |

## Scope and Success Criteria

* Scope: Parent branch rebase (`7f83f4749`) and resolution of Findings 1 through 5 across `src/core` and `src/api`.
* Assumptions: `origin/feat/demo-164-chat-grounding-provenance-0900` is the active stacked parent branch and has advanced by 1 commit (`7f83f4749`) since `02ab20cac`.
* Success criteria:
  * Every research question is answered with exact `path:line` codebase evidence (`C1`–`C15`).
  * Rebase conflicts and cross-test interactions with `7f83f4749` are identified before editing.
  * Alternatives and edge cases (e.g., legitimate numbers in canonical baseline responses, summary-only candidate callers in tests) are analyzed in the Contrarian wave.
  * Zero source edits occur during Research.

## Task Research Requests

* Explicit requests:
  1. Rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900`.
  2. Replace forbidden `"human-approved"` wording in `heldout_eval.py` and `src/core/README.md`.
  3. Pin `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` for `HELDOUT-FREEZE-2026-10-15`, check live `_capability_version_snapshot()` drift in `check_heldout_freeze()`, and stop re-signing mutated manifests in `tokenomics_comparison.py`.
  4. Close summary-only bypasses in `tokenomics_comparison.py` (explicit `evaluation_outcome`, `accepted_case_ids`, `gate_failures`; `currency` match; `baseline["manifest_digest"]` check; candidate `lever_config["prompt"]` leakage check).
  5. Flag ungrounded numbers (`\b\d+\b`) and `ZF-*` identifiers in `_check_statement_support`, and gate per-case scoring in `evaluate_heldout()` on `freeze["ready_for_evaluation"]`.
* Inferred research questions: What changed on `origin/feat/demo-164-chat-grounding-provenance-0900`? Which numbers/`ZF-*` tokens appear in canonical baseline responses vs captured sources? Which existing tests omit newly required summary candidate fields?

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                    | Source / checkpoint | Effect on active brief, evidence, or revalidation               |
|----------------------------------------------------------|----------------------------------------------------------|---------------------|-----------------------------------------------------------------|
| narrow                                                   | Focused validation tier; no Docker or full local gate    | Caller prompt       | Validate via targeted `unittest`, `mypy`, `ruff`, and rename audit |
| exclude                                                  | Do not push branch to remote                             | Caller prompt       | Commit locally and leave `git status --short` empty             |

## Research Questions

|  # | Sub-question                                                                                                                | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What changed on `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) and how does it affect our diff?        | breadth         | H        | answered |
| Q2 | Where does `"human-approved"` appear across `src/`, and what exact rule does `test_content_standard.py` enforce?             | straightforward | H        | answered |
| Q3 | How should `FROZEN_THRESHOLDS_DIGEST`, `FROZEN_MANIFEST_DIGEST`, live version drift, and candidate model override work?      | depth           | H        | answered |
| Q4 | How do summary-only candidates, baseline projection, currency parity, and prompt-lever isolation interact in `core` + `api`? | depth           | H        | answered |
| Q5 | How should `_check_statement_support` validate `\b\d+\b` and `ZF-*` tokens without false positives on canonical responses?   | depth           | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/ai-108-heldout-eval-research.md`, `.copilot-tracking/reviews/logs/2026-11-15/ai-108-heldout-eval-review.md` (`RV-001`–`RV-004`), and the independent exact-head functional review for `18dc9d132`.
* Reused (verified) findings: `zava_forward.core` remains stdlib-only (`ALLOWED = {"core"}`) and all evaluation logic must remain deterministic and network-free.
* New parent commit discovered: `origin/feat/demo-164-chat-grounding-provenance-0900` moved from `02ab20cac` to `7f83f4749` (`#1761`).

## Cycle 1 Execution

### Wave 1: Wider (Inline)

* Inspected `git fetch origin` state (`7f83f4749`), `src/` grep matches for `"human-approved"` (`C2`, `C3`, `C4`), all files touched on `feat/ai-108-heldout-eval-0228`, and parent diff `02ab20cac..7f83f4749` (`C1`).
* Inline disposition: Direct inline inspection used because the entire working set spans 8 files in one repository.
* Findings:
  * **Parent branch advance (`Q1`, `C1`)**: `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by commit `7f83f4749`, which modified `src/api/src/zava_forward/api/server.py` (`GET /api/ai/report`) to import `chat_eval` alongside `ai_eval` and return `"chat_evaluation": chat_eval.run_eval()` as a fifth top-level key alongside `"evaluation"`, `"live"`, `"registry"`, and `"consumption"`. Rebasing `18dc9d132` onto `7f83f4749` intersects at `server.py` lines 907–941 and requires updating `test_heldout_eval_api.py:97` (`C14`) and `src/api/README.md:15` (`C15`) to include `"chat_evaluation"` in the top-level `GET /api/ai/report` key set.
  * **Content standard violation (`Q2`, `C2`, `C3`, `C4`)**: `CopyAudit.test_ai_label_is_exact_and_never_implies_approval` (`C2`) strips `"human-approved by"` and asserts `"human-approved"` never appears in any `src/api/src/zava_forward/api/*.py` or `src/core/src/zava_forward/core/*.py` file. Grep across `src/` shows the only unauthorized hits are `heldout_eval.py:4`, `heldout_eval.py:1397` (`C3`), and `src/core/README.md:15` (`C4`). Replacing `"human-approved"` with `"human-authorized"` (or `"person-reviewed"`) clears `test_content_standard.py` completely.

### Wave 2: Deeper (Inline)

* Inspected `heldout_eval.py` (`C5`, `C6`, `C7`, `C8`, `C9`) and `tokenomics_comparison.py` (`C10`, `C11`, `C12`) alongside `assistants.capture()` (`C13`) and existing unit/API tests (`C14`).
* Findings:
  * **Pinned frozen digests, live capability-version drift, and immutable model lever (`Q3`, `C5`, `C6`, `C9`, `C11`)**:
    * Currently `canonical_heldout_manifest()` builds `capability_versions` from live `_capability_version_snapshot()` and calls `approve_manifest(...)` at runtime (`C9`). Instead, `heldout_eval.py` should define `CANONICAL_FREEZE_ID = "HELDOUT-FREEZE-2026-10-15"`, static `FROZEN_VERSIONS` and `FROZEN_CAPABILITY_VERSIONS` maps representing the frozen state at `HELDOUT-FREEZE-2026-10-15`, and pinned module constants `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST`. `canonical_heldout_manifest()` should embed `"freeze_id": CANONICAL_FREEZE_ID`, those frozen version maps, and a static `"threshold_approval"` dict using `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` without calling `approve_manifest(...)` dynamically.
    * In `check_heldout_freeze()` (`C5`), after validating `capability_versions` structure, compare each capability's frozen `("task", "prompt", "policy", "source")` (and `"model"` unless overridden) against live `_capability_version_snapshot()`. When prompt/policy/task/source versions differ between `manifest["capability_versions"]` and `_capability_version_snapshot()`, append `f"capability_version_drift:{','.join(drifted_keys)}"` to `blockers`.
    * In `tokenomics_comparison.py`, delete `_manifest_for_candidate_model()` (`C11`) so a candidate model comparison never mutates `manifest["versions"]["model"]` or re-signs `threshold_approval`. Instead, add `expected_serving_model: str | None = None` to `heldout_eval.evaluate_heldout(...)` (`C8`): `check_heldout_freeze(manifest)` validates the untouched frozen manifest and its pinned `FROZEN_MANIFEST_DIGEST`, while `evaluate_heldout` checks response serving versions against `expected_serving_model` when supplied for a single-lever model candidate.
  * **Summary-only candidate comparison hardening (`Q4`, `C9`, `C10`, `C12`)**:
    * `baseline_candidate_from_evaluation()` (`C9`) does not currently include `manifest_digest`; adding `"manifest_digest": hashes.get("manifest_digest")` allows `_validate_baseline_artifact` (`_validate_baseline` in `tokenomics_comparison.py`, `C10`) to enforce `baseline.get("manifest_digest") == freeze["manifest_digest"]` (raising `ValueError` or recording a blocker if missing/mismatched; raising `ValueError` when `baseline["manifest_digest"] != freeze["manifest_digest"]` fails closed on tampered/mismatched baselines).
    * For summary-only candidates (candidates without `responses` in `_extract_candidate_metrics`, `C12`): require explicit `evaluation_outcome` (in `heldout_eval.OUTCOMES`, never defaulting to `"pass"`), explicit `accepted_case_ids` (subset of `case_ids`, never defaulting to `case_ids`), and explicit `gate_failures` (a sequence of non-empty strings, e.g. `[]` when clean, raising `ValueError` if any of the three fields is omitted or malformed, and propagating any non-empty `gate_failures` into `failure_reasons`).
    * Enforce currency parity (`candidate_usage.currency == baseline_usage.currency`): require explicit non-empty `currency` on candidate and baseline usage and record a gate failure (`currency_mismatch:{cand_currency}!={base_currency}`) or raise `ValueError` when currencies differ so cross-currency cost subtraction never occurs (`net_saving_reported` forced to `"0.000000"` / `is_saving=False`).
    * Collect candidate prompt overrides (`cand_levers["prompt"]` whenever `cand_levers["prompt"] != base_levers["prompt"]`, or all candidate `lever_config["prompt"]` strings plus optional `candidate.get("rendered_prompts")`) and pass them into `heldout_eval.check_prompt_tuning_isolation(...)` so any held-out case ID or 6-word `expected_answer` shingle embedded in a candidate prompt override trips `holdout_leakage_clear` (`isolation["isolated"] is False`) and fails the candidate/suite.
  * **Statement factual support for numbers & `ZF-*` IDs, plus sample-floor pre-gate (`Q5`, `C7`, `C8`, `C13`)**:
    * Add `_check_statement_support(texts, grounded_text)` in `heldout_eval.py` and invoke it in both `_evaluate_assistant_case()` (`C7`, checking `output["summary"]` and each `finding["text"]`, plus citation locator tokens against the case fixture + captured `snap["sources"]` + `snap["citations"]`) and `_evaluate_legacy_case()` (`C7`, checking `clean` / statement texts or priority `reason` texts against `sources` labels + case IDs). Any integer token (`\b\d+\b`) or `ZF-[A-Za-z0-9-]+` case identifier in candidate output that does not appear in the grounded source text for that case increments `unsupported_claims` and appends `"unsupported_factual_claim"` to `critical_errors` (`passed = False`).
    * In `evaluate_heldout()` (`C8`), change `if not freeze["blockers"] and isolation["isolated"]:` to `if freeze["ready_for_evaluation"] and isolation["isolated"]:` so unmet cohort or total sample floors (`not freeze["sample_sufficient"]`) prevent per-case scoring from running while keeping `outcome == "insufficient"` and preserving `denominators` and `insufficient_reasons`.

### Wave 3: Contrarian (Inline)

* Audited every canonical baseline response in `canonical_baseline_responses()` (`C9`, lines 1852–1986) against `_check_statement_support` to verify zero false positives on legitimate grounded numbers or `ZF-*` identifiers!
* Findings:
  * **Crucial false-positive audit on canonical baseline responses (`C9`, `C13`)**:
    * Let's check every number (`\b\d+\b`) and `ZF-*` token in `canonical_baseline_responses()`:
      1. `HO-AST-AP-01`: `"Survey is on file; PAS 2035 design document is still required."` -> contains `"2035"`! Where does `"2035"` appear in `snap` for `HO-AST-AP-01`? Look at `rec_ap_01["technical"] = {"design_version": "pas2035-v2"}`! Notice `"pas2035-v2"` has NO word boundary before `2035` (`pas` is alphanumeric, so `\b2035\b` does NOT match `"pas2035-v2"`, whereas `\b2035\b` DOES match `"PAS 2035"` in the summary, OR `assistants.REGISTRY["assessment-preparation"]["purpose"]` mentions PAS 2035)!
         WHAT A CATCH!! Checking `\b\d+\b` in `"PAS 2035"` against `snap["sources"]` where `"design_version": "pas2035-v2"` has `pas2035` concatenated would have failed `HO-AST-AP-01` unless either (a) grounded numbers extract all digit runs `\d+` from grounded sources (so `"pas2035-v2"` yields `{"2035", "2"}`), OR `"PAS 2035"` / domain standard names (`PAS 2035`, `SHDF Wave 3`) are grounded via `re.findall(r"\d+", grounded_corpus)`! Look: `re.findall(r"\d+", ...)` on `"pas2035-v2"` extracts `"2035"` and `"2"`!
      2. Let's check EVERY OTHER canonical baseline response for `\b\d+\b` and `ZF-*`:
         - `HO-AST-FE-01`: `"SHDF Wave 3 funding reference is blank..."` -> `"3"`! In `snap["sources"]["funding"]["route"]`: `"SHDF Wave 3"` -> contains `"3"`!
         - `HO-AST-QE-02`: `"Conflicting humidity readings detected at 08:00Z..."` and `"Sensor SENS-110..."` -> `"08"`, `"00"`, `"110"`! In `snap["sources"]["sensors"]`: `"2026-10-25T08:00:00Z"` and `"SENS-110"` -> `re.findall(r"\d+", grounded)` extracts `"08"`, `"00"`, `"110"`! Notice `\b08\b` also matches `"T08:00:00Z"` ONLY IF `T` wasn't alphanumeric—`T` IS alphanumeric, so `\b\d+\b` on `"2026-10-25T08:00:00Z"` would NOT extract `"08"` if we used `\b\d+\b` on the source side, whereas `re.findall(r"\d+", grounded_text)` DOES extract `"08"` from `"T08:00:00Z"` and `"2035"` from `"pas2035-v2"`!
         - `HO-LEG-BR-01`: `"Case ZF-HO-111 ... waited 27 days ..."` -> `ZF-HO-111` (case key in `sources`), `27` (`Days in stage: 27`).
         - `HO-LEG-SU-01`: `"Waiting 19 days ..."` -> `19` (`Days in stage: 19`).
         - `HO-LEG-PR-01`: `case_id: "ZF-HO-114A"`, `reason: "Open Electrical safety issue..."` -> `ZF-HO-114A` in `sources`, no extra numbers in `reason`! And in the regressing candidate in `tokenomics_comparison.py:534`: `reason: "Longest wait selected first."`, `cites: ["Days in stage: 31"]` -> clean on factual support, fails on safety priority miss as intended!
         - `HO-LEG-FD-01`: `"Loft insulation under SHDF Wave 3 ... survey-zf-ho-115.pdf ... Needs: lodged PAS 2035 compliance certificate"` -> Look! `HO-LEG-FD-01` has `"3"` (`Funding route: SHDF Wave 3`), `"zf-ho-115"` (`Document: survey-zf-ho-115.pdf` and case ID `ZF-HO-115`), AND `"2035"` in `"Needs: lodged PAS 2035 compliance certificate"`! Does `ai_tasks.source_labels(rec_leg_fund)` contain `"2035"`?!
           LOOK AT `ai_tasks.source_labels` (`ai_tasks.py:61-89`): `source_labels` does NOT include `technical.design_version` (`pas2035-v2`), whereas `ai_prompts.PROMPTS["funding_draft"]` explicitly instructs the model about PAS 2035 / retrofit funding compliance! Wait: let's check `ai_prompts.py` to see if `"2035"` is in the prompt or if standard retrofit scheme/standard numbers (`PAS 2035`, `PAS 2030`) appear in `ai_prompts`! Even simpler: in `_check_statement_support`, strip standard designation `"PAS 2035"` / `"PAS 2030"` (or check numbers excluding `"PAS 2035"` standard title, OR check `HO-LEG-FD-01` wording)! Wait: if we strip standard citations `[[...]]` first, then allow standard name `PAS 2035` (regex `r"\bPAS\s+2035\b"`, `re.IGNORECASE`) or include `fixture` record fields, wait: should a legacy task be allowed to invent a number from `fixture` that wasn't in `sources`? NO—legacy tasks only see `sources` (`source_labels`)! Why did `HO-LEG-FD-01` say `"Needs: lodged PAS 2035 compliance certificate"`? Because PAS 2035 is the UK retrofit standard name (like ISO 9001), or `HO-LEG-FD-01` can either recognize `\bpas\s+2035\b` as a named technical standard (not a case metric) OR `HO-LEG-FD-01` baseline text can say `"Needs: lodged retrofit compliance certificate"` (`expected_answer` stays untouched or aligned? Wait: changing `expected_answer` would change `FROZEN_MANIFEST_DIGEST`, which is totally fine BEFORE pinning `FROZEN_MANIFEST_DIGEST`, OR recognizing `\bpas\s+2035\b` keeps canonical manifest 100% unchanged AND avoids false-flagging any response mentioning the standard name "PAS 2035"!). Even better: stripping `\bpas\s+2035\b` (case-insensitive) before scanning `\b\d+\b` means `"PAS 2035"` (a regulatory standard title, not a numeric claim about a case) won't false-positive, while `"waited 99 days"`, `"45% humidity"`, `"GBP 9999"`, or `"ZF-HO-999"` WILL immediately be flagged as `unsupported_claims`!
      3. Let's also check normalized numeric strings (e.g., `"08"` vs `"8"`? No, keep exact digit-token membership from `re.findall(r"\d+", grounded_source_str)` so `"99"` or `"42"` not in `grounded_source_str` is always caught, and strip `ZF-[A-Za-z0-9-]+` matches first before scanning `\b\d+\b` so `"ZF-HO-111"` is checked as a `ZF-*` identifier against grounded `ZF-*` IDs rather than double-counting `"111"`!). That's super clean and prevents double-counting `ZF-HO-999` as both an ungrounded `ZF-*` ID and an ungrounded number `999` (or counts 1 unsupported claim per ungrounded token cleanly)!
  * **Existing summary-only tests in `test_tokenomics_comparison.py` and `test_heldout_eval_api.py` (`C14`)**:
    * Existing summary-only test fixtures in `test_tokenomics_comparison.py` and `test_heldout_eval_api.py` omitted `evaluation_outcome` and `gate_failures`. Once `_extract_candidate_metrics` requires `responses` OR explicit `evaluation_outcome`, `accepted_case_ids`, and `gate_failures`, we will update existing valid summary-only test fixtures to include `"evaluation_outcome": "pass"` and `"gate_failures": []`, and add dedicated negative tests proving that omitting any of `evaluation_outcome`, `accepted_case_ids`, or `gate_failures` is rejected (`ValueError` -> HTTP `400` in API), non-empty `gate_failures` forces `outcome="failure"` (`is_saving=False`), currency mismatch fails closed, mismatched `baseline["manifest_digest"]` fails closed, and candidate `lever_config["prompt"]` containing a held-out case ID or answer shingle fails `holdout_leakage_clear`!

## Evidence Log

| ID  | Kind | Location                                                              | Summary                                                                                                                               |
|-----|------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| C1  | code | `src/api/src/zava_forward/api/server.py:904`                          | Parent commit `7f83f4749` adds `"chat_evaluation": chat_eval.run_eval()` to `GET /api/ai/report`.                                     |
| C2  | code | `src/api/tests/test_content_standard.py:160`                          | `test_ai_label_is_exact_and_never_implies_approval` forbids `"human-approved"` (unless `"human-approved by"`) in `api` and `core`.    |
| C3  | code | `src/core/src/zava_forward/core/heldout_eval.py:4`                    | Unauthorized `"human-approved"` occurrences at lines 4 and 1397 in `heldout_eval.py`.                                                 |
| C4  | doc  | `src/core/README.md:15`                                               | `"human-approved thresholds"` wording in `src/core/README.md`.                                                                        |
| C5  | code | `src/core/src/zava_forward/core/heldout_eval.py:167`                  | `check_heldout_freeze()` validates `capability_versions` structure and `threshold_approval`, currently lacking live drift comparison. |
| C6  | code | `src/core/src/zava_forward/core/heldout_eval.py:1359`                 | `_capability_version_snapshot()` computes live `task`, `model`, `prompt`, `policy`, and `source` versions across all 11 capabilities. |
| C7  | code | `src/core/src/zava_forward/core/heldout_eval.py:494`                  | `_evaluate_assistant_case()` and `_evaluate_legacy_case()` (`:615`) validate citations and `required_tokens` without `_check_statement_support`. |
| C8  | code | `src/core/src/zava_forward/core/heldout_eval.py:701`                  | `evaluate_heldout()` currently gates scoring on `not freeze["blockers"]` (`:859`) instead of `freeze["ready_for_evaluation"]`.        |
| C9  | code | `src/core/src/zava_forward/core/heldout_eval.py:1396`                 | `canonical_heldout_manifest()` dynamically calls `approve_manifest(...)` (`:1793`); `baseline_candidate_from_evaluation()` (`:1989`) omits `manifest_digest`. |
| C10 | code | `src/core/src/zava_forward/core/tokenomics_comparison.py:90`          | `_validate_baseline()` validates baseline fields without binding `baseline.get("manifest_digest") == freeze["manifest_digest"]`.      |
| C11 | code | `src/core/src/zava_forward/core/tokenomics_comparison.py:129`         | `_manifest_for_candidate_model()` mutates `versions["model"]` and re-signs the frozen manifest dynamically.                           |
| C12 | code | `src/core/src/zava_forward/core/tokenomics_comparison.py:157`         | `_extract_candidate_metrics()` and `compare_candidates()` (`:260`) default `accepted_case_ids`/`evaluation_outcome`, skip currency check, and omit candidate `lever_config["prompt"]` from isolation scan. |
| C13 | code | `src/core/src/zava_forward/core/assistants.py:155`                    | `assistants.capture()` builds closed-allowlist `snap["sources"]` and `snap["citations"]` per assistant capability.                    |
| C14 | code | `src/api/tests/test_heldout_eval_api.py:94`                           | `test_get_ai_report_preserves_top_level_keys_and_embeds_heldout_summaries` checks top-level `GET /api/ai/report` keys and summary POST payloads. |
| C15 | doc  | `src/api/README.md:14`                                                | Documents `GET /api/ai/report` top-level keys (`evaluation`, `chat_evaluation` after rebase, `live`, `registry`, `consumption`).       |

## Synthesis and Alternatives

### Alternatives Evaluated

| Option | Summary | Trade-offs | Disposition |
|---|---|---|---|
| Option A: Pin static `HELDOUT-FREEZE-2026-10-15` constants + `expected_serving_model` parameter + strict summary schema/currency/manifest-digest/prompt-lever isolation + `_check_statement_support` + `ready_for_evaluation` gate | Keep `canonical_heldout_manifest()` completely static with pinned `FROZEN_THRESHOLDS_DIGEST` & `FROZEN_MANIFEST_DIGEST`, detect live `_capability_version_snapshot()` drift in `check_heldout_freeze()`, pass `expected_serving_model` to `evaluate_heldout()` without touching the frozen manifest, enforce strict summary-only verification in `tokenomics_comparison.py`, and check `\b\d+\b` & `ZF-*` support | Satisfies every finding cleanly without weakening digest immutability or introducing false positives | **Selected** |
| Option B: Keep dynamic `approve_manifest` in `canonical_heldout_manifest()` and assert digest only in a unit test | Move digest check into `test_heldout_eval.py` only | Production callers (`GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`) would still forge dynamic approvals on drifted prompts at runtime; violates Finding 3 | Rejected |
| Option C: Disallow summary-only candidates completely in `compare_candidates()` | Require full `responses` on every candidate | Breaks summary-payload API contract (`POST /api/ai/candidate-comparison`) instead of hardening it with explicit `evaluation_outcome`, `accepted_case_ids`, `gate_failures`, currency parity, and prompt-isolation checks | Rejected |

## Decisions and Risks

* **Selected recommendation**: Option A across four bounded implementation phases:
  1. Rebase `feat/ai-108-heldout-eval-0228` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), preserving both `chat_evaluation` and the enriched `evaluation` (`held_out`, `tokenomics_comparison`) in `server.py`, `test_heldout_eval_api.py`, and `src/api/README.md`.
  2. Fix the content-standard violation by replacing `"human-approved"` with `"human-authorized"` in `heldout_eval.py` and `src/core/README.md`.
  3. Pin `CANONICAL_FREEZE_ID = "HELDOUT-FREEZE-2026-10-15"`, `FROZEN_THRESHOLDS_DIGEST`, and `FROZEN_MANIFEST_DIGEST` in `heldout_eval.py`, enforce `"capability_version_drift"` detection in `check_heldout_freeze()`, gate per-case scoring on `freeze["ready_for_evaluation"]`, add `_check_statement_support` flagging ungrounded `\b\d+\b` numbers and `ZF-*` case IDs, include `manifest_digest` in `baseline_candidate_from_evaluation()`, and support `expected_serving_model` in `evaluate_heldout()` so `tokenomics_comparison.py` never mutates or re-signs a frozen manifest.
  4. Harden `tokenomics_comparison.py` (`_validate_baseline_artifact` manifest-digest check, explicit `evaluation_outcome` + `accepted_case_ids` + `gate_failures` when `responses` is omitted, currency equality check between candidate and baseline usage, and candidate `lever_config["prompt"]` scanning through `check_prompt_tuning_isolation()` with `holdout_leakage_clear` reporting), update/add focused unit and API tests, and run the full requested focused validation suite.

## Readiness and Handoff

* **Research Disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Self-Check**:
  * [x] Three waves (`Wider`, `Deeper`, `Contrarian`) executed in order.
  * [x] All questions `Q1`–`Q5` answered with `C1`–`C15` `path:line` evidence.
  * [x] Parent branch advance (`7f83f4749`) and canonical false-positive edge cases analyzed before planning.
  * [x] Zero source files modified during Research.
