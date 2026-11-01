# Issue 156 research: executable design traceability gate (2026-11-01)

* Task: issue-156-design-trace-gate-executable; parent: prior 2026-10-18 RPI (PR #400, #401 merged).
* Research disposition: reused plus bounded fresh inspection. Planning Readiness: Ready.

## Evidence

* Issue #156 AC2-4 are ticked; AC1 (each screen feature links journey, task flow, design artefact) is unmet because all 74 screen traces say `NOT SUPPLIED` for the current design version. Closure audit 2026-10-31 confirms no new ticks.
* The register is the 5-column Markdown table under "Known screen features and exact trace or gap" in `docs/reference/research/ux/zava-forward-prototype-profile-review.md` (74 rows, reference-style links defined near line 447).
* Gap: the gate is prose only. Nothing machine-checks that every screen row names a journey, a flow (or explicit gap) and a design artefact (or explicit NOT SUPPLIED), so "feature delivery design review gate" cannot be run or demonstrated.
* Existing offline-tool pattern: `tools/check-demo-feedback.py` with `tools/test_*.py` unittest outside any package; stdlib only.

## Decision

Deliver a stdlib `tools/check-design-trace.py` that parses the register, validates structure and link resolution, and reports gate state (screens with a supplied design vs `NOT SUPPLIED`). It never fabricates design evidence: while any design is NOT SUPPLIED the gate verdict is `blocked` (exit 1). AC1 therefore stays unmet; PR uses `Refs #156`.

## Out of scope

Authoring designs, human review, accessibility/content evidence, ambiguities, new UI, mvp/ or prototype/ code.
