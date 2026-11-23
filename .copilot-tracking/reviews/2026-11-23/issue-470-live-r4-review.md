# Review, issue 470 live r4

Executed once. Outcome: conformant.

* The `--markdown` option changes output format only; verdict logic and exit codes are untouched (tested for exit 0 and 3).
* The review found no open material findings. Criterion 4 is reported unproven, not ticked.
* Routed follow-up: run two matched `--all` arms (ABBA) outside this task, then record `compare --markdown` output in the delivery PR.
