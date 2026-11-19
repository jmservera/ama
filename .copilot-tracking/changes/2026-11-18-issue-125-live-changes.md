---
title: Changes for issue 125 live demo evidence
ms.date: 2026-11-18
---

Refs #125. Tier FOCUSED: no `src/` change, so FULL tier and mypy/ruff do not apply; `rpi-checks.py --all` not run. Classification basis: docs and evidence only.

## Files

* Added `docs/reference/research/issue-125-live-discovery-assistant-evidence-2026-11-18.md` and `issue-125-live-workbench-home-2026-11-18.png`.
* Updated `docs/reference/README.md` (index) and appended `docs/reference/log.md`.
* Added `.copilot-tracking/evidence/2026-11-18/issue-125-live/` (probe scripts, JSON, CLI output, test output) and RPI artifacts.

## Validation

* `PYTHONPATH=$PWD/src:tests python3 -m unittest` for the five `test_discovery_assistant_*` modules in `src/core`: 47 run, 46 pass, 1 environment failure (HOME replaced, user-site import path lost; recorded in the evidence note).
* `python3 -m zava_forward.core discovery-demo`: exit 0, `overall_passed` true, company DENY.
* Live probes (`probe1.py`, `probe2.py`): discovery paths identical to an unrelated control path. No Azure change.
* Literal scan of docs and evidence for the three credential values: no match.

## Per-criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| Readiness list satisfied before connection to company data | Unproven (cannot be proven for the demo) | Needs human-supplied Phase 0, access and privacy evidence; gate shows NOT_READY 10 of 10 and DENY |
| Assistant has no write access to operational systems | Partly proven at demo scope only; not ticked | Pure policy module, no route live, writes denied and not dispatched; no real operational system or access review exists |
| Compared against manual analysis and conventional reporting | Unproven (cannot be proven for the demo) | `criterion_met:false`, no human results; conventional table is not independent |
