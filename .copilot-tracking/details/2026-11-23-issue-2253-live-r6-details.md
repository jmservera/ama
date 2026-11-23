---
title: Issue 2253 live r6 details
ms.date: 2026-11-23
---

Phase 1: add `test_resident_sensor_chart_geometry_with_dense_history`; run `python3 -m unittest tests.test_epic149_child_ux_contracts`, ruff check, ruff format check and mypy in `src/api`.
Refs #2253. Details for the plan phases: the harness is a node script passed on stdin by the Python test; it builds a stub `document` whose elements record tag, attributes, children and textContent, evaluates the sliced source with `vm`, calls `sensorChart` with synthetic histories and prints the SVG node list as JSON. Python asserts on the JSON.
