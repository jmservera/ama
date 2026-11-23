---
title: Issue 2312 live r2 details (2026-11-23)
ms.date: 2026-11-23
---

## Phase details

* Shape errors: `prediction for case X missing`, `prediction for case X malformed: <reason>`; `correct` counts only well-formed answers equal to expected.
* Critical errors are deduplicated per case with `set` over strings.
* CLI: `python -m zava_forward.agents.eval_harness MANIFEST PREDICTIONS [--recorded RESULT]`; prints the report as sorted JSON; with `--recorded` prints the `verify_recorded` verdict instead.
* Tests: missing prediction, string `critical_errors`, duplicate error counted once, CLI exit codes and determinism via `main(argv)`.
