---
title: Research for issue 125 live demo proof of the read-only discovery assistant
ms.date: 2026-11-18
---

Refs #125. Task issue-125-live. Research disposition: executed. Planning Readiness: Ready.

## Scope

Synthetic desktop demo; live Azure authorised in rg ama (cap USD 700, no drills, no Key Vault rotation, no production change). Unticked criteria: (1) readiness list satisfied before company data connection; (2) no write access to operational systems; (3) compared against manual analysis and conventional reporting.

## Findings

* Source: five pure modules `src/core/src/zava_forward/core/discovery_assistant_{boundary,drafting,evaluation,acceptance,demo}.py` plus the `discovery-demo` CLI (PR #1355, `a0f7cf1`, ancestor of this branch). No `src/api`, `src/agents` or `src/orchestrator` code references them.
* Deployed demo API `ca-cutover-test-demo-api` runs image `sha256:5368f4e4...e17e5fb` (revision `--0000031`). Live probes (signed in as the employee demo account, Playwright, credentials never printed) show discovery-named paths behave exactly like an unrelated control path: GET 403 "Your role does not include this", POST 404 "Not found". The workbench home shows no discovery or evidence assistant. So the live demo exposes no discovery assistant route, read or write.
* Static scan (AST) of the five modules: no network, store, subprocess, file, model or credential imports. `datetime` is used only for `fromisoformat` parsing, no clock call. Only `discovery_assistant_demo` prints (its CLI report).
* CLI run: `company_connection` DENY, readiness NOT_READY with all 10 items missing, `write_source_system`, `contact_resident` and `rank_properties` denied (`DENIED_BY_AUTHORITY_BOUNDARY`), `read_company_dataset` denied (`NOT_ON_READ_ONLY_ALLOWLIST`), every decision `attempted:false, dispatched:false, writes_to_source_system:false`, `model_used:false`, status UNAPPROVED_DESIGN_HYPOTHESIS, comparison `criterion_met:false` with no human result pointers, three identical repeat digests.
* Offline tests: 47 discovery assistant tests, 46 pass. One fails only in this environment (`InstalledCommandTests.test_demo_runs_from_this_worktree_without_inputs`): the test replaces HOME, so the user-site `.pth` that makes `zava_forward` importable disappears (`ModuleNotFoundError`). Equivalent CLI run with explicit PYTHONPATH succeeded (cli-demo.txt). Not a product defect.
* Limits: the three criteria concern company data, operational systems and actual human comparison; the demo holds none of these.

## Evidence

All under `.copilot-tracking/evidence/2026-11-18/issue-125-live/`: `offline-tests.txt`, `offline-tests-abs.txt`, `cli-demo.txt`, `probe1.py/json`, `probe2.py/json`, `static_scan.py/json`, `workbench-home.png`, `common.py`.

## Planning readiness

Ready: docs/evidence-only; no source change; Tier FOCUSED.
