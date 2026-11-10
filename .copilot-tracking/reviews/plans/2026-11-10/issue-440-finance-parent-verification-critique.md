---
title: Issue 440 finance-parent verification critique
description: The single final-candidate critique of the verification plan, written before execution
ms.date: 2026-11-10
---

Execution: once, by the parent author, before any test run (no nested agents, per the brief). Verdict: `proceed with amendments`; all findings are compatible with the brief and applied directly. No significant or divergent issue needs a user decision.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | The ambient interpreter resolves `zava_forward.*` to the primary checkout, so a bare run would observe other bytes and call it parent evidence | Applied: external venv with `--no-deps` editable installs of this worktree; record `direct_url`, `__file__` and blob hashes before any test is run |
| 2 | Editable installs may leave `*.egg-info` under `src/*`, which is ignored but would break a "clean including ignored" claim | Applied: record via `git status --ignored` after the run, remove only artefacts this task created, and state it in the changes record |
| 3 | Core and API share test module names; the API test needs flat Core helpers and the `tests` namespace together | Applied: select explicit module names only, record `sys.path` order and resolved `__file__` for `dataset`, `test_form_staging`, `tests.test_mvp` |
| 4 | The API test blob on main differs from the finance blob, so a pass could be misread as main compatibility | Applied: the API result is labelled parent-only; the file-level overlap is reported as unverified main integration |
| 5 | Installing build tools needs the network, in tension with "no network" | Applied: limited to hashed pinned build tools into an external venv; disclosed; no model, provider or Azure access; if it fails, stop as `blocked` rather than fall back to ambient installs |
| 6 | A type or lint run on an unchanged tree adds no observation and a selected-file surrogate would be misleading | Applied: not selected |
| 7 | Historical test counts must not be quoted as expectations | Applied: counts are taken only from this run's output |

Rejected: none. Plan is not re-critiqued.
