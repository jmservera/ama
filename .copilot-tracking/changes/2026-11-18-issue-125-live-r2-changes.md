---
title: Issue 125 live r2 changes
date: 2026-11-18
---

Refs #125. Tier FOCUSED (docs only; no src change). No Azure resource created or changed; throwaway venv removed.

## Files

* Added docs/reference/research/issue-125-live-r2-discovery-assistant-2026-11-18.md
* Edited docs/reference/README.md (index line), docs/reference/log.md (entry)
* Added .copilot-tracking/evidence/2026-11-18/issue-125-live-r2/ (sanitised probes, scan, CLI output, tests, screenshot)

## Per-criterion table

| Criterion | Proven for demo? | Basis | Production-only |
| --- | --- | --- | --- |
| Readiness list satisfied before connection to company data | Unproven | Gate NOT_READY / DENY; inputs need Phase 0 human evidence | Yes |
| Assistant has no write access to operational systems | Unproven (demo behaviour shown) | No I/O imports, writes denied and never dispatched, no live route (same as control) | Yes: needs approved operational connection |
| Compared against manual analysis and conventional reporting | Unproven | criterion_met false, zero human results | Yes: needs analysts on real data |

## Validation

* Playwright live probes (probe1/probe2): discovery GET 403, POST 404, same as control.
* `python -m zava_forward.core discovery-demo`: exit 0, DENY.
* Five discovery_assistant test modules: 46/47 user-site (uninstalled package), 47/47 in clean venv with pip install -e src/core.
* mypy/ruff: not applicable, no Python changed. rpi-checks --all not run (FOCUSED).
* Documentation link and diff review.
