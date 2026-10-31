---
title: Employee briefing validation capacity correction details
description: Exact validation boundaries and publication completion evidence
ms.date: 2026-10-31
---

## Opening State

Task 531 / employee-briefing-loading-531-capacity-correction. Existing runner,
pip environment and pinned axe are available. Main integration completed.
No dependency install needed after successful import. Current user direction
allows API/Ruff without lock and requires queued heavy validation.

<!-- rpi:phase id=P01 -->
## P01: Execute and reconcile assurance

<!-- rpi:task id=P01-T01 -->
### P01-T01: Main integration

Completed merge 18c1531f; main 1330869ea675ff019958846330108b4f45e163ce is ancestor.
Rubric, workflow and gate tool match main byte-for-byte; log merged naturally.
No conflict resolution discarded either history.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Requested local validation

From src/api with external pip venv, PYTHONDONTWRITEBYTECODE=1 and
PYTHONPATH=../core/tests:../agents/tests, run unittest discover -s tests -q.
Run python -m ruff check . --no-cache and python -m ruff format --check .
with RUFF_CACHE_DIR outside checkout. Record counts, failures and skips.
The component configuration may exclude checks from Ruff; explicitly run
Ruff lint on changed runner as well to verify exact target. An explicit
file-only format invocation bypasses the inherited checks/*.py exclusion;
record that diagnostic and compare the main baseline before any unrelated
whole-file reformat. The configured project format gate remains authoritative.

Run flock -w 1800 -E 75 /tmp/ama-rpi-heavy.lock <venv-python> -m
checks.loading_briefing_browser_check --axe <existing-pinned-axe>
--out <new-external-browser-output>. Retry once with a fresh output only if
exit 75 means the lock was not acquired. Never retry an assertion failure as
capacity failure. Runner creates/stops constructed loopback server; use existing
external-scratch TemporaryDirectory hook if needed, not a new production helper.
PC-001 disposition: the mandatory external bootstrap is
/home/azureuser/.copilot/session-state/150adff8-0bdd-4492-abae-8a03af70abcf/files/run-loading-browser.py.
It overrides tempfile.TemporaryDirectory's explicit dir argument with its own
external scratch root. It adds -B only to the exact owned command
[sys.executable, "-m", "zava_forward.api.server"], preserving its environment
whitelist and every other subprocess. The launcher also disables bytecode.
The runner's existing healthz probe verifies responsiveness.
Verify process responsiveness from its owned server/browser execution and output.
Retain all axe reports/incompletes and three roundtrip results. No live data/model.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Reconciliation and original correction Review

Record each observed command and result, any tightly coupled failure/fix and
unchanged approval boundaries. Only mark P01-T02 after actual execution.
Fresh independent reviewer activates rpi-review, reads entire branch diff vs
current main plus correction/prior artifacts, writes only original correction
Review. Retain original parent's adverse outcome; do not relabel it conformant.
Review findings route later work rather than a second Review.

<!-- rpi:phase id=P02 -->
## P02: Publish exact committed candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Commit

Resolve gh api user, privacy-safe local email; author and committer same identity.
Commit all correction evidence plus original independent Review with requested
Copilot trailer. Source staging explicit; no secret/generated heavy output.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Full exact-head gate

Fetch main; if base drifted, merge authorized latest main without force, preserve
main rubric/both logs and repeat invalidated validation. Complete gate:
python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 1800
--base <current-main-sha> --out <new-external-directory>.
It owns the same flock internally; do not outer-wrap it and deadlock.
Retry once with new output only on Global heavy-resource lock timeout.
Missing SQL/browser/scanner prerequisites block publication, never a cloud skip.
Retain output external; verify receipt --base <fresh-current-origin-main-sha>.
Independent exact-head assessor reads committed boundary and verified receipt,
writes assessment only externally, no source edits/commit. Repeat verification
immediately before push if assessment did not alter identities.

<!-- rpi:task id=P02-T03 -->
### P02-T03: PR publication

git push -u origin HEAD, no force. gh pr create --base main with external body
listing dated original and correction artifacts, observed checks and honest
unmet live AC7/specialist-note contribution. Use Refs #531. Leave hosted checks,
human approval and merge to owner. Record remote publication evidence externally
to avoid invalidating the authoritative final receipt with a later evidence commit.
After publication, mirror the canonical state externally for final completed
publication status; keep the committed state as the pre-gate handoff snapshot.
