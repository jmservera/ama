---
title: AMA Case Study 48
description: Research and solution design for the Zava Forward retrofit programme
---

## Repository Purpose

![Capstone rubric score](./.github/rubric/scores/badge.svg)

The badge shows the latest recorded [capstone rubric score](./.github/rubric/README.md).

This repository develops Case Study 48 into a research-backed proposal,
business requirements, agent architecture, delivery plan and presentation for
the Zava Forward retrofit programme at Zava North Homes.

> [!NOTE]
> Zava North Homes, Zava Forward and their organisational context are fictional
> and are used solely for this presentation exercise. Project reference
> documents treat Zava North Homes as the case organisation so the scenario
> can be analysed consistently and presented credibly.

## Core Documents

* [Project Knowledge Base](./docs/reference/README.md), the index for all
  evidence, research, method and project memory
* [Original Case Study 48](./docs/case_study_48_original.md)
* [Case Study 48 Addendum](./docs/case_study_48_addendum.md)
* [Agentic Retrofit Programme BRD](./docs/brds/agentic-retrofit-programme-brd.md)
* [Zava Forward Workbench PRD](./docs/prds/zava-forward-retrofit-programme-demonstrator.md)
* [Azure architecture](./docs/adrs/0001-azure-architecture.md) and
  [pilot-readiness decisions](./docs/adrs/0002-pilot-readiness-architecture.md)
* [Working MVP and current limits](./src/api/README.md)
* [Source projects, package boundaries and CI cut-over](./src/README.md)
* [Deployment and identity initialization](./infra/README.md)
* [Branding migration and historical exceptions](./tools/rename-zava.md)
* [Housing Association Primer](./docs/reference/research/sector/housing-association-primer.md)
* [Company Profile Research](./docs/reference/research/company/company-profile-research.md)
* [UK Social Housing Baseline Research](./docs/reference/research/sector/uk-social-housing-baseline-research.md)

## Source cut-over archive

The owner signed off cut-over (#201) on 2026-10-27. The remaining `mvp/`
pointer is retired; `prototype/` was already retired. Current code, tests,
images and run instructions are under [src](./src/README.md).
The local annotated archive tag `v0.21.0` follows the BRD version at cut-over
and targets `65a514ed20e97816dbf47e9fb981ab4cfe40597d`, the last commit before
pointer deletion. Earlier executable content remains in that commit's history.
The tag is not pushed by this change; the owner publishes it explicitly:

```bash
git push origin refs/tags/v0.21.0:refs/tags/v0.21.0
```

See the [dated cut-over record](./docs/architecture/cutover-evidence-pack.md#owner-authorized-directory-retirement-2026-10-27)
for reference exceptions and remaining acceptance boundaries. Workflow/check
names are unchanged.
