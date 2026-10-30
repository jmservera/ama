---
title: Case journey round eight implementation evidence
description: Shared mutation exclusion and queue draft correction
ms.date: 2026-10-29
---

Task 526-round8, full-plan scope. Intake HEAD 33b0cde3.
Research Ready; sole critique Complete / Revise with PC-001 applied and PC-002
rejected for conflict with explicit caller direction, as recorded in plan.

## P01 Implementation

Shared transport now locks every employee JSON POST by endpoint, action and
target through response parsing and error classification. Mutable note,
revision and document kind cannot bypass exclusion. Unrelated targets remain
independent. Raw resident/challenge forms now use this transport without aborting
their dispatched writes on route changes. Malformed mutation JSON throws rather
than consuming fields; strict raw history behavior is preserved.

Queue sessions belong to the authenticated me object, independent of caseSession.
Latest fields are captured at listing completion and restored by ID/revision.
Existing shared field helpers now accept explicit snapshot/reconciliation
ownership. Changed/missing revisions use copy-only recovery with discard.
Failed listings keep mounted cards and offer GET-only retry. Navigation discard
and authentication changes detach the queue state; late responses cannot repaint.

Sibling audit: all writes in app, assistants, panels, ops, chat and timecapture
use api. case-workspace and role-screens have no mutation owner. The two raw
panel fetches were the only bypasses and are removed. Resident template and
timecapture event callbacks now display transport/duplicate errors instead of
leaving rejected event promises unhandled. This is a tightly coupled local
judgment, not a feature/authority/design divergence.

Focused regressions: two added shipped-code unit methods cover the complete
transport target matrix/body-parsing lifetime and old/failed/changed/missing queue
listings. Existing raw matrix now rebuilds both families mid-flight and covers
strict malformed 200/409/503 responses. No method/helper removals. One new journey
browser helper tests fieldless advance, raw resident and fresh challenge handlers
through refresh and refusal/uncertain/malformed outcomes with axe. Existing
assistant helpers now assert queue success/later-edit/verification/refusal cleanup
and old/failed/fresh/changed/missing listing draft retention with axe.

## P02 Validation and Review

Initial focused units: 27 pass, exit 0. External evidence:
/home/azureuser/.copilot/session-state/080db6d6-d0c1-4fa2-88bc-88315035d344/files/round8-initial/unit.log.

Initial browser attempt round8-browser-01: journey passed, including new pending
reconstruction and malformed feedback states. Assistants failed because the
new test tried editing a case card after Refresh proposals had removed it while
its replacement listing was deliberately held. The queue stays mounted, whereas
the case panel uses cached recovery. Corrected test timing: case edits precede
replacement, queue edits occur after the GET starts. Failure evidence retained
unchanged in external session files/round8-browser-01.

Final source validation completed under one successful `flock -E 75 -n`
admission on `/tmp/ama-rpi-heavy.lock`; the wrapper permits 15-second admission
retries, at most 40 minutes. The lock released when the check command exited.

Authoritative external root:
/home/azureuser/.copilot/session-state/080db6d6-d0c1-4fa2-88bc-88315035d344/files/round8-validation-02.

Commands ran from src/api with this worktree's ../../.venv/bin/python and
PYTHONPATH containing absolute worktree paths for api/src, core/src, agents/src,
api/tests, core/tests and agents/tests:

```bash
python -m unittest discover -s tests -q
ruff check --line-length 100 src tests checks
mypy
python -m checks.case_journey_browser_check \
  --axe /tmp/ama-526-evidence/axe-4.10.3.min.js --out <external-root>/journey
python -m checks.assistants_browser_check \
  --axe /tmp/ama-526-evidence/axe-4.10.3.min.js --out <external-root>/assistants
```

* Full API discovery: 1,208 tests, exit 0, 316 reported skips, 445.325 seconds.
  Skipped integrations do not establish SQL/live acceptance. Focused
  test_case_journey + test_workspace_scripts separately passed all 27 tests.
* Ruff at 100 columns: exit 0. Mypy: all 99 owning source files pass.
  Changed unit file passes Ruff format check.
* Journey: 319 PASS assertions, 57 pinned axe states, zero violations/page
  errors; Chromium 156.0.8078.4 and real chrome.tabs.setZoom=2.
* Assistants: 206 checks, 56 pinned axe states, zero violations/page errors;
  Chromium 155.0.8059.39.
* Both browser suites use axe 4.10.3,
  SHA256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb.
  Journey has 56 incomplete axe items and assistants 56; these still require
  manual review and are not an accessibility conformance claim.
* Eight audited employee JS modules pass node --check; git diff --check passes.
  No dependency change, test removal, generated source or golden replacement.

Final API diff SHA256 against intake HEAD:
e3c2f8f6e947bafacc370dc16c70ba9e4d2b4e9d30baa28982f8bcd165601d78.
Unit log SHA256:
11843284fc4c8b98460256859786597b4888590ce2f3c8464101a34633fb16a4.
Journey results/log SHA256:
360372d816ed902a891cdec57a11a5118c4475c72f07f348ecd504f4c506bc03 /
ebec6967e20cb274c13f27bd07ec49f4f47bc5addfe5e983d2e3bd401989662d.
Assistants results/log SHA256:
79a267a215aade4ec7d50d5b8832f7571ad1abf6d42843488654b979776ce379 /
2cbc0ae9dedaf05ddc2cb330b6e986e3f2d3828c6dccc4632b7e788cd76aef38.

No Azure command or full publication gate ran. No publication receipt,
hosted/human/deployed acceptance, SQL/scanner gate or push is claimed.
P01/P02 executed. Sole independent Review Complete / Not accepted at
.copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round8-review.md.
It confirms both original round-seven defects corrected, but independently
reproduces two Medium raw-form lifecycle defects: detached feedback after
reconstruction and disabled retained challenge forms after authoritative recovery.
Both route to a distinct round-nine child under the user's existing direction
to continue until Conformant. This Review will not be rewritten or repeated.
This reconciled source/evidence is committed locally before that correction.
