# Changes: issue 125 live run 3

Refs #125. No `src/` change; tier FOCUSED (docs only). Divergence: the docs files were drafted during Plan, before this record existed; they are not source.

Files: docs/reference/research/issue-125-live-r3-discovery-assistant-2026-11-19.md (added), docs/reference/README.md (one sentence), docs/reference/log.md (entry), .copilot-tracking/ artifacts and evidence.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Readiness list satisfied before connection to company data | Unproven (production-only, Phase 0/#123 approvals) | CLI NOT_READY/DENY; research note |
| No write access to operational systems | Demo behaviour proven; criterion unproven (needs approved operational connection) | write tool denial, no live route, 47/47 tests |
| Compared against manual analysis and conventional reporting | Unproven (needs human results on real data) | `criterion_met:false`, zero human pointers |

## Validation

* `python -m unittest discover -s tests -p 'test_discovery_assistant_*.py'` in src/core, clean venv: 47 OK.
* `python -m zava_forward.core discovery-demo`: DENY as above.
* mypy/ruff not applicable (no Python change). Hosted CI not observed; nothing pushed.
