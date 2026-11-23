# Review 2244 live r4 (2026-11-23)

Executed once. Outcome: conformant, with open follow-ups. Boundary: lawstore.py and its tests.

* The check is read-only; a race falls to the idempotent locked path. Wrong ledger kind still reaches the SystemExit.
* Open: live proof of C3/C4 needs the owner deploy; C5 lock holder unknown.
