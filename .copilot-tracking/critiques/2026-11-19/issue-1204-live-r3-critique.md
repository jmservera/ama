# Critique: issue 1204 r3

Executed once. Verdict: proceed.

* Risk: overstating. The window tests only no-progress and recovery rules; the schema lacks approval, closure-batch and global-stop fields. The note must say so and keep the box unticked.
* Risk: contradicting r2 silently. State the correction (r2 found no tick_log; three exist).
* Rejected: adding an exporter tool; the three databases have three different schemas and are private session state.
