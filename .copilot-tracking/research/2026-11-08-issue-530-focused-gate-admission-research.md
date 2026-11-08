---
title: Issue 530 focused-gate admission research (supersedes Phase 4 wording)
ms.date: 2026-11-08
---

* Task: `issue-530-focused-gate-admission-prep`, continuation of `issue-530-chat-local-unit`. Research disposition: executed (read-only runner inspection). Planning Readiness: Ready.
* Start: HEAD `ed19cb941e9e562a28eea91285aa4490f23244e2`, tree `d9129d4378fd1ad0b2613cfe85a959019704a22a`, Main `f548b65f4aa31eb92a2cc9cb801130e422daed7f`, clean. FULL107 holds the canonical lock; this work is preparation only and executes no runner, probe, test or install.
* Original records are preserved unchanged. The original Phase 4 stays recorded as blocked and not executed.

## Findings

* Ambiguity: the original plan allowed `--changed` only if it "neither takes the canonical lock nor schedules Docker, Trivy, SQL or browser work". The maintained `tools/rpi-checks.py` always enters `heavy_lock(args.lock_timeout, ...)` and always selects `preflight`, which runs version probes (`python3`, `node`, `docker`, `az bicep`, `actionlint`, `shellcheck`, `trivy`). That condition can therefore never hold, so the original plan could never authorise the required focused gate. This is a plan defect, not a runner defect; the runner is not changed.
* Actual changed-path set (`git diff --name-only --no-renames f548b65f...HEAD`): seven files, all under `.copilot-tracking/` (`INERT_PREFIXES`). The records added by this continuation are also under `.copilot-tracking/`, so the set stays inert. No `src/`, `tools/`, `infra/` or `.github/` path changed.
* Prospective `--changed` selection from `changed_groups`: starts `{preflight, static}`; inert paths add nothing; closure adds `namespace` (static depends on it). Selected groups, in order: `preflight`, `namespace`, `static`. `tooling` is not selected.
* Prospective skips (`skipped_groups`, `SKIP_REASONS`): `project-core`, `project-agents`, `project-api`, `project-orchestrator`, `project-importer` ("no path of src/<name> or a project it depends on changed"); `infra` (no path under infra/ or its tests changed); `migration` (no path forced the full matrix); `browser` (no src/api web or checks path changed); `mssql` (no store, schema, SQL or SQL dependency path changed); `image-*` (no runtime, Dockerfile or requirements path changed); `logo-0600` (no consumer runtime, build or dependency path of the API image changed). The exact list is read from the runner's own receipt in the later run; this list is derived from source, not observed.
* What the selected groups do (read from source; the critique corrected an earlier understatement): `preflight` needs Python 3.12 and a reachable Docker daemon (checked before lock acquisition) plus version probes (`python3`, `node`, `docker`, `az bicep`, `actionlint`, `shellcheck`, `trivy` pinned 0.76.0); it does not run ruff. `namespace` creates the gate's own venvs and installs the project distributions without dev extras. `static` installs pinned PyYAML, ruff and mypy, byte-compiles `src/{core,agents,api,orchestrator}/src`, runs `node --check` on web scripts, git tracking checks, actionlint over the workflows and the runner's own unittest discovery (`tools/`). Package installs may need a package index. None starts SQL Server, builds images, scans or drives a browser.
* Conclusion: tracking-only scope selects no heavyweight service, build, scan, SQL or browser group. Version probes and the namespace install are required maintained behaviour and are permitted in the future admission. If the real selection differs, report it; do not change tier or checks.
* Source qualification: git tree ids at `ed19cb94` for `src` `a59e4c48becd662a178a56b3329da3cfbb3fee66`, `tools` `4e21fc7440c39c7d67728a938938c0f47751034d`, `infra` `c1c120a8fdb14b2620a981597a3e333e29c4091a`, `.github` `8b0afca00f621ae3422640d8befe85ad8109e5d2`; `src` and `tools` equal Main `f548b65f`.

## Evidence boundary

Read-only inspection only. Nothing was executed against the runner. SQL role matrix, cost ledger, browser and live AI criteria remain unmet.
