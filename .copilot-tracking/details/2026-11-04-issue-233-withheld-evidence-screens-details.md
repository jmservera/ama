# Details: issue 233 withheld panels on evidence screens

* Phase 1: panels appended after the last panel of each screen. Items: resident choices and contact history (technical), contact history and access (quality), household detail beyond need, funding amounts and claim values. Reuses `screenWithheld`, so wording states withholding is not authorisation.
* Phase 2: test checks both screen blocks contain `screenWithheld([` and the funding item.
* Phase 3: trace tension row records the screens with "source-level test only".
* Phase 4: api tests for role screens, programme, procurement, technical and quality; atlas checker; ruff; mypy (tests included) from `src/api`.
