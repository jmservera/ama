---
title: Zava Forward importer
description: Status, fixtures and boundaries of the quarantining document import workload (ADR 0001, ADR 0006)
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

The importer (`zava_forward.importer`) is the quarantining import workload described in ADR 0001. The former `mvp/` application had no import service, so the former `mvp/README.md` had no importer content to move in M6 of #199. Today the project holds a version module, a `python -m zava_forward.importer` entry point and its tests.

* Fixtures: `evals/document_form_fixtures.json` (document-form fixtures, registered in `src/agents/evals/registry.json`) with its test in `tests/`.
* Boundary: the project imports `zava_forward.core` only (the document controls and scanner live in `core`, `doc_controls`); no project imports it. Dependency rule tests are in `tests/test_dependency_rule.py`.
* Not built: the import service, its quarantine store and its image behaviour beyond the skeleton. The upload checks and local scanner that exist today are in the [api](../api/README.md) and [core](../core/README.md) documentation and are labelled synthetic.

Run the suite from `src/importer` with `python3 -m unittest discover -s tests`. The index of projects is [src/README.md](../README.md).
