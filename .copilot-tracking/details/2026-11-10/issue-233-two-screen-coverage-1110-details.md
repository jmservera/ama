---
title: Issue 233 two-screen tension coverage details
description: Phase details for the technical and quality screen coverage increment
ms.date: 2026-11-10
---

## Phase 1 details

* In `tension_data()` after `data = synthetic_data()`: `extra = technical_quality_data()["cases"][0]`; set `data["cases"][0]["technical"] = extra["technical"]` and `["quality"] = extra["quality"]`. Leave `measures` and `documents` unchanged so the three existing screens are unaffected.
* Constants: `TECHNICAL = "Technical queue"`, `QUALITY = "Quality queue"`; withheld lists copied from role-screens.js lines for each screen.

## Phase 2 details

* `check_technical`: panel titles include Technical readiness, Design version, Separate sign-offs, Returns and routing, Missing references, then withheld last; Missing references precedes withheld; withheld text via `check_withheld`; fixture values shown (design version, recorder, change note, signed-off assessment, Returned design with reason, Needs reassessment, Coordination Not given); readiness panel does not claim completeness; stock conflict SQ-1 unresolved shown; no funding amounts; `check_readonly`.
* `check_quality`: panels `Loft insulation: Returned` and `Cavity wall insulation: Fixed, awaiting reinspection` before withheld; readiness is not the all-accepted success text; defect owner, not yet fixed, remediation evidence supplied/not supplied, "No evidence" for the blank check; withheld via `check_withheld`; `check_readonly`.
* Both: `open_screen` keeps ZF-1 selected in the URL; widths loop with `check_regions_and_keys` and scroll check; screenshots under existing env switch.

## Phase 3 details

* Tests: complete technical list passes; complete quality list passes; dropped item fails; absent "Withholding is not authorisation" fails.

## Phase 4 and 5 details

* Pinned tools from `~/.venvs/zf123-pinned`. Runtime from the read-only pinned playwright venv with this worktree first on PYTHONPATH. Docs: one sentence per file, ISO dates, no em dashes.
