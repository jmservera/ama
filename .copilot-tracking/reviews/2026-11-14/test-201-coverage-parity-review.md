---
title: Issue 201 coverage baseline parity review
ms.date: 2026-11-14
---

Refs #201. Review executed once; outcome: conformant for scope, with routed follow-ups.

* Count and wiring parity proven locally; matches planned scope and file list.
* Finding F1 (routed, later work): measured line/branch coverage is not configured or recorded, so "equal or greater coverage" stays UNMET in the evidence pack; needs a baseline coverage run at `v0.21.0` versus candidate.
* Finding F2 (routed): no hosted CI result on a candidate commit; `src-ci.yml` runs on pull requests only. Requested wiring file `ci-affected.yml` does not exist; `src-ci.yml` plus `tools/ci-affected.py` were used.
* Human review and hosted CI remain required; nothing pushed.
