# Research: issue #107 live proof (2026-11-18)

Disposition: executed. Planning Readiness: Ready.

Scope: two unticked criteria on #107 (independent SQL worker/race tests; matching approved exercise record plus delivered-build version-linked real AI, SQL, Azure evidence). Demo only, docs/evidence only, Tier FOCUSED.

Findings (full record in docs/reference/research/issue-107-live-assistants-evidence-2026-11-18.md):
* Criterion 1 is provable: tests `test_assistant_release.MssqlUnleasedRevocation` run on a disposable local SQL Server 2022 container (the fixture refuses Azure SQL); SQLite restart/old-image tests exist.
* Criterion 2 approved side is not provable: the live app has no approved release and OQ-017 names no approver. Denial side is provable with a live read and invoke probe.
* Heavy lock /tmp/ama-rpi-heavy.lock exists; rpi-checks.py is not used.
