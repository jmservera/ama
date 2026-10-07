---
title: Proper Warm PoC Implementation
description: Application source and pointers to the independently maintained architecture and runbook
ms.date: 2026-10-08
ms.topic: how-to
---

This directory contains the local synthetic implementation. Architecture,
operations, validation/resource inventory and teardown are maintained in
[the separate documentation PR #27](https://github.com/jmservera/ama/pull/27),
not duplicated with application code.

* [Full runbook](https://github.com/jmservera/ama/blob/51d8ae41caaa4535ad53c7268f874ce5334242ee/docs/architecture/proper-warm-runbook.md)
* [Local and Azure PoC architecture](https://github.com/jmservera/ama/blob/51d8ae41caaa4535ad53c7268f874ce5334242ee/docs/architecture/proper-warm-poc.md)
* [Resource ledger and safe teardown](https://github.com/jmservera/ama/blob/51d8ae41caaa4535ad53c7268f874ce5334242ee/docs/architecture/proper-warm-resources.md)
* [Scenario and coverage manifest](./manifest.json)

Those links pin the transferred documentation and work before either PR merges.
The running app is local-only; demo roles are not authentication and the assistant
is a simulator. No Azure or M365 resources are provisioned by this implementation.
Moving documentation does not stop the container, remove its persistent volume
or execute the documented teardown.
