---
title: Keyboard probe compatibility checkpoint changes (Refs #440 #132)
description: Implementation record for the documentary checkpoint
ms.date: 2026-11-11
---

## Changes

* `docs/architecture/cutover-evidence-pack.md`: appended section "Keyboard probe compatibility integrated-main checkpoint (2026-11-11, Refs #440 #132 #134)". Frontmatter unchanged (`ms.date` already 2026-11-11).
* `docs/reference/log.md`: appended one entry. No index change (the pack is already indexed).
* Own tracking: research, plan, details, critique, changes, review, state.

## Divergences and amendments

* After drafting, two overreaching phrases were corrected before commit: an unsupported exclusion of PR 1384 and 185 history, and "full 24-path change" read by Root and reviewer (reworded to the supplied change diff).
* Critique finding CK-01 was applied in details before implementation.

## Checks actually run (read-only; no runtime)

| Check | Result |
| --- | --- |
| `git fetch origin main`; resolve | `74e63363`, tree `e89381c5`; equals pin, no movement |
| `git diff f8939a5a 74e63363 -- src` | empty |
| Five document blobs at the pin vs recorded values | equal |
| `gh api` Source CI run 42958485921, jobs; PR 1438 state; comments 6786933451 and 6786645682 | as recorded |
| Anchor of the new heading occurs once; `git diff --check` | exit 0; non-ASCII scan of added lines empty |

Not run: tests, browser, pip, SQL, Docker, model, cloud, `rpi-checks`.

## Author Review

Executed once by the author after the checks above. Outcome: conformant with open limits, recorded in the [review](../../reviews/2026-11-11/keyboard-checkpoint-440-1111-review.md).
