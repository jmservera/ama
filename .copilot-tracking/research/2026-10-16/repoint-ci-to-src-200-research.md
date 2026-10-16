---
title: Issue 200 source cut-over research
ms.date: 2026-10-16
---
<!-- markdownlint-disable-file -->

## Research Brief

Issue #200, task slug `repoint-ci-to-src-200`. Audience: implementation and
review. Focused, internal convergence research for the explicitly requested
full RPI loop. Resolve live CI, container, infrastructure, tooling and documentation
paths against merged src packages; preserve historical records and mvp/.
No private datasets, .env or .vscode are read. No resource deployment is assumed.

## Research Parameters and Direction Controls

Trusted evidence root: `.copilot-tracking/research/2026-10-16/`.
Questions: which live references remain, which merged packaging contracts apply,
and which acceptance gates can be evidenced locally?
The caller explicitly requires keeping current workflow/check names and recording
the naming question. Issue comments also contain a 2026-10-15 owner decision to
retain those names until after cut-over. Later naming remains separate work.
ADR 0006's updated src build context overrides its older project-context comment.

## Extension Registry and Participation

Repository instructions and caller scope selected; RPI phase skills selected.
No external/domain research needed for this mechanical cut-over. Research lanes
remain inline because they trace one coupled deployment path. No specialist
delegation. Non-interactive intake; explicit user direction supplies phase authority.

## Research Cycle Log

Cycle 1 opening: Wider inventories live targets; Deeper checks packaging and
commands; Contrarian checks stale historical identifiers and deployment claims.
Prior knowledge: source moves already merged; verify rather than copy code.
Research disposition: executed. Planning Readiness: Ready.

### Wider wave

Merged #199 already moved every executable file: `git ls-files mvp` returns
only `mvp/README.md`. Existing 2026-10-15 issue-200 artifacts describe the
generator and committed-data guard already delivered. Do not redo that move.
Reflection: remaining work is consistency and regression coverage, not migration.

### Deeper wave and evidence

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | `.github/workflows/mvp-ci.yml:1`, `.github/workflows/mvp-validation.yml:1` | Names and job IDs retained; paths already mostly src but omit shared src build inputs |
| C2 | `src/api/src/zava_forward/api/__main__.py:1`, `src/api/Dockerfile:49` | ADR entry point prints version instead of serving; Docker bypasses it |
| C3 | `infra/modules/containerapps.bicep:240`, `infra/modules/containerapps.bicep:396` | Job module names already migrated but both use apiImage |
| C4 | `src/api/Dockerfile:11`, `src/orchestrator/Dockerfile:1` | API unnecessarily packages orchestrator; isolated job image already exists |
| C5 | `src/core/src/zava_forward/core/factory.py:11`, `src/core/src/zava_forward/core/synthetic/__init__.py:8` | Runtime defaults inside cwd, unlike generator's external default; shared folder/file convention exists |
| C6 | `tools/rename-zava.py:133`, `tools/rename-zava.py:390`, `tools/rename-zava.py:446` | Branding tool still targets retired web/policy paths and can recreate mvp/web |
| C7 | `.gitignore:12`, `.github/workflows/mvp-validation.yml:55` | src data ignore and guard already delivered |
| C8 | `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py:29`, `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_mvp_coverage.py:5` | Generator uses installed core; coverage imports core; preserve filenames and dated recipes |
| C9 | `infra/scripts/initialize-workbench-staff.py:1`, `infra/tests/test_initialize_workbench_staff.py:13` | Already use installed packages; SQL driver guide still suggests PYTHONPATH |
| W1 | https://github.com/jmservera/ama/issues/200 (read with comments 2026-10-16) | Owner retained check names on 2026-10-15; caller independently requires preservation |

Reflection: reuse the existing synthetic path resolver for runtime defaults,
preserving exact configured JSON filenames. Move jobs to the existing orchestrator
image without changing identities or permissions.

### Contrarian wave

Historical ADR context, parity rows, dated deployment tags and original naming
assertions are evidence, not stale live instructions. Blind replacement would
destroy provenance. Existing src-ci expects the API entry point to print a version;
update that specific probe when the real entry point starts serving.
Docker requires noninteractive sudo locally; Bicep 0.48.1 is available. Installed
packages and mypy/ruff are missing, so local validation must install with pip.
Azure deployment is not needed to verify this path-only change and is not
claimed: new-tag deployment/healthy revision acceptance remains unmet.

## Alternatives and Decision State

Accept isolated orchestrator image plus real API entry point and narrow path fixes.
Reject copying workloads or changing check names. Defer cloud deployment, private
data relocation/backup and final naming/branch-protection rename to owner cut-over.
No new legal rule, approval, feature or SQL dialect is introduced.

## Planning Readiness and Continuation

Ready for Plan under the explicit full-loop parent. One focused three-wave cycle
covers the material questions; no second cycle would change the scoped decision.
Artifacts self-check: internal evidence and external issue provenance recorded,
private data not read, pre-existing delivered work distinguished from new work.
