---
title: 149 UX complete parent changes
ms.date: 2026-11-13
---

* Merged 8006506142 (#152) onto 8e786b62d with --no-ff; no conflicts.
* Divergence: the merge left stale sha256 entries for workbench-manifest.json and test_workbench.py in docs/reference/research/retrofit-synthetic-data/scenario-manifest.json (test_scenario_manifest and test_needs_inventory errored). Refreshed both digests.
* Validation (src/api, PYTHONPATH=tests:../core/tests:../agents/tests, venv /tmp/venv-uxp-1420): test_programme_screen 24 OK, test_content_standard 20 OK, test_design_system 9 OK, test_workbench 6 OK, test_role_screens 9 OK, test_role_screens_conformance 12 OK, test_scenario_manifest 8 OK, test_needs_inventory 11 OK after the digest fix.
* ruff check clean; ruff format --check 152 files formatted; mypy (strict via pyproject) no issues in 236 files.
* Not run: browser checks, full RPI gate (Focused tier), hosted CI.
