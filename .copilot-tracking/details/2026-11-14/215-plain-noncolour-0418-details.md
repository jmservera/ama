---
title: Details - #215 non-colour, keyboard and plain-language matrix
description: Phase details for the test-only change
ms.date: 2026-11-14
ms.topic: reference
---

## Phase 1

Classes: `RoleCoverageTests`, `NonColourSignalTests`, `PlainLanguageToggleTests`, `DoubtAndNoSourceTests`, `LiveRegionRoleTests`. The role list is checked against `zava_forward.core.projection.STAFF_ROLES`.

## Phase 2

Aliases re-export `RegulatoryCueTests`, `ProvenanceAndOutcomeTests`, `WidgetKeyboardTests` and `RegulatoryDisclosureTests` without copying cases.

## Phase 3

No change to `chat-widget.js`. `test_accessibility_baseline.py`, `test_scenario_manifest.py` and `test_needs_inventory.py` run as proof, and the recipe SHA in `scenario-manifest.json` stays valid.

## Phase 4

Commands per the task. Focused tier; basis: tests only, no workflow, dependency, deployment or security-control change.
