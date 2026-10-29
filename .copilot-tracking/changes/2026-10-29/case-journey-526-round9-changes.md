---
title: Case journey round nine implementation evidence
description: Mounted raw-form feedback and retained challenge recovery
ms.date: 2026-10-29
---

Task526-round9, full-plan scope; intake 24d7ca9c. Research reused/Ready and sole
critique Complete/Pass. Preserve all earlier original outcomes.

## P01

Implemented session-owned raw presentation state and retained-form synchronization
in panels.js. The latest form renderer receives eventual feedback, disabled/busy
state and error focus. Whole-form challenge restoration rebinds presentation
without clearing transport locks or history barriers. Input/reset events preserve
pending/history feedback. Successful writes with failed reload instruct history
recovery; fresh accepted history restores usable retained controls.
The existing acknowledged-success draft rule remains: a challenge form edited
during its successfully recorded write stays disabled with explicit draft
feedback, even after history recovery, until confirmed discard. Newly rebuilt
forms are not that recorded form. This avoids turning presentation recovery
into authority to repeat an acknowledged action.

Extended the existing shipped-code raw unit matrix and journey reconstruction
helper with mounted feedback, actual retained-form restoration, subsequent
typing, structured/malformed outcomes, successful writes/failed reloads and
corrected retry. No unit methods or browser helpers added/removed. API README
describes the behavior. No transport/queue redesign or significant divergence.

## P02

Final validation and sole independent Review completed; retained locally together.
No Azure/push/publication acceptance. External output prefix:
/home/azureuser/.copilot/session-state/080db6d6-d0c1-4fa2-88bc-88315035d344/files/.

## Preserved Development Attempts

* round9-focused-01: 27 focused units passed.
* round9-validation-01: 117 related units passed, one skip; Ruff100 and mypy99
  passed. Journey found that the challenge input listener erased pending status
  during later typing. Fixed the state/render synchronization, added the same
  input event to the unit matrix. Assistants/challenge not reached.
* round9-validation-02: same 117 units/static checks passed. Extended raw
  lifecycle cases passed; a later existing successful-resident assertion still
  expected the old literal Recording/empty status. Updated it to require the
  new explicit pending/success feedback. Assistants/challenge not reached.
* round9-validation-03: same 117 units/static checks passed. Journey caught
  an intercepted retry-count race: request notification preceded route callback
  delivery. Added an observable pending-transport wait before count inspection,
  retaining the exact one-retry assertion. Assistants/challenge not reached.
* round9-validation-04: 117 related units/static checks, journey (407 assertions)
  and assistants (206 checks) passed. The optional challenge invocation lacked
  its required --axe/--out arguments and exited before executing; no challenge
  success was claimed from this attempt.
* round9-challenge-01: default, history, navigation and refresh-draft modes
  passed with pinned axe. The pending-draft mode exposed that initial raw
  presentation recovery enabled an acknowledged challenge's later draft.
  Preserved its original assertion and fixed exact-form acknowledged state;
  added unit/browser coverage distinguishing this from unconfirmed outcomes.
* round9-validation-05: 117 related units ran, one skipped, one failed because
  the expanded successful-challenge unit expected the resident success wording
  instead of the preserved submitted-values feedback. Corrected that exact
  assertion without changing the existing challenge suite or behavior.

Each attempt used the caller's flock -n admission and worktree src/test imports.
Failed output remains external and unchanged. These were implementation-time
iterations, not repeated critiques or Reviews.

## Final Validation

Final external directory: round9-validation-06 under the prefix above.
One successful admitted command ran all final suites with the caller's
flock -E 75 -n /tmp/ama-rpi-heavy.lock, 15-second retries bounded at 40 minutes.
No lock contention occurred. From src/api, PYTHONPATH explicitly included
this worktree's api/core/agents src and test directories; .venv supplied Python,
Ruff and mypy. No dependency or server source changes.

```bash
python -m unittest test_case_journey test_workspace_scripts -q
python -m unittest test_case_journey test_workspace_scripts \
  test_accessibility_baseline test_design_system test_content_standard \
  test_procurement_api test_resident_api test_timecapture -q
ruff check --line-length 100 src tests checks
mypy
python -m checks.case_journey_browser_check --axe <pinned-axe> --out <out>/journey
python -m checks.assistants_browser_check --axe <pinned-axe> --out <out>/assistants
python -m checks.challenge_browser_check --axe <pinned-axe> --out <out>/challenge-default.json
```

The last command also ran with each existing --history, --navigation,
--refresh-draft and --pending-draft mode and a separate output file.
Pinned axe: /tmp/ama-526-evidence/axe-4.10.3.min.js, version 4.10.3,
SHA256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.

* Focused: 27 tests pass, 2.591 seconds.
* Related: 117 tests pass, one skip, 43.623 seconds. Expected unknown-law-store
  diagnostics from synthetic fixtures are present; no live rule acceptance.
* Ruff100 passes; mypy passes for 99 source files; panels.js node syntax,
  changed unit Ruff format and git diff --check pass.
* Journey: 406 PASS assertions, 87 axe states, zero violations/page errors,
  Chromium 156.0.8078.4, real chrome.tabs.setZoom=2.
* Assistants: 206 checks, 56 axe states, zero violations/page errors,
  Chromium 155.0.8059.39.
* All five unchanged challenge check modes pass: default/history/refresh-draft/
  pending-draft include 11 axe states with zero violations; navigation records
  two committed writes, zero stale refresh reads and no page errors.
* Journey has 86 incomplete axe items, assistants 56. Automated results are not
  manual WCAG, whole-system, hosted, deployed, legal or human acceptance.
* Prior round-eight full API discovery: 1,208 tests passed with 316 skips.
  Final round-nine validation intentionally used the planned related selectors;
  no new full-discovery claim is made.

Final API diff SHA256 against intake 24d7ca9c:
4ff233b6f48662b082a0010b9053014edb1ae7d9f3014b09a42614b0bd5d748b.
Final unit.log SHA256:
63a9b70e38103155297510227f78edf01c30beba0cb54ef6566290b37a330eec.
Journey results/log SHA256:
06d98e38e400f3c0ed20124118a241d2b2fa15e5645ad005e5936484fb92ed69 /
582755d632e770ba9dbf330b55db6ce917001a86710e7fac232dc3d6793823ac.
Assistants results/log SHA256:
9052748a28fec49cc0ca0391b25160f0ec18673f7b019a04c940ae49bcb3514a /
260b43d55d4674311b0c57acfcbc1bb3a9c9aa46ba7fb74e779ad1a02a23f590.
Challenge default/history/navigation/refresh-draft/pending-draft JSON SHA256:
fbf98101ac767c77350cf4348fdc53cf80c3419648738c5edc13e880d9c468dd /
1373f3b44934d44e621ef8adabb8056b8b076966f51e0674afc8ffbe409bc0c6 /
94e38ca7a0dee526ea24b47d5436f09456c922f0085e857d210ee1518c1a8ced /
57f8283e6a08b6bbd589e1c8b6cf3a0cf2997415d2739d077cb4ff8e26f4b9d7 /
93932ecdb3365026255a1229c6c2e1d7d25a7a32144f442f909aef8a49851ee6.

No Azure/full local publication gate, receipt, scanner/SQL publication check,
hosted/human approval, push or remote mutation is claimed. Coordinator owns
the fresh-base exact-head publication gate and any later push.

## Review and Local Handoff

Sole independent Review execution Complete / outcome Conformant, zero findings:
.copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round9-review.md.
Independent shipped-JavaScript lifecycle/navigation probes and exact evidence
hash verification supplement the supplied passing checks. Assessed source
boundary is unchanged. No later implementation amendment or repeated Review.

P01/P02 complete; current automatic task completed in Follow-up, automatic
session still running with no selected child. This local Conventional Commit
retains source, research, plan, details, original critique, changes, original
Review and state. Original round-eight Not accepted remains in 24d7ca9c.
Authenticated GitHub identity supplies repository-local privacy-safe author and
committer email; required Copilot trailer included. Refs #526 is non-closing.
No push. Coordinator owns separately authorized publication gate/receipt/push,
hosted approval and manual accessibility/human acceptance.

## Post-Commit Upstream Handoff

Reviewed implementation/evidence commit: 7b987c63f070dff8466acdecc661dd5143985cb4.
Clean worktree and committed API diff hash independently match the frozen
Review boundary. Round-eight correction remains 24d7ca9c.

Final upstream inspection discovered rubric bot commit 27d11262 on the topic
remote, changing only .github/rubric/scores/badge.svg and latest.json.
The shared remote-tracking ref advanced after intake. The requested
git pull --ff-only was attempted and safely refused the now-diverged history.
No merge, rebase, amend, cherry-pick, force-push or ordinary push was performed.
Coordinator must reconcile this upstream bot change without losing the two
local corrections, then rerun the mandatory exact-head publication gates.
This additional local handoff-metadata commit changes no reviewed executable
source and does not claim an exact-head gate or a repeated Review.
