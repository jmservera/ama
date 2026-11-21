# Plan: issue 2204 role sign-in proof (2026-11-21)

Tier: focused (documentation and evidence only; no src change). Basis: no executable, workflow, dependency or infrastructure edit; `rpi-checks.py --all` not run by instruction.

## Critique (executed once, final candidate)

* Verdict: accepted with direct dispositions.
* Risk: a local matrix could be mistaken for live sign-in. Disposition: the research note labels it "not a live sign-in" and criterion 1 stays partly proven and unticked.
* Risk: screenshots may show an account name or case data. Disposition: account chip hidden, only two denial screens kept, credential literal scan found no match.
* Risk: wrong probe path read as a defect. Disposition: kept as adverse evidence and explained.
* Risk: ticking criterion 1 without live roles. Disposition: left to the owner; not ticked.

## Phases

1. Add the research note, index row and log entry. Done.
2. Record the changes file with the per-criterion table.
3. Review once; commit locally; no push.
