---
title: Issue 115 live critique
date: 2026-11-18
---

Single final-candidate critique (self, one pass).

* Risk: writing to the real `ledger-digests` container. Disposition: accepted; read-only verify, tamper on a copy container only, no `--publish`.
* Risk: throwaway job costs and leftovers. Disposition: accepted; job deleted, copy deleted (soft delete retention noted).
* Risk: claiming "scheduled" proof from a manual run. Disposition: accepted; recorded as unproven for the cron schedule.
* Risk: changing workspace networking to read logs. Disposition: rejected; console stream used.

Verdict: proceed.
