# Issue 2188 live review (2026-11-23)

Review executed once on the diff of `tools/rpi-checks.py`, `tools/test_rpi_checks.py` and the research note. Outcome: conformant, no open material findings.

* Deadlock: images hold one slot and wait only on the leaf `trivy_lock`; mssql acquires slots under `docker_gate`, so acquirers cannot interleave. Release is in `finally` for exactly the slots held.
* Exclusivity preserved: mssql takes all four slots; the test asserts zero overlap.
* Receipt semantics and commands unchanged; only scheduling differs.
* Open items (routed as follow-ups, not repeated here): timed whole-gate before/after pair needs the coordinator's full gate; real four-image build timing; Trivy serialisation necessity unproven; findings D4 (shard worker budget) and D1/D2 of the gate-speed review remain separate issues.
