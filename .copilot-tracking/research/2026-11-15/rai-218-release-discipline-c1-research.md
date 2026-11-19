---
description: "Primary research artifact for Issue #218 c1 traceability AST caching correction (PR #1807 CI failure)"
---
<!-- markdownlint-disable-file -->

# Task Research: rai-218-release-discipline-c1

| Field              | Value                                                                       |
|--------------------|-----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                  |
| Researcher / agent | RPI Agent (`rpi-research`)                                                  |
| Status             | Complete                                                                    |
| Artifact path      | .copilot-tracking/research/2026-11-15/rai-218-release-discipline-c1-research.md |

## Research Brief

* What to research: Root cause, hot-path callers, caching contract, immutability guarantees, and focused regression verification for repeated AST parsing in `rai_control_plane.verify_traceability_targets(None)` causing the `case_journey_browser_check.py:1004` timing race in `PR #1807`.
* Why it matters: `PR #1807` passed 9/10 `Source projects CI` jobs and failed only in `src-api` at `case_journey_browser_check.py:1004` because `GET /api/assistants` executes `exercise_acceptance_report()` -> `traceability_summary(None)` -> `verify_traceability_targets(None)`, incurring ~135ms of disk reads and `ast.parse()` across 16 test files (43 targets) on every request.
* Audience or intended use: Downstream `rpi-plan`, `rpi-implement`, and `rpi-review` phases for correction cycle `c1` on `feat/rai-218-release-discipline`.
* Scope: `src/core/src/zava_forward/core/rai_control_plane.py`, `src/core/src/zava_forward/core/assistants.py`, `src/api/src/zava_forward/api/web/assistants.js`, `src/api/src/zava_forward/api/web/case-workspace.js`, `src/api/checks/case_journey_browser_check.py`, `src/core/tests/test_rai_control_plane_218.py`, and `src/api/tests/test_assistants.py`.
* Non-goals: Modifying `src/api/checks/case_journey_browser_check.py` or `scenario-manifest.json`, changing HTTP schemas, running `tools/rpi-checks.py`, or pushing/opening PRs.
* Criteria: Repeated `verify_traceability_targets(None)` calls complete in `<1ms` without caller-mutation leakage across calls; explicit `verify_traceability_targets(repo_root=...)` calls remain uncached for negative/synthetic tests; strict `mypy`, `ruff`, and focused unit suites pass.
* Requested outputs: Converged `c1` implementation design with `path:line` codebase evidence and measured latency baseline.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                              |
|--------------------------------------|----------------------------------------------------------------------------------------------------|
| Research question(s)                 | How does `verify_traceability_targets(None)` slow `GET /api/assistants`, and how do we cache the default path safely under `<1ms` while keeping explicit `repo_root` uncached and mutation-safe? |
| Codebase scope                       | `src/core/` and `src/api/` in `/home/azureuser/source/ama-demo-wt/feat-218-rai-release`            |
| External scope                       | none                                                                                               |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/rai_control_plane.py`, `src/core/tests/test_rai_control_plane_218.py`, `src/api/checks/case_journey_browser_check.py` |
| Initial external candidate areas     | none                                                                                               |
| Research posture                     | focused                                                                                            |
| Posture provenance                   | caller-specified                                                                                   |
| Explicit limits / deadline           | Focused tier validation (`ruff`, `mypy`, `unittest`); commit locally on `feat/rai-218-release-discipline`; do not push |
| Posture-specific completion basis    | focused scope and materiality                                                                      |
| Edits allowed during research?       | no, research-only                                                                                  |
| Resolved evidence root               | `.copilot-tracking/`                                                                               |
| Known constraints / excluded sources | Preserve browser-check recipes (`case_journey_browser_check.py` and `scenario-manifest.json` untouched); preserve strict `mypy` (`strict = true` in `src/core`) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                  | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason                                  |
|---------------------|----------------------------|---------------------------------------------------|----------------------------------------------|------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and evidence root | Focused validation tier, Markdown and git trailer conventions | Selected: governs validation tier and commit rules         |
| Skill               | `python-foundational`      | Python stdlib caching and typing conventions       | Optional Python guidance                     | Skipped: bounded 1-module stdlib `functools.lru_cache` fix |
| Research specialist | `rpi-researcher`           | General delegated lane worker                      | Separate lane evidence file                  | Skipped (inline): tightly coupled single-trace root cause  |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                               | Answers / unanswered | Resulting decision or selected further research                     |
|------------------|-------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------|
| Intake           | Non-interactive autopilot session with explicit root cause and required fix supplied | N/A (autonomous)     | Execute focused 3-wave inline research and converge on immutable cache |
| Direction change | No scope ambiguity or boundary expansion arose                                      | N/A                  | Retain focused `src/core` caching scope                              |
| Convergence      | Evidence completely answers Q1..Q3 with measured baseline (`134.90ms`)              | N/A                  | Mark Planning Readiness `Ready` and advance to `rpi-plan`            |

## Scope and Success Criteria

* Scope: `verify_traceability_targets` caching in `src/core/src/zava_forward/core/rai_control_plane.py` and regression test coverage in `src/core/tests/test_rai_control_plane_218.py`.
* Assumptions: `REQUIREMENT_TRACEABILITY` and repository test files on disk are static for the lifetime of an API server process when `repo_root is None` (verified via codebase grep).
* Success criteria:
  * Every research question is answered with `path:line` citations.
  * Baseline latency and caller chain from `GET /api/assistants` to `verify_traceability_targets(None)` are verified.
  * Cache immutability, explicit `repo_root` bypass, and strict `mypy` typing are verified.

## Task Research Requests

* Explicit requests: Cache `verify_traceability_targets(None)` in `rai_control_plane.py`, prove `<1ms` repeated latency and immutability, add regression test in `src/core/tests/test_rai_control_plane_218.py`, run `ruff`/`mypy`/`unittest`, and commit on `feat/rai-218-release-discipline` without pushing.
* Inferred research questions: Which other endpoints invoke `verify_traceability_targets(None)`? Could caller mutation corrupt cached state? Does any test monkeypatch `REQUIREMENT_TRACEABILITY` or `_default_repo_root`?
* Caller constraints and non-goals: Research phase is strictly read-only; no push or PR creation.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                          | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|--------------------------------------------------------------------------------|---------------------|---------------------------------------------------|
| narrow                                                   | Fix the hot path in `rai_control_plane.py` without relaxing browser-check waits | Caller intake       | Constrains fix to `src/core` and `test_rai_control_plane_218.py` |
| exclude                                                  | Do not push branch or open a PR                                                | Caller intake       | Local commit only after `rpi-review`              |

## Research Questions

|  # | Sub-question                                                                                                    | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How does `verify_traceability_targets(None)` cause the `case_journey_browser_check.py:1004` failure?            | straightforward | H        | answered |
| Q2 | Which callers invoke `verify_traceability_targets` and do any tests mutate its return value or patch constants? | breadth         | H        | answered |
| Q3 | What caching structure guarantees `<1ms` default calls, uncached explicit `repo_root`, and strict `mypy` safety? | depth          | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/rai-218-release-discipline-research.md`, `.copilot-tracking/research/2026-11-15/rai-218-release-admission-hardening-research.md`, `.copilot-tracking/reviews/logs/2026-11-15/rai-218-release-admission-hardening-review.md`.
* Reused (verified) findings: `verify_traceability_targets` was introduced under `PC-004` in `rai-218-release-discipline` to AST-verify 43 test targets across 15 Epic #218 requirement entries without importing `src/api` from `src/core`.
* Superseded / stale: Uncached per-request execution of `verify_traceability_targets(None)` inside `exercise_acceptance_report()` was assumed cheap during unit testing, but measured `134.90ms` per call on disk, racing async `GET /api/assistants` in browser checks.

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused `src/core` hot-path fix; no browser-check edits; no push.
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: Inline 3-wave verification across `src/core` and `src/api`.

#### Wave 1: Wider

* Plan and independent lanes: Sweep all call sites of `verify_traceability_targets`, `traceability_summary`, `exercise_acceptance_report`, `REQUIREMENT_TRACEABILITY`, and `_default_repo_root` across `src/`.
* Worker evidence relationships or inline fallback: Inline grep/view mapped every caller (`assistants.py`, `store.py`, `governance.py`, `ai_tasks.py`, `test_rai_control_plane_218.py`, `test_rai_release_readiness_api_218.py`) and confirmed zero monkeypatches of `REQUIREMENT_TRACEABILITY` or `_default_repo_root` (`C1`, `C2`, `C3`).
* Reflection: `exercise_acceptance_report()` is called on every `GET /api/assistants` (`Assistants.registry`), `GET /api/governance`, and `GET /api/ai/report` request, all passing `repo_root=None`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact frontend/browser timing interaction (`case_journey_browser_check.py:994-1009`, `assistants.js:181-209`, `case-workspace.js:83-101`) and baseline Python timing of `verify_traceability_targets(None)`.
* Plan and independent lanes: Inspect the JS rendering flow after `POST /api/cases/ZF-1/read-doc` and time `verify_traceability_targets(None)`.
* Worker evidence relationships or inline fallback: Inline view and timing probe confirmed `verify_traceability_targets(None)` takes `134.90ms` parsing 16 test files / 43 targets (`C4`), while `case_journey_browser_check.py:998-1002` waits only for `#case-panel-survey .aimeta` (rendered from the case payload) and immediately reads `[data-case-ai-summary]`, which stays `"AI review count loading."` until `assistantCasePanel`'s `GET /api/assistants` resolves and sets `panel.dataset.waiting` (`C5`, `C6`, `C7`).
* Reflection: Eliminating the `~135ms` per-request AST parse in `verify_traceability_targets(None)` directly restores sub-millisecond `GET /api/assistants` response time so `assistantCasePanel` resolves alongside `/api/assistants/proposals` as before `PR #1807`.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge (a) caching `dict[str, Any]` directly with `@functools.lru_cache`, (b) adding an explicit Playwright wait in `case_journey_browser_check.py`, and (c) breaking `repo_root=Path(...)` negative tests (`test_verify_traceability_targets_fails_closed_when_target_missing`).
* Plan and independent lanes: Evaluate mutability hazards, CI manifest SHA-256 constraints, and test isolation.
* Worker evidence relationships or inline fallback: (a) Caching a `dict` directly on `verify_traceability_targets` would share mutable `dict` and `unresolved: list[dict[str, str]]` across callers and would also require `Path` hashability on arbitrary `repo_root` arguments while polluting cache entries with temporary test directories; (b) editing `case_journey_browser_check.py` would require updating `scenario-manifest.json` SHA-256 and would hide a real `~135ms` per-request server regression on `/api/assistants`; (c) caching only an internal zero-arg `@functools.lru_cache(maxsize=1)` helper `_cached_default_traceability_targets()` that returns an immutable `tuple[bool, int, tuple[tuple[str, str, str], ...]]` when `repo_root is None`—and reconstructing a fresh `dict` + `list[dict[str, str]]` on each call while routing `repo_root is not None` directly to `_verify_traceability_targets_uncached(repo_root)`—eliminates both `Path(__file__).resolve()` and `ast.parse()` overhead on the hot path and prevents any caller mutation (`C4`, `C8`).
* Reflection: Contrarian checks confirm the internal immutable-tuple `@functools.lru_cache(maxsize=1)` helper is strictly superior to direct dict caching or browser-check edits.

#### Parent Synthesis and Disposition

| Material / claim                                                                                   | Evidence IDs | Parent disposition | Evidence-based rationale                                                                                      | Primary-artifact treatment      |
|----------------------------------------------------------------------------------------------------|--------------|--------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------|
| Cache `repo_root is None` via `@functools.lru_cache(maxsize=1)` returning immutable tuple + fresh dict reconstruction | `C1`, `C4`, `C8` | accepted           | Drops repeated default calls from `134.90ms` to `<0.05ms`, prevents caller mutation, and keeps strict `mypy` clean | Selected Recommendation         |
| Run `_verify_traceability_targets_uncached(repo_root)` whenever `repo_root is not None`            | `C4`, `C8`   | accepted           | Preserves deterministic fail-closed testing on synthetic/temporary `repo_root` directories                    | Selected Recommendation         |
| Cache `verify_traceability_targets` return `dict` directly via `@lru_cache`                        | `C4`         | rejected           | Leaks shared mutable `dict`/`list` state to callers and caches transient `tmp_dir` `Path` arguments           | Rejected Alternative 1          |
| Modify `case_journey_browser_check.py` to wait for `[data-waiting]`                                | `C5`, `C6`, `C7` | rejected       | Leaves `135ms` AST-parse regression on every `/api/assistants` call and alters `scenario-manifest.json` recipe | Rejected Alternative 2          |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Scope completely covered with direct codebase and timing evidence; zero unresolved hypotheses.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: `inline: tightly coupled single-trace performance root cause across 5 files completed faster and with exact line precision inline`

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | `Assistants.registry(user)` calls `rai_control_plane.exercise_acceptance_report(...)` with default `repo_root=None` on both non-SQL and SQL paths | `src/core/src/zava_forward/core/assistants.py:1793-1896` | grep / view | high | Invoked by `GET /api/assistants` |
| C2 | `exercise_acceptance_report` calls `traceability_summary(repo_root)` on every invocation | `src/core/src/zava_forward/core/rai_control_plane.py:1113` | view | high | Also called by `store.py`, `governance.py`, and `ai_tasks.py` |
| C3 | `REQUIREMENT_TRACEABILITY` and `_default_repo_root` are never monkeypatched anywhere in `src/` | `src/core/src/zava_forward/core/rai_control_plane.py:424-794` | grep | high | Safe to cache default repo-root AST scan per process |
| C4 | `verify_traceability_targets(repo_root=None)` resolves `_default_repo_root()` and `ast.parse()`s 16 test files (43 targets) on every call, taking `134.90ms` uncached | `src/core/src/zava_forward/core/rai_control_plane.py:811-885` | view / bash | high | Measured via `time.perf_counter()` |
| C5 | After `POST /api/cases/ZF-1/read-doc`, `case_journey_browser_check.py` waits for `#case-panel-survey .aimeta` and immediately reads `[data-case-ai-summary]` | `src/api/checks/case_journey_browser_check.py:994-1009` | view | high | Exact failing check on PR #1807 (`line 1004`) |
| C6 | `assistantCasePanel` awaits `Promise.all([api("/api/assistants"), api("/api/assistants/proposals?case_id=...")])` before setting `panel.dataset.waiting` | `src/api/src/zava_forward/api/web/assistants.js:195-209` | view | high | Delayed by `~135ms` `GET /api/assistants` AST scan |
| C7 | `case-workspace.js` renders `"AI review count loading."` whenever `!assistant.hasAttribute("data-waiting")` | `src/api/src/zava_forward/api/web/case-workspace.js:87-99` | view | high | Explains exact CI failure string `"AI review count loading."` |
| C8 | `test_verify_traceability_targets_fails_closed_when_target_missing` passes an explicit `repo_root=root` `TemporaryDirectory` path | `src/core/tests/test_rai_control_plane_218.py:468-484` | view | high | Explicit `repo_root` path must remain uncached |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

No external sources used.

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `GET /api/assistants` triggers `verify_traceability_targets(None)` (~`134.90ms` of disk reads + `ast.parse()` over 16 files), delaying `assistantCasePanel` setting `data-waiting` past `#case-panel-survey .aimeta` mount | `C1`, `C2`, `C4`, `C5`, `C6`, `C7` | high | Fix server hot path in `rai_control_plane.py` |
| Q2 | All production callers pass `repo_root=None`, zero tests patch `REQUIREMENT_TRACEABILITY` or `_default_repo_root`, and negative tests pass explicit `repo_root=Path(tmp)` | `C1`, `C2`, `C3`, `C8` | high | Cache `repo_root is None` only; keep `repo_root is not None` uncached |
| Q3 | Internal `@functools.lru_cache(maxsize=1)` helper returning `tuple[bool, int, tuple[tuple[str, str, str], ...]]` + per-call dict/list reconstruction achieves `<1ms` latency, caller-mutation safety, and strict `mypy` compliance | `C4`, `C8` | high | Ready for `rpi-plan` |

## Key Discoveries

* Uncached `verify_traceability_targets(None)` takes `134.90ms` per call in this environment across 43 AST targets in 16 files (`C4`).
* Reconstructing the outer `dict[str, Any]` and `unresolved: list[dict[str, str]]` from a cached immutable tuple `(all_resolved, verified_count, tuple_of_unresolved_triples)` costs microseconds (`<0.05ms`) while guaranteeing callers cannot mutate cached state (`C4`).
* Keeping `repo_root is not None` uncached preserves `test_verify_traceability_targets_fails_closed_when_target_missing` and any synthetic directory probes without cache pollution (`C8`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Extract `_verify_traceability_targets_uncached(root: Path) -> dict[str, Any]` in `src/core/src/zava_forward/core/rai_control_plane.py`, add `@functools.lru_cache(maxsize=1)` helper `_cached_default_traceability_targets() -> tuple[bool, int, tuple[tuple[str, str, str], ...]]`, and have `verify_traceability_targets(repo_root: Path | None = None) -> dict[str, Any]` bypass the cache when `repo_root is not None` and materialize a fresh `dict`/`list` from `_cached_default_traceability_targets()` when `repo_root is None`. Add a focused regression test in `src/core/tests/test_rai_control_plane_218.py` verifying cache hit (`<1ms` repeated call), caller-mutation isolation, and uncached explicit `repo_root`.
* Rationale: Directly eliminates the ~135ms per-request bottleneck on `GET /api/assistants`, `GET /api/governance`, and `GET /api/ai/report` with zero schema change, zero browser-check recipe modifications, full mutation safety, and strict `mypy` compatibility.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`
* Implementation impact: `src/core/src/zava_forward/core/rai_control_plane.py` and `src/core/tests/test_rai_control_plane_218.py`.
* Confidence: `high`: Root cause, timing, and callers are directly measured in code.

File tree:

```text
src/core/
  src/zava_forward/core/
    rai_control_plane.py          (modified: cache default verify_traceability_targets(None))
  tests/
    test_rai_control_plane_218.py (modified: add caching, <1ms latency, and mutation-isolation regression test)
```

### Alternative: Direct `@functools.lru_cache` on `verify_traceability_targets`

* Approach: Decorate `verify_traceability_targets(repo_root: Path | None = None)` directly with `@functools.lru_cache`.
* Trade-offs: Slightly fewer lines of code, but returns a shared mutable `dict` and `list` that callers could mutate in-place, and caches temporary `Path` arguments passed during tests.
* Evidence refs: `C4`, `C8`
* Rejection rationale: Violates caller-mutation safety and caches explicit test `repo_root` paths unnecessarily.

### Alternative: Add `[data-waiting]` wait in `case_journey_browser_check.py`

* Approach: Change `src/api/checks/case_journey_browser_check.py:1001` to wait for `assistant[data-waiting]` before reading `[data-case-ai-summary]`.
* Trade-offs: Masks the race in one test check, requires updating the recipe SHA-256 in `scenario-manifest.json`, and leaves a ~135ms disk + AST parse tax on every `/api/assistants` request.
* Evidence refs: `C5`, `C6`, `C7`
* Rejection rationale: Treats the symptom rather than the server regression introduced in PR #1807.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: `none`
* Important: `none`
* Follow-up: Live owner governance appointments (`OQ-017`, `OQ-018`, `OQ-019`) remain tracked as explicit real-AI delivery gate deferrals.
* Residual uncertainty: `none`

## Planning Readiness

* Research disposition: `executed`
* Planning Readiness: `Ready`
* Handoff target: `.copilot-tracking/plans/2026-11-15/rai-218-release-discipline-c1-plan.md`
