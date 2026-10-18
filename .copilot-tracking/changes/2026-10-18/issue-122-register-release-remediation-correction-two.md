---
title: Issue 122 correction TWO FINAL execution receipt
description: Separate unavailable SQL source correction evidence, not another original Review
ms.date: 2026-10-18
---

## Disposition and Intake

Correction TWO and FINAL of SAME issue-122-register-release-remediation task.
Implementation is exercised, not independently accepted. No new critique or
original Review. Original Complete / Not accepted and independent adverse
finding remain immutable; historical exhausted two cycles are not reset.
RV-002 Low malformed metadata echo is a distinct excluded follow-up.
Any remaining blocking finding routes to human, not a third source correction.

Predecessor integration exited zero and recorded stopped state. Live clean
local/remote/PR398 intake was d0a6f616afde75bda50665ba5b77555621dc3432,
base/main 9403dc6a8f52f1f04c5ad910faab11a57c29ee78; PR OPEN/draft,
closingIssuesReferences empty. Process inspection found current correction-two
worker, not an active predecessor. No drift or source dirt at intake.
Normal commits/push ONLY; no rebase, force push, readiness, merge or issue/board
mutation. If main moves, retain pinned base and report to coordinator.

Independent input is preserved verbatim in correction-two-independent-input.json,
attributed to reviewer 733cb491-5a80-4b82-8034-12671261e9d4, coordinator
event 8f76b215-93d9-4129-88be-77ca37968648. It reviews the complete prior
51-path c20052e4 boundary, not merely a recent patch. Its blocking Medium is
SQL/schema unavailability falsely classified as an empty unsupported JSON
source. Supplied coordinator probe subsequently demonstrated actual runtime:
11 retained releases, real constructor with migration failure, complete producer
and valid offline result before correction. Both supplied script and original
red output are preserved separately, byte-identical, with provenance in manifest.
This is correction input, not a replacement original RPI Review.

## Source Candidate and Exact Delta

Source candidate: 5fa69b3e299a9fbe16c0ae7839fb3613eaff09d0.
Pinned base: 9403dc6a8f52f1f04c5ad910faab11a57c29ee78.
Final publication head is the commit containing the final evidence metadata;
resolve it from Git/remote/PR, not an impossible self-referential manifest hash.

Four source/test/documentation files differ from intake:

* src/core/src/zava_forward/core/assistants.py: three added production lines,
  before the unsupported JSON branch. Existing schema_error means supported SQL
  is unavailable: total null/unknown, truncated true, source_status unavailable,
  safe pre-existing migration/manual message. Missing release evidence remains
  missing; no empty release proof is synthesized.
* src/api/tests/test_continuity_epoch_export.py: actual initialized migration
  failure with retained releases; actual JSON unsupported and SQL full/empty
  positives; normal HTTP full and two limited audiences without private driver
  text; natural invalid updatable-ledger MSSQL migration with retained event and
  release rows. Recomputed ordinary digest/forced complete remains invalid
  against original unchanged externally held head. Manual case/register reads
  remain available. All SQL databases are UUID task-owned.
* src/api/tests/test_continuity.py: replace uninitialized J/sql=False test double
  with real Assistants(JSON Store) construction and cleanup; same assertions.
* src/api/README.md: document unavailable schema versus honest unsupported JSON
  and known-empty SQL, safe operator message and incomplete evidence.

Every other source byte/mode is unchanged from intake. Protected upstream
procurement/server/consultation, queue, recorder and DPIA code/tests retain
exact pinned bytes/modes; README retains all additive sections. KB log unchanged.
No constructor catch, verifier or producer validation was weakened. Numeric
correction ONE, privacy/recorded need, full canonical ledger, all-retained-release
lifecycle/count/association/chronology, epoch/lease/current release, provider
dispatch, stock, safety, consent, funding and authority controls remain intact.

Installed assistants SHA-256:
6e9506f7b340933de9c67d1a8eef8701a1403530d188ddfb59bdc479d76624b2.
Unchanged continuity SHA-256:
4afcabd0cfbc495dc71d6b4869f42da5c8db500909c6aab129d20194586883ad.
Installed image:
sha256:e2dc7eb237901f69e37ff6b78aed796da4b9e36fcb4aa61c310327fb119b23f5.
UID/GID 10001, installed site-packages paths, exact source hashes verified.

## Fresh Commands and Results

Run from repository root with existing installed editable distributions and
venv. No dependency install or manifest change. Exact command/result payloads,
including failures, are in correction-two-commands.json; complete raw outputs
are individual correction-two logs listed and hashed in the manifest.
Commands overlap; counts below are not additive unique-test totals.

Host focused command:

```bash
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity_epoch_export.EpochTests test_assistants.ContractTests \
  test_assistants.ApiTests test_continuity test_role_endpoint_inventory -q
```

Final: 86/86 pass, zero skips. Earlier subset 52/52 pass.
Expected fixture law-store absence is explicitly logged Unknown, not suppressed
or converted to approval. All private-input canaries remain synthetic.

Coordinator probe command:

```bash
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python \
  /home/azureuser/.copilot/session-state/28a50b1e-793d-4cd3-b584-4ab290f9a34f/files/coordinator122-unavailable-probe.py
```

Final 15/15 pass, zero skips: imported OfflineTests adds two tests to supplied
original 13. Probe retains 11 SQL releases, source unavailable/unknown count,
producer complete false, offline valid false/complete false. The supplied
historical red result remains 13 tests/one failure, not relabelled green.

Static command:

```bash
for project in core api; do
  (cd "src/$project" && ../../.venv/bin/ruff check . &&
    ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy) || exit
done
```

Final core/API Ruff, format and mypy pass; 125/57 mypy files.

Actual SQL runner, unchanged except unique name and selectors:

```bash
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python - <<'PY'
import importlib.util, sys
p = '.copilot-tracking/changes/2026-10-18/issue-122-register-release-remediation-owned-sql.py'
spec = importlib.util.spec_from_file_location('owned_sql', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.NAME = 'zf-122-correction-two-sql-28a50b1e'
sys.argv = [p, 'test_continuity_epoch_export.MssqlOfflineTests',
            'test_continuity_epoch_export.MssqlHttpTests.test_http_migration_failure_reports_incomplete_without_driver_details']
raise SystemExit(m.main())
PY
```

Actual SQL Server 16.0.4305.5, 16/16 pass, zero skips. Natural migration failure
uses UUID WITH LEDGER=ON database, earlier bad UPDATABLE_LEDGER_TABLE with retained
event and release; actual constructor disables SQL and export stays incomplete/
offline-invalid without dropping rows. Additional final three-selector run uses
zf-122-correction-two-final-sql-28a50b1e and natural invalid-ledger/direct-failure/
HTTP tests after explicit pre-export head assertions: 3/3 pass, zero skips.
Only those UUID databases are dropped; each exact owned container removed in
finally. No existing test's fixed-name database destruction was executed.

Installed image commands:

```bash
docker build -q -f src/api/Dockerfile -t zf-122-correction-two-28a50b1e:local src
.venv/bin/python src/check-container.py api zf-122-correction-two-28a50b1e:local
docker run --rm --name zf-122-correction-two-tests-final-28a50b1e \
  --read-only --cap-drop=ALL --security-opt=no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,uid=10001,gid=10001 \
  --tmpfs /state:rw,nosuid,nodev,uid=10001,gid=10001 \
  -e PYTHONPATH=/tests/api:/tests/core:/tests/agents \
  --mount type=bind,source="$PWD/src/api/tests",target=/tests/api,readonly \
  --mount type=bind,source="$PWD/src/core/tests",target=/tests/core,readonly \
  --mount type=bind,source="$PWD/src/agents/tests",target=/tests/agents,readonly \
  --entrypoint python zf-122-correction-two-28a50b1e:local -m unittest \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity_epoch_export.EpochTests test_assistants.ContractTests \
  test_assistants.ApiTests test_continuity test_role_endpoint_inventory -q
```

Final installed image 86/86 pass, zero skips; earlier subset 52/52 pass.
Checker Docker controls/negative probes/responsive startup pass. Only test
directories mounted, never application source or private working data.
Separate network-none read-only parity probe verifies installed bytes and UID.
Unique image tag removed after tests; no owned running/stopped containers remain.
No broad system prune or unrelated image/database/container deletion.

### Failed Attempts Retained

* Before fix: three targeted tests, one positive pass, four expected negative
  subcase failures (direct SQL source and three HTTP audiences). Source complete
  incorrectly true for full audience, unsupported instead of unavailable for
  limited. Supplied coordinator probe before fix discovers 15 tests and fails
  twice: original reproduction plus new direct regression.
* Initial static API import sorting failed. Existing Ruff fixed only changed
  import ordering. Next API mypy failed indirect fixtures.SqlStore re-export;
  direct SqlStore import corrected it. That wrapper used break and returned
  zero despite mypy failure; its output is explicitly FAILED, never green.
* First installed byte-parity one-liner had a mismatched-brace SyntaxError.
  Corrected probe syntax passes, with no production change.
* Additional register/role run: 34 tests, 33 pass/one AttributeError from old
  uninitialized J test double lacking schema_error. Real JSON service
  initialization replaces it, preserving every existing assertion. Final full
  host/image 86-test boundaries pass. No production fallback was added.
* First receipt-generator execution expected full_changed_inventory in the
  older immutable manifest; that historical schema uses full_boundary. Corrected
  only the generator key. Its failed command/result is preserved; no source
  or historical artifact was changed.
* First evidence-commit compound command stopped at git diff --cached --check:
  byte-preserved unittest output contains a trailing space, and a raw Git patch
  contains space-prefixed context blank lines. Its separately sequenced normal
  push still ran, publishing only tested source candidate 5fa69b3e. Evidence
  commit and embedded guard had not run. Live local/remote/PR equality at that
  source head and unchanged pinned base/draft/empty refs were immediately
  reverified. Raw evidence is not rewritten to satisfy whitespace formatting.
  Subsequent textual diff checks exclude only raw .log/.patch evidence, with
  source checked separately; evidence publication uses a properly guarded
  normal push. The compound attempt is not reported as a successful commit.

## Frozen Evidence and Complete Boundary

All 44 entries of prior integration manifest verified, all 48 preceding immutable
issue-122 artifacts frozen at intake, original 27 included. Original manifests,
assessments, research, prior independent input and older receipts/logs unchanged.
Current plan/details/changes/state updates are descriptive; original adverse
outcomes are not replaced with Pass.

```text
New original Review e43d6ec67d83b788e97d68fd2be20523ef962f7ac5aeb544fabc0886adbf93e4
New single critique 343c3e14ecebe3fa813b2bb8c0a0a914b555a786996dd987c583356798d36ca7
Historical Review 9d9d0bff0fdda5a8d163967c4ba8a997ee1bc315ae5a896611fc331aff200abc
Historical critique 4eeda2d60235f571916a83de65fa9cda8d73e2159291a50286e8055328fc77be
```

Full source+artifact inventory, byte hashes/modes, prior 51-path and intake
55-path reconciliation, protected upstream parity, commands and raw evidence
are in correction-two.json. The manifest excludes only its own hash to avoid
self-reference; its path/mode remain in inventory.
Complete boundary: 80 paths, nine inherited owned source/config/test/guide paths
and 71 artifacts. Relative to intake, four source/test/guide paths intentionally
change; the other 284 source paths retain bytes/modes. All 279 protected upstream
source paths remain exact pinned bytes/modes; the other five owned source paths
are unchanged. All 48 prior immutable artifacts retain bytes/modes.

Complete preceding worker logs read/preserved under session files, unchanged:

```text
/tmp/rpi-122-remediation.log
60769 bytes / 1184 lines
7d8d069be3350dcf80504b21476b8e11adc2e2eae35ed9407625c7d02d1180cf
/tmp/rpi-122-correction-one.log
43365 bytes / 730 lines
51146f98244f4eda2ff925fec7374c552034b7d69246f46f509784e7595c7583
/tmp/rpi-122-publish.log
17659 bytes / 304 lines
8b453baff70135dffcefaebe2c76623b37782e8150eca3f5caeffbf7b8bee87a
/tmp/rpi-122-consultation-integration.log
16326 bytes / 265 lines
30a1e213610a97dcf56644b167f440940b2a50c2f58453e7c27e4d0287512b46
```

Copy directory:
/home/azureuser/.copilot/session-state/28a50b1e-793d-4cd3-b584-4ab290f9a34f/files/.
Copies named correction-two-original-rpi-122-{remediation,correction-one,publish,consultation-integration}.log.
Full current worker stream: /tmp/rpi-122-correction-two.log (growing until exit;
not misrepresented as a frozen complete copy before process shutdown).

Historical correction ONE evidence remains historical: 66 focused, host/image
151 run/133 pass/18 skips each, owned SQL 32/32. Coupled command FAILED:
547 entries/432 pass/114 skips/one namespace-import error. Separately corrected
resident command 9 run/8 pass/one skip. Recent consultation integration was
93 run/80 pass/13 skips. None is claimed as fresh correction TWO validation.

## Publication and Required Stop

Authenticated account resolved fresh via gh api user, repository-local noreply
used for both author and committer, Conventional Commit and Copilot trailer.
Source commit above followed by evidence/metadata commit and normal publication.
PR398 stays OPEN/draft, Refs #122 only, closing references empty. Exact final
head/base and clean status recorded by post-publication verification in session
files and draft PR body, not fabricated inside its own commit.

STOP for SAME independent reviewer to assess correction and integration delta
against prior complete 51-path boundary and actual adverse probes. No independent
acceptance/readiness claim or review boxes. Actual authority/OQ-017, witnessed
authorized drill, immutable external Azure-head custody, Azure SQL drill and
enforceable legacy-image exclusion remain unmet. No private .env/ZF_DATA/support
or datasets read, no Azure/IAM/Graph/live inference/spend, no uv/mvp.
