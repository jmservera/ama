<!-- markdownlint-disable-file -->
# Research: pinned-tool validation of recovered #123 (2026-11-09)

Parent: [recovery-main-reconcile-123](recovery-main-reconcile-123-research.md). Refs #123, #128, #440. Tier: owner-selected demo-targeted (no `rpi-checks --all`).

## Evidence

* Frozen HEAD `6023741cb42d62f71d47e1780b6ccb765d596fd6`, branch `fix/demo-recovery-123-1109`, tree clean at start; fetched `origin/main` `b46a9ad9a9619db535368d1b2cbbddec8110e122` (unchanged after fetch).
* Prior handoff recorded lint/type checks under ruff 0.17.3 and mypy 2.4.1.
* Repository pins: `src/core/pyproject.toml` `[project.optional-dependencies] dev = ["ruff==0.17.1", "mypy==2.4.0"]`; CI installs `ruff==0.17.1`. `src/core/requirements.txt` and `requirements.in` carry no ruff/mypy pins.
* The earlier checks therefore ran under non-pinned versions. That mismatch outcome stays recorded as is; it is not a failure of the code, and it is not evidence under the pin.
* Handoff text suggested "publish then independently review". Correct order: coordinator independent assessment of the frozen HEAD precedes any publication.

## Disposition

Research executed. Planning Readiness: Ready. Scope: rerun existing lint, format, mypy and the 146-test selection under pinned tools in an isolated venv; no source, manifest or pin change; no SQL, browser, Azure, API or new fairness/security work.
