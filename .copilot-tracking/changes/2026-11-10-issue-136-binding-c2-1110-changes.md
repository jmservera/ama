---
title: Issue 136 binding C2 changes
description: Changes record for the bounded C2
ms.date: 2026-11-10
---

## Edit

Only `infra/tests/test_bicep_policy.py` (21 insertions, 5 deletions, four hunks), on the tracking commit after C1 head `c6310ea91`.

* Ruff format (isolated, line length 100) wrapped the four introduced long lines (2192, 2234, 2244, 2294, all attributed by `git blame` to `53fcf666c`).
* `refusals` annotated as `dict[str, tuple[dict[str, object], str]]`, removing the two introduced mypy `dict-item` diagnostics. No ignore, `Any`, cast or config change.
* The C1 import fallback, clock and readback changes, Bicep, README, image and all controls are untouched.

## Evidence (raw files in `ROOT/phase136-binding-c2-evidence-1110/proof`)

* Red on the C1 head: `red2-ruff-check` FOUR E501 (exit 1), `red2-ruff-format` four hunks (exit 1), `red2-mypy` five diagnostics (exit 1). This corrects the C1 summary that said three E501.
* Base `d52f20a5`: `base-ruff-check` and `base-ruff-format` exit 0; `mypy-base` exit 1 with three diagnostics.
* Green: `green-ruff-check` and `green-ruff-format` exit 0 on both infra tests; `green-mypy` exit 1 with only the three baseline diagnostics (same messages as base, shifted line numbers), so not a strict pass. mypy on this file is a README-documented local diagnostic, not a workflow step.
* Impacted tests pass: policy 60, container contract 7, IoT Hub 23, API simulation 30, startup 4 on image `sha256:cc1ec99e86db174ffc0bfac94512db423bfd81fe80c1a8e637f5e04dfe5aaea8` (ID reconfirmed, `src/` identical to base); Bicep build and lint exit 0 for main, guard and containerapps.
* Misruns preserved: `green-*.nofix-misrun.*` ran before the fix was applied (wrong patch path); `test-*.prefix-unfixed.*` are regression runs on the unfixed file, rerun after the fix.
* Heavy lock: first attempt busy (holder flock pid 3943948, not killed or queued), a later single attempt succeeded; no leftover containers.
* Process disclosure: an exploratory fix preceded research-open (`premature-exploratory-fix.patch`), reverted with `git apply -R` and reapplied after implement-start. No stash, reset or hooks override.
