---
title: Test design, coordinator behavior 005 (issue 1204)
ms.date: 2026-11-06
---

* Design ID: HVE-TD-AMA-BDC-20261106-01. Status returned: Complete. Persisted verbatim in designer-return.md (same folder, sha256 recorded in test-log.md); that file is the design of record with scenarios S01 to S20 and their prompts.
* Dispatch evidence: generic task subagent (agent_type general-purpose because the interface requires a type; no selected custom agent), requested model gpt-5.6-sol (first canonical High model), accepted without error on the first dispatch; this first real dispatch served as the availability check, no canary. The returned content states "Runtime model identity is not exposed to me", so returned model metadata is unavailable and the executed model is recorded as requested-and-accepted, not independently confirmed.
* Lead validation: 20 scenarios; all R1 to R9 mapped (coverage map in the return); prompts are self-contained with embedded fixture facts; no scenario names the artifact, path, headings, authoring history or test framing (checked by reading the prompts' structure and grepping for "agent", ".md", "coordinator" in prompt sections, see test-log.md); negative and conflict cases present (S01, S06, S12/S13, S14, S08, S19); intentionally untested behavior and gaps stated by the designer (no real SQL/GitHub/schedule/shell/native host).
* Designer did not write files; the lead persisted the return unmodified.
