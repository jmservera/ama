<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-501 default fixture correction research
description: Prospective research for correction cycle 1 of review finding RV-501
ms.date: 2026-10-26
---

Written 2026-10-26 after the RV-001 review returned Non-conformant (RV-501) and before the plan, critique and any source edit. Start: clean local head `d4f19c70914e82917508552236cf2e599f89bf80`. Earlier reviews are unchanged; this is a new correction cycle, not retroactive compliance.

Findings from reading `tools/test_check_demo_feedback.py`:

* `bundle()` (line ~180) defaults `case_write=case_write()` and `ai=ai_record()`, both hand-assembled dicts. About 60 tests call them directly and mutate deep copies.
* `contact()` and the 40-contact cap test (~548) build handcrafted contact lists; the cap needs 40 existing contacts, which the constructed dataset does not hold, so that one is a justified handcrafted boundary constructor.
* The runtime `RuntimeFixture` added in d4f19c70 already produces the same shapes via `Store.log_call`, `detail`, `verify_ledger`, a reload and `ai_priority` with only `_chat` scripted.
* Runtime construction costs a temporary directory and a Store per call. Immutable baselines cached per distinct request (the default call, a 120 character outcome) plus `copy.deepcopy` per test are enough.
* `core_helpers` currently raises `unittest.SkipTest` when a helper resolves outside the checkout; repository standards expect a clear failure, so it becomes an assertion error. The shared test helper path `src/core/tests` is permitted.

Plan basis: make `case_write()` and `ai_record()` return deep copies of cached runtime-produced baselines (same names, same defaults, no renamed old constructors); keep a separately named `handcrafted_contact` only for the 40-contact cap and oldest-first style boundaries; add regressions that the default `bundle()` equals the runtime baseline and fails if the helper stops using the runtime. Run existing tests to see which depend on hand-set values; adjust them to read values from the baseline, not to loosen assertions. No checker or `src` change. A real checker mismatch would be reported as a blocker.

Limits unchanged: JSON store reload is not SQL durability; offline test release is not release admission; 980 expected baseline is configured, distinct from live 443 open and 980 total; no gate, install, Docker, browser, live or push.
