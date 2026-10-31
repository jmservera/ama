---
title: Resident issue 466 phase details
description: Exact bounded targets and evidence expectations
ms.date: 2026-10-31
---

## Metadata

Task 466 / resident-sensor-gauges-466.
Plan: .copilot-tracking/plans/2026-10-31/resident-sensor-gauges-466-plan.md.
Research: .copilot-tracking/research/2026-10-31/resident-sensor-gauges-466-research.md.
Initial readiness: source coverage verified; candidate ready for one critique.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Current decision/contract documentation | Complete |
| P02 | Fresh local tests and one Review | Local checks Complete; Review pending |
| P03 | Clean committed-candidate publication | Pending P02 |

<!-- rpi:phase id=P01 -->
## P01: Reconcile current decisions

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update guides and knowledge routing

src/api/README.md acceptance table currently says scope unproven; explicit
2026-10-31 direction now supplies that decision. Record it, retain prior
model/cap/credential choice and differentiate acceptance from activation.
docs/architecture/resident-assistant-prototype.md should gain a dated current
section before the unchanged 2026-10-27 implementation. It must distinguish
eligible generated questions from protected document/safety paths and explain
existing default-off controls. Update its frontmatter, docs/reference/README.md
routing/date and append docs/reference/log.md without changing older entries.
No source/UI/infra/test edit. Completion evidence: exact diff, valid relative
links, decision trace and unchanged runtime/activation files.

<!-- rpi:phase id=P02 -->
## P02: Validate and review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Fresh local checks

From src/api run
`PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`,
`ruff check .` and `ruff format --check .`, preserving skips/counts and failures. Run existing
resident core suites and sensor, assistant and generated-answer Playwright
harnesses. Use existing synthetic generator/constructed residents only.
Use pinned axe for assistant scans if available; report any incompletes.
External task environment/logs; `/tmp/ama-rpi-heavy.lock` for heavy tests.
New/removal tests: zero/none. No model/credential/Azure operation.
Completion evidence: API 1430/320 skips, core 20/zero skips, Ruff both pass,
three existing local Chromium harnesses passed; chat 32 scans, zero violations,
42 incomplete rule/state results. Exact logs/hashes in changes record.
Critique PC-002 applied above. PC-001's claimed parent /tmp prohibition is not
present in supplied constraints; shared-lock instructions remain as required
by src/README.md. Original critique remains unchanged.

<!-- rpi:task id=P02-T02 -->
### P02-T02: One independent Review

Reconcile completed plan markers, changes, exact logs/hashes and limitations.
Fresh Review agent reads full bounded diff, original critique and evidence,
writes only dated Review. Preserve outcome and route findings to later work.
No second Review or fixing Review findings within this task.

<!-- rpi:phase id=P03 -->
## P03: Publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Exact candidate

Resolve authenticated id/login for local noreply author/committer, commit all
implementation/original evidence with required trailer. Run root
`python3 tools/rpi-checks.py --all --base <fetched-main> --out <new-external-dir>`
after commit. Verify receipt against freshly fetched main immediately before
independent exact-head publication assessment and push. Full gate self-locks;
do not wrap it in another flock. Preserve failures externally; never bypass
missing SQL/browser/scanner requirements. Push only the requested branch and
create main PR with Refs #466 and fresh evidence/limits. Owner retains merge.
Final receipt/PR metadata stay external to avoid invalidating the committed
candidate. P03 commit/full-gate remain pending at original Review by design.
Fetch after local validation found main advanced to
1330869ea675ff019958846330108b4f45e163ce. Ordinary branch-only integration
preserves both histories before Review; no main checkout, rewrite or rebase.
The preliminary implementation commit enables that integration. The original
Review and final evidence are committed afterward, before the full gate.
