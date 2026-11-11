<!-- markdownlint-disable-file -->
# Publication disposition: issue-144-permit-sql-1111

Refs #144 only. Metadata-only record. It qualifies, and does not erase, the earlier authored review [issue-144-permit-sql-e5-sql-1111-review.md](issue-144-permit-sql-e5-sql-1111-review.md) and the original handoff, which remain unchanged.

## Independent assessment

Full report: [issue-144-permit-sql-runtime-independent-1111.json](issue-144-permit-sql-runtime-independent-1111.json), an exact copy of the independently generated output. It assessed head `bef608b7cd31746d75a076dbb742246b1821511b`, not any later commit. Report sha256 `562b6ed58099a84161f7120d706e7ef3ae384d255418c3b9884d141582b599cb`.

* Verdict: APPROVE_WITH_COMMENTS. Two Medium findings, both about the external disposable driver. No application or test-source finding.
* The reviewer independently supports the real SQL seven passes and the exact N1 and N2 causes.

## Root disposition

* Accept only the recorded local permit-boundary observations as evidence for publishing the unchanged direct-only test module, subject to final exact-head assessment and hosted PR checks. No application defect or blocking source finding is established.
* Medium 1 (SQL-phase producers lack an admitted 600 s hard bound) and Medium 2 (cleanup can report success despite a failed unlink or absence check) stay OPEN on existing #144. No new issue, driver fix, rerun or automatic budget. Neither contract is waived, and neither is claimed to have passed. Universal 600 s producer conformity and fail-closed cleanup error-path conformity are not accepted.
* The driver is external, not shipped by this PR, and not endorsed for reuse. The earlier generic CONFORMANT description is limited by this assessment.
* E1 to E5 remain counted with zero remaining.
* The five deployment, load and restart criteria of #144 remain unproven.

## Observed evidence and limits

* Source `3bfa7e2a89efce6f4b5bfffe1e668c2a50b720d5`, tree `5b238bfa2099f1672c91fb77aad86c9074b18c49`, module sha256 `2f45a6905337328793b5937c3079e407735cd54484b51b3949d6c7b8520de017`. Driver sha256 `4b6d0eef27bf520b41fabe36bf54beb65198003f1240fb60e906a0b5a5d3ec8b`.
* Logged by the recorded local execution: seven SQL tests ok, with WITNESS values for lock wait, key, SPID and database clock, and the stored marker `issued_at`. The passing assertions are the test results. The logged values are supporting observations. The reviewer inspected this evidence and did not execute the tests itself.
* N1 failed exactly case 1 and case 3, and N2 failed exactly case 5 and case 6 `E2-CONFLICT-ROOT`, each once.
* Authority wording correction: in the E1-AUTHORITY witness the authority end was 1794405571.567 and the release was 1794405570.128. That leaves 1.439 s, below the required 2 s dispatch window. The release was not after expiry. The original handoff wording stays as written.
* Local disposable SQL Server evidence only. It is not production, real AI, whole-#144, full-gate or human acceptance.
