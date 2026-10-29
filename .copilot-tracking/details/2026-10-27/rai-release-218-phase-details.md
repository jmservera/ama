<!-- markdownlint-disable-file -->

# Phase Details: rai-release-218

Date: 2026-10-27. Task #218. Candidate scope follows research C1-C10.

<!-- phase: P01 -->
## P01: Release policy dependencies

<!-- task: P01-T01 -->
### P01-T01: Reproduce actual dependency omissions

Use the existing synthetic SQLite Base and release_support fixture, never the
normal data path. Patch actual ranking.CURRENT with a copied new policy and
quality.CHECKLISTS with copied definitions. Test real admission, not only a
manually corrupted stored binding. Confirm unrelated capabilities unchanged. PC-001: independently mutate only
the quality keyword mapping, then only its first-match ordering with overlapping
keywords, leaving checklist definitions/version labels fixed. Even when the
selected case checklist is unchanged, actual release admission must deny.
Check every unrelated assistant and retained-route binding stays identical.
Record exact pre-fix failure command and observed assertions.

<!-- task: P01-T02 -->
### P01-T02: Bind policy content

Stock assistant: hash current ranking policy with existing policy_hash;
capture ranking.describe(ranking.CURRENT), not a default-bound old object.
Retained priority: include the same policy_hash in its existing policy binding.
Quality assistant: include checklist definition/mapping fingerprint, preferably
through one quality-owned helper to avoid copying private mapping semantics.
Keep existing nondependent binding shapes stable where possible. New dependent
fingerprints intentionally deny old releases until independently recorded renewal.
Do not renew any real release or change ranking/checklist rules.

<!-- phase: P02 -->
## P02: Oversight and integrated evidence

<!-- task: P02-T01 -->
### P02-T01: Scripted oversight mechanics only

Use plausible critical defects with syntactically valid source IDs to prove
acceptance requires explicit source verification, rejection/correction retains
actor/reason/signature, stale sources block reliance and domain state never
changes. Include a negative control where a script falsely attests wrong text:
record that the software cannot establish reviewer competence or truth.
No observed human detection rate, timing or benefit is fabricated; actual
same-scenario workflow-only effort comparison remains Not run.

<!-- task: P02-T02 -->
### P02-T02: Local validation

Session-owned venv was required after import failed; editable core/agents/API
with declared dev extras installed via pip. Use it for all commands.
From src/api run focused release/assistant/continuity/operator suspension selectors;
from core run resident challenge tests and full core suite as practical; run
API discovery with required shared-test paths. Run component Ruff/mypy.
No SQL Server/browser/Azure claim follows from SQLite/unittest success.
No full or heavy gate. Existing environment-gated skips are not passes.

<!-- task: P02-T03 -->
### P02-T03: Acceptance accounting

Record each #219/#222/#223/#221/#220 criterion separately in changes evidence.
For each distinguish observed local mechanics, unmet approval dependency and
unimplemented coverage. Do not edit upstream whole-feature acceptance to Pass.
Component README explains new dependency versions and human boundary.

<!-- phase: P03 -->
## P03: Review and publication

<!-- task: P03-T01 -->
### P03-T01: Independent Review

Exactly one fresh reviewer inspects final source/test diff, plan and validation
evidence. Preserve its original outcome and route findings without a second
Review in this task. Human acceptance is not replaced by this code review.

<!-- task: P03-T02 -->
### P03-T02: Publish qualified PR

Resolve gh api user and repository-local privacy-safe identity; commit source
and all original RPI evidence with Conventional Commit/trailer. Fetch main and
record base; no rebase, force-push or merge. One PR to main uses Refs for all
named issues, explicitly lists owner decisions and no full-gate authorization.
