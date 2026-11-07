# Review: assistant release integrity regression (#107)

Review execution: executed once by the author, not independent. Outcome: Conformant to the bounded scope; delivered-build acceptance NOT established. Boundary: the single test addition plus artifacts over base add72cc90.

Changes: [changes](../changes/2026-11-07-assistant-release-integrity-107-changes.md). Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-plan.md).

## Findings

* `src/api/tests/test_assistant_release.py` new test: uses file SQLite with genuinely separate store connections and threads; this is not SQL Server race evidence and the tests do not claim it. The thread race is a barrier-start overlap, not a proven interleaving.
* The test asserts on exact allowance caps (100 calls, 2000000 tokens) derived from the shared test config; a config default change fails it loudly.
* Web guidelines: no web file changed; not applicable.
* Preserved: default-off, finite admission, role/case/source permissions, SQL leases/dedup, no controlled writes, human review. No production file touched.

## Smallest remaining human/live gates

1. Authorised approver and release record (C6; `ZF_ASSIST_RELEASE_APPROVERS` unset).
2. Authoritative serving-version attestation source (C8); an alias or `response.model` is not one.
3. Disposable SQL Server run of the assistant classes and this test shape; real AI, Azure and CON-009/AC-057 delivered-build evidence (C10 SQL part, C13).
4. FULL gate on admitted head, independent exact-head review, hosted CI, owner approval.

## Routed follow-ups

1. Run SQL Server variant under the admitted gate; if wanted, mirror this test in the `ZF_SQL_SERVER` class.
2. Per-assistant/accepted-proposal attribution joins (C16) remain separate metering work.

No issue tick or closure is claimed; PR should use Refs #107 and #104.
