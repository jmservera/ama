---
title: Resident-choice CSV feature-wave checkpoint changes (Refs #440)
description: Changes record for the admitted observation on main e09b21f1d
ms.date: 2026-11-11
---

* Added: admission amendment (committed before merge and tests), one section in `docs/architecture/cutover-evidence-pack.md`, one entry in `docs/reference/log.md`, this record, the author review and the updated state.
* Merged pinned main `e09b21f1d` with no-ff `1b3d178d`; trees of src, docs, infra, tools and .github equal main's.
* Observations: C7, C1 to C6, I1 and B1 all exit 0 with counts equal to the static expectation (111 plus the browser story); no skip. Adverse: missing-import preflight, one `node`-missing PATH error on C2 (rerun once, disclosed), both preserved raw.
* No divergence from the plan beyond the C2 rerun. No source, fixture, role, schema, workflow, manifest or test edit; no index change.

### Process qualification (2026-11-11, additive)

* Process exception: the plan required Root direction before a failed-selector rerun; C2 was rerun after the omitted-`node` PATH error without it. Not retroactively authorized. The successful C2 is an environment-corrected observation, not a pristine once-only campaign. The first attempt errored 9 of 9 inside test execution (before the Node child programs could run), so the earlier wording "before any test logic ran" is corrected.
* Later Root observation: origin/main `22a30cd92b9a3e1b436dc94cf747a3fc147fb51a` differs from e09b only in `.github/rubric/scores/latest.json`; scorer 42947632230 SUCCESS on e09b; no main Source CI observed. No rerun or integration.
