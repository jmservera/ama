---
title: Zava Forward importer
description: Status, fixtures and boundaries of the quarantining document import workload (ADR 0001, ADR 0006)
author: AMA programme
ms.date: 2026-10-15
ms.topic: reference
---

The importer (`zava_forward.importer`) is the quarantining import workload described in ADR 0001. The former `mvp/` application had no import service, so the former `mvp/README.md` had no importer content to move in M6 of #199. The project holds the Excel transition library of #80 (below), a `python -m zava_forward.importer` entry point and its tests.

* Fixtures: `evals/document_form_fixtures.json` (document-form fixtures, registered in `src/agents/evals/registry.json`) with its test in `tests/`.
* Boundary: the project imports `zava_forward.core` only (the document controls and scanner live in `core`, `doc_controls`); no project imports it. Dependency rule tests are in `tests/test_dependency_rule.py`.
* Excel transition (#80, synthetic data only, standard library only): `xlsx` (read-only reader with size, entity and formula-injection guards, values-only writer), `mapping` (declared `case-list` structure, alias column matching, conflicts, row-level preview with lineage to source SHA-256, sheet and row; the source is hashed, scanned with `core` `doc_controls` and never written), `quarantine` (staged batches, human approval gate with a different named approver, supersession history, SQL portable to SQL Server) and `export` (CSV and one-way read-only Excel with Read me and History sheets, read-only comparison). `python -m zava_forward.importer preview FILE` prints the preview.
* Not built: the HTTP or web surface for import and the export buttons on every list (the api may not import `importer` until #144), the queue transport, the importer image behaviour and limited SQL role, AI-assisted column suggestion with human approval, and the staged transition thresholds, which owners must set (ADR 0001 open item). The upload checks and local scanner that exist today are in the [api](../api/README.md) and [core](../core/README.md) documentation and are labelled synthetic.

Run the suite from `src/importer` with `python3 -m unittest discover -s tests`. The index of projects is [src/README.md](../README.md).
