<!-- markdownlint-disable-file -->
# Issue88 authorized sensor-main integration

## Authorization and Actual Execution

Integration only, not a third defect-correction cycle. Coordinator authorized
rebase of own topic fix/resident-update-remedy-controls-88 / PR392 onto freshly
fetched origin/main943febc23e99e397724cb81d2580f781b91e13f7 (sensor PR393).
Expected exact old remote d27782a77aaaa2d3571e1869f9464365c48e419c verified
with clean worktree/local matching branch before any write. Main graph:
943febc2 ->74617981 ->22670277. No #394 unmerged source/dirty sibling read.

Actual git rebase943febc2 replayed ten resident commits. Sole textual conflict
was docs/reference/log.md at first implementation commit. Read both entries,
retained complete sensor prefix then resident append; no blind ours/theirs.
Store imports and core guide auto-merged. Store retains sensor export_fields
import and prompt_case/scalars before outbound briefing/document paths plus
resident followup_view and all existing domain guards.

Rebase result before metadata receipt:
051bb1958e5c9b4b2f8dd04d0b35216687e4d67a.
Strict initial suffix assertion found a missing separating newline at the
conflict boundary (upstream prefix itself was exact). Repaired that one blank
line explicitly; second full proof passed. This was formatting resolution, no
runtime fault/correction. Normal integration evidence commit includes it.

## Exact Source, Test and Evidence Parity

Compared own old patch74617981..d27782a7 to new943febc2..rebasedHEAD,
extracting every added/removed line (excluding diff headers/hunks). Exact equality
across all fourteen src paths:

* src/api/README.md, server.py, web/app.js, web/panels.js, test_resident_api.py.
* src/core/README.md, finance.py, projection.py, resident_decisions.py,
  sqlstore.py, store.py, workflows.py, test_handoff_lifecycle.py,
  test_resident_decisions.py.

Compared shared Store/core guide delta d27782a7..rebasedHEAD to sensor
74617981..943febc2: exact added/removed-line equality too. Every nonoverlapping
sensor src path is byte-identical to943febc2, including export_fields,
synthetic/sensor_backfill current-generator verified replay/admission, raw status
and document-before-dispatch validation, closed chat/map export and sensor tests.
No import or guard omitted. All previous resident RPI artifacts including
original Review/critique and correction ONE/TWO receipts are byte-identical to
old published head, not rewritten or re-reviewed.

Before this new log entry, exact final log equality was proved:
full943febc2 log bytes + complete resident suffix from d27782a7 after74617981.
New integration entry appends after both. All index table routes from each
head are retained verbatim. No source change is in this metadata receipt.

SHA256:

* Resident source937a81417a6d073c8ce8f85d976f834af84ab09f0ce1a60c418a158b81587883.
* Resident core tests5e19249110e758aa0490cc9f90d6d6f76342040c2fb883bce875be41233d23a7.
* Combined Store cdf7c1bc2a6e439249d34ad189fdfa0c9a5d135b21024a2679302d7fe00ee552.

## Fresh Combined Validation

Sequential installed-src commands, no dependency reinstall or private fixtures:

```bash
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests:src/api \
  .venv/bin/python -m unittest \
  test_resident_decisions.JsonResidentDecisions \
  test_resident_decisions.SqlResidentDecisions test_resident_api \
  test_sensor_privacy test_sensor_backfill test_sensor_stock test_sensor_faults \
  test_documents test_chat_privacy test_ai_tasks test_chat_isolation \
  test_chat_panel test_document_controls -q
```

240 run96.504s,237pass/three existing skips: resident JSON-only rollback in
SQLite, opt-in resident browser, opt-in actual sensor SQL. Includes corrected
resident responsibility-clock matrix/identity/concurrent-writer/recovery/HTTP,
sensor current-generator replay/admission and tamper refusal, raw status/
document/chat/map closed boundary tests. In this root command test_chat_panel
resolves core module by deliberate core-first fixture path; API panel is separately
and unambiguously executed below. Explicit absent-law-store diagnostics remain
visible; no invented legal approval.

```bash
cd src/core
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
cd ../agents
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
PYTHONPATH=tests:../core/tests ../../.venv/bin/python -m unittest discover -s tests -q
cd ../api
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest \
  test_ai_tasks test_chat_isolation test_chat_panel test_document_controls -q
```

All statics passed: core64formatted/117typed, agents19formatted/23typed,
API23formatted/55typed. Agents94pass/no skips18.012s. Explicit API-local
AI/chat-panel/document boundary100pass/no skips78.459s. Counts overlap prior
selectors; do not sum into a unique-test total. git diff --check passed.

No persistence semantics conflict/change: resident patch, sensor admission and
SQL hooks exact as separately delivered. Therefore no SQL/container restart:
prior correction TWO nine actual MSSQL passes and sensor actual SQL admission
receipts remain historical, not fresh integrated SQL claims. Own prior containers/
credentials already removed; no idle server. No changed web bytes, so prior
guideline/browser/JS/image receipts historical, no repeat or WCAG claim.
No full-core discovery claimed, no paid model, Azure/Graph/IAM/public access,
real resident contact, private input or approvals.

## Exact Criteria and Independent Gates

Purpose/current owner/due/basis still use unchanged update_record and tests.
Response/package never cascades into remedy/defect/query closure: unchanged
separate response/remedy plus mixed-clock tests pass fresh combined selectors.
Each status retains own owner/date: correction TWO route/state responsibility
source/test bytes exact and actual JSON/SQLite matrix passes fresh here.
Sensor current-generator admission and closed exports retain full merged intent.
No new source defect found requiring another correction cycle.

Original single Review/critique and adverse historical dispositions retained.
Source acceptance and final integration disposition remain coordinator-owned;
no independent self-Pass, new full Review, merge or issue closure. Wider
governance RV-001 remains planning-parent/repository-owner routing at next #81
triage to Legal/Housing/Complaints, not a substitute for bounded criterion proof.

## Publication State

Implementation integration and local checks complete; publication pending.
Only authorized exact topic lease:
refs/heads/fix/resident-update-remedy-controls-88:
d27782a77aaaa2d3571e1869f9464365c48e419c.
Fresh gh api user privacy-safe local author/committer plus Copilot trailer required
for evidence commit. No main write/merge/issue closure. Final exact published head
will be in PR body and final handoff; CI unreported checks pending, not green.
Resume ID3a36c179-e1e3-4332-9c33-fa947262fd79.
