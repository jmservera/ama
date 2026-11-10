# Details: Registry observation parent transition

* Merge: ordinary `--no-ff` of `eff05737` into `ffb3e4158`, merge commit parents in that order.
* Conflict resolution: pack and README conflicts are both-appended-at-EOF; keep the `origin/main` side first, then the Registry section/paragraph unchanged except the wording edits below. Log: verify auto-merge keeps both entry sets in order.
* Wording edits: in the Registry section replace the "declared child ... not retargeted" sentence with the actual transition (PR 1396 squash `eff05737` at 15:09:16Z, topic merged main by ordinary merge at Root's explicit direction, `6cc59776` remains the historical pin, fresh main `eff05737` has equal `src`, `infra`, `tools` ids so no source drift); README and log mention likewise. Pinned-source and trigger rows keep `6cc59776`.
* Verify: `git diff` vs `origin/main` shows only additions; grep for conflict markers; ASCII check; link targets exist.
