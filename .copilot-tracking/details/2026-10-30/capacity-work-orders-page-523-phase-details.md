---
title: Capacity and work orders issue 523 phase details
description: Bounded implementation and evidence contracts
ms.date: 2026-10-30
---

Task: 523 / capacity-work-orders-page-523. Research:
.copilot-tracking/research/2026-10-30/capacity-work-orders-page-523-research.md.

<!-- rpi:phase id=P01 -->
## P01: Scoped acceptance implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Extend the existing check

Current runtime is already repaired by merged #528. Do not edit core's
null-preserving projection or duplicate the current HTTP regression.
Reuse checks.regulatory_ux_check.AXE_SHA256's pinned digest value for axe validation.
Implementation judgment: keep the same constant locally, as other standalone
checks do, so direct script invocation remains supported without importing
checks as a package or pulling unrelated regulatory test fixtures into this check.
Expose small typed load/scan helpers suitable for the single new unit-test file.
Add `--axe` without breaking current invocations. Scan #app only, using the
existing tag set, at seeded, both initial 503 errors and final empty state.
Use native focus and Enter on Try again, verifying focused state and actual
successful reads. No new UI or styling. Keep all existing SQL fixture ownership,
external network denial, draft retention and late-401 assertions.

Test budget: one new file, at most four methods, no removals. Test the actual
helpers with constructed objects, not static string assertions. Reject wrong
axe bytes explicitly before owned_store. Keep a clean scan distinct from no scan.
Document optional invocation, scope and non-conformance boundaries in the
existing Capacity page compatibility section.

<!-- rpi:phase id=P02 -->
## P02: Validation and review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Package quality

System Python lacks Playwright; shared /tmp/mv lacks installed core. Provision a
fresh external environment via pip and editable core, agents and api[dev].
Use src/api as cwd and the exact requested source/test PYTHONPATH. Run
`python3 -m unittest discover -s tests -q`, `ruff check .`,
`ruff format --check .` and `mypy`. Keep commands, counts and failures externally.
Start with helper tests and existing legacy procurement regression.

<!-- rpi:task id=P02-T02 -->
### P02-T02: SQL browser acceptance

Acquire the caller's shared heavy lock with flock -w 600. The existing CLI
acquires its own lock, so call its public owned_store/check functions from an
external session runner while the outer lock is held, generating the exact
same seed/register fixture as main. Never use an inherited database.
PC-001 correction: before generation, store or App construction, reproduce main's
`patch.dict(os.environ, safe_env, clear=True)` with only PATH, HOME, TMPDIR, LANG
and LD_LIBRARY_PATH from the parent. Do not retain ZF_*, cloud/model/storage,
authentication or unrelated settings. The test-source PYTHONPATH is interpreter
bootstrap only; clear it with the environment before application construction.
Use pinned axe 4.10.3 downloaded from the repository's existing trusted CDN and
verify digest. Run Chromium against the constructed loopback app and retain
stdout/exit evidence. The harness asserts responsiveness through successful
login/API and rendered route checks. It shuts down its server and removes only
its uniquely named SQL container. All navigation entries must be exercised.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Original Review and commit

Review once, independently, only after implementation validation is reconciled.
No second Review or in-task repair of routed findings. If production web files
remain unchanged, explicitly record no changed-web-file review scope; the
existing screen's scans are bounded engineering evidence, not WCAG conformance.
Resolve GitHub account id/login and repository-local privacy-safe email before
committing with required coauthor. Do not push. After committing attempt the
complete local gate to a fresh external directory. Offline-only prerequisites
may block; no Azure commands/cloud fallback or fabricated success.
Final receipt remains external. An unavailable or failed complete gate must be
reported as a publication blocker, not as passing local acceptance.
