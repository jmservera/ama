---
title: Issue 121 resident advisor dispatch hold research
date: 2026-11-17
---

* Scope: assess #121 against main eb51af5c9; evidence only, no DPO or Legal approvals recorded or implied. Focused tier, desktop-only demo.
* Prior delivery: register, dispatch_hold and rights clock in `src/core/.../data_protection.py`; hold wired in `core/ai.py` (`run`, `look_at`, `_request`).
* Measured gap (to reproduce): `src/api/.../resident_demo/aoai.py` `AzureAdvisor` posts a resident question and case progress to Azure OpenAI with no `dispatch_hold` check, so `ZF_DATA_PROCESSING=actual` does not stop that path (DH-006, criterion 3).
* Out of scope: `AzureTopicProvider` (fixed topic word only), #1818/#1641 (mssqlstore, chat grounding), all approvals (criteria 1, 2).
* Planning readiness: Ready.

## Measurement

* Reproduced 2026-11-17: new test `test_actual_processing_mode_blocks_both_paths_before_reserve_or_transport` in `src/api/tests/test_resident_aoai.py` fails on main: with `ZF_DATA_PROCESSING=actual`, events were `reserve, token, transport` for both the topic and question paths.
