---
title: Details - numeric boundary D1
description: Phase details for the two numeric corrections
ms.date: 2026-11-10
---

## Phase 1

Add command tests in `src/agents/tests/test_paired_report_command.py`:

* a negative 401-digit integer and a small negative for `elapsed_seconds` and `review_seconds`: exit 1, empty stdout, message with `observation N`, the key and `negative`, no `Traceback`, and an explicit `--record` temporary destination untouched.
* a subnormal cards `elapsed_seconds` (5e-324) with chat 31536000: exit 1, empty stdout, option-prefixed `not finite` refusal, record destination untouched.
* exactly 31536000 accepted for both fields; 31536001 refused with `exceeds`.

Run first and capture the red result.

## Phase 2

In `_check_observation` replace the upper-bound test by `value < 0 or value > MAX_SECONDS` with separate messages (`must not be negative`, `exceeds`). In `constructed_section`, after the scorer returns, call `json.dumps(result, allow_nan=False)` inside `try/except ValueError` and refuse with `derived values are not finite (for example an elapsed ratio from a near-zero cards duration)`. In `main`, build the section before `run()` so refusal precedes report generation and `--record`.

## Phase 3

README: one sentence for the negative and derived-finite refusal. Validation as in the plan.
