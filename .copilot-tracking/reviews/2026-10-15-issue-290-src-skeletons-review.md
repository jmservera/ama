---
title: Issue 290 review
ms.date: 2026-10-15
---

Review executed once after implementation; outcome: conformant with open items.

| Acceptance criterion | Evidence |
| --- | --- |
| `src/README.md` indexes projects and states the dependency rule | `src/README.md` |
| Five projects, own `pyproject.toml`, import root, tests outside the package | `src/*/pyproject.toml`, `src/*/src/zava_forward/*`, `src/*/tests`; tests and ruff and mypy pass locally |
| PEP 420 namespace, five distributions side by side | No `__init__.py` at `zava_forward`; all five editable installs import; namespace test in each project and CI job `src-namespace` |
| `core` has `sql` and `blob` extras; `agents` installs neither | `core/pyproject.toml`; agents metadata test; local agents image has no `mssql_python` or `azure` |
| Hashed requirements and four Dockerfiles with digest pin, user 10001, no data, read-only root | `requirements.txt` per project; local builds and runs passed. CI re-checks |
| Import test per project enforces the dependency rule | `tests/test_dependency_rule.py` with a detector self-test |
| One CI job per project and existing `mvp` jobs keep passing | `src-ci.yml` matrix; `mvp-ci.yml` untouched; local mvp suite 719 OK. CI result pending |
| `.dockerignore` and `.gitignore` keep `data/` out; `ZF_DATA` | `src/.dockerignore`, `.gitignore`, Dockerfile `ENV`, job `src-no-working-data` |
| Installs and tests green locally first, then in CI | Local green recorded in the changes artifact; CI pending |

Findings:

* Docker build context differs from the ADR wording; the ADR is amended and the decision is listed in the pull request.
* Open: CI run and Trivy result; the per-project core extras are provisional; `mvp/` and move-not-copy work remain in #199.

Follow-ups: first CI run on the pull request; #199 module moves; #144 removes the `api` to `agents` edge.
