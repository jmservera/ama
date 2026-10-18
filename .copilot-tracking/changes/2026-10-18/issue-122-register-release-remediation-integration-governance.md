---
title: Issue 122 pinned governance integration receipt
description: Integration-only parity, focused shared-write validation and publication evidence
ms.date: 2026-10-18
---

## Scope and Disposition

SAME issue-122-register-release-remediation task, P06 INTEGRATION ONLY. No source
correction/third cycle, critique or second original Review. Correction TWO FINAL
was independently accepted bounded Pass by SAME reviewer
733cb491-5a80-4b82-8034-12671261e9d4 at
96099bb57c58e76b4afc7d278ff5f17be43f5a8d, base9403dc6a.
That prior acceptance payload is preserved verbatim separately. It is not a
Pass for this new integration delta. Original adverse assessments remain immutable.
RV-002 Low malformed metadata echo remains a separate excluded follow-up.
Any material source conflict/bug routes human after exhausted correction cycles.

Owner-authorized exact intake: clean local/remote/PR398
96099bb57c58e76b4afc7d278ff5f17be43f5a8d, prior base
9403dc6a8f52f1f04c5ad910faab11a57c29ee78, OPEN/draft/empty closing refs.
Fetched main exactly578631ac75cc8c6a7af53922c6aaae4435e7761c (PR409).
Rebased only owned topic,22commits, no conflict or manual source edit.
Integrated source candidate9f930d820f4133227717dc7b319903372ad8396e.

Only authorized rewrite:
refs/heads/fix/continuity-epoch-export-122:96099bb57c58e76b4afc7d278ff5f17be43f5a8d.
Unexpected topic advance stops. Publish pinned integration even if main later
moves, report without additional rebase. Subsequent receipt normal push.
Draft stays draft; no issue/board/merge action.

## Complete Source and Artifact Parity

Complete normalized nine-path owned patch before/after is exactly equal.
Normalization removes only Git index metadata and hunk numeric coordinates;
all source lines, context, paths and modes remain. No extra README/config
normalization exemption was needed.
Normalized patch SHA-256:
422a926caf38c825a98dac307cf90bcc12b226b365cec5135edb8b2c267ae574.
Before/after stable patch ID:8c04a096ac0a1e79289da685b55f1713d66f4fc8.

Seven owned source/test paths retain exact intake blobs/modes. API README and
pyproject have exact additive upstream composition: removing only the upstream
insertions recovers the accepted96099bb5 bytes. Both mypy test exemptions survive.
Both README contributions survive; no framework or operational contract changed.

All2642protected upstream files, including280src, match target blobs/modes:
governance/sqlstore/server/HTTP/core tests/config/docs and prior queue, recorder,
DPIA and consultation controls are preserved. All other upstream files are also
protected, not merely selected production files. KB log exact target bytes/mode;
upstream append-only additions preserved. No owned KB entry was added.

All73preceding immutable issue122 artifacts retain bytes/modes, including original
27 and full previous80-path boundary evidence. No adverse Review, critique,
research, prior receipt/manifest/log or independent finding was rewritten.
Current plan/details/changes/state are reconciled descriptively; new receipt/
manifest/raw outputs are separate.
Complete new boundary93paths:9inherited owned source/config/test/guide and
84artifacts, compared with prior80paths. Full inventory and hashes/modes live
in separate integration-governance.json.

Numeric overflow guard, SQL unavailable classification, lifecycle/source/count/
chronology/association checks, privacy/recorded need, canonical proof, epoch/
lease/current release/provider dispatch and authority/holds keep exact intent.
Current integration inherits upstream governance functionality without granting
authority or bypassing any continuity/safety/resident/funding hold.

## Shared SQL-Write Assessment

PR409 inserts governance mark_committed immediately after SQL COMMIT and adds
persisted-context rollback handling in the shared SQL writer. The witness mutates
only a present thread-local rai_evidence_write context. That context is installed
only in the RAI evidence append path and restored to its previous value in
finally. Continuity and assistant writers do not install it. No cross-context
success synthesis or continuity exception relaxation was introduced by integration.

Existing SqlEvidenceRegister tests exercise current actor recheck/precommit
audit rollback, competing writer/stale revision, postcommit acknowledgement,
immediate following commit-hook failure, lock-exit failure and recovery/pending
quarantine. Existing shared SQL store, assistant independent-connection durability,
continuity and role suites passed alongside these new upstream tests.
No changed owned production intent or unresolved concern remains from this
assessment, so no redundant actual SQL/image run was performed. Earlier actual
SQL/nonroot image evidence remains historical, not fresh integration evidence.

## Fresh Commands and Results

All commands use existing venv/installed src distributions and synthetic temp
fixtures, never private working data. No dependency install. Complete commands/
results are retained in integration-governance-commands.json; raw outputs and
their hashes/modes are in the separate manifest.

```bash
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_governance tests.test_governance_evidence_api \
  test_continuity_epoch_export.OfflineTests test_continuity_epoch_export.HttpTests \
  test_continuity_epoch_export.EpochTests test_assistant_release \
  test_continuity test_role_endpoint_inventory -q
```

173run/157pass/16skips. All16skips are MssqlEvidenceRegister, explicit
"opt-in task-owned loopback SQL". The fresh run contains65governance,
10governanceHTTP,14offline,10continuityHTTP,8epoch,32assistant release,
15continuity and19endpoint role tests. No namespace import ambiguity:
src/api is on path and governance HTTP uses tests.test_governance_evidence_api.

```bash
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_sqlstore test_assistants.DurabilityTests test_role_matrix -q
```

51/51 pass, zero skips. Shared-store atomicity, assistant independent-connection
claims and role contracts remain exercised.

```bash
for project in core api; do
  (cd "src/$project" && ../../.venv/bin/ruff check . &&
    ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)
done
```

Executed with set -e; core/API lint/format/mypy pass,125/58mypy files.
No formatting or source edits were made to pass these checks.

Exact unchanged coordinator probes were rerun from session copies:

```bash
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python \
  /home/azureuser/.copilot/session-state/28a50b1e-793d-4cd3-b584-4ab290f9a34f/files/integration-governance-coordinator-probes.py
PYTHONPATH=src/api:src/api/tests:src/core/tests:src/agents/tests .venv/bin/python \
  /home/azureuser/.copilot/session-state/28a50b1e-793d-4cd3-b584-4ab290f9a34f/files/coordinator122-unavailable-probe.py
```

3/3 numeric/lifecycle/real-HTTP privacy methods pass, including18numeric subcases
at producer/verifier boundaries, four unreferenced-lifecycle defects and
recorded-need false/true/false for two roles with canonical nonmutation.
Unavailable source probe15/15 passes, including11retained SQL releases/real
constructor/export, unknown source counts, producer incomplete and offline
invalid against unchanged external head. It imports14OfflineTests; overlaps
focused suite, not additive unique coverage.

Probe outputs identify integrated9f930d82. Their unchanged owned source hashes
are bound to final publication via complete patch/byte parity in the manifest.
No new failed command, source conflict or source edit in this integration.
Expected law-store absence and injected rollback/acknowledgement failures are
visible in passing test output, not silent fallbacks or operational approval.

## Historical Evidence and Immutable Hashes

Prior correction TWO: host86/86, installed nonroot image86/86, actual owned
SQL16/16 and overlapping final3/3, coordinator15/15, all zero skips; core/API
quality/checker/source parity pass. Prior correction ONE:66focused,
host/image151run133pass18skip each, actualSQL32/32. Earlier coupled command
FAILED547entries432pass114skip/one namespace-import error; corrected resident
command9run8pass/one skip. Consultation integration93run80pass13skip.
All remain historical, with all failed attempts and raw whitespace preserved.
No patch-wide whitespace Pass is asserted; source/text checks are separate.

```text
New original Review e43d6ec67d83b788e97d68fd2be20523ef962f7ac5aeb544fabc0886adbf93e4
New single critique 343c3e14ecebe3fa813b2bb8c0a0a914b555a786996dd987c583356798d36ca7
Historical Review 9d9d0bff0fdda5a8d163967c4ba8a997ee1bc315ae5a896611fc331aff200abc
Historical critique 4eeda2d60235f571916a83de65fa9cda8d73e2159291a50286e8055328fc77be
```

Complete prior worker logs preserved as byte-identical copies under session
files, integration-governance-original-rpi-122-{name}.log. Source paths/hashes:

```text
/tmp/rpi-122-remediation.log 60769bytes/1184lines
7d8d069be3350dcf80504b21476b8e11adc2e2eae35ed9407625c7d02d1180cf
/tmp/rpi-122-correction-one.log 43365bytes/730lines
51146f98244f4eda2ff925fec7374c552034b7d69246f46f509784e7595c7583
/tmp/rpi-122-publish.log 17659bytes/304lines
8b453baff70135dffcefaebe2c76623b37782e8150eca3f5caeffbf7b8bee87a
/tmp/rpi-122-consultation-integration.log 16326bytes/265lines
30a1e213610a97dcf56644b167f440940b2a50c2f58453e7c27e4d0287512b46
/tmp/rpi-122-correction-two.log 45458bytes/801lines
dfe36c746ebf7b2db53694d30e0e074df0ab41465d7be84078049cf6b64f9fd0
```

Session directory:
/home/azureuser/.copilot/session-state/28a50b1e-793d-4cd3-b584-4ab290f9a34f/files/.
All earlier inherited logs/manifests remain unchanged and referenced.
Full current worker stream, if captured by coordinator, finishes at process
exit; fresh individual command outputs are complete committed raw evidence.
Current full worker stream is /tmp/rpi-122-governance-integration.log, confirmed
from the active coordinator tee process. It remains growing until exit and
is not falsely reported as a frozen complete copy now.

## Publication and Required Stop

Authenticated gh account resolved freshly; repository-local noreply email for
author and committer, Conventional Commit and Copilot trailer. Exact authorized
96099bb5lease only; final metadata receipt normal push. Full final source/artifact
inventory and hashes/modes are in integration-governance.json. Manifest omits
only its own hash to avoid self-reference; final commit/head is externally
resolved by local/remote/PR equality and post-publication session verification.
PR398 remains OPEN/draft with empty closing references; Refs #122 only.

STOP for SAME independent reviewer to assess final integration delta and
source parity. Prior bounded Pass is retained, not extended by self-claim to
the new base. Original adverse assessments unchanged; no third correction.
Actual authority/OQ017, witnessed authorized drill, immutable external Azure
head custody, Azure SQL drill and enforceable legacy-image exclusion remain
unmet. No private .env/ZF_DATA/support/data, uv/mvp, Azure/Graph/IAM/spend,
legal/currentness/approval inference, issue/board action or merge.
