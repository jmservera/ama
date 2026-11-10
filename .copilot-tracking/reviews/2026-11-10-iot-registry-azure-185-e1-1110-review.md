<!-- markdownlint-disable-file -->
# Review: #185 Registry adapter extension E1 (inventory completeness and traceback context)

Executed once, 2026-11-10 (after `implement-done` witnessed 14:11:35Z), by the implementing agent (no nested agent). Boundary: working tree against frozen starting head `c7cfb463d5d9bd57e9f72e457cf0073b6b7c7e76`, three source paths. Independent exact-head assessment by Root remains required and is not claimed. The review is not repeated in this task and no further correction is made here.

## Execution

Read the full source and test diff and the README diff against the brief, the independent findings F1 and F2, the research and the plan. Reran nothing beyond the validation recorded in the [changes](../changes/2026-11-10-iot-registry-azure-185-e1-1110-changes.md) record (89 focused tests OK, Root repro 2 OK, Ruff check and format clean, Core mypy 286 files clean, all in an isolated venv).

## Outcome

Conformant for the E1 scope. F1 and F2 are repaired with old-fail and new-pass regressions. Residual items below are routed to later user-selected work. E1 consumed; extension remaining 4; no further correction is authorized by this record.

## Checks

* F1: `list_run` no longer skips any entry it cannot classify. Every entry without a string `statusReason` is read, within 100 reads per call, and is returned (exactly marked), excluded (unmarked, other run, absent) or the call refuses with a fixed code. The 1000-device saturation refusal is unchanged. Whole-run teardown through the real SDK path now refuses `TEARDOWN_MANIFEST_INCOMPLETE:1` before any DELETE when a hidden marked non-enrolled identity exists.
* F2: every `RegistryError` hides ambient caller context. A 13-path test raises each public refusal inside a caller handler and checks the formatted traceback, repr and `__suppress_context__`; `__cause__` is None.
* No new SDK method, code, provider, permission or manifest policy; `create`, `run_of` and `delete` still refuse non-enrolled IDs, so no destructive path widens. No wildcard or unconditioned delete.
* Ownership boundary: only the adapter, its tests and the README changed, plus dated records. No `device_identity`, `device_provision`, CLI, API, infra, schema, pyproject or KB edit. origin/main adoption not needed; not done.

## Findings (routed, none blocking)

* R1 (low): a hub with more than 100 unmarked devices in one listing now makes `list_run` refuse (truthful, bounded); documented in the README. A different bound or a paged listing would be a later user-selected design.
* R2 (low): the suppressed context object stays reachable by code that walks `__context__`; documented. Stronger isolation would need a caller-side change outside this boundary.
* R3 (info): the simulator models the documented REST table; Azure create-only, ETag, list limit and RBAC behaviour is unobserved. No live operation was performed.
* R4 (open, out of scope): Registry-before-credential order, no auth-update and the whole #185 credential lifecycle remain open.
* R5 (info): the full Core discover timed out locally (290s) and is not claimed; hosted CI and the full gate are unobserved; focused tier only.
* R6 (info): `origin/main` (`c9e15acb`) changed `src/core/README.md` and `pyproject.toml`; a mechanical merge is expected at publication and is not claimed resolved.
