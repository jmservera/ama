---
title: Issue 136 binding C1 research
description: Research for one bounded C1 on the public simulation startup binding, covering two independent Medium findings and execution-evidence retention
ms.date: 2026-11-10
---

## Execution and boundary

Research disposition: `executed`, 2026-11-10, input frozen at HEAD `53fcf666c9e757a8bb33d6b557158fa963920ade` (tree `c09579e4ad92fea3c1dce5d5b8c98bc93133f2bf`), base and target `d52f20a5198de7269f39daf794911545aee01ced`. Refs #136 and #1288 only. One bounded C1; no reset of the whole-issue history, no automatic C2. The original [research](2026-11-10-issue-136-simulation-binding-1110-research.md), plan, critique, changes and review are preserved byte for byte.

## Independent disposition (recorded, not a C1 approval)

An independent comprehensive Functional review of the frozen candidate (reviewer commit reference d5ea3652) returned `approve_with_comments` with two Medium findings, no Critical or High. It ran no tests; the original pass claims stayed producer claims because the native log held commands but not full outputs.

* F1 (retained from the original Low, regraded Medium): `simulation_lane` is imported before the `try` in the rendered recipe, so an older but otherwise usable API image lacking the module exits before `os.execv` instead of starting the ordinary API with the manual lane. The image guard rejects only the `k8se/quickstart` placeholder, not arbitrary incompatible versions.
* F2 (new): the Docker test calls `Lane.observe()` under the real clock in each container run; a legitimate 300 second slot crossing between restarts makes `added` nonzero without any reset, so the assertion is nondeterministic. `Lane.open` accepts `clock=`.
* Retained limits: ACA runtime behaviour untested, operator-provisioned durable SQL allowance, editable-install mismatch (now resolved in an owned venv), pre-existing `RUF100` baseline.

## Source facts (HEAD, unchanged `src/`)

* `git diff d52f20a5 HEAD -- src` is empty; `src/api/Dockerfile` blob `a7dfb2e4e`. The first image `zava-forward-api:rpi-136sim-d52f20a` still has ID `sha256:cc1ec99e86db174ffc0bfac94512db423bfd81fe80c1a8e637f5e04dfe5aaea8` (inspect retained in the external proof), so it is reused with no rebuild.
* `Lane.open(env, working=(), clock=time.time)`; `store_id` is read from `sim_meta`; `observe()` stores up to 12 five-minute slots floor-aligned to the clock; `state()` and `view()` expose readings.
* `containerapps.bicep` recipe: import at line 2 of the recipe, outside `try`; `os.execv` outside `try`. The F1 fix is moving the import into the existing `try`. `except Exception` already catches `ImportError` and prints only `getattr(error,"code",type(error).__name__)`; `lane` is only referenced inside `try`, so no later use of an unbound name exists.
* CI lint for infra tests: `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` on `infra/tests/test_bicep_policy.py` (workflow `src-ci.yml` lines 243-244) with `ruff==0.17.1`, and the same README commands (lines 1191-1193). `test_public_simulation_startup.py` is not in that workflow list; the same isolated configuration is applied to it as a relevant check. The first run used default (non-isolated) ruff and its RUF100 and format output is not a faithful baseline; the isolated run is the correct one and any failure is preserved, not waived.

## Environment

Owned venv `/tmp/c1venv136` with `ruff==0.17.1`, `mypy==2.4.0` and pip-installed `src/core`, `src/agents`, `src/api` from this worktree; imported origins are under the venv `site-packages` (retained in proof). Shared editables (which point at another checkout) are not used or modified.

## Evidence gap

The first run retained commands but piped several to `tail`. C1 captures complete stdout, stderr and real exit statuses to `ROOT/phase136-binding-c1-evidence-1110/proof` using subprocess capture or `PIPESTATUS`, preserving adverse results. Local Docker health uses the default JSON store and is not MSSQL, browser-auth or Azure evidence; accounting remains supported by source review (`ZF_STORE=mssql` fixed in the template).

## Approach

* A1 Recipe: move the import into `try`. Keep paths, `provision`, validation, error code report and the final `execv`. No broad success fallback.
* A2 Test: one explicit fixed clock for both probes via `Lane.open(env, clock=lambda: FIXED)`, startup command untouched. Assert unchanged `store_id` and reading identities across restart and `added == 0` at the same instant. Negative controls: the old real-clock probe with a crossing slot (clock advanced by 300 seconds) shows the old assertion fails while persistence is intact; an import failure case runs the same rendered command with the module made unavailable inside the owned image so the ordinary API still serves `/healthz`.
* A3 README: minimal clarification of the placeholder guard limit, the missing-module manual fallback and the test clock.

## Risks

* Making the import fail inside the actual image needs an owned mechanism that leaves the image and recipe unchanged: a bind-mounted shadow package path via a harness-only `PYTHONPATH` entry that provides a failing `zava_forward.core.simulation_lane`. It is a harness input, not a change to the rendered command. Planning Readiness: `Ready`.
